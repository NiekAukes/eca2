import neca
from neca.events import *
from neca.log import logger
import logging
import random
import json

# see what the engine is doing
# set to logging.WARNING to suppress info messages, etc
logger.setLevel(logging.DEBUG)  

LOOKBACK = 5000
ADVANCE_RATE = 50
REFRESH_RATE = 1

stocks = ["aapl"]

@event("init")
def init(ctx, e):
    # load the stock data
    for stock in stocks:
        with open(f"{stock}.json", "r") as f:
            data = json.load(f)
            ctx[stock] = data
            fire_global("roll", (stock, 0))

    ctx["chart_type"] = "candlestick"
    

@event("roll")
def roll(ctx, event):
    symbol, i = event
    #rolls the stock data 20 paces
    data = ctx[symbol].copy()
    data["results"] = ctx[symbol]["results"][i:i+ADVANCE_RATE]
    #fire_global("stock_data", data)
    ctx["stock"] = data
    for d in data["results"]:
        if d["o"] < d["l"] or d["o"] > d["h"]:
            print(f"Data error: {d}")
        if d["c"] < d["l"] or d["c"] > d["h"]:
            print(f"Data error: {d}")
    if len(ctx[symbol]["results"]) > i + ADVANCE_RATE:
        fire_global("roll", (symbol, i+ADVANCE_RATE), delay=REFRESH_RATE)
        fire_global("stock_data", data)
    else:
        ctx["end"] = True
        

@event("stock_data")
def stock_data(ctx, data):
    ctx["stock"] = data
    
    # process the data and send it to the client
    processed_data = []
    for d in data["results"][-LOOKBACK:]:
        processed_data.append({
            "x": d["t"],
            "y": [d["o"], d["h"], d["l"], d["c"]]
        })
    
    #print(f"Stock data received: {processed_data}")
    ctx["stockdata"] = processed_data
    fire_global("update_chart", None)        

chartkeys = {
    'o': 0,
    'h': 1,
    'l': 2,
    'c': 3
}

@event("update_chart")
def update_chart(ctx, e):
    stockdata = ctx.get("stockdata", [])
    # possibly format the data for other chart types
    chart_type = ctx.get("chart_type", "candlestick")
    
    # lines can be drawn on the chart based on open, high, low, close
    if chart_type[:4] == "line":
        key = chartkeys[chart_type[4]]
        stockdata = [{"x": d["x"], "y": d["y"][key]} for d in stockdata]
        chart_type = "line"

    
    emit("stock", {
        "action": "updateSeries",
        "newSeries": [
            {
            "type": chart_type,
            "name": "candle",
            "data": stockdata
            }
        ]
    })
# starts the server and prevents the program from exiting
neca.start() 