class FileInfo:
    def __init__(self, *, name, uri, path=None, size=None, checksums=None):
        self.name = str(name)
        self.uri = str(uri)
        self.checksums = checksums
        self.path = str(path) if path else None
        self.size = int(size) if size else None


class InputInfo:
    def __init__(self, files):
        self.files = list(files)

    @classmethod
    def from_json_data(cls, json_data: dict) -> "InputInfo":
        return cls(files=[FileInfo(**d) for d in json_data.get("files", ())])
