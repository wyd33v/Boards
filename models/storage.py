"""
A class for temp in-memory or pickle 
"""



# def singleton(cls):
#     instances = {}
#     def get_instance(*args, **kwargs):
#         if cls not in instances:
#             instances[cls] = cls(*args, **kwargs)
#         return instances[cls]
#     return get_instance

# @singleton
# class Storage:
#     def __init__(self):
#         pass


import json
import pickle


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Storage(metaclass=SingletonMeta):
    storage = {}
    file_path = None
        
    @classmethod
    def initialize_storage(cls):
        cls.storage = {}
        try:
            with open(cls.file_path, "rb") as f:
                pass # pickle file for exists in system. skip
        except FileNotFoundError:
            open(cls.file_path, 'a').close() # create empty file if not exists

    @classmethod
    def dump_data(cls):
        with open(cls.file_path, "wb") as f:
            pickle.dump(cls.storage, f, 0)
        print("data was dumped")
    
    @classmethod
    def load_data(cls):
        cls.storage = {}
        with open(cls.file_path, "rb") as f:
            cls.storage = pickle.load(f)
        print("data was loaded")
        
    def get_all(self):
        items = []
        for k, v in self.storage.items():
            items.append(v)
        return items

    @classmethod
    def get(cls, id):
        return cls.storage.get(id)
    
    def add(self):
        self.storage[self.id] = self


