from pathlib import Path
from typing import Optional

from Controllers import FileComparerController
from Views import FileLineCounterView
from Models import FileLineCounterModel
from .PythonStandardValidatorController import (
    PythonStandardValidatorController)
from .LineAnalyzerController import LineAnalyzerController
from FileReader import FileReader

class FileLineCounterController:
    """
    Controller for counting physical lines and methods per class 
    in Python files.
    It processes individual files or directories and validates compliance
    with Python coding standards.
    """

    def __init__(
        self,
        file_line_counter_view: FileLineCounterView = None,
        file_line_counter_model: FileLineCounterModel = None
    ):
        """
        Initializes the FileLineCounterController.
        """
        self.__file_line_counter_view = file_line_counter_view
        self.__file_line_counter_model = file_line_counter_model
        self.__file_comparer_controller = FileComparerController

    def set_file_line_counter_view(
        self,
        file_line_counter_view: FileLineCounterView
    ):
        """
        Sets the view for the file line counter.
        """
        self.__file_line_counter_view = file_line_counter_view

    def set_file_line_counter_model(
        self,
        file_line_counter_model: FileLineCounterModel
    ):
        """
        Sets the model for the file line counter.
        """
        self.__file_line_counter_model = file_line_counter_model

    def get_file_line_counter_view(self):
        """Returns the current file line counter view."""
        return self.__file_line_counter_view

    def get_file_line_counter_model(self):
        """Returns the current file line counter model."""
        return self.__file_line_counter_model

    def process_file_path(self, old_path, new_path):
        """
        Processes the given file path, determining whether it is a directory
        or a Python file, then counts it's physical lines in a class and sum 
        the total physical lines in the proyect.
        """
        path_old_object = Path(old_path)
        path_new_object = Path(new_path)

        line_counting_results = {}

        if path_old_object.is_dir():
            self.__process_directory(path_old_object, line_counting_results)
        elif path_old_object.is_file():
            if path_old_object.suffix == ".py":
                # Check if the file exists in the new project
                if self.file_exists_anywhere(path_old_object, path_new_object):
                    print("File exists in new project")
                    # Find the path to the new file
                    path_to_new_file = self.find_matching_file(
                        path_old_object,
                        path_new_object
                    )
                    # Metrics for the new file
                    new_file_metrics = self.get_file_metrics(path_to_new_file)
                    line_counting_results[path_to_new_file.name] = new_file_metrics
                file_metrics = self.get_file_metrics(path_old_object)
                line_counting_results[path_old_object] = file_metrics
            else:
                line_counting_results[path_old_object] = \
                    ("error","Not a Python file", "None")
                
        line_counting_results["Total"] = \
        self.calculate_total_physical_lines(line_counting_results)

        self.__file_line_counter_model.set_line_count_results(
            line_counting_results)
           
    def calculate_total_physical_lines(self, line_counting_results):
        """
        Sum the total physical lines of all file classes processed.
        """
        total_physical_lines = 0

        for file_path, metrics in line_counting_results.items():
            if isinstance(metrics, tuple) and len(metrics) == 3:
                class_name, physical_lines, methods_count = metrics
                if isinstance(physical_lines, int):
                    total_physical_lines += physical_lines
        return "", total_physical_lines, ""
 
    def __process_directory(
        self,
        directory: Path,
        line_counting_results
    ):
        """
        Recursively processes a directory to count lines
        in all Python classes.
        """
        for file in directory.iterdir():
            if file.is_file() and file.suffix == ".py":
                file_metrics = self.get_file_metrics(file)
                line_counting_results[file] = file_metrics
            elif file.is_dir():
                self.__process_directory(file, line_counting_results)

    def get_file_metrics(self, new_file_path):
        """
        Retrieves the physical line count of a Python class.
        Retrieves the class name and methods count of a Python class.
        """
        file_lines = self.get_file_lines(new_file_path)

        is_valid = self.__validate_file_compliance_with_standard(file_lines)

        if is_valid:
            class_name = self.__extract_class(file_lines)
            physical_line_count = self.__count_physical_lines(file_lines)
            methods_count = self.__count_methods(file_lines)

            return class_name, physical_line_count, methods_count

        return "Doesn't comply with Standard", "None", "None"
    
    def get_file_lines(self, file_path):
        """
        Reads the lines of a given file.
        """
        file_reader = FileReader(file_path)
        return file_reader.read_file()

    def __validate_file_compliance_with_standard(self, file_lines):
        """
        Validates whether a file complies with Python coding standards.
        """
        standard_validator = PythonStandardValidatorController(file_lines)
        return standard_validator.validate_compliance_with_standard()

    def __count_physical_lines(self, file_lines):
        """
        Counts the physical lines of code in a class.
        """
        physical_file_line_counter = LineAnalyzerController(file_lines)
        return physical_file_line_counter.count_physical_lines()
    
    def __count_methods(self, file_lines):
        """
        Counts the methods in a class.
        """
        methods_counter = LineAnalyzerController(file_lines)
        return methods_counter.count_methods()
    
    def __extract_class(self, file_lines):
        """
        Extract the class name.
        """
        class_name_extractor = LineAnalyzerController(file_lines)
        return class_name_extractor.extract_class()
    
    def file_exists_anywhere(
        self,
        old_file: Path,
        new_project_root: Path
    ) -> bool:
        """
        Checks whether a file with the same name as `old_file` exists 
        anywhere recursively within `new_project_root`.

        Args:
            old_file (Path): Path to the original file (only the name will be used).
            new_project_root (Path): Root directory of the new project.

        Returns:
            bool: True if a file with the same name exists in any subdirectory
                of the new project, False otherwise.
        """
        if not old_file.is_file():
            return False

        old_file_name = old_file.name

        return any(file.name == old_file_name for file in new_project_root.rglob("*.py"))
    
    def find_matching_file(
        self,
        old_file: Path,
        new_project_root: Path
    ) -> Optional[Path]:
        """
        Searches recursively in `new_project_root` for a file with the same name 
        as `old_file` and returns its full path if found.

        Args:
            old_file (Path): Path to the original file (only the name is used).
            new_project_root (Path): Root directory of the new project.

        Returns:
            Optional[Path]: Full path to the matching file in the new project,
                            or None if not found.
        """
        if not old_file.is_file():
            return None

        old_file_name = old_file.name

        for file in new_project_root.rglob("*.py"):
            if file.name == old_file_name:
                return file

        return None

    def manage_model_changes(self):
        """
        Updates the view with the latest line counting results
        from the model.
        """
        line_counting_results = \
            self.__file_line_counter_model.get_line_count_results()

        self.__file_line_counter_view.show_metric_results(
            line_counting_results)
