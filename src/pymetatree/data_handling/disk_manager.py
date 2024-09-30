"""
This module provides a `DiskManager` class for managing data storage and retrieval operations on disk.

The `DiskManager` class allows you to save data as JSON files on disk and load data from JSON files.
It handles the creation of the data storage directory if it doesn't exist and provides methods for
saving and loading data.

The module also includes exception handling for various errors that may occur during disk operations,
such as OSError (for file operations), TypeError (for invalid input data), and ValueError (for invalid
JSON data).
"""

import os
import json
from loguru import logger
from typing import List, Dict

logger.add("eawag_data_connector.log", rotation="1 MB", level="INFO")


class EAWAGDiskManager:
    """
    A class for managing data storage and retrieval on disk.

    Attributes:
        data_storage_directory (str): The directory path where data will be stored.

    Methods:
        save_data_as_json(data: List[Dict], file_name: str) -> None:
            Saves the provided data as a JSON file on disk.
        load_json_data(file_name: str) -> List[Dict]:
            Loads and returns data from a JSON file on disk.
    """
    def __init__(self, data_storage_directory: str) -> None:
        self.data_storage_directory = data_storage_directory
        if not os.path.exists(self.data_storage_directory):
            try:
                os.makedirs(self.data_storage_directory)
            except OSError as e:
                logger.error(f"Error creating data storage directory: {e}")
                raise e

    def save_data_as_json(self, data: List[Dict], file_name: str) -> None:
        """
        Saves the provided data as a JSON file on disk.

        Args:
            data (List[Dict]): The data to be saved as a JSON file.
            file_name (str): The name of the file to be saved.

        Raises:
            OSError: If there is an error creating or writing to the file.
            TypeError: If the provided data is not a list of dictionaries.
        """
        if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
            raise TypeError("Input data must be a list of dictionaries.")
        file_path = os.path.join(self.data_storage_directory, file_name)
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except OSError as e:
            logger.error(f"Error while saving reaction data: {e}")
            raise e

    def load_json_data(self, file_name: str) -> List[Dict]:
        """
        Loads and returns data from a JSON file on disk.

        Args:
            file_name (str): The name of the file to be loaded.

        Returns:
            List[Dict]: The data loaded from the JSON file.

        Raises:
            OSError: If there is an error reading the file.
            ValueError: If the file contents are not valid JSON.
        """
        file_path = os.path.join(self.data_storage_directory, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except OSError as e:
            logger.error(f"Error while loading reaction data: {e}")
            raise e
        except ValueError as e:
            logger.error(f"Invalid JSON file: {e}")
            raise e
        return data


# Not functional yet:
class ElsevierDiskManager:
    def __init__(self) -> None:
        self.base_directory = settings.disk_storage.elsevier_directory
        self.reactions_dir = os.path.join(settings.disk_storage.elsevier_directory, "reactions")
        os.makedirs(self.reactions_dir, exist_ok=True)

    def get_file_paths(self, extension: str) -> List:
        file_paths = []
        for root, dirs, files in os.walk(self.base_directory):
            for file in files:
                if file.endswith(extension):
                    file_path = os.path.join(root, file)
                    file_paths.append(file_path)
        return file_paths

    def get_reaction_file_path(self, reaction_id: str) -> str:
        return os.path.join(self.reactions_dir, f"{reaction_id}.json")


