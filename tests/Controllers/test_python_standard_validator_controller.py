import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/../.."))

from Controllers.PythonStandardValidatorController import PythonStandardValidatorController


@pytest.mark.parametrize("file, expected", [
    ([
        'print("Hola mundo")\n',
        'x = 10\n',
        'def suma(a, b):\n',
        '    return a + b\n'
    ], True),

    ([
        'print("Esta línea es muy larga y definitivamente tiene más de 79 caracteres, por lo que debería fallar")\n'
    ], False),

    ([], True),

    ([
        'x = "Corto"\n',
        'print("Este es un texto válido")\n',
        'print("Pero esta línea es demasiado larga porque tiene más de 79 caracteres y debe fallar")\n'
    ], False)
])
def test_validate_compliance_with_standard(file, expected):
    """
    Tests the validation of Python code compliance with the standard.

    This test function uses parameterization to check if different Python code snippets 
    comply with the expected coding standard. It verifies if the `validate_compliance_with_standard` 
    method correctly identifies whether the given lines of code adhere to the defined rules.
    """
    validator = PythonStandardValidatorController(file)
    assert validator.validate_compliance_with_standard() == expected