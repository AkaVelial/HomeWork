import json
from abc import ABC, abstractmethod


class Model(ABC):
    file = ""
    fields = []

    def generate_dict(self):
        return self.__dict__

    @classmethod
    @abstractmethod
    def get_el_by_id(cls, id):
        pass

    @classmethod
    def get_all(cls):
        try:
            with open(cls.file, "r") as file:
                data = json.loads(file.read())
                for el in data:
                    for key in cls.fields:
                        print(el[key])
        except FileNotFoundError:
            print(f"File {cls.file} not found")

    @classmethod
    def get_file_data(cls):
        try:
            with open(cls.file, "r") as file:
                data = json.loads(file.read())
                return data
        except Exception as e:
            print("Error reading file:", e)
            return []

    @classmethod
    def save_to_file(cls, data):
        try:
            with open(cls.file, "w") as file:
                file.write(json.dumps(data))
        except IOError:
            print(f"Error: could not write to file {cls.file}")

    def save(self):
        data = self.get_file_data()
        new_el = self.generate_dict()
        if len(data) >= 1:
            new_el["id"] = len(data) + 1
        else:
            new_el["id"] = 1
        data.append(new_el)
        self.save_to_file(data)

    def update(self):
        data = self.get_file_data()
        for el in data:
            if el["id"] == self.id:  # unresoldev atr reference "id" for class Model ???
                for key in self.fields:
                    el[key] = input("Type a new " + key + ": ")
        self.save_to_file(data)

    # def update(self, **kwargs):
    #     data = self.get_file_data()
    #     for el in data:
    #         if el["id"] == self.id:
    #             for key, value in kwargs.items():
    #                 el[key] = value
    #     self.save_to_file(data)
