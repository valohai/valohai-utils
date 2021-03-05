import valohai

params = {
    "seq_length": 14,
    "num_epochs": 200,
}

def prepare(a, b):
    print(f"this is fake method {a} {b}")
    
valohai.prepare(step="mystep", default_parameters=params, image="valohai/keras")
