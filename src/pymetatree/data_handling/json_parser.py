import json
import os
import logging
import string
from typing import Dict
import abc

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class JSONParser(abc.ABC):
    def parse_data(self, file_name: str) -> Dict:
        pass

    def save_reactions(self, reaction_data: Dict, file_name: str) -> None:
        pass


class ElsevierJSONParser:
    @staticmethod
    def parse_file(file_name: str, directory: str) -> Dict:
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            printable = set(string.printable)
            filtered_content = ''.join(filter(lambda x: x in printable, content))
            data = json.loads(filtered_content)
        return data

    @staticmethod
    def save_reaction(reaction_info: Dict, file_name: str, directory: str) -> None:
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'w') as file:
            json.dump(reaction_info, file, indent=4)