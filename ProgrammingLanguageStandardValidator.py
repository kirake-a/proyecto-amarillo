from abc import ABC, abstractmethod


class ProgrammingLanguageStandardValidator(ABC):
    """
    An abstract base class for validating 
    compliance with a programming language standard.

    This class provides an interface for checking 
    whether a given file adheres to a specific programming 
    language's standard.
    """

    def __init__(self, file):
        """
        Initializes the validator with the given file.
        """
        self.file = file

    @abstractmethod
    def validate_compliance_with_standard(self):
        """
        Abstract method that must be implemented by subclasses 
        to check if the given file complies with the programming
        language standard.
        """
        pass
