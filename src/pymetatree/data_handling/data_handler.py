"""
This module provides a DataHandler class and its concrete implementation EawagDataHandler for handling
various data operations related to chemical reaction data.

The DataHandler class is an abstract base class that defines the interface for downloading, saving,
loading, and processing chemical reaction data. It also includes methods for extracting templates
from the data, generating a list of unmapped reactions for mapping, saving the mapping list, and
applying the mapped reactions to the original dataset.

The EawagDataHandler class is a concrete implementation of the DataHandler class that handles data
operations specifically for the EAWAG data source.

The module also includes exception handling for various errors that may occur during data handling
operations.
"""

import logging
import abc
from typing import Dict, List, Optional

from pymetatree.data_handling.models import ChemicalReaction
from pymetatree.data_handling.data_extractor import EawagDataExtractor
from pymetatree.template.constructors import TemplateConstructor
from pymetatree.template.exceptions import TemplateConstructionError
from pymetatree.data_handling.disk_manager import EAWAGDiskManager
from pymetatree.data_handling.mapping_manager import MappingManager
from pymetatree.data_handling.exceptions import (
    DataHandlerError,
    DiskError,
    TemplateError,
    MappingError,
    ResourceNotFoundError
)
from pymetatree.blueprint.blueprint_handler import BlueprintHandler

logger = logging.getLogger(__name__)


class DataHandler(abc.ABC):
    """
    Abstract base class for handling data operations.
    """
    @abc.abstractmethod
    def download_data(self, package: str, limit: Optional[int] = None) -> None:
        """
        Download data from a specified package.

        Args:
            package (str): The name of the package to download data from.
            limit (Optional[int]): An optional limit on the number of reactions to download.
        """
        pass

    @abc.abstractmethod
    def get_data(self) -> List[ChemicalReaction]:
        """
        Get the downloaded data as a list of ChemicalReaction objects.

        Returns:
            List[ChemicalReaction]: A list of ChemicalReaction objects.
        """
        pass

    @abc.abstractmethod
    def save_data(self, file_name: str) -> None:
        """
        Save the downloaded data to a file.

        Args:
            file_name (str): The name of the file to save the data to.
        """
        pass

    @abc.abstractmethod
    def load_data(self, file_names: [str]) -> None:
        """
        Load the data from a file.

        Args:
            file_names (List[str]): A list of file names to load the data from.
        """
        pass

    @abc.abstractmethod
    def extract_templates(self) -> None:
        """
       Extract templates from the downloaded data.
       """
        pass

    @abc.abstractmethod
    def generate_blueprints(self) -> None:
        pass

    @abc.abstractmethod
    def save_blueprints(self, file_name: str) -> None:
        pass

    @abc.abstractmethod
    def load_blueprints(self, file_names: [str]) -> None:
        pass

    @abc.abstractmethod
    def get_list_to_map(self) -> List[Dict[str, str]]:
        """
        Get a list of dictionaries representing the unmapped reactions in the correct format
        to input into the external mapper.

        Returns:
            List[Dict[str, str]]: A list of dictionaries for mapping.
        """
        pass

    @abc.abstractmethod
    def save_list_to_map(self, file_name: str) -> None:
        """
        Save the mapping list to a file.

        Args:
            file_name (str): The name of the file to save the data to.
        """
        pass

    @abc.abstractmethod
    def append_mapped_list(self, file_name: str, file_format: str) -> None:
        """
        Append the mapped reactions to the original dataset.

        Args:
            file_name (str): The name of the mapped reactions file.
            file_format: Either JSON or SMI
        """
        pass


