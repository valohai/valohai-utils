import json

from valohai_yaml.objs.base import Item


class FileInfo(Item):
    def __init__(self, *, name=None, path=None, size=None, uri=None, checksums=None):
        self.name = str(name)
        self.path = str(path) if path else None
        self.size = int(size) if size else None
        self.uri = str(uri) if uri else None
        self.checksums = checksums if checksums else None


class InputInfo(Item):
    def __init__(self, *, name, files):
        self.name = name
        if not isinstance(files, list):
            files = [files]
        self.files = files

    def serialize(self):
        return {
            self.name: {
                "files": [o.serialize() for o in self.files]
            }
        }

    def to_json(self):
        return json.dumps(self.serialize(), sort_keys=True, indent=4)

    @classmethod
    def parse(cls, data: dict) -> "InputInfo":
        name = [*data][0]
        obj = cls(name=name, files=[FileInfo.parse(f) for f in data[name].get('files', [])])
        return obj
