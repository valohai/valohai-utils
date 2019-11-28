import os
import valohai

params = {
  "param1": True,
  "param2": "asdf",
  "param3": 123,
  "param4": 0.0001,
}

inputs = {
  "input1": "asdf",
  "input2": ["yolol", "yalala"]
}

def prepare(a, b):
  print("this is fake method %s %s" % (a, b))


prepare("this should not be parsed")
valohai.utils.prepare("this should not be parsed either")
valohai.prepare("foobar", parameters=params, inputs=inputs)

