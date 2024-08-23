"""
The "events" module provides a flexible event handling system for managing and handling events within your application.

Events are a fundamental part of many software systems, allowing different parts of your code to communicate and respond to specific occurrences or triggers. This module offers a set of tools to manage events, define event handlers, and emit events within your application.

Most used functions and decorators:
- @event(key): A decorator for event handlers. Functions decorated with @event(key) will be called when "fire_global(key, context)" is invoked with the specified key. It attaches the event to the global rules object.

- @condition(condition): Sets a condition for an event handler. It attaches the condition to the global rules object.

- fire_global(eventname, data, delay=None): Emits a global event with the given name in the global context. All functions annotated with @event(key) are called with the provided context.

- fire_all(eventname, data, delay=None): Emits an event with the given name in every context. All functions annotated with @event(key) are called for each context.

- create_context(name=None, ruleset=None): Creates a new context and returns it. You can specify the ruleset to use for this context, and optionally, provide a name. If no ruleset is specified, the global ruleset is used.

- emit(event, data, id=None): Emits a new event to the outside world, typically to a web browser. You can specify the event name, data (convertible to JSON through json.dumps), and an optional identifier.

Example Usage:
```python
from events import Ruleset, event, fire_global, create_context, emit

# Define event handlers
@event("user_login")
def handle_login(context, event_data):
    # Handle user login event
    pass

# Emit a global event
fire_global("user_login", {"user_id": 123})

# Emit an event to the outside world (browser)
emit("browser_event", {"message": "Hello, world!"})
```
"""

from time import sleep
from typing import Callable, Any, Dict, List, Optional, Tuple
from neca.log import logger
from datetime import datetime, timedelta
import neca.settings as settings
from threading import RLock



class Ruleset:
    """
    a Ruleset object is a collection of rules that can be used to handle events.
    rules are functions that take a context and an event as arguments.
    they are called when an event is fired.
    """

    class Rule:
        """
        a rule is a function that takes a context and an event as arguments.
        it is called when an event is fired.
        
        mostly used for internal bookkeeping. If you're a user,
        you probably won't need to use this class directly.
        """
        def __init__(self, 
                     func: Callable[["Context", Any], None], 
                     keys: List[str], 
                     varnames: Tuple[str], 
                     min_args: int,
                     include_context: bool = False):
            self.func = func
            self.conditions = []
            self.keys = keys
            self.varnames = varnames
            self.min_args = min_args
            self.include_context = include_context
            
        def add_condition(self, condition: Callable[["Context", Any], bool]):
            """
            adds a condition to the rule.
            """
            self.conditions.append(condition)
            
        def check_conditions(self, context: Any, args, kwargs) -> bool:
            """
            checks if all conditions are met.
            """
            for condition in self.conditions:
                if not condition(context, *args, **kwargs):
                    return False
            return True
            
    
    def __init__(self):
        self.functions: Dict[Callable[..., None], Ruleset.Rule] = {}
        
        # a dictionary of rules, indexed by event name
        # "eventname": [rule1, rule2, ...]
        # "eventname2": [rule3, rule4, ...]
        self.index: Dict[str, List[Ruleset.Rule]] = {}
        
        
    
    def event(self, key: str):
        """
        decorator for event handlers, 
        the decorated function will be called when context.fire(key, context) is called 
        on the key given to this decorator.
        """
        
        def decorator(func: Callable[..., None]):
            # check if the function is callable
            if not callable(func):
                raise ValueError("function is not callable")
            
            # if the arg count is greater than 0, include the context
            include_context = func.__code__.co_argcount > 0

            # get the function arguments, these are the first n variables of the function
            argnames =  func.__code__.co_varnames[:func.__code__.co_argcount]
            
            # get or create the rule
            rule: Ruleset.Rule = self.functions.get(func, Ruleset.Rule(
                func, 
                [], 
                argnames, 
                func.__code__.co_argcount - len(func.__defaults__ or []), 
                include_context))
            rule.keys.append(key)
            
            # the function is indexed by the key
            if key not in self.index:
                self.index[key] = []
            else:
                # check if the function arguments are equal to other functions with the same key
                other_params = self.index[key][0].varnames
                if len(other_params) <= 1 and len(rule.varnames) > 1:
                    raise ValueError(f"""function '{func.__name__}' has data arguments, but other functions with key '{key}' do not.""")
                elif other_params != rule.varnames and not (len(other_params) <= 1 and len(rule.varnames) <= 1):
                    raise ValueError(f"""function '{func.__name__}' has different data arguments than other functions with key {key}.
                    {func.__name__} has arguments: {rule.varnames}
                    other functions have arguments: {other_params}""")
                
            # check if the rule is already in the index
            if rule in self.index[key]:
                raise ValueError(f"function already registered for event key: {key}. You can only register a function once per event key.")
            self.index[key].append(rule)
                
            if func not in self.functions:
                # register the function as a rule
                # the function is indexed by itself
                self.functions[func] = rule
                
            return func
        return decorator
        

    #def fire(self, eventname: str, data: Any, delay: Optional[float] = None):
    #    """
    #    emits an event with the given name in the current context.
    #    When this function is called, every function annotated with @event(key) is called.
    #    with the given context.
    #    """
    #    # for now just call fire_global
    #    fire_global(eventname, data, delay)


    def condition(self, condition: Callable[..., bool]):
        """
        sets a condition for an event handler. 
        """

        
        
        def decorator(func: Callable[..., None]):
            # check if function is registered
            if func not in self.functions:
                # add the function to the rules with an empty keyset
                attached_function_argnames = func.__code__.co_varnames[:func.__code__.co_argcount]
                self.functions[func] = Ruleset.Rule(func, 
                                                    [], 
                                                    attached_function_argnames, 
                                                    func.__code__.co_argcount - len(func.__defaults__ or []),
                                                    func.__code__.co_argcount > 0)
            
            # check if the condition arguments are equal to the attached function
            other_params = self.functions[func].varnames
            condition_params = condition.__code__.co_varnames[:condition.__code__.co_argcount]

            if len(other_params) <= 1 and len(condition_params) > 1:
                raise ValueError(f"""condition '{condition.__name__}' has data arguments, but the attached function '{func.__name__}' does not.""")
            elif other_params != condition_params and not (len(other_params) <= 1 and len(condition_params) <= 1):
                raise ValueError(f"""condition '{condition.__name__}' has different data arguments than the attached function '{func.__name__}'.
                {condition.__name__} has arguments: {condition_params}
                {func.__name__} has arguments: {other_params}""")

            


            # add the condition to the rule
            self.functions[func].add_condition(condition)
            return func
        
        return decorator

