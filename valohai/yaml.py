from collections import OrderedDict

import yaml
from valohai_yaml.objs.config import Config

# https://stackoverflow.com/questions/42518067/how-to-use-ordereddict-as-an-input-in-yaml-dump-or-yaml-safe-dump
yaml.add_representer(
    OrderedDict,
    lambda dumper, data: dumper.represent_mapping(
        "tag:yaml.org,2002:map", data.items()
    ),
)


def config_to_yaml(config: Config) -> str:
    """Serialize Valohai Config to YAML

    :param config: valohai_yaml.objs.Config object
    """

    return yaml.dump(config.serialize(), default_flow_style=False)
