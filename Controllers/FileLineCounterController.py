from pathlib import Path
from typing import Optional

from Controllers.FileComparerController import FileComparerController
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
        self.__file_comparer_controller = FileComparerController()
        self.__file_analyzer_controller = LineAnalyzerController()

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
            self.__process_directory(
                path_old_object,
                path_new_object,
                line_counting_results
            )
        elif path_old_object.is_file():
            if path_old_object.suffix == ".py":
                # Check if the file exists in the new project
                if self.file_exists_anywhere(path_old_object, path_new_object):
                    # Find the path to the new file
                    path_to_new_file = self.find_matching_file(
                        path_old_object,
                        path_new_object
                    )
                    # Metrics for the new file
                    new_file_metrics = self.get_file_metrics(
                        path_to_new_file, path_old_object
                    )
                    line_counting_results[path_old_object] = new_file_metrics
            else:
                line_counting_results[path_old_object] = \
                    ("error","Not a Python file", "None")
                
        line_counting_results["Total"] = \
        self.calculate_total_physical_lines(line_counting_results)

        self.__file_line_counter_model.set_line_count_results(
            line_counting_results
        )
           
    def calculate_total_physical_lines(self, line_counting_results):
        """
        Sum the total physical lines of all file classes processed.
        Sum the total added lines of all file classes processed.
        Sum the total deleted lines of all file classes processed.
        """
        total_physical_lines = 0
        total_added_lines = 0
        total_removed_lines = 0

        for file_path, metrics in line_counting_results.items():
            if isinstance(metrics, tuple) and len(metrics) == 5:
                _, physical_lines, _, \
                added_lines, removed_lines = metrics
                if isinstance(physical_lines, int) \
                    and isinstance(added_lines, int) \
                    and isinstance(removed_lines, int):
                    total_physical_lines += physical_lines
                    total_added_lines += added_lines
                    total_removed_lines += removed_lines
        return "", total_physical_lines, "", \
            total_added_lines, total_removed_lines
 
    def __process_directory(
        self,
        old_directory: Path,
        new_directory: Path,
        line_counting_results
    ):
        """
        Recursively processes a directory to count lines
        in all Python classes.
        """
        old_files = {
            file.relative_to(old_directory): file for file in old_directory.rglob("*.py")
        }
        new_files = {
            file.relative_to(new_directory): file for file in new_directory.rglob("*.py")
        }

        # Common files (they are in both)
        for relative_path in old_files.keys() & new_files.keys():
            old_file = old_files[relative_path]
            new_file = new_files[relative_path]
            file_metrics = self.get_file_metrics(new_file, old_file)
            line_counting_results[old_file] = file_metrics

        # Deleted files (they are in old but not in new)
        for relative_path in old_files.keys() - new_files.keys():
            old_file = old_files[relative_path]
            line_counting_results[old_file] = ("Deleted", 0, 0, 0, 0)

        # Files added (they are in new but not in old)
        for relative_path in new_files.keys() - old_files.keys():
            new_file = new_files[relative_path]
            new_file_metrics = self.get_file_basic_metrics(new_file)
            line_counting_results[new_file] = new_file_metrics

    def get_file_basic_metrics(self, file_path):
        """
        Retrieves the physical line count of a Python class.
        Retrieves the number of methods in a Python class.
        """
        file_lines = self.get_file_lines(file_path)
        is_valid = self.__validate_file_compliance_with_standard(file_lines)
        
        if not is_valid:
            return "New file doesn't comply with Standard", "None", "None", 0, 0
        
        new_lines = \
            self.__file_analyzer_controller.count_physical_lines(file_lines)
        methods_count = \
            self.__file_analyzer_controller.count_methods(file_lines)

        return "New file", new_lines, methods_count, 0, new_lines

    def get_file_metrics(self, new_file_path, old_file_path):
        """
        Retrieves the physical line count of a Python class.
        Retrieves the class name and methods count of a Python class.
        """
        file_lines = self.get_file_lines(new_file_path)

        is_valid = self.__validate_file_compliance_with_standard(file_lines)

        if is_valid:
            class_name, physical_line_count, methods_count = \
                self.__file_analyzer_controller.get_all_data(file_lines)

            added_lines, removed_lines = \
                self.__file_comparer_controller.compare_files(
                    old_file_path,
                    new_file_path
                )
            
            # self.__file_comparer_controller.add_modification_comments(
            #     old_file_path, 
            #     new_file_path
            # )

            return class_name, physical_line_count, \
            methods_count, added_lines, removed_lines

        return "Doesn't comply with Standard", "None", "None", 0, 0
    
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

        return any(
            file.name == old_file_name for file in new_project_root.rglob("*.py")
        )
    
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
            line_counting_results
        )
