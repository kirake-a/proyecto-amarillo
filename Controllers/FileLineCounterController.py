from pathlib import Path
from .PythonStandardValidatorController import (
    PythonStandardValidatorController)
from .LineAnalyzerController import LineAnalyzerController
from FileReader import FileReader

import re


class FileLineCounterController:
    """
    Controller for counting logical and physical lines in Python files.
    It processes individual files or directories and validates compliance
    with Python coding standards.
    """

    def __init__(self, file_line_counter_view=None,
                 file_line_counter_model=None):
        """
        Initializes the FileLineCounterController.
        """
        self.__file_line_counter_view = file_line_counter_view
        self.__file_line_counter_model = file_line_counter_model

    def set_file_line_counter_view(self, file_line_counter_view):
        """
        Sets the view for the file line counter.
        """
        self.__file_line_counter_view = file_line_counter_view

    def set_file_line_counter_model(self, file_line_counter_model):
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

    def process_file_path(self, file_path):
        """
        Processes the given file path, determining whether it is a directory
        or a Python file, then counts it's logical and physical lines
        in a class and sum the total lines.
        """
        path_object = Path(file_path)
        line_counting_results = {}
        

        if path_object.is_dir():
            self.__process_directory(path_object, line_counting_results)
        elif path_object.is_file():
            if path_object.suffix == ".py":
                file_metrics = self.get_file_metrics(path_object)
                line_counting_results[path_object] = file_metrics
            else:
                line_counting_results[path_object] = \
                    ("error","Not a Python file", "None")
                
        line_counting_results["Total"] = \
        self.calculate_total_lines(line_counting_results)

        self.__file_line_counter_model.set_line_count_results(
            line_counting_results)
        
        #self.calculate_total_lines(line_counting_results)
        
    def calculate_total_lines(self, line_counting_results):
        """
        Sum the total logical and physical lines 
        of all file classes processed.
        """
        total_logical_lines = 0
        total_physical_lines = 0

        for file_path, metrics in line_counting_results.items():
            if isinstance(metrics, tuple) and len(metrics) == 4:
                class_name, logical_lines, physical_lines, \
                methods_count = metrics
                if isinstance(logical_lines, int) \
                and isinstance(physical_lines, int):
                    total_logical_lines += logical_lines
                    total_physical_lines += physical_lines
        return "", total_logical_lines, total_physical_lines, ""
 

    def __process_directory(self, directory, line_counting_results):
        """
        Recursively processes a directory to count lines in all Python classes.
        """
        for file in directory.iterdir():
            if file.is_file() and file.suffix == ".py":
                file_metrics = self.get_file_metrics(file)
                line_counting_results[file] = file_metrics
            elif file.is_dir():
                self.__process_directory(file, line_counting_results)

    def get_file_metrics(self, file):
        """
        Retrieves the logical and physical line count of a Python class.
        Retrieves the class name and methods count of a Python class.
        """
        file_lines = self.get_file_lines(file)
        is_valid = self.__validate_file_compliance_with_standard(file_lines)


        if is_valid:

            class_name = self.__extract_class(file_lines)
            physical_line_count = self.__count_physical_lines(file_lines)
            logical_line_count = self.__count_logical_lines(file_lines)
            methods_count = self.__count_methods(file_lines)
            return class_name, logical_line_count, \
            physical_line_count, methods_count

        return "No class", "Doesn't comply with Standard", "None", "None" 
    
    def get_file_lines(self, file_path):
        """
        Reads the lines of a given file.
        """
        file_reader = FileReader(file_path)
        return file_reader.read_file()

    def __validate_file_compliance_with_standard(self, file_lines):
        """
        Validates whether a file complies with Python coding standards..
        """
        standard_validator = PythonStandardValidatorController(file_lines)
        return standard_validator.validate_compliance_with_standard()

    def __count_logical_lines(self, file_lines):
        """
        Counts the logical lines of code in a class.
        """
        logical_file_line_counter = LineAnalyzerController(file_lines)
        return logical_file_line_counter.count_logical_lines()

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

    def manage_model_changes(self):
        """
        Updates the view with the latest line counting results
        from the model.
        """
        line_counting_results = \
            self.__file_line_counter_model.get_line_count_results()

        self.__file_line_counter_view.show_metric_results(
            line_counting_results)
