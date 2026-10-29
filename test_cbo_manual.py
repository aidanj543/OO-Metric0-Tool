
from pathlib import Path

from metrics.cbo import (
    calculate_cbo,
    get_class_dependencies
)

import ast


# Read hospital management code
source_code = Path(
    "samples/hospital_management.py"
).read_text(encoding="utf-8")

# Calculate CBO
results = calculate_cbo(source_code)

# Parse the code to identify dependencies
tree = ast.parse(source_code)

classes = [
    node for node in tree.body
    if isinstance(node, ast.ClassDef)
]

class_names = {node.name for node in classes}

print("------ Coupling Between Objects (CBO) -------")

for class_node in classes:

    dependencies = get_class_dependencies(
        class_node,
        class_names
    )

    cbo = results[class_node.name]

    print(f"\nClass: {class_node.name}")
    print(f"Dependencies: {sorted(dependencies)}")
    print(f"CBO: {cbo}")
