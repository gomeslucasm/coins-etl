import json
import os
from uuid import uuid4


class DataBase:
    """
    Simple database class that saves data to a JSON file.

    Attributes:
        __storage (dict): Stores the database data.
        __file_path (str): Path to the JSON file used for data persistence.

    Methods:
        __init__(): Initializes the instance and loads data from the JSON file.
        __load(): Loads data from the JSON file.
        __save(): Saves data to the JSON file.
        save(table_name: str, data: dict): Saves a new record to the specified table.
    """

    __storage = None
    __file_path = "db.json"

    def __init__(self):
        """Initializes the instance and loads data from the JSON file."""
        self.__load()

    def __load(self):
        """Loads data from the JSON file. If the file does not exist, initializes an empty storage."""
        if os.path.exists(self.__file_path):
            with open(self.__file_path, "r") as file:
                self.__storage = json.load(file)
        else:
            self.__storage = {}

    def __save(self):
        """Saves the current data to the JSON file."""
        with open(self.__file_path, "w") as file:
            json.dump(self.__storage, file, indent=4)

    def save(self, *, table_name: str, data: dict):
        """
        Saves a new record to the specified table.

        Args:
            table_name (str): The name of the table where the record will be saved.
            data (dict): Dictionary containing the record data.

        Returns:
            dict: The saved record with an additional 'uuid' field.
        """
        if table_name not in self.__storage:
            self.__storage[table_name] = []

        data["uuid"] = str(uuid4())
        self.__storage[table_name].append(data)
        self.__save()

        return data


def get_db() -> DataBase:
    """
    Returns an instance of the DataBase class.

    Returns:
        DataBase: An instance of the DataBase class.
    """
    return DataBase()
