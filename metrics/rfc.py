
import ast


def get_response_set(class_node):
    """
    Find the methods that belong to a class's
    direct response set.

    Includes:
    1. Methods declared in the class
    2. Distinct attribute-style methods they call
    """

    response_set = set()

    # Identify methods explicitly defined in the class
    methods = [
        node for node in class_node.body
        if isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef)
        )
    ]

    # Add each declared method to the response set
    for method in methods:
        response_set.add(method.name)

    # Find method calls inside each declared method
    for method in methods:

        for node in ast.walk(method):

            if isinstance(node, ast.Call):

                if isinstance(node.func, ast.Attribute):
                    called_method = node.func.attr

                    response_set.add(called_method)

    return response_set


def calculate_rfc(source_code: str) -> dict[str, int]:
    """
    Calculate Response for a Class (RFC).

    RFC = number of distinct declared and
    directly called attribute-method names.
    """

    # Step 1: Parse the Python source
    tree = ast.parse(source_code)

    results = {}

    # Step 2: Locate class definitions
    for node in tree.body:

        if isinstance(node, ast.ClassDef):

            # Step 3: Find the response set
            response_set = get_response_set(node)

            # Step 4: Calculate RFC
            results[node.name] = len(response_set)

    return results
