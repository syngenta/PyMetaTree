"""
This module provides a `MappingManager` class for managing the mapping of chemical reactions.

The `MappingManager` class is responsible for generating a list of unmapped reactions in a specific
format suitable for external mapping, updating the original data with the mapped reactions, and
saving/loading the mapping list to/from disk.

The class uses the `ChemicalReaction` model from the `pymetatree.data_handling.models` module and
the `DiskManager` class from the `pymetatree.data_handling.disk_manager` module for disk operations.

The module also includes exception handling for file not found errors that may occur during disk
operations.
"""

from typing import List, Dict
from pymetatree.data_handling.models import ChemicalReaction
from pymetatree.data_handling.disk_manager import EAWAGDiskManager


class MappingManager:
    """
    Class for managing the mapping of chemical reactions.

    Attributes:
        data (List[ChemicalReaction]): A list of ChemicalReaction objects.
        disk_manager (DiskManager): An instance of the DiskManager class.
        mapped_list (List[Dict[str, str]]): A list of mapped reactions.
    """
    def __init__(self, data: List[ChemicalReaction]) -> None:
        """
        Initialize a MappingManager instance.

        Args:
            data (List[ChemicalReaction]): A list of ChemicalReaction objects.
        """
        self.data = data
        self.disk_manager = EAWAGDiskManager()
        self.mapped_list = None

    def generate_list_to_map(self) -> List[Dict[str, str]]:
        """
        Generate a list of dictionaries containing unmapped reactions.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing unmapped reactions.
        """
        list_to_map = []
        for reaction in self.data:
            list_entry = {
                "input_string": reaction.unmapped_smiles_canonicalized,
                "query_id": reaction.uid
            }
            list_to_map.append(list_entry)
        return list_to_map

    def update_data(self, mapped_data: List[Dict[str, str]]) -> None:
        """
        Update the original data with the mapped reactions.

        Args:
            mapped_data (List[Dict[str, str]]): A list of dictionaries containing mapped reactions.
        """
        for mapped_reaction in mapped_data:
            for unmapped_reaction in self.data:
                if mapped_reaction["query_id"] == unmapped_reaction.uid:
                    unmapped_reaction.mapped_smiles = mapped_reaction["output_string"]

    def save_list_to_disk(self, file_name: str) -> None:
        """
        Save the list of unmapped reactions to disk.

        Args:
            file_name (str): The name of the file to save the data to.
        """
        data = self.generate_list_to_map()
        self.disk_manager.save_data_as_json(data, file_name)

    @staticmethod
    def read_mapped_smi(file_name: str):
        with open(file_name, 'r') as f:
            lines = f.readlines()
        data = []
        for line in lines:
            line = line.strip()
            if line:
                parts = line.split(' ')
                if len(parts) == 2:
                    smiles, uid = parts
                    data.append({'query_id': uid, 'output_string': smiles})
        return data


    def load_list_from_disk(self, file_name: str, file_format: str) -> None:
        """
        Load the list of mapped reactions from disk.

        Args:
            file_name (str): The name of the file to load the data from.
            file_format: Either JSON or smi.

        Raises:
            FileNotFoundError: If the specified file does not exist.
        """
        if file_format == "json":
            try:
                self.mapped_list = self.disk_manager.load_json_data(file_name)
            except FileNotFoundError:
                raise FileNotFoundError(f"File '{file_name}' not found.")
        elif file_format == "smi":
            self.mapped_list = self.read_mapped_smi(file_name)

