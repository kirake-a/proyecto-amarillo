import pytest
import logging
from FileReader import FileReader


@pytest.fixture
def python_test_file(tmp_path):
    """
    Creates a temporary Python test file with sample content.
    """
    file_path = tmp_path / "test_script.py"
    file_content = (
        "import os\n\n"
        "def funcion_prueba():\n"
        '    print("Hola, mundo!")\n\n'
        "# Fin del script\n"
    )
    file_path.write_text(file_content, encoding="utf-8")
    return file_path


def test_read_python_file(python_test_file):
    """
    Tests reading a valid Python file.

    The test verifies that:
    - The file is read correctly.
    - The returned content matches the expected content.
    """
    file_reader = FileReader(str(python_test_file))
    content = file_reader.read_file()

    expected_content = [
        "import os\n",
        "\n",
        "def funcion_prueba():\n",
        '    print("Hola, mundo!")\n',
        "\n",
        "# Fin del script\n",
    ]
    assert (
        content == expected_content
    ), "El contenido del archivo Python no coincide."

def test_read_python_file_not_found(caplog):
    """
    Tests the case when a python file is not found.
    It should return an empty list
    """
    file_reader = FileReader("no_existe.py")

    with caplog.at_level(logging.ERROR):
        content = file_reader.read_file()
        assert "El archivo no_existe.py no existe." in caplog.text

    assert content == [], "Debe devolver una lista vacía."


@pytest.fixture
def empty_test_file(tmp_path):
    """
    Creates an empty Python test file.
    """
    file_path = tmp_path / "empty_script.py"
    file_path.write_text("", encoding="utf-8")
    return file_path


def test_read_python_file_empty(empty_test_file):
    """
    Tests reading an empty Python file
    The test verifies that:
    - An empty file returns an empty list.
    """
    file_reader = FileReader(str(empty_test_file))
    content = file_reader.read_file()

    assert content == [], (
        "El contenido del archivo vacío debe ser una lista vacía."
    )
