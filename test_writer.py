import os
import re


def write_test_file(function_name, test_code, output_dir="tests"):
    os.makedirs(output_dir, exist_ok=True)
    test_file_name = f"test_{function_name}.py"
    file_path = os.path.join(output_dir, test_file_name)

    with open(file_path, "w") as f:
        f.write(test_code)
    
    print(f"✅ Test written to: {file_path}")


def postprocess_test_code(test_code, function_name, module_name):
    """
    Ajusta automáticamente el código de test generado por LLM:
    - Reemplaza el nombre del módulo (your_module → module_name).
    - Reemplaza el nombre de la función si el LLM usó otra (detectada por regex).
    - Agrega docstring de advertencia opcional.
    """

    # Reemplaza el módulo de importación
    test_code = test_code.replace("your_module", module_name)

    # Detecta si usó un nombre de función incorrecto
    match = re.search(r"def test_(\w+)\(", test_code)
    if match:
        used_name = match.group(1)
        if used_name != function_name:
            test_code = test_code.replace(used_name, function_name)

    # Remueve markdown ```python``` si viene de OpenAI
    test_code = test_code.replace("```python", "").replace("```", "")

    return test_code.strip()


def clean_llm_output(text: str) -> str:
    """
    Limpia el texto generado por el LLM:
    - Elimina bloques de código markdown.
    - Elimina aclaraciones tipo 'make sure to replace ...'.
    - Retorna solo el código.
    """
    # Quita ```python ... ```
    text = re.sub(r"```(?:python)?", "", text)
    
    # Elimina líneas al final que empiecen con 'Make sure' u otras aclaraciones
    lines = text.strip().splitlines()
    lines = [line for line in lines if not re.match(r"(?i)^make sure|^note|^replace", line.strip())]

    return "\n".join(lines).strip()