class EawagDataHandler(DataHandler):
    def __init__(self, data_storage_directory: str) -> None:
        """
        Initialize an EawagDataHandler instance.
        """
        self.data_storage_directory = data_storage_directory
        self.disk_manager = EAWAGDiskManager(self.data_storage_directory)
        self.eawag_data: List[ChemicalReaction] = []
        self.blueprints = None

    def download_data(self, package_name: str, limit: Optional[int] = None) -> None:
        """
        Download data from the specific EAWAG package.

        Args:
            package_name (str): The name of the EAWAG package to download data from.
            limit (Optional[int]): An optional limit on the number of reactions to download.

        Raises:
            DataHandlerError: If an error occurs while downloading the data.
        """
        try:
            extractor = EawagDataExtractor(package_name)
            self.eawag_data = extractor.extract_data(limit)
        except ResourceNotFoundError as e:
            raise DataHandlerError(f"Error downloading data: {e}") from e

    def get_data(self) -> List[ChemicalReaction]:
        """
        Get the downloaded Eawag data as a list of ChemicalReaction objects.

        Returns:
            List[ChemicalReaction]: A list of ChemicalReaction objects.
        """
        return self.eawag_data

    def save_data(self, file_name: str) -> None:
        """
        Save the downloaded Eawag data to a file.

        Args:
            file_name (str): The name of the file to save the data to.

        Raises:
            DiskError: If an error occurs during data saving.
        """
        try:
            data_as_dict = [reaction.model_dump() for reaction in self.eawag_data]
            self.disk_manager.save_data_as_json(data_as_dict, file_name)
        except Exception as e:
            raise DiskError(f"Error saving data: {e}") from e

    def load_data(self, file_names: [str]) -> None:
        """
        Load Eawag data from a file.

        Args:
            file_names (List[str]): A list of file names to load the data from.

        Raises:
            DiskError: If an error occurs during data loading.
        """
        try:
            eawag_data = []
            for file_name in file_names:
                loaded_data = self.disk_manager.load_json_data(file_name)
                eawag_data.extend([ChemicalReaction(**reaction) for reaction in loaded_data])
            self.eawag_data = eawag_data
        except Exception as e:
            raise DiskError(f"Error loading data: {e}") from e

    def extract_templates(self) -> None:
        """
        Extract templates from the downloaded Eawag data.

        Raises:
            TemplateError: If an error occurs during template extraction.
        """
        try:
            template_constructor = TemplateConstructor()
            for i, reaction in enumerate(self.eawag_data):
                self.eawag_data[i] = template_constructor.extract_from_chemical_reaction_object(reaction)
        except TemplateConstructionError as e:
            raise TemplateError(f"Error extracting templates: {e}") from e

    def get_list_to_map(self) -> List[Dict[str, str]]:
        """
        Get a list of dictionaries representing the unmapped reactions in the correct format
        to input into the external mapper.

        Returns:
            List[Dict[str, str]]: A list of dictionaries for mapping.

        Raises:
            MappingError: If an error occurs during mapping list generation.
        """
        try:
            mapping_manager = MappingManager(self.eawag_data)
            return mapping_manager.generate_list_to_map()
        except Exception as e:
            raise MappingError(f"Error generating mapping list: {e}") from e

    def save_list_to_map(self, file_name: str) -> None:
        """
        Save the mapping list to a file.

        Args:
            file_name (str): The name of the file to save the data to.

        Raises:
            MappingError: If an error occurs during mapping list saving.
            DiskError: If an error occurs during disk operations.
        """
        try:
            mapping_manager = MappingManager(self.eawag_data)
            mapping_manager.save_list_to_disk(file_name)
        except Exception as e:
            if isinstance(e, DiskError):
                raise DiskError(f"Error saving data: {e.message}") from e
            elif isinstance(e, MappingError):
                raise MappingError(f"Error saving mapping list: {e.message}") from e
            else:
                print(f"An error occurred: {e}")

    def append_mapped_list(self, file_name: str, file_format: str) -> None:
        """
        Append the mapped reactions to the original dataset.

        Args:
            file_name (str): The name of the mapped reactions file.
            file_format: Either JSON or SMI

        Raises:
            MappingError: If an error occurs during mapping application.
            DiskError: If an error occurs during disk operations.
        """
        try:
            mapping_manager = MappingManager(self.eawag_data)
            mapping_manager.load_list_from_disk(file_name, file_format)
            mapping_manager.update_data(mapping_manager.mapped_list)
            self.eawag_data = mapping_manager.data
        except Exception as e:
            if isinstance(e, MappingError):
                raise MappingError(f"Error applying mappings: {e.message}") from e
            elif isinstance(e, DiskError):
                raise DiskError(f"Error applying mappings: {e.message}") from e
            else:
                print(f"An error occurred: {e}")

    def generate_blueprints(self) -> None:
        reactions = self.get_data()
        blueprints = []
        for reaction in reactions:
            bp_handler = BlueprintHandler(reaction)
            blueprints.append(bp_handler.blueprint.model_dump())
        self.blueprints = blueprints

    def save_blueprints(self, file_name: str) -> None:
        disk_manager = EAWAGDiskManager(self.data_storage_directory)
        disk_manager.save_data_as_json(self.blueprints, file_name)

    def load_blueprints(self, file_name: [str]) -> None:
        pass
