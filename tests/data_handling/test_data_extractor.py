import pytest
import requests
from unittest.mock import patch
from pymetatree.data_handling.data_extractor import handle_network_error
from pymetatree.data_handling.exceptions import NetworkError


def test_handle_network_error_no_exception():
    with handle_network_error():
        pass  # No exception should be raised


def test_handle_network_error_with_exception():
    with patch('requests.exceptions.RequestException',
               side_effect=requests.exceptions.RequestException('Network error')):
        with pytest.raises(NetworkError):
            with handle_network_error():
                raise requests.exceptions.RequestException('Network error')
            