import json
import pathlib


class ValohaiTestEnvironment:
    def __init__(self, root_dir: str):
        self.root_path = pathlib.Path(root_dir)
        self.config_path = self.root_path / "config"
        self.inputs_path = self.root_path / "inputs"
        self.outputs_path = self.root_path / "outputs"

    def build(self):
        for path in (
            self.root_path,
            self.config_path,
            self.inputs_path,
            self.outputs_path,
        ):
            path.mkdir(exist_ok=True, parents=True)
        (self.config_path / "parameters.json").write_text(
            json.dumps(self.get_parameters())
        )
        (self.config_path / "inputs.json").write_text(json.dumps(self.get_inputs()))

    def get_inputs(self):
        return {
            "single_image": {
                "files": [
                    {
                        "checksums": {
                            "md5": "c8e7e1fc344be6982710f54d47191ef6",
                            "sha1": "628a43d996686e654934e27c99e51afe432fc164",
                            "sha256": "8c712905b799905357b8202d0cb7a244cefeeccf7aa5eb79896645ac50158ffa",
                        },
                        "name": "Example.jpg",
                        "path": "%s/single_image/Example.jpg" % self.inputs_path,
                        "size": 27661,
                        "uri": "https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg",
                    }
                ]
            },
            "images_in_subdirs": {
                "files": [
                    {
                        "name": "label1/Example.jpg",
                        "path": "%s/images_in_subdirs/label1/Example.jpg"
                        % self.inputs_path,
                        "size": 27661,
                        "uri": "https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg",
                    },
                    {
                        "name": "label2/Example.jpg",
                        "path": "%s/images_in_subdirs/label2/Example.jpg"
                        % self.inputs_path,
                        "size": 27661,
                        "uri": "https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg",
                    },
                ]
            },
            "input_with_archive": {
                "files": [
                    {
                        "name": "archive.zip",
                        "path": "%s/input_with_archive/archive.zip" % self.inputs_path,
                    }
                ]
            },
        }

    def get_parameters(self):
        return {"foobar": 123, "test": "teststr"}
