
import ast


def get_class_dependencies(class_node, class_names):
    """
    Find other classes referenced by a class.

    Only classes defined in the analyzed file count.
    """

    dependencies = set()

    # Inspect all nodes inside the class
    for node in ast.walk(class_node):

        if isinstance(node, ast.Name):

            referenced_name = node.id

            # Check whether this name is another class
            if (
                referenced_name in class_names
                and referenced_name != class_node.name
            ):
                dependencies.add(referenced_name)

    return dependencies


def calculate_cbo(source_code: str) -> dict[str, int]:
    """
    Calculate Coupling Between Objects (CBO).

    CBO = number of unique other classes referenced.
    """

    # Step 1: Parse source code
    tree = ast.parse(source_code)

    # Step 2: Find all top-level classes
    classes = [
        node for node in tree.body
        if isinstance(node, ast.ClassDef)
    ]

    # Step 3: Collect class names
    class_names = {
        class_node.name for class_node in classes
    }

    results = {}

    # Step 4: Analyze each class
    for class_node in classes:

        dependencies = get_class_dependencies(
            class_node,
            class_names
        )

        # Step 5: Count unique dependencies
        results[class_node.name] = len(dependencies)

    return results
