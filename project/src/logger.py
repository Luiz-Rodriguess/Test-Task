from datetime import datetime

class Logger:
    def __init__(self):
        self.deleted = []
        self.created = []
        self.changed = []

    def addDeleted(self,message):
        self.deleted.append(message)
    
    def addCreated(self,message):
        self.created.append(message)
    
    def addChanged(self,message):
        self.changed.append(message)
    
    def simpleLog(self) -> str:
        log_string =  f"{len(self.created)} items created\n"
        log_string += f"{len(self.deleted)} items deleted\n"
        log_string += f"{len(self.changed)} items changed\n"
        return log_string
    
    def detailedLog(self) -> str:
        log_string = f"{datetime.now()}\n\n"
        for item in self.created:
            log_string += f"{item}\n"
        for item in self.deleted:
            log_string += f"{item}\n"
        for item in self.changed:
            log_string += f"{item}\n"
        log_string += "\n"
        return log_string