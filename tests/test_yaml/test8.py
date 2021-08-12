import valohai

params = {
    "batch_size": {
        "default": 32,
        "type": "integer",
        "description": "Size of the training batch",
        "pass-as": "--batch:{v}",
        "optional": True,
        "multiple-separator": "!",
    },
    "learning_rate": {
        "default": 0.001,
    },
    "dropout": 0.2,
}

inputs = {
    "classes": {
        "default": "s3://special-bucket/foo/bar/**.txt",
        "optional": True,
        "filename": "asdf.txt",
        "keep-directories": "full",
    },
    "images": {
        "default": "s3://special-bucket/images/**.jpg",
    },
    "weights": "s3://special-bucket/weights/yolo.pb",
}

valohai.prepare(step="train", default_parameters=params, default_inputs=inputs)
