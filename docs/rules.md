# Rules and Contexts

## General
Rules and Contexts form the backbone of neca. they are used to handle events and store data. A rule is a function that is invoked when an event is fired in a context. A context is a place where events can be fired and data can be stored. Every program has a global context, using the global ruleset. A context can have its own ruleset, which can be used to override the global ruleset.

## Rules
a rule is a function that takes a context and an event as arguments.
it is invoked when an event is received in the `Context`

example of a rule:
```python
from neca.events import event
@event('message') # @event is a decorator that registers the function as a rule, the function attached will be invoked when an event of type 'message' is received
def message(context, event):
    print(event)
```
this code creates a rule in the global ruleset. this ruleset is used as a default ruleset for all contexts. a context can have its own ruleset.


the example below shows how to create your own ruleset and add a rule to it.
```python
from neca.events import Ruleset, event
my_ruleset = Ruleset()

@my_ruleset.event('message')
def message(context, event):
    print(event)
```

### Conditions
you can add a condition to a rule by using the `@condition` decorator.
```python
from neca.events import Ruleset, event, condition

@event('message')
@condition(lambda context, event: event == 'hello')
def message(context, event):
    print(event)
```
the condition is a function that takes a context and an event as arguments and returns a boolean value. if the condition returns `True` the rule will be invoked, otherwise it will be ignored.

<div class="warning">
    When using custom rulesets, you need to use 
    <code>@my_ruleset.condition</code> 
    instead of 
    <code>@condition</code>
</div> 

## Contexts
a context is a class that inherits from `neca.Context`. it is used to store data and rules. a context must have a `Ruleset`, if no ruleset is provided, the global ruleset will be used.

a context is a place where events can be fired. when an event is fired in a context, all rules will be checked and invoke if the conditions are met.

example of how to use a context:
```python
@event('message') # this rule will be added to the global ruleset
def message(context, event):
    context.fire('message', context['abc']) # this will fire the 'message' event in the context
```

a context may store data. this data can be accessed by using the operator (`[]`).

### Creating a context
you can also create your own context by using `create_context()` in `neca.events`.
```python
from neca.events import create_context, Ruleset
my_ruleset = Ruleset()
ctx = create_context(ruleset=my_ruleset, "MyContext")
```

<style>
    .warning {
        background-color: #eed20220;
        padding: 10px;
        border-radius: 5px;
    }

</style>