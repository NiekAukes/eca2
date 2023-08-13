# The Event System
The event system is one of the most integral parts of neca. It allows you to 
easily add asynchronous functionality to your project, without having to worry
about the underlying implementation (and the complexity that comes with it).

## What is an event?
An event is a message that is sent to a specific event handler. The event
handler can then decide what to do with the event. To create an event handler,
you can use the `@event` decorator. This decorator takes the name of the event
as an argument. The event handler will then be called whenever an event with
that name is sent.

```python
from neca.events import event

@event("my_event")
def my_event_handler(context, data):
    print("my_event was sent!")
```

## Sending an event
To send an event, you can use the `fire_global` function. This function takes the event name and the data as arguments. The data can be any object. The event handler will receive this data as an argument.

```python
from neca.events import fire_global

fire_global("my_event", "hello world!")
```

## Event Conditions
You can also add conditions to your event handlers. Conditions are functions that are called before the event handler is called. If the condition returns `False`, the event handler will not be called. This can be useful if you want to add a filter to your event handler.

```python
from neca.events import event, condition, fire_global

@event("my_event")
@condition(lambda context, data: data == "hello world!")
def my_event_handler(context, data):
    print("my_event was sent!")
    print("context data:", context["my_data"])


fire_global("my_event", "hello world!") # my_event was sent!
fire_global("my_event", "hello!") # nothing happens
```
you can also use this syntax:
```python
from neca.events import event, condition, fire_global

def my_condition(context, data):
    return data == "hello world!"

@event("my_event")
@condition(my_condition)
def my_event_handler(context, data):
    print("my_event was sent!")
    print("context data:", context["my_data"])
```

## Event context
The event handler receives a context object as its first argument. This object stores the general context information and is persistent across events fired within this context. Normally there is only one context, but you can create multiple contexts if you want to. This can be useful if you want to handle events differently in different contexts.

```python
from neca.events import event, fire_global

@event("my_event")
def my_event_handler(context, data):
    print("my_event was sent!")
    print("context data:", context["my_data"])
```
To learn more about contexts, check out the [contexts documentation](context_rulesets.md).