class Context:
    def __init__(self, ruleset: Ruleset, name: Optional[str] = None):
        self._data: Dict[Any, Any] = {}
        self.ruleset = ruleset
        
        if name is None:
            self.name = str(id(self))
        else:
            self.name = name
            
    
    def __getitem__(self, key: Any):
        return self._data[key]
    
    def __setitem__(self, key, value):
        self._data[key] = value
    
    def __delitem__(self, key):
        del self._data[key]
    
    def __contains__(self, key):
        return key in self._data
    
    def __str__(self) -> str:
        return f"Context({self.name})"
    
    def fire(self, event_name: str, *args, delay: Optional[float] = None, **kwargs):
        """
        emits an event with the given name in the current context.
        When this function is called, every function annotated with @event(key) is called.
        with the given context.
        
        key: the name of the event
        delay: the delay in seconds before the event is fired
        args/kwargs: the arguments to pass to the event handlers
        """
        # check if an event handler exists for this event
        if event_name not in self.ruleset.index:
            # no rules for this event, send a warning
            # to notify what is going on
            logger.warning(f"no rules for event: {event_name}")
            return

        # check if the args and kwargs are valid
        expected_args = self.ruleset.index[event_name][0].varnames
        kwargs_keys = set(kwargs.keys())

        # throw error if not all kwargs are expected
        if not kwargs_keys.issubset(set(expected_args)):
            raise ValueError(f"unexpected keyword arguments: {kwargs_keys - set(expected_args)}")
        
        # take the remaining args and check with the expected args
        if len(expected_args) > 1:
            if len(args) > len(expected_args) - 1:
                raise ValueError(f"too many positional arguments: {args[len(expected_args):]}")
            if len(args) < self.ruleset.index[event_name][0].min_args - 1:
                raise ValueError(f"not enough positional arguments: missing {expected_args[len(args):]}")
        elif len(args) > 0:
            raise ValueError(f"unexpected positional arguments: {args}")


        Manager.add_event(event_name, self, delay, args, kwargs)
    
    def fire_immediate(self, key: str, args: List[Any] = [], kwargs: Dict[str, Any] = {}):
        """
        emits an event with the given name in the current context.
        When this function is called, every function annotated with @event(key) is called.
        with the given context.
        
        WARNING: this function fires the event immediately, without waiting for the event loop.
        
        key: the name of the event
        args/kwargs: the arguments to pass to the event handlers
        """
            
        # for now just use the global rules object
        rules = self.ruleset.index.get(key, [])
        if rules == []:
            # no rules for this event, send a warning
            # to notify what is going on

            # TODO: this technically can't happen anymore,
            # because fire() checks if the event exists
            logger.warning(f"no rules for event: {key}")
            return
            
        for rule in rules:
            if rule.check_conditions(self, args, kwargs):
                # call the function
                if rule.include_context:
                    rule.func(self, *args, **kwargs)
                else:
                    rule.func(*args, **kwargs)
            else:
                # send a debug message
                logger.debug(f"rule for {rule.func} did not meet conditions for event: {key}")
        
