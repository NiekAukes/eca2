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
from typing import Callable, Any, Dict, List, Optional
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
        def __init__(self, func: Callable[["Context", Any], None], keys: List[str]):
            self.func = func
            self.conditions = []
            self.keys = keys
            
        def add_condition(self, condition: Callable[["Context", Any], bool]):
            """
            adds a condition to the rule.
            """
            self.conditions.append(condition)
            
        def check_conditions(self, context: Any, event: Any) -> bool:
            """
            checks if all conditions are met.
            """
            for condition in self.conditions:
                if not condition(context, event):
                    return False
            return True
            
    
    def __init__(self):
        self.functions: Dict[Callable[["Context", Any], None], Ruleset.Rule] = {}
        
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
        
        def decorator(func: Callable[["Context", Any], None]):
            # check if the function is callable
            if not callable(func):
                raise ValueError("function is not callable")
            

            # get or create the rule
            rule = self.functions.get(func, Ruleset.Rule(func, []))
            rule.keys.append(key)
            
            
            # the function is indexed by the key
            if key not in self.index:
                self.index[key] = []
                
            # check if the rule is already in the index
            if rule in self.index[key]:
                # raise an error
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


    def condition(self, condition: Callable[["Context", Any], bool]):
        """
        sets a condition for an event handler. 
        """
        
        def decorator(func: Callable[["Context", Any], None]):
            
            # check if function is registered
            if func not in self.functions:
                # add the function to the rules with an empty keyset
                self.functions[func] = Ruleset.Rule(func, [])
            
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
    
    def get(self, key: Any, default: Any = None):
        return self._data.get(key, default)
    
    def __setitem__(self, key, value):
        self._data[key] = value
    
    def __delitem__(self, key):
        del self._data[key]
    
    def __contains__(self, key):
        return key in self._data
    
    def __str__(self) -> str:
        return f"Context({self.name})"
    
    def fire(self, event_name: str, data: Any = None, delay: Optional[float] = None):
        """
        emits an event with the given name in the current context.
        When this function is called, every function annotated with @event(key) is called.
        with the given context.
        
        key: the name of the event
        data: the data to pass to the event handlers
        delay: the delay in seconds before the event is fired
        """
        Manager.add_event(event_name, data, self, delay)
    
    def fire_immediate(self, key: str, data: Any):
        """
        emits an event with the given name in the current context.
        When this function is called, every function annotated with @event(key) is called.
        with the given context.
        
        WARNING: this function fires the event immediately, without waiting for the event loop.
        
        key: the name of the event
        data: the data to pass to the event handlers
        """
            
        # for now just use the global rules object
        rules = self.ruleset.index.get(key, [])
        if rules == []:
            # no rules for this event, send a warning
            # to notify what is going on
            logger.warning(f"no rules for event: {key}")
            return
            
        for rule in rules:
            if rule.check_conditions(self, data):
                # call the function
                #try:
                    rule.func(self, data)
                #except TypeError as e:
                    #logger.error(f"error while calling function {rule.func.__name__} for event {key}: {e}")
                    #logger.warn(f"is your function missing an argument? event handlers should have the signature: func(context, event)")
                # Try catch block commented out because it was causing unrelated errors to be caught

            else:
                # send a debug message
                logger.debug(f"rule for {rule.func} did not meet conditions for event: {key}")
        
    
    

class Manager:
    """
    the manager keeps track of the rules and contexts.
    """
    class PendingEvent:
        """
        Data class for pending events.
        """
        def __init__(self, key: str, data: Any, stamped: datetime,
                     context: Any = None, delay: Optional[float] = None):
            """
            key: the name of the event
            data: the data to pass to the event handlers
            stamped: the timestamp of when the event was created
            context: the context for which the event was created
            delay: the delay in seconds before the event is fired
            """
            self.key = key
            self.data = data
            self.stamped = stamped
            self.context = context
            self.delay = delay
            
    global_ruleset: Ruleset = Ruleset()
    global_context: Context = Context(global_ruleset, "global")
    rulesets: List[Ruleset] = [global_ruleset]
    contexts: List[Context] = [global_context]

    # lock for the pending events, add_event may be 
    # called from multiple threads
    _lock = RLock()
    
    pending_event_keys: List[PendingEvent] = []
    
    @staticmethod
    def eventLoop():
        """
        the event keeps an eye on the events and calls the 'init' event when the engine starts.
        """
        # wait 100 ms before calling init
        # so that the web server has time to start
            
        sleep(0.1)
        logger.debug("calling init event")
        fire_global("init", None)
        while True:
            # sort the pending events by timestamp + delay
            Manager._lock.acquire()
            Manager.pending_event_keys.sort(key=lambda x: x.stamped + timedelta(seconds=x.delay or 0))
            
            # loop over the pending events
            # and fire those that are ready
            for pending_event in Manager.pending_event_keys:
                if pending_event.stamped + timedelta(seconds=pending_event.delay or 0) < datetime.now():
                    # fire the event
                    pending_event.context.fire_immediate(pending_event.key, pending_event.data)
                    # remove the event from the list
                    Manager.pending_event_keys.remove(pending_event)
                else:
                    break
            Manager._lock.release()
            # sleep for 10 ms
            sleep(0.01)
    
    @staticmethod
    def add_event(key: str, data: Any, context: Context, delay: Optional[float] = None):
        """
        adds an event to the event loop. The event will be fired after the given delay.
        """
        Manager._lock.acquire()
        Manager.pending_event_keys.append(Manager.PendingEvent(key, data, datetime.now(), context, delay))
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


def fire_global(eventname: str, data: Any, delay: Optional[float] = None):
    """
    emits a global event with the given name in the global context.
    When this function is called, every function annotated with @event(key) is called.
    with the given context.
    
    key: the name of the event
    data: the data to pass to the event handlers
    delay: the delay in seconds before the event is fired
    """
    Manager.add_event(eventname, data, Manager.global_context, delay)
    
def fire_all(eventname: str, data: Any, delay: Optional[float] = None):
    """
    emits an event with the given name in every context.
    When this function is called, every function annotated with @event(key) is called.
    """
    for context in Manager.contexts:
        Manager.add_event(eventname, data, context, delay)
    

def create_context(name: Optional[str] = None, ruleset: Optional[Ruleset] = None) -> Context:
    """
    creates a new context and returns it.
    ruleset: the ruleset to use for this context. If None, the global ruleset is used.
    name: the name of the context. If None, the name becomes the object id of the context.
    """
    context = Context(ruleset or Manager.global_ruleset, name)
    Manager.contexts.append(context)
    return context

def emit(event, data, id = None, sid: str | None = None):
    """
    Emits a new event to the outside world (which is usually the browser).

    name: the name of the emitted event
    data: a piece of data that can be converted to JSON through json.dumps
    id: optional identifier to be emitted. None indicates no identifier is emitted.
    sid: the session id to emit to. If None, the event is emitted to all sessions.
    """
    if id is not None:
        data.update({"id": id})
    settings.socket.emit(event, data, to=sid)