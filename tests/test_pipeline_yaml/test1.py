from valohai import Pipeline


def main(config) -> Pipeline:
    pipe = Pipeline(name="mypipeline", config=config)

    # Define nodes
    extract = pipe.execution("Batch feature extraction")
    train = pipe.task("Train model")
    evaluate = pipe.execution("Evaluate")

    # Configure training task node
    train.linear_parameter("learning_rate", min=0, max=1, step=0.1)

    # Configure pipeline
    extract.output("a*").to(train.input("aaa"))
    extract.output("a*").to(train.input("bbb"))
    train.output("*").to(evaluate.input("models"))

    return pipe
