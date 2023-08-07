# Tutorial 1: The Event System
Hello tutorialists! Welcome to the first tutorial of NECA. In this tutorial we will learn how to use the event system and how to create a simple page.

## Learning goals
- Learn about `@event` and `fire_global()`
- Learn about creating loops using the event system

## The Event system
the NECA framework is governed by an event system. this means that everything that happens in your application is triggered by an event. events can be triggered by an outside source, such as a user clicking a button, or by your own code. events can be handled by any number of event handlers. event handlers are functions that are called when an event is triggered. event handlers can be registered to an event using the `@event` decorator. let's look at an example:

```python
@event("my_event")
def my_event_handler(context, data):
    print("my_event was triggered!")
```

some events are triggered by outside sources, one such event is the `'init'` event. this event is triggered when your server is ready to serve requests.


### Task 1: create the init event handler
in main.py, create an event handler for the `'init'` event. make it print `"hello world"`.

<details>
<summary>Solution</summary>

```python
@event("init")
def init():
    print("hello world")
```
</details>

## The `fire_global()` function
the `fire_global()` function is used to trigger an event. it takes two arguments: the name of the event and the data to pass to the event handlers.

```python
fire_global("my_event", "hello world")
```

### Task 2: trigger your own event
create a new event handler for the event `'my_event'`. make it print the data it receives. then, trigger the event using `fire_global()` in the init event handler.

<details>
<summary>Hint 1</summary>
create a new event

```python
@event("my_event")
def my_event_handler(context, data):
    print(data)
```
</details>

<details>
<summary>Hint 2</summary>
amend the init event handler to trigger the event

```python
@event("init")
def init():
    fire_global("my_event", "hello world")
```

</details>

<details>
<summary>Solution</summary>

```python
@event("init")
def init():
    fire_global("my_event", "hello world")

@event("my_event")
def my_event_handler(context, data):
    print(data)
```
</details>

## Creating Asynchronous loops
the event system used by NECA can be leveraged to create asynchronous loops. creating an infinite while loop inside an event will cause the event system to stall.

```python
@event("init")
def init():

@event("my_event")
def my_event_handler(context, data):
    # don't do this!
    for i in range(100): 
        print("hello world")
        sleep(1) # sleeps also cause the event system to stall
```

instead, you can recursively call the event handler using `fire_global()`.

```python
@event("init")
def init():
    fire_global("my_event", 0)

@event("my_event")
def my_event_handler(context, data):
    print("hello world")

    # fire the event a maximum of 100 times
    if data < 100:
        fire_global("my_event", data + 1, delay=1)
```

### Task 3: create two infinite loops that alternate at even and odd seconds
create two infinte event sequences, one that prints `"Odd"` every odd second and one that prints `"Even"` every even second. (there are multiple ways to do this)

<details>
<summary>Hint 1</summary>
create two events, one for odd seconds and one for even seconds


```python
@event("odd")
def odd(context, data):
    print("Odd")
    fire_global("odd", data + 1, delay=1)

@event("even")
def even(context, data):
    print("Even")
    fire_global("even", data + 1, delay=1)
```
</details>

<details>
<summary>Hint 2</summary>
trigger the events in the init event handler

```python
@event("init")
def init():
    fire_global("even", 0)
    fire_global("odd", 0, delay=1)
```

</details>
<details>
<summary>Solution</summary>

```python
@event("init")
def init():
    fire_global("even", 0)
    fire_global("odd", 0, delay=1)

@event("odd")
def odd(context, data):
    print("Odd")
    fire_global("odd", data + 1, delay=1)

@event("even")
def even(context, data):
    print("Even")
    fire_global("even", data + 1, delay=1)
```
</details>

<details>
<summary>Alternative solution</summary>
this solution only uses one infinite loop, but alternates between two event handlers.

```python
@event("init")
def init():
    fire_global("even", 0)

@event("even")
def even(context, data):
    print("Even")
    fire_global("odd", data + 1, delay=1)

@event("odd")
def odd(context, data):
    print("Odd")
    fire_global("even", data + 1, delay=1)
```