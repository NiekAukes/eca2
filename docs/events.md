# Events (Deprecated)
## Firing events
Events can be fired in a context by using the `fire` method.
```python
context.fire('message', 'hello world')
```
The `fire` method takes two arguments: the event type and the event data.

### firing events in other contexts
in addition to the `fire` method in a specific context, there is also the `fire_global` method in `neca.events`, and a `fire_all` method in `neca.Context`. the `fire_global` method fires an event in the global context, and the `fire_all` method fires an event in all contexts.
```python
from neca.events import fire_global, fire_all

fire_global('message', 'hello world') # fires only in the global context
fire_all('message', 'hello world') # fires in all contexts
```

### Delayed events
you can also specify a delay for the event to be fired after a specific amount of time.
```python
context.fire('message', 'hello world', delay=5) # fires after 5 seconds
```

### fire_immediate
Events fired with the `fire`, `fire_global` or `fire_all` methods are executed by the event loop. This means that the code after the `fire` method will be executed before or at the same time as the event is fired. if you want to wait for the event to be handled before continuing, you can use the `fire_immediate` method.
```python
context.fire_immediate('message', 'hello world') # fires immediately without waiting for the event loop
```

