import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/../.."))

import time
from pathlib import Path
import customtkinter as ctk
from Views.FileLineCounterView import FileLineCounterView
from Controllers.FileLineCounterController import FileLineCounterController
from Models.FileLineCounterModel import FileLineCounterModel


@pytest.fixture(scope="function")
def start_tkinter_app():
    """
    Fixture to initialize the Tkinter application for testing.
    Sets up the controller, view, and model, and links them together.
    """
    controller = FileLineCounterController()
    view = FileLineCounterView(controller)
    model = FileLineCounterModel(controller)

    controller.set_file_line_counter_view(view)
    controller.set_file_line_counter_model(model)

    view.update()

    yield controller, view, model

    view.quit()


def test_filepath_with_single_file(start_tkinter_app, tmp_path):
    """
    Test function to simulate writing a file path and clicking
    the "Get Metrics" button. Verifies that the file path
    is registered correctly and the results are displayed
    in the resulting window.
    """
    controller, view, model = start_tkinter_app

    test_file = tmp_path / "test_script.py"
    test_file.write_text("print('Hello, World!')\nprint('Goodbye!')")

    view.file_entry.insert(0, str(test_file))

    view.file_button.invoke()

    time.sleep(2)

    assert view.file_entry.get() == str(
        test_file), "File path was not registered correctly!"

    assert hasattr(view, "result_window"), "Result window was not opened!"
    result_window = view.result_window

    assert result_window.title() == "Metric Results", "Result incorrect!"

    canvas = result_window.winfo_children()[0]
    table_frame = canvas.winfo_children()[0]

    headers = table_frame.winfo_children()[:3]
    assert headers[0].cget(
        "text") == "Filename", "Filename header is incorrect!"
    assert headers[1].cget(
        "text") == "Logical Lines", "Logical Lines header is incorrect!"
    assert headers[2].cget(
        "text") == "Physical Lines", "Physical Lines header is incorrect!"

    rows = table_frame.winfo_children()[3:]
    assert len(rows) == 3, "Incorrect number of rows in the table!"

    filename_label = rows[0]
    logical_lines_label = rows[1]
    physical_lines_label = rows[2]

    assert str(filename_label.cget("text")) == str(
        test_file), "Filename in the table is incorrect!"
    assert logical_lines_label.cget(
        "text") == "0", "Logical line count is incorrect!"
    assert physical_lines_label.cget(
        "text") == "2", "Physical line count is incorrect!"


def test_file_path_with_multiple_files(start_tkinter_app, tmp_path):
    """
    Test function to simulate entering a directory path containing
    multiple Python files. Verifies that the application processes
    the directory and displays the correct metrics.
    """
    controller, view, model = start_tkinter_app

    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()

    file1 = test_dir / "script1.py"
    file1.write_text("print('Hello, World!')\nprint('Goodbye!')")

    file2 = test_dir / "script2.py"
    file2.write_text("x = 5\ny = 10\nprint(x + y)")

    file3 = test_dir / "script3.py"
    file3.write_text("# This is a comment\nprint('Hello')")

    view.file_entry.insert(0, str(test_dir))

    view.file_button.invoke()

    time.sleep(2)

    assert view.file_entry.get() == str(
        test_dir), "Directory path was not registered correctly!"

    assert hasattr(view, "result_window"), "Result window was not opened!"
    result_window = view.result_window

    assert result_window.title() == "Metric Results", "Result incorrect!"

    canvas = result_window.winfo_children()[0]

    table_frame = canvas.winfo_children()[0]

    headers = table_frame.winfo_children()[:3]
    assert headers[0].cget(
        "text") == "Filename", "Filename header is incorrect!"
    assert headers[1].cget(
        "text") == "Logical Lines", "Logical Lines header is incorrect!"
    assert headers[2].cget(
        "text") == "Physical Lines", "Physical Lines header is incorrect!"

    rows = table_frame.winfo_children()[3:]
    assert len(rows) == 9, "Incorrect number of rows in the table!"

    expected_results = {
        file1: (0, 2),
        file2: (0, 3),
        file3: (0, 1),
    }

    for i, (filename, metrics) in enumerate(expected_results.items()):
        filename_label = rows[i * 3]
        logical_lines_label = rows[i * 3 + 1]
        physical_lines_label = rows[i * 3 + 2]

        assert str(filename_label.cget("text")) == str(
            filename), f"Filename {filename} is incorrect!"
        assert logical_lines_label.cget("text") == str(
            metrics[0]), f"Logical lines for {filename} are incorrect!"
        assert physical_lines_label.cget("text") == str(
            metrics[1]), f"Physical lines for {filename} are incorrect!"


