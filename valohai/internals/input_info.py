import json

class FileInfo:
    def __init__(self, *, name=None, path=None, size=None, uri=None, checksums=None):
        self.name = str(name) if name else None
        self.path = str(path) if path else None
        self.size = int(size) if size else None
        self.uri = str(uri) if uri else None
        self.checksums = checksums if checksums else None

    def to_serializable_dict(self):
        result = {}
        if self.name:
            result['name'] = self.name
        if self.path:
            result['path'] = self.path
        if self.size:
            result['size'] = self.size
        if self.uri:
            result['uri'] = self.uri
        if self.checksums:
            result['checksums'] = self.checksums
        return result

    def to_json(self):
        return json.dumps(self.to_serializable_dict(), sort_keys=True, indent=4)

    @classmethod
    def from_json_data(cls, json_data: dict) -> "FileInfo":
        obj = cls(**json_data)
        return obj


class InputInfo:
    def __init__(self, *, name, files):
        self.name = name
        if not isinstance(files, list):
            files = [files]
        self.files = files

    def to_serializable_dict(self):
        return {
            self.name: {
                "files": [o.to_serializable_dict() for o in self.files]
            }
        }

    def to_json(self):
        return json.dumps(self.to_serializable_dict(), sort_keys=True, indent=4)

    @classmethod
    def from_json_data(cls, *, name, json_data: dict) -> "InputInfo":
        obj = cls(name=name, files=[FileInfo.from_json_data(f) for f in json_data.get('files', [])])
        return obj
