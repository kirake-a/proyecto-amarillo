import pytest
from unittest.mock import Mock, patch
import customtkinter as ctk

import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/../.."))

from Views.FileLineCounterView import FileLineCounterView
from Controllers.FileLineCounterController import FileLineCounterController
from Models.FileLineCounterModel import FileLineCounterModel
import time


@pytest.fixture
def mock_controller():
    """
    Pytest fixture that creates a mock controller instance.
    """
    return Mock()


@pytest.fixture(scope="function")
def start_tkinter_app():
    """
    Fixture to initialize the Tkinter application for testing.

    This sets up the controller, view, and model, links them together, 
    and updates the view before yielding the components.
    """
    controller = FileLineCounterController()
    view = FileLineCounterView(controller)
    model = FileLineCounterModel(controller)

    controller.set_file_line_counter_view(view)
    controller.set_file_line_counter_model(model)

    view.update()

    yield controller, view, model

    view.quit()


@pytest.fixture
def file_line_counter_view(mock_controller):
    """
    Fixture that initializes the FileLineCounterView with a mock controller.
    """
    return FileLineCounterView(mock_controller)


def test_initialization(file_line_counter_view):
    """
    Tests whether the FileLineCounterView initializes correctly.
    """
    assert file_line_counter_view.title() == "FileLineCounter"
    assert isinstance(file_line_counter_view.main_frame, ctk.CTkFrame)


def test_rendering_of_components(start_tkinter_app):
    """
    Tests whether all required UI components are rendered in the view.
    """
    controller, view, model = start_tkinter_app

    time.sleep(2)

    assert hasattr(view, "header"), "Header was not rendered!"
    assert hasattr(view, "file_entry"), "File entry was not rendered"
    assert hasattr(view, "file_button"), "File button was not rendered"
