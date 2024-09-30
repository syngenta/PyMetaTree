"""
This module provides functionality for extracting chemical reaction data from various data sources.

It includes an abstract base class `DataExtractor` and a concrete implementation `EawagDataExtractor`
for extracting data from the EAWAG data source.

The module also includes a context manager `handle_network_error` to handle network errors that may
occur during data extraction.
"""
import os.path

from loguru import logger
import abc
from enviPath_python.enviPath import *
from contextlib import contextmanager
from pymetatree.data_handling.exceptions import (
    LimitExceededError,
    NetworkError
)
from pymetatree.data_handling.json_parser import ElsevierJSONParser
from pymetatree.data_handling.models import ChemicalReaction
from pymetatree.data_handling.db_connector import EAWAGDataConnector
from pymetatree.data_handling.disk_manager import ElsevierDiskManager
from typing import List, Dict

logger.add("eawag_data_connector.log", rotation="1 MB", level="INFO")

# We use here hardcoded configuration for the EAWAG enviPath database. This will change in the future, so as to
# use a proper configuration file and configuration manager.
EAWAG_DATABASE_CONFIG = {
    "database": {
        "host": "https://envipath.org"
    },
    "packages": {
        "eawag_soil": {
            "name": "EAWAG_SOIL",
            "url": "https://envipath.org/package/5882df9c-dae1-4d80-a40e-db4724271456"
        },
        "eawag_sludge": {
            "name": "EAWAG_SLUDGE",
            "url": "https://envipath.org/package/7932e576-03c7-4106-819d-fe80dc605b8a"
        },
        "eawag_bbd": {
            "name": "EAWAG_BBD",
            "url": "https://envipath.org/package/32de3cf4-e3e6-4168-956e-32fa5ddb0ce1"
        }
    }
}


@contextmanager
def handle_network_error():
    """Context manager to handle network errors."""
    try:
        yield
    except Exception as e:
        logger.error(f"Network error while extracting reactions: {e}")
        raise NetworkError(f"Network error while extracting reactions: {e}") from None


class DataExtractor(abc.ABC):
    """
    Abstract base class for data extractors.

    This class defines the interface for extracting chemical reaction data from various data sources.
    Concrete implementations of this class should implement the `extract_data` method.
    """
    @abc.abstractmethod
    def extract_data(self, limit: Optional[int] = None) -> List[ChemicalReaction]:
        """Extract chemical reaction data.

        Args:
            limit (Optional[int]): Maximum number of reactions to extract.

        Returns:
            List[ChemicalReaction]: List of extracted chemical reactions.
        """
        pass


class EawagDataExtractor(DataExtractor):
    """
    Class for extracting chemical reaction data from EAWAG data source.

    This class implements the `DataExtractor` interface for extracting chemical reaction data
    from the EAWAG data source.
    """
    def __init__(self, package_key: str) -> None:
        self.package_name = EAWAG_DATABASE_CONFIG["packages"][package_key]["name"]
        self.package_url = EAWAG_DATABASE_CONFIG["packages"][package_key]["url"]
        self.host_instance = EAWAG_DATABASE_CONFIG["database"]["host"]
        self.connector = EAWAGDataConnector(self.package_url, self.host_instance)

    def extract_data(self, limit: Optional[int] = None) -> List[ChemicalReaction]:
        """Extract chemical reaction data from EAWAG data source.

        Args:
            limit (Optional[int]): Maximum number of reactions to extract.

        Returns:
            List[ChemicalReaction]: List of extracted chemical reactions.

        Raises:
            LimitExceededError: If the provided limit is not a positive integer or None.
            EAWAGDataConnectorError: If an error occurs while extracting reactions.
        """
        if limit is not None and (not isinstance(limit, int) or limit <= 0):
            raise LimitExceededError("Limit must be positive integer or None")
        with handle_network_error():
            raw_reactions = self.connector.get_reactions()[:limit] if limit else self.connector.get_reactions()
        reactions = []
        for raw_reaction in raw_reactions:
            reaction_json = raw_reaction.get_json()
            eawag_reaction = ChemicalReaction(**reaction_json)
            eawag_reaction.dataset = self.package_name
            reactions.append(eawag_reaction)
        return reactions


class ElsevierDataExtractor:
    def __init__(self) -> None:
        self.json_parser = ElsevierJSONParser()
        self.disk_manager = ElsevierDiskManager()

    def extract_reactions(self) -> None:
        json_file_paths = self.disk_manager.get_file_paths('.json')
        for file_path in json_file_paths:
            data = self.json_parser.parse_file(os.path.basename(file_path), os.path.dirname(file_path))
            self.save_reactions(data)

    def save_reactions(self, data: Dict) -> None:
        for reaction_id, reaction_data in data['Edges'].items():
            reaction_info = {
                'Reaction ID': reaction_id,
                'Reactant RN': reaction_data['Reactant RN'],
                'Product RN': reaction_data['Product RN'],
                'Additional Products': reaction_data['Additional Products'],
                'Reactant': data['Nodes'][reaction_data['Reactant RN']],
                'Products': [data['Nodes'][rn] for rn in reaction_data['Product RN']]
            }
            reaction_file_path = self.disk_manager.get_reaction_file_path(reaction_id)
            self.json_parser.save_reaction(reaction_info, os.path.basename(reaction_file_path),
                                           os.path.dirname(reaction_file_path))
