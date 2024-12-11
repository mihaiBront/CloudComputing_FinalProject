import json
import logging as log

class Serializable(object):    
    @classmethod
    def from_dict(cls, json_dict: dict):
        """This method constructs a class from a Parsed JSON

        Args:
            json_dict (dict): Parsed ('json.loads()') JSON (
            or a mroe extensive class; some parameters may be ignored)

        Returns:
            any: Instance of the current class
        """
        
        log.error("This method is pending implementation")
        return None
    
    def to_dict(self):
        """This method converts the class to a dictionary

        Returns:
            dict: Dictionary representation of the class
        """
        return self.__dict__.copy()
    
    @classmethod
    def deserialize(self, json_string: str):
        """This method constructs a class from a JSON string

        Args:
            json_string (str): Serialized JSON representing this class (
            or a mroe extensive class; some parameters may be ignored)

        Returns:
            _type_: _description_
        """
        json_data = json.loads(json_string)
        return self.from_dict(json_data)
    
    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)