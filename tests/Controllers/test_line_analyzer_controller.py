import pytest
from Controllers.LineAnalyzerController import LineAnalyzerController


@pytest.mark.parametrize("file_content,expected_physical,expected_logical",[
    ([], 0, 0),
    (["# Esto es un comentario"], 0, 0),
    (["\"\"\" Este es un docstring \"\"\""], 0, 0),
    (["\"\"\"", "    Esto también es un docstring", "\"\"\""], 0, 0),
    (["print('Hola')"], 1, 0),
    (["print('Hola')", "print('Mundo')"], 2, 0),
    (["print('Hola')  # Comentario"], 1, 0),
    (["resultado = 1 + 2 + \\", "3 + 4"], 2, 0),
    (["print('Hola')", "a = 5 + \\", "6 + \\", "7", 
      "# Esto es un comentario", "if True: (",
      "    print('if')", ")", 
      "lista = [", "   1, 2, 3,", "   4, 5", "]"], 11, 1),
    (["def ejemplo(",
      "self, param1, param2):",
      "\"\"\"Este es un docstring de una sola línea.\"\"\"",
      "path_object = Path(file_path), line_counting_results = {}",
      "print('Hola, mundo')", "", "\"\"\"", "Este es un docstring",
      "de múltiples líneas.",
      "\"\"\"", "print('Adiós, mundo')"], 5, 1),
      (["class MyClass:\n",
        "    def my_method(self):\n",
        "        if True:\n",
        "            for i in range(10):\n",
        "                print(i)\n",
        "        elif False:\n",
        "            print('if')\n",
        "            print('for')\n",
        "            print('switch')\n",
        "            print('try')\n",
        "        else:\n",
        "            print('else')\n",
        "    # This is a comment\n",
        "    def another_method(self):\n",
        "        pass\n",
        "    if lif > 0 for x in range(10):\n",
        "        print('Múltiples estructuras')"], 16, 7)
      

])
def test_line_counting(file_content, expected_physical, expected_logical):
    """
    Tests the logical and physical line 
    counting functionality of the LineAnalyzerController.

    The test ensures that:
    - Comments and docstrings are ignored in logical line counting.
    - Multi-line expressions (tuples, lists, dictionaries)
      are counted correctly.
    - Explicit line continuations (using `backlash`) are handled properly.
    - Empty lines do not affect the count.
    - Complex structures like function definitions and control statements 
    are processed correctly.
    """
    analyzer = LineAnalyzerController(file_content)

    assert analyzer.count_physical_file_lines() == expected_physical
    assert analyzer.count_logical_file_lines() == expected_logical