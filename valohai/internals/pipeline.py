from valohai_yaml.objs import Config


def get_pipeline_from_source(source_path: str, old_config: Config) -> Config:
    """Gets the pipeline definition by executing the main() in the source Python file.

    The file is expected to contain:

    def main(config) -> Pipeline:
        pipeline = Pipeline(name="foo", config=config)
        # ... Pipeline definition ...
        return pipeline

    :param source_path: Path of the Python source code file containing the pipeline definition
    :param old_config: Currently config for the Valohai project (used for validation)

    """
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        name="pipeline_source", location=source_path
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "main"):
        raise AttributeError(f"{source_path} is missing main() method!")
    pipe = module.main(old_config)
    return Config(pipelines=[pipe.to_yaml()])
