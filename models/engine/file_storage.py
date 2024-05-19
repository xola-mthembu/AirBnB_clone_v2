#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Represent an abstracted storage engine.

    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Return a dictionary of instantiated objects in __objects.

        If a cls is specified, returns a dictionary of objects of that type.
        Otherwise, returns the __objects dictionary.
        """
        if cls is not None:
            if isinstance(cls, str):
                cls = eval(cls)
            cls_dict = {}
            for k, v in self.__objects.items():
                if type(v) == cls:
                    cls_dict[k] = v
            return cls_dict
        return self.__objects

    def new(self, obj):
        """Set in __objects obj with key <obj_class_name>.id"""
        self.__objects["{}.{}".format(type(obj).__name__, obj.id)] = obj

    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        odict = {o: self.__objects[o].to_dict() for o in self.__objects.keys()}
        with open(self.__file_path, "w") as f:
            json.dump(odict, f)

    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists."""
        try:
            with open(self.__file_path, "r") as f:
                objdict = json.load(f)
                self.__objects = {k: eval(v["__class__"])(**v) for k, v in
                                  objdict.items()}
        except FileNotFoundError:
            return

    def delete(self, obj=None):
        """Delete obj from __objects if it's inside.

        If obj is equal to None, the method should not do anything.
        """
        if obj is not None:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """Call reload() method for deserializing the JSON file to objects."""
        self.reload()
