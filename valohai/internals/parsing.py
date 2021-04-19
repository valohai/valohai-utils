import ast
from collections import namedtuple
from typing import Any, Dict, List, Optional


def is_module_function_call(node: ast.Call, module: str, function: str) -> bool:
    try:
        return node.func.attr == function and node.func.value.id == module  # type: ignore
    except AttributeError:
        return False


class PrepareParser(ast.NodeVisitor):
    """Parses .py file for Valohai inputs, parameters, step name

    Using AST parser, visits all method calls of a Python file.

    If a call to valohai.prepare() method is found, iterate through
    it's arguments and look for inputs, parameters and a step name.

    All possible ways to call prepare() are not supported

    Works:
        valohai.prepare(parameters={"param1": "foobar"})

    Works:
        parameters={"param1": "foobar"}
        valohai.prepare(parameters=parameters)

    Fails:
        import valohai as herpderp
        herpderp.prepare(parameters={"param1": "foobar"})

    Fails:
        from valohai import prepare
        prepare(parameters={"param1": "foobar"})

    Fails:
        valohai.prepare(parameters=get_parameters())
    """

    assignments: Dict[str, Any]  # TODO: embetter type
    parameters: Dict[str, Any]  # TODO: embetter type
    inputs: Dict[str, Any]  # TODO: embetter type
    step: Optional[str]

    def __init__(self) -> None:
        self.assignments = {}
        self.parameters = {}
        self.inputs = {}
        self.step = None
        self.image = None

    def visit_Assign(self, node: ast.Assign) -> None:
        try:
            self.assignments[node.targets[0].id] = ast.literal_eval(node.value)  # type: ignore
        except ValueError:
            # We don't care about assignments that can't be literal_eval():ed
            pass

    def visit_Call(self, node: ast.Call) -> None:
        if is_module_function_call(node, "valohai", "prepare"):
            self.process_valohai_prepare_call(node)

    def process_valohai_prepare_call(self, node: ast.Call) -> None:
        self.step = "default"
        if hasattr(node, "keywords"):
            for key in node.keywords:
                if key.arg == "default_parameters":
                    self.process_default_parameters_arg(key)
                elif key.arg == "default_inputs":
                    self.process_default_inputs_arg(key)
                elif key.arg == "step":
                    self.step = ast.literal_eval(key.value)
                elif key.arg == "image":
                    self.image = ast.literal_eval(key.value)

    def process_default_inputs_arg(self, key: ast.keyword) -> None:
        if isinstance(key.value, ast.Name) and key.value.id in self.assignments:
            self.inputs = {
                key: value if isinstance(value, List) else [value]
                for key, value in self.assignments[key.value.id].items()
            }
        elif isinstance(key.value, ast.Dict):
            self.inputs = {
                key: value if isinstance(value, List) else [value]
                for key, value in ast.literal_eval(key.value).items()
            }
        else:
            raise NotImplementedError()

    def process_default_parameters_arg(self, key: ast.keyword) -> None:
        if isinstance(key.value, ast.Name) and key.value.id in self.assignments:
            self.parameters = self.assignments[key.value.id]
        elif isinstance(key.value, ast.Dict):
            self.parameters = ast.literal_eval(key.value)
        else:
            raise NotImplementedError()


def parse(source):
    tree = ast.parse(source)
    parser = PrepareParser()
    parser.visit(tree)
    result = namedtuple("result", ["step", "parameters", "inputs", "image"])
    return result(
        step=parser.step,
        parameters=parser.parameters,
        inputs=parser.inputs,
        image=parser.image,
    )
