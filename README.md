# valohai-utils
Python helper library for the Valohai machine learning platform.

# Install
```bash
pip install valohai-utils
```

# Execution
Run locally
```bash
python mycode.py
```
Run in the cloud
```bash
vh yaml step mycode.py
vh exec run -a mystep
```

# What does valohai-utils do?

- Generates and updates the `valohai.yaml` configuration file based on the source code
- Agnostic input handling (single file, multiple files, zip, tar)
- Parse command-line parameters
- Compress outputs
- Download inputs for local experiments
- Straightforward way to print metrics as Valohai metadata
- Code parity between local vs. cloud

# Parameters

[Valohai parameters ](https://help.valohai.com/hc/en-us/articles/4419896836881-Use-parameters) are variables & hyper-parameters that are parsed from the command-line. You define parameters in a dictionary:

```python
default_parameters = {
    'iterations': 100,
    'learning_rate': 0.001
}
```

The dictionary is fed to `valohai.prepare()` method:

The values given are **default** values. You can override them from the command-line or using the Valohai web UI.

## Example
```python
import valohai

default_parameters = {
    'iterations': 10,
}

valohai.prepare(step="helloworld", default_parameters=default_parameters)

for i in range(valohai.parameters('iterations').value):
    print("Iteration %s" % i)
```

# Inputs

[Valohai inputs](https://help.valohai.com/hc/en-us/articles/4422921110929-Add-input-files-to-your-execution) are the data files required by the experiment. They are automatically downloaded for you, if the data is from a public source. You define inputs with a dictionary:

```python
default_inputs = {
    'input_name': 'http://example.com/1.png'
}
```

An input can also be a list of URLs or a folder:

```python
default_inputs = {
    'input_name': [
        'http://example.com/1.png',
        'http://example.com/2.png'
    ],
    'input_folder': [
        's3://mybucket/images/*',
        'azure://mycontainer/images/*',
        'gs://mybucket/images/*'
    ]
}
```

Or it can be an archive full of files (uncompressed automagically on-demand):

```python
default_inputs = {
    'images': 'http://example.com/myimages.zip'
}
```

The dictionary is fed to `valohai.prepare()` method.

The url(s) given are **defaults**. You can override them from the command-line or using the Valohai web UI.

## Example
```python
import csv
import valohai

default_inputs = {
    'myinput': 'https://pokemon-images-example.s3-eu-west-1.amazonaws.com/pokemon.csv'
}

valohai.prepare(step="test", default_inputs=default_inputs)

with open(valohai.inputs("myinput").path()) as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
```

# Outputs

[Valohai outputs](https://help.valohai.com/hc/en-us/articles/4419909997713-Upload-output-data) are the files that your step produces an end result.

When you are ready to save your output file, you can query for the correct path from the `valohai-utils`.

## Example
```python
image = Image.open(in_path)
new_image = image.resize((width, height))
out_path = valohai.outputs('resized').path('resized_image.png')
new_image.save(out_path)
```

Sometimes there are so many outputs that you may want to compress them into a single file.

In this case, once you have all your outputs saved, you can finalize the output with the `compress()` method.

## Example
```python
valohai.outputs('resized').compress("*.png", "images.zip", remove_originals=True)
```

# Logging

You can log metrics using the [Valohai metadata system](https://help.valohai.com/hc/en-us/articles/4419919418129-Collect-and-view-metrics) and then render interactive graphs on the web interface. The `valohai-utils` logger will print JSON logs that Valohai will parse as metadata.

It is important for visualization that logs for single epoch are flushed out as a single JSON object.

## Example
```python
import valohai

for epoch in range(100):
    with valohai.metadata.logger() as logger:
        logger.log("epoch", epoch)
        logger.log("accuracy", accuracy)
        logger.log("loss", loss)
```

## Example 2
```python
import valohai

logger = valohai.logger()
for epoch in range(100):
    logger.log("epoch", epoch)
    logger.log("accuracy", accuracy)
    logger.log("loss", loss)
    logger.flush()
```

# Distributed Workloads

`valohai.distributed` contains a toolset for running distributed tasks on Valohai.

```python
import valohai

if valohai.distributed.is_distributed_task():

    # `master()` reports the same worker on all contexts
    master = valohai.distributed.master()
    master_url = f'tcp://{master.primary_local_ip}:1234'

    # `members()` contains all workers in the distributed task
    member_public_ips = ",".join([
        m.primary_public_ip
        for m
        in valohai.distributed.members()
    ])

    # `me()` has full details about the current worker context
    details = valohai.distributed.me()

    size = valohai.distributed.required_count
    rank = valohai.distributed.rank  # 0, 1, 2, etc. depending on run context
```

# Full example

## Preprocess step for resizing image files

This example step will do the following:
1. Take image files (or an archive containing images) as input.
2. Resize each image to the size provided by the width & height parameters.
3. Compress the resized images into `resized/images.zip` Valohai output file.

```python
import os
import valohai
from PIL import Image

default_parameters = {
    "width": 640,
    "height": 480,
}
default_inputs = {
    "images": [
        "https://dist.valohai.com/valohai-utils-tests/Example.jpg",
        "https://dist.valohai.com/valohai-utils-tests/planeshark.jpg",
    ],
}

valohai.prepare(step="resize", default_parameters=default_parameters, default_inputs=default_inputs)


def resize_image(in_path, out_path, width, height, logger):
    image = Image.open(in_path)
    logger.log("from_width", image.size[0])
    logger.log("from_height", image.size[1])
    logger.log("to_width", width)
    logger.log("to_height", height)
    new_image = image.resize((width, height))
    new_image.save(out_path)


if __name__ == '__main__':
    for image_path in valohai.inputs('images').paths():
        with valohai.metadata.logger() as logger:
            filename = os.path.basename(image_path)
            resize_image(
                in_path=image_path,
                out_path=valohai.outputs('resized').path(filename),
                width=valohai.parameters('width').value,
                height=valohai.parameters('height').value,
                logger=logger
            )
    valohai.outputs('resized').compress("*", "images.zip", remove_originals=True)
```

CLI command:
```
vh yaml step resize.py
```

Will produce this `valohai.yaml` config:
```yaml
- step:
    name: resize
    image: python:3.11-slim
    command: python ./resize.py {parameters}
    parameters:
    - name: width
      default: 640
      multiple-separator: ','
      optional: false
      type: integer
    - name: height
      default: 480
      multiple-separator: ','
      optional: false
      type: integer
    inputs:
    - name: images
      default:
      - https://dist.valohai.com/valohai-utils-tests/Example.jpg
      - https://dist.valohai.com/valohai-utils-tests/planeshark.jpg
      optional: false
```

# Configuration

There are some environment variables that affect how `valohai-utils` works when not running within a Valohai execution context.

* `VH_FLAT_LOCAL_OUTPUTS`
  * If set, flattens the local outputs directory structure into a single directory.
    This means that outputs from subsequent runs can clobber old files.

# Development

If you wish to further develop `valohai-utils`, remember to install development dependencies and write tests for your additions.

### Linting

Lints are run via pre-commit.

If you want pre-commit to check your commits via git hooks,

```
pip install pre-commit
pre-commit install
```

You can also run the lints manually with `pre-commit run --all-files`.

### Testing

```bash
pip install -e . -r requirements-dev.txt
pytest
```
