# valohai-utils
Python helper library for the Valohai machine learning platform.

# install
```python
pip install valohai-utils
```

# execution
Run locally
```python
python mycode.py
```
Run in the cloud
```python
vh yaml step mycode.py
vh exec run -a mystep
```

# What does it do?

- Updates `valohai.yaml` based on source code
- Agnostic input handling (single file, multiple files, zip, tar)
- Parse command-line parameters
- Compress outputs
- Download inputs for local experiments
- Straightforward JSON logs
- Fully reproducible for local vs. cloud

# Parameters

Parameters are variables & hyper-parameters that are parsed from the command-line. You define a parameters in a dictionary: 

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

Inputs are the data files required by the experiment. They are automatically downloaded for you. You define a inputs with a dictionary:

```python
default_inputs = {
  'input_name': 'http://example.com/1.png'
}
```

Input can also have list of urls:

```python
default_inputs = {'input_name': [
  'http://example.com/1.png', 
  'http://example.com/2.png'
]}
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

# Logging

Valohai platform parses JSON logs as metadata.

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

# Full example

## Preprocess step for resizing image files

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
        "https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg",
        "https://homepages.cae.wisc.edu/~ece533/images/airplane.png",
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
                out_path=valohai.outputs('images').path(filename),
                width=valohai.parameters('width').value,
                height=valohai.parameters('height').value,
                logger=logger
            )
```
