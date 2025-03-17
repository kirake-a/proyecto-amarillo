import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/../.."))

from unittest.mock import Mock
from Models.FileLineCounterModel import FileLineCounterModel


@pytest.fixture
def mock_controller():
    """
    Creates a mock object for the controller to be used in the model.
    """
    return Mock()


@pytest.fixture
def model(mock_controller):
    """
    Creates an instance of FileLineCounterModel with a mocked controller.
    """
    return FileLineCounterModel(mock_controller)


def test_initialization(model, mock_controller):
    """
    Tests that the model initializes correctly with the provided controller.

    The test verifies that:
    - The controller is correctly assigned.
    - The line count results are initially set to None.
    """
    assert (
        model._FileLineCounterModel__file_line_counter_controller
        == mock_controller
    )
    assert model._FileLineCounterModel__line_count_results is None


def test_set_line_count_results(model, mock_controller):
    """
    Tests that setting line count results updates the model correctly.

    The test verifies that:
    - The line count results are stored properly.
    - The controller is notified of the change via `manage_model_changes`.
    """
    fake_results = {"test.py": (10, 20)}
    model.set_line_count_results(fake_results)

    assert model.get_line_count_results() == fake_results
    mock_controller.manage_model_changes.assert_called_once()


def test_get_line_count_results(model):
    """
    Tests that the model correctly returns stored line count results.

    The test verifies that:
    - The getter method retrieves the correct stored results.
    """
    fake_results = {"test.py": (15, 30)}
    model.set_line_count_results(fake_results)
    assert model.get_line_count_results() == fake_results


def test_inform_changes_to_controller(model, mock_controller):
    """
    Tests that the model correctly informs the controller of changes.

    The test verifies that:
    - The `inform_changes_to_controller` method successfully triggers
      the `manage_model_changes` method in the controller.
    """
    model.inform_changes_to_controller()
    mock_controller.manage_model_changes.assert_called_once()