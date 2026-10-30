
import ast
from pathlib import Path

from metrics.rfc import calculate_rfc, get_response_set


# Read the Python source file
source_code = Path(
    "samples/hospital_management.py"
).read_text(encoding="utf-8")


# Parse the code into an AST
tree = ast.parse(source_code)

# Calculate RFC
results = calculate_rfc(source_code)

print("------ Response for a Class (RFC) ------")

for node in tree.body:

    if isinstance(node, ast.ClassDef):

        response_set = get_response_set(node)

        print(f"\nClass: {node.name}")
        print(f"Response Set: {sorted(response_set)}")
        print(f"RFC: {results[node.name]}")
