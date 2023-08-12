# Contexts & Rules
## Contexts
A `Context` is an object that stores persistent data and contains a [Ruleset](#rulesets). It is primarily used for data storage. Each context may have its own ruleset, which can be used to override the global ruleset.

### Creating a context
you can create your own context by using `create_context()` in `neca.events`.
```python
from neca.events import create_context, Ruleset

ctx = create_context("MyContext")
```

### Accessing data
A context may store data. this data can be accessed by using the operator (`[]`).
```python
ctx['abc'] = 123
print(ctx['abc']) # 123
```

### Firing events in contexts
You can fire an event in a specific context by using the `fire()` method. It behaves the same as the `fire_global()` function, but it fires the event in the context it is called on instead of the global context.
```python
context.fire('message', 'hello world')
```

## Rulesets
A `Ruleset` is a collection of rules (event handlers). It is used to store rules and conditions. 
Example of how to use a ruleset:
```python
from neca.events import Ruleset

my_ruleset = Ruleset()

@my_ruleset.event('message')
@my_ruleset.condition(lambda context, event: event == 'hello')
def message(context, event):
    print(event)
```

> when you use the `@event` or `@condition` decorator, the rule or condition will be added to the global ruleset. 

### adding your own ruleset to a context
You can add your own ruleset to a context by passing it to the `ruleset` argument in `create_context()`.
```python
from neca.events import create_context, Ruleset

my_ruleset = Ruleset()
ctx = create_context(ruleset=my_ruleset, "MyContext")
```