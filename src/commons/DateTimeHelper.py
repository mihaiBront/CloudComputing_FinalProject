from datetime import datetime

class DateTimeHelper(object):
    @staticmethod
    def dateStrFromUtcInt(date: int)  -> str:
        return datetime.utcfromtimestamp(date).strftime('%Y-%m-%d') 
    
    @staticmethod
    def hourFromDaysecondsInt(dayseconds: int) -> str: #TODO: Review if this needs to be timezone aware or not
        hour, minutes = divmod(dayseconds, 3600)
        minutes, seconds = divmod(minutes, 60)
        
        hour = str(hour).zfill(2)
        if hour == "24":
            hour = "00"
        minutes = str(minutes).zfill(2)
        seconds = str(seconds).zfill(2)
        
        return f"{hour}:{minutes}:{seconds}" 
    
    @staticmethod
    def getTimestampNow() -> str:
        return datetime.fromtimestamp(datetime.now().timestamp())
    
    @staticmethod
    def dateTimeFromStr(string) -> str:
        return datetime.strptime(string, '%Y-%m-%d %H:%M:%S')
    
    @staticmethod
    def changeDatePartString(string, newDate: datetime) -> str:
        return datetime.strptime(string, '%Y-%m-%d %H:%M:%S').replace(year=newDate.year, month=newDate.month, day=newDate.day).strftime('%Y-%m-%d %H:%M:%S')
        