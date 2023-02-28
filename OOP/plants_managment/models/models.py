import json


class DatabaseObject:
    file = ""

    def generate_dict(self):
        raise NotImplementedError()

    def save(self):
        try:
            with open(self.file, "r") as file:
                objects = json.loads(file.read())
        except FileNotFoundError:
            objects = []

        obj = self.generate_dict()
        if len(objects) >= 1:
            obj["id"] = len(objects) + 1
        else:
            obj["id"] = 1
        objects.append(obj)

        try:
            with open(self.file, "w") as file:
                file.write(json.dumps(objects, indent=4))
        except IOError:
            print("Error saving to file: ", self.file)

    @classmethod
    def get_all(cls):
        try:
            with open(cls.file, "r") as file:
                objects = json.loads(file.read())
        except FileNotFoundError:
            objects = []

        for obj in objects:
            for key, value in obj.items():
                print(key, value)


class Plant(DatabaseObject):
    file = "database/plants.json"

    def __init__(self, name, address):
        self.name = name
        self.address = address

    def generate_dict(self):
        return {
            "name": self.name,
            "address": self.address
        }


class Employee(DatabaseObject):
    file = "database/employees.json"

    def __init__(self, name, email, plant_id):
        self.name = name
        self.email = email
        self.plant_id = plant_id

    def generate_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "plant_id": self.plant_id
        }
