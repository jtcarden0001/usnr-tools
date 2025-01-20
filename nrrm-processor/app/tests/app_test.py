import pytest
import os
from ..app import start

def test_hello_app():
    assert 1 == 1

def test_app_start():
    start()
    assert True

