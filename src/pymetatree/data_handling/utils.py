# NB: This code is not being used by the system anymore.

import os
import json
from typing import Any, Dict


def get_config(config_file: str) -> Dict[str, Any]:
    """
    Load configuration from a JSON file.

    Args:
        config_file (str): The path to the configuration file.

    Returns:
        Dict: The configuration data as a dictionary.
    """
    current_dir = os.getcwd()
    config_file_path = os.path.join(current_dir, config_file)
    with open(config_file_path, "r") as file:
        data = json.load(file)
    return data
