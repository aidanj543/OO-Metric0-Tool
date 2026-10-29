import ast

def calculate_wmc(source_code: str)-> dict[str, int]:
    tree = ast.parse(source_code) #Converts the Python code into an AST

    results = {} #Stores results for each class

    for node in tree.body: #Looks for class definitions
        if isinstance(node, ast.ClassDef):
            method_count = 0
            for item in node.body:
                if isinstance(
                    item,
                    (ast.FunctionDef, ast.AsyncFunctionDef)
                ):
                    method_count +=1
            results[node.name] = method_count #Save the Class's WMC
    return results