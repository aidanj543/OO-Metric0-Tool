import ast

from metrics.wmc import calculate_wmc
from metrics.com import calculate_com
from metrics.cbo import calculate_cbo
from metrics.rfc import calculate_rfc

def analyze_code(source_code: str) -> list[dict]:
    """
    Validate Python source code, calculate all
    four OO metrics, and combine their results.
    """

    # Step 1: Validate the input
    if not isinstance(source_code, str):
        raise ValueError("Source code must be text.")

    if not source_code.strip():
        raise ValueError("Please provide Python code.")

    # Step 2: Check for Python syntax errors
    tree = ast.parse(source_code)

    # Step 3: Make sure classes exist
    classes = [
        node for node in tree.body
        if isinstance(node, ast.ClassDef)
    ]

    if not classes:
        raise ValueError(
            "No class definitions found in the Python code."
        )

    # Step 4: Calculate each metric
    wmc_results = calculate_wmc(source_code)
    com_results = calculate_com(source_code)
    cbo_results = calculate_cbo(source_code)
    rfc_results = calculate_rfc(source_code)

    # Step 5: Combine results by class
    results = []

    for class_name in wmc_results:
        results.append({
            "Class": class_name,
            "WMC": wmc_results[class_name],
            "COM": com_results[class_name],
            "CBO": cbo_results[class_name],
            "RFC": rfc_results[class_name]
        })

    return results