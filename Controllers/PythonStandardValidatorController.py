from Utils.ProgrammingLanguageStandardValidator import (
    ProgrammingLanguageStandardValidator)

class PythonStandardValidatorController(ProgrammingLanguageStandardValidator):
    """
    Controller class for validating Python file compliance with PEP 8.

    Inherits from ProgrammingLanguageStandardValidator
    to check specific Pythoncode formatting rules, such as line length.
    """

    def __init__(self, file):
        """
        Initializes the PythonStandardValidatorController with
        the specified file.
        """
        super().__init__(file)
        self.MAX_CHAR_PER_LINE = 79

    def validate_compliance_with_standard(self):
        """
        Validates the compliance of the file with PEP 8 standards.

        This method checks if all lines in the file comply with
        the maximum allowedline length (79 characters).
        If any line exceeds this length, the validation fails.
        """
        return self.__validate_length_of_line()

    def __validate_length_of_line(self):
        """
        Checks the length of each line in the file to ensure
        it does not exceed the PEP 8 limit of 79 characters.
        """
        for line in self.file:
            if len(line) > self.MAX_CHAR_PER_LINE:
                return False

        return True
