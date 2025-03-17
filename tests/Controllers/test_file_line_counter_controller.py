import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/../.."))

from unittest.mock import Mock
from unittest.mock import patch
from Controllers.FileLineCounterController import FileLineCounterController


@pytest.fixture
def mock_view():
    """
    Creates a mock object for the controller's view.
    """
    return Mock()


@pytest.fixture
def mock_model():
    """
    Creates a mock object for the controller's model.
    """
    return Mock()


@pytest.fixture
def controller(mock_view, mock_model):
    """
    Creates an instance of FileLineCounterController with 
    mocked view and model.

    """
    return FileLineCounterController(mock_view, mock_model)


def test_initialization(controller, mock_view, mock_model):
    """
    Tests the initialization of the controller with provided
    mock view and model.
    """
    assert controller.get_file_line_counter_view() == mock_view
    assert controller.get_file_line_counter_model() == mock_model


def test_set_file_line_counter_view(controller, mock_view):
    """
    Tests that the controller updates its view correctly.
    """
    controller.set_file_line_counter_view(mock_view)
    assert controller.get_file_line_counter_view() == mock_view


def test_set_file_line_counter_model(controller, mock_model):
    """
    Tests that the controller updates its model correctly.
    """
    controller.set_file_line_counter_model(mock_model)
    assert controller.get_file_line_counter_model() == mock_model


def create_mock_path_object(is_dir, is_file, suffix):
    """
    Creates a mock object representing a file path with specified 
    properties.
    """
    mock_path_object = Mock()
    mock_path_object.is_dir.return_value = is_dir
    mock_path_object.is_file.return_value = is_file
    mock_path_object.suffix = suffix
    return mock_path_object


@patch("Controllers.FileLineCounterController.Path")
def test_process_file_path_with_file(mock_path, controller):
    """
    Tests that the controller correctly processes a valid Python file.
    """
    mock_file = create_mock_path_object(
        is_dir=False, is_file=True, suffix=".py"
    )
    mock_path.return_value = mock_file

    with patch.object(controller, "get_file_metrics",
                      return_value=(10, 20)) as mock_get_metrics:
        controller.process_file_path("test.py")

    mock_get_metrics.assert_called_once_with(mock_file)
    (controller.get_file_line_counter_model()
     .set_line_count_results.assert_called_once())


@patch("Controllers.FileLineCounterController.Path")
def test_process_file_path_with_directory(mock_path, controller):
    """
    Tests that the controller correctly processes a directory.
    """
    mock_directory = create_mock_path_object(
        is_dir=True, is_file=False, suffix=""
    )
    mock_path.return_value = mock_directory

    with patch.object(controller,
                      "_FileLineCounterController__process_directory",
                      return_value=None) as mock_process_dir:
        controller.process_file_path("test_dir")

    mock_process_dir.assert_called_once_with(mock_directory, {})


@patch("Controllers.FileLineCounterController.Path")
def test_process_file_path_invalid_file(mock_path, controller):
    """
    Tests that the controller handles an invalid file type correctly.
    """
    mock_invalid_file = create_mock_path_object(
        is_dir=False, is_file=True, suffix=".txt"
    )
    mock_path.return_value = mock_invalid_file

    controller.process_file_path("test.txt")

    expected_error_message = "Not a Python file"
    (controller.get_file_line_counter_model()
     .set_line_count_results.assert_called_once_with(
         {mock_invalid_file: ("error", expected_error_message)}
    ))


def test_get_file_metrics_valid_file(controller):
    """
    Tests that the controller correctly calculates file metrics for 
    a valid file.
    """
    mock_file = Mock()
    with patch.object(controller, "get_file_lines",
                      return_value=["print('Hello')"]):
        with patch.object(controller,
        "_FileLineCounterController__validate_file_compliance_with_standard",
                          return_value=True):
            with patch.object(controller,
            "_FileLineCounterController__count_logical_file_lines",
                              return_value=5):
                with patch.object(controller,
                "_FileLineCounterController__count_physical_file_lines",
                                  return_value=10):
                    result = controller.get_file_metrics(mock_file)

    assert result == (5, 10)


def test_get_file_metrics_invalid_file(controller):
    """
    Tests that the controller returns an error when a file does not comply 
    with the standard.
    """
    mock_file = Mock()
    with patch.object(controller, "get_file_lines",
                      return_value=["print('Hello')"]):
        with patch.object(controller,
        "_FileLineCounterController__validate_file_compliance_with_standard",
                          return_value=False):
            result = controller.get_file_metrics(mock_file)

    assert result == ("error", "Doesn't comply with Standard")