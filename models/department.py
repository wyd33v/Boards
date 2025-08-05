"""
A file that contains class of Department and everything related.
"""
import uuid

from models.storage import Storage


class Department(Storage):
    file_path = "./data/departments"

    def __init__(self, department_name):
        self.id = uuid.uuid4()
        self.name = department_name
        super().add()
        print("department was created")

    @classmethod
    def get_all(cls):
        print(len(cls.storage))
        return cls.storage.items()
    
    