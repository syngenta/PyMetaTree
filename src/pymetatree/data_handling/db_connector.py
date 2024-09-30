"""
This module provides a class `EAWAGDataConnector` for connecting to the EAWAG data source and
retrieving chemical reactions. It uses the `enviPath` library to interact with the EAWAG API.

The `EAWAGDataConnector` class establishes a connection with the EAWAG data source using the provided
package URL and host instance. It provides a method `get_reactions` to retrieve a list of chemical
reactions from the specified package. The method includes retry logic using the `tenacity` library
to handle network errors.

The module also includes exception handling for various errors that may occur during the data
retrieval process, such as network errors, invalid host instances, invalid package URLs, and
resource not found errors.
"""

import tenacity
from loguru import logger
from enviPath_python.enviPath import *
from enviPath_python.objects import Reaction
from pymetatree.data_handling.exceptions import (
    NetworkError,
    InvalidHostInstanceError,
    InvalidPackageURLError,
    ResourceNotFoundError
)

logger.add("eawag_data_connector.log", rotation="1 MB", level="INFO")


class EAWAGDataConnector:
    """
    A class to connect to the EAWAG data source and retrieve reactions.
    """
    def __init__(self, package_url: str, host_instance: str) -> None:
        """
        Initialize the EAWAGDataConnector instance.

        Args:
            package_url (str): The URL of the package to retrieve reactions from.
            host_instance (str): The host instance for the enviPath API.

        Raises:
            PackageNotFoundError: If the specified package URL is invalid.
        """
        if not host_instance:
            raise InvalidHostInstanceError("Host instance cannot be empty.")
        if not package_url:
            raise InvalidPackageURLError("Package URL cannot be empty.")
        self.host_instance = host_instance
        self.package_url = package_url
        self.eP = enviPath(self.host_instance)
        try:
            self.pkg = Package(self.eP.requester, id=self.package_url)
        except ValueError as e:
            logger.error(f"Error creating Package instance for {self.package_url}: {e}")
            raise ResourceNotFoundError(f"Error: {e}") from None

    @tenacity.retry(stop=tenacity.stop_after_attempt(5),
                    wait=tenacity.wait_exponential(multiplier=1, max=60),
                    retry=tenacity.retry_if_exception_type(NetworkError))
    def get_reactions(self) -> List[Reaction]:
        """
        Retrieve reactions from the specified package.

        Returns:
            List[Reaction]: A list of Reaction objects.

        Raises:
            NetworkError: If there is a network error while retrieving reactions.
            EAWAGDataConnectorError: If there is an error while retrieving reactions.
        """
        try:
            return self.pkg.get_reactions()
        except requests.exceptions.RequestException as e:
            logger.error(
                f"Network error while retrieving reactions from package {self.package_url}: {e}"
            )
            raise NetworkError(f"Network error while retrieving reactions: {e}") from None
