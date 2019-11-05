class FileInfo:
    def __init__(self, *, name, path, size, uri, checksums):
        self.name = str(name)
        self.path = str(path)
        self.size = int(size)
        self.uri = str(uri)
        self.checksums = checksums


class InputInfo:
    def __init__(self, files):
        self.files = list(files)

    @classmethod
    def from_json_data(cls, json_data: dict) -> "InputInfo":
        return cls(files=[FileInfo(**d) for d in json_data.get("files", ())])
