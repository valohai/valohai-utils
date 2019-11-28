import ast
from typing import List


def ast_to_value_recursive(ast_value):
    if isinstance(ast_value, ast.Num):
        return ast_value.n
    elif isinstance(ast_value, ast.Str):
        return ast_value.s
    elif isinstance(ast_value, ast.NameConstant):
        return bool(ast_value.value)
    elif isinstance(ast_value, ast.Dict):
        result = {}
        for k, v in zip(ast_value.keys, ast_value.values):
            result[k.s] = ast_to_value_recursive(v)
        return result
    elif isinstance(ast_value, ast.List):
        result = []
        for v in ast_value.elts:
            result.append(ast_to_value_recursive(v))
        return result
    return None


def parse(source):
    class PrepareParser(ast.NodeVisitor):
        def __init__(self):
            self.assignments = {}
            self.parameters = {}
            self.inputs = {}
            self.step = None

        def visit_Assign(self, node):
            self.assignments[node.targets[0].id] = ast_to_value_recursive(node.value)

        def visit_Call(self, node):
            if hasattr(node, "func") and \
                hasattr(node.func, "attr") and \
                node.func.attr == 'prepare' and \
                hasattr(node.func, "value") and \
                hasattr(node.func.value, "id") and \
                node.func.value.id == 'valohai':

                self.step = "default"
                if hasattr(node, "keywords"):
                    for key in node.keywords:
                        if key.arg == "parameters":
                            if key.value.id in self.assignments:
                                self.parameters = self.assignments[key.value.id]
                        if key.arg == "inputs":
                            if key.value.id in self.assignments:
                                self.inputs = {
                                    key: value if isinstance(value, List) else [value]
                                    for key, value in self.assignments[key.value.id].items()
                                }
                if hasattr(node, "args"):
                    self.step = node.args[0].s



    tree = ast.parse(source)
    parser = PrepareParser()
    parser.visit(tree)
    return parser.step, parser.parameters, parser.inputs
