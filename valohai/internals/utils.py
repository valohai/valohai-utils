def uri_to_filename(uri: str) -> str:
    return uri.rpartition("/")[-1].split("?", 1)[0]
