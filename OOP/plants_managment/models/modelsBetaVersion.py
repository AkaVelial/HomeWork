import json


class Plant:

    file = "database/plants.json"

    def __init__(self, name, address):
        self.name = name
        self.address = address

    def generate_dict(self):
        return {
            "name": self.name,
            "address": self.address
        }

    def save(self):
        file = open(self.file, "r")
        datalist = json.loads(file.read())
        file.close()
        file = open(self.file, "w")
        data = self.generate_dict()
        if len(datalist) >= 1:
            data["id"] = len(datalist) + 1
        else:
            data["id"] = 1
        datalist.append(data)
        file.write(json.dumps(datalist, indent=4))
        file.close()

    @classmethod
    def get_all(cls):
        file = open(cls.file, "r")
        datalist = json.loads(file.read())
        file.close()
        for data in datalist:
            for key, value in data.items():
                print(key, value)


class Employee(Plant):

    file = "database/employees.json"

    def __init__(self, name, email, plant_id):
        super().__init__(None, None)
        self.name = name
        self.email = email
        self.plant_id = plant_id

    def generate_dict(self):
        employee_dict = super().generate_dict()
        employee_dict["name"] = self.name
        employee_dict["email"] = self.email
        employee_dict["plant_id"] = self.plant_id
