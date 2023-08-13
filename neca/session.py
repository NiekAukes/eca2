from events import *
## NOT YET USED AND UNFINISHED

class SessionContext(Context):
    def __init__(self, session: "Session", ruleset: Ruleset, name: Optional[str] = None):
        super().__init__(ruleset, name)
        self.session = session
        
    def emit(self, eventname: str, data: Any):
        self.session.emit(eventname, data)
        
    def __str__(self) -> str:
        return f"SessionContext({self.name})"
    
    def __setitem__(self, key, value):  
        self._data[key] = value
        
        # update the client on the context change  
        self.emit("\1", {key: value})
    
    def __delitem__(self, key):
        del self._data[key]
        
        # update the client on the context change
        self.emit("\2", key)
    

class Session:
    def __init__(self, socket, name: Optional[str] = None):
        self.socket = socket
        self.context = SessionContext(self, Ruleset(), name)
        
    def emit(self, eventname: str, data: Any):
        self.socket.emit(eventname, data)
        

class SessionManager:
    def __init__(self):
        self.sessions: List[Session] = []
        
    def create_session(self, s, name: Optional[str] = None) -> Session:
        session = Session(s, name)
        self.sessions.append(session)
        return session