import logging

class FileReader():
    """
    A utility class for reading the contents of a file.

    This class provides methods to read a file's content while handling 
    errors such as missing files or unexpected exceptions. Errors are 
    logged for debugging purposes.
    """

    def __init__(self, file_path):
        """
        Reads the content of the file and returns it as a list of lines.
        """
        self.__file_path = file_path

    def read_file(self):
        """
        Reads the content of the file and returns it as a list of lines.
        Handles errors when given an unvalid filepath or there
        is an error while reading it
        """
        try:
            with open(self.__file_path, "r", encoding="utf-8") as file:
                return file.readlines()
        except FileNotFoundError:
            logging.error(f"El archivo {self.__file_path} no existe.")
        except Exception as e:
            logging.error(f"Error al leer el archivo {self.__file_path}: {e}")

        return []
