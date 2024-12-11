from datetime import datetime
import numpy as np

class DateTimeHelper(object):
    @staticmethod
    def dateStrFromUtcInt(date: int)  -> str:
        return datetime.utcfromtimestamp(date).strftime('%Y-%m-%d')
    
    def hourFromDaysecondsInt(dayseconds: int) -> int:
        hour, minutes = divmod(dayseconds, 3600)
        minutes, seconds = divmod(minutes, 60)
        
        hour = str(hour).zfill(2)
        minutes = str(minutes).zfill(2)
        seconds = str(seconds).zfill(2)
        
        return f"{hour}:{minutes}:{seconds}"