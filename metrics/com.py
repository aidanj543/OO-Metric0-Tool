
import ast
from itertools import combinations


class AttributeVisitor(ast.NodeVisitor):
    """Find instance attributes accessed by a method."""

    def __init__(self):
        self.attributes = set()

    def visit_Attribute(self, node):
        # Detect self.attribute
        if (
            isinstance(node.value, ast.Name)
            and node.value.id == "self"
        ):
            self.attributes.add(node.attr)

        self.generic_visit(node)

    def visit_Call(self, node):
        # Do not count self.method() as a data attribute
        if (
            isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "self"
        ):
            for arg in node.args:
                self.visit(arg)

            for keyword in node.keywords:
                self.visit(keyword.value)

        else:
            self.generic_visit(node)


def get_method_attributes(method):
    """Return the instance attributes used by a method."""

    visitor = AttributeVisitor()

    for statement in method.body:
        visitor.visit(statement)

    return visitor.attributes


def calculate_com(source_code: str) -> dict[str, float]:
    """Calculate pairwise Cohesion of Methods (COM)."""

    tree = ast.parse(source_code)
    results = {}

    for node in tree.body:

        if not isinstance(node, ast.ClassDef):
            continue

        methods = [
            item for item in node.body
            if isinstance(
                item,
                (ast.FunctionDef, ast.AsyncFunctionDef)
            )
        ]

        # Special cases
        if len(methods) == 0:
            results[node.name] = 0.0
            continue

        if len(methods) == 1:
            results[node.name] = 1.0
            continue

        # Extract attributes for each method
        attribute_sets = [
            get_method_attributes(method)
            for method in methods
        ]

        # Generate all possible method pairs
        pairs = list(combinations(attribute_sets, 2))

        shared_pairs = 0

        for attrs_a, attrs_b in pairs:
            # Intersection finds shared attributes
            if attrs_a.intersection(attrs_b):
                shared_pairs += 1

        # Calculate cohesion ratio
        com = shared_pairs / len(pairs)

        results[node.name] = round(com, 2)

    return results