def test_file_path_with_no_python_files(start_tkinter_app, tmp_path):
    """
    Test function to simulate entering a directory path containing
    multiple Python files. Verifies that the application processes
    the directory and displays the correct metrics.
    """
    controller, view, model = start_tkinter_app

    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()

    view.file_entry.insert(0, str(test_dir))

    view.file_button.invoke()

    time.sleep(2)

    assert view.file_entry.get() == str(
        test_dir), "Directory path was not registered correctly!"

    assert hasattr(view, "result_window"), "Result window was not opened!"
    result_window = view.result_window

    assert result_window.title() == "Metric Results", "Result incorrect!"

    canvas = result_window.winfo_children()[0]
    table_frame = canvas.winfo_children()[0]

    headers = table_frame.winfo_children()[:3]
    assert headers[0].cget(
        "text") == "Filename", "Filename header is incorrect!"
    assert headers[1].cget(
        "text") == "Logical Lines", "Logical Lines header is incorrect!"
    assert headers[2].cget(
        "text") == "Physical Lines", "Physical Lines header is incorrect!"

    rows = table_frame.winfo_children()[3:]
    assert len(rows) == 0, "Should have 0 rows"


def test_filepath_with_nested_directories(start_tkinter_app, tmp_path):
    """
    Test function to simulate entering a directory path containing multiple
    Python files.Verifies that the application processes the directory
    and displays the correct metrics.
    """
    controller, view, model = start_tkinter_app

    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()

    sub_dir = test_dir / "sub_dir"
    sub_dir.mkdir()

    file1 = sub_dir / "script1.py"
    file1.write_text("print('Hello, World!')\nprint('Goodbye!')")

    file2 = sub_dir / "script2.py"
    file2.write_text("x = 5\ny = 10\nprint(x + y)")

    file3 = sub_dir / "script3.py"
    file3.write_text("# This is a comment\nprint('Hello')")

    file4 = test_dir / "script4.py"
    file4.write_text("a = 1\nb = 2\nprint(a + b)")

    view.file_entry.insert(0, str(test_dir))

    view.file_button.invoke()

    time.sleep(2)

    assert view.file_entry.get() == str(
        test_dir), "Directory path was not registered correctly!"

    assert hasattr(view, "result_window"), "Result window not opened!"
    result_window = view.result_window

    assert result_window.title() == "Metric Results", "Result not correct!"

    canvas = result_window.winfo_children()[0]
    table_frame = canvas.winfo_children()[0]

    headers = table_frame.winfo_children()[:3]
    assert headers[0].cget(
        "text") == "Filename", "Filename header is incorrect!"
    assert headers[1].cget(
        "text") == "Logical Lines", "Logical Lines header is incorrect!"
    assert headers[2].cget(
        "text") == "Physical Lines", "Physical Lines header is incorrect!"

    rows = table_frame.winfo_children()[3:]
    assert len(rows) == 12, "Incorrect number of rows in the table!"

    expected_results = {
        file4: (0, 3),
        file1: (0, 2),
        file2: (0, 3),
        file3: (0, 1),
    }

    for i, (filename, metrics) in enumerate(expected_results.items()):
        filename_label = rows[i * 3]
        logical_lines_label = rows[i * 3 + 1]
        physical_lines_label = rows[i * 3 + 2]

        assert str(filename_label.cget("text")) == str(
            filename), f"Filename {filename} is incorrect!"
        assert logical_lines_label.cget("text") == str(
            metrics[0]), f"Logical lines for {filename} are incorrect!"
        assert physical_lines_label.cget("text") == str(
            metrics[1]), f"Physical lines for {filename} are incorrect!"