class PendingEvent:
    """
    Data class for pending events.
    """
    def __init__(self, key: str, stamped: datetime,
                    context: "Context", delay: Optional[float] = None, args: List[Any] = [], kwargs: Dict[str, Any] = {}):
        """
        key: the name of the event
        stamped: the timestamp of when the event was created
        context: the context for which the event was created
        delay: the delay in seconds before the event is fired

        args/kwargs: the arguments to pass to the event handlers
        """
        self.key = key
        self.args = args
        self.kwargs = kwargs
        self.stamped = stamped
        self.context = context
        self.delay = delay
    

class Manager:
    """
    the manager keeps track of the rules and contexts.
    """
    
            
    global_ruleset: Ruleset = Ruleset()
    global_context: Context = Context(global_ruleset, "global")
    rulesets: List[Ruleset] = [global_ruleset]
    contexts: List[Context] = [global_context]

    # lock for the pending events, add_event may be 
    # called from multiple threads
    _lock = RLock()
    

    pending_event_keys: List[PendingEvent] = []
    
    @staticmethod
    def eventLoop(stop_on_empty: bool = False):
        """
        the event keeps an eye on the events and calls the 'init' event when the engine starts.
        """
        # wait 100 ms before calling init
        # so that the web server has time to start
            
        sleep(0.1)
        logger.debug("calling init event")
        fire_global("init")
        while True:
            # sort the pending events by timestamp + delay
            Manager._lock.acquire()
            Manager.pending_event_keys.sort(key=lambda x: x.stamped + timedelta(seconds=x.delay or 0))
            
            # loop over the pending events
            # and fire those that are ready
            for pending_event in Manager.pending_event_keys:
                if pending_event.stamped + timedelta(seconds=pending_event.delay or 0) < datetime.now():
                    # fire the event
                    pending_event.context.fire_immediate(pending_event.key, pending_event.args, pending_event.kwargs)
                    # remove the event from the list
                    Manager.pending_event_keys.remove(pending_event)
                else:
                    break

            if stop_on_empty and len(Manager.pending_event_keys) == 0:
                # stop the event loop
                Manager._lock.release()
                return
            Manager._lock.release()
            # sleep for 10 ms
            sleep(0.01)
    
    @staticmethod
    def add_event(key: str, context: Context, delay: Optional[float] = None, args: Tuple[Any, ...] = tuple(), kwargs: Dict[str, Any] = {}):
        """
        adds an event to the event loop. The event will be fired after the given delay.
        """
        Manager._lock.acquire()
        Manager.pending_event_keys.append(PendingEvent(key, datetime.now(), context, delay, args, kwargs))
        Manager._lock.release()
    
    
    
    
def event(key: str):
    """
    decorator for event handlers, 
    the decorated function will be called when fire_global(key, context) is called 
    on the key given to this decorator.

    same as Rules.event, but attaches the event to the global rules object.
    """
    return Manager.global_ruleset.event(key)

def condition(condition: Callable[[Any, Any], bool]):
    """
    sets a condition for an event handler. 

    same as Rules.condition, but attaches the condition to the global rules object.
    """
    return Manager.global_ruleset.condition(condition)


def fire_global(eventname: str, *args, delay: Optional[float] = None, **kwargs):
    """
    emits a global event with the given name in the global context.
    When this function is called, every function annotated with @event(key) is called.
    with the given context.
    
    key: the name of the event
    data: the data to pass to the event handlers
    delay: the delay in seconds before the event is fired
    """
    Manager.global_context.fire(eventname, *args, delay=delay, **kwargs)
    
def fire_all(eventname: str, *args, delay: Optional[float] = None, **kwargs):
    """
    emits an event with the given name in every context.
    When this function is called, every function annotated with @event(key) is called.
    """
    for context in Manager.contexts:
        context.fire(eventname, *args, delay=delay, **kwargs)
    

def create_context(name: Optional[str] = None, ruleset: Optional[Ruleset] = None) -> Context:
    """
    creates a new context and returns it.
    ruleset: the ruleset to use for this context. If None, the global ruleset is used.
    name: the name of the context. If None, the name becomes the object id of the context.
    """
    context = Context(ruleset or Manager.global_ruleset, name)
    Manager.contexts.append(context)
    return context

def emit(event, data, id=None):
    """
    Emits a new event to the outside world (which is usually the browser).

    name: the name of the emitted event
    data: a piece of data that can be converted to JSON through json.dumps
    id: optional identifier to be emitted. None indicates no identifier is emitted.

    """
    if id is not None:
        data.update({"id": id})
    settings.socket.emit(event, data)