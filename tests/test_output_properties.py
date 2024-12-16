"""Test handling the execution output metadata properties."""

import json
import logging
import random
import string
import time
from pathlib import Path

import pytest  # type: ignore

import valohai

logger = logging.getLogger(__name__)


def test_create_properties(tmp_metadata_file):
    """Test creating a properties file."""
    with valohai.output_properties() as properties:
        properties.properties_file = tmp_metadata_file

        # file in the outputs directory
        properties.add(file="file.txt", properties={"foo": "bar"})
        # file in a subdirectory
        properties.add(file="path/to/file.txt", properties={"baz": "qux"})
        # file can also be a Path object
        properties.add(
            file=Path("path/to/another/file.txt"), properties={"quux": "quuz"}
        )

        # check that the properties are set
        assert properties._files_properties.get("file.txt") == {"foo": "bar"}
        assert properties._files_properties.get("path/to/file.txt") == {"baz": "qux"}
        assert properties._files_properties.get("path/to/another/file.txt") == {
            "quux": "quuz"
        }

    # check that the properties are saved to the file
    saved_properties = read_json_lines(tmp_metadata_file)
    assert saved_properties.get("file.txt") == {"foo": "bar"}
    assert saved_properties.get("path/to/file.txt") == {"baz": "qux"}
    assert saved_properties.get("path/to/another/file.txt") == {"quux": "quuz"}


def test_add_to_existing_properties(tmp_metadata_file):
    """You can add new properties to a file that already has properties."""
    with valohai.output_properties() as properties:
        properties.properties_file = tmp_metadata_file

        properties.add(
            file="file.txt", properties={"foo": "bar", "baz": "will be overwritten"}
        )
        properties.add(
            file="file.txt", properties={"baz": "can overwrite existing value"}
        )
        properties.add(file="file.txt", properties={"corge": "can add new properties"})

    assert properties._files_properties.get("file.txt") == {
        "foo": "bar",
        "baz": "can overwrite existing value",
        "corge": "can add new properties",
    }


def test_add_files_to_dataset(tmp_path, random_string):
    """Add files to a new dataset version."""
    with valohai.output_properties() as properties:
        properties.properties_file = tmp_path / "valohai.metadata.jsonl"
        dataset_version_1 = properties.dataset_version_uri("dataset-1", "version")
        dataset_version_2 = properties.dataset_version_uri(
            "dataset-2", "another-version"
        )

        properties.add(
            file="properties_and_dataset_version.txt",
            properties={"foo": "bar"},
        )
        properties.add_to_dataset(
            file="properties_and_dataset_version.txt",
            dataset_version=dataset_version_1,
        )

        properties.add_to_dataset(
            file="only_dataset_version.txt",
            dataset_version=dataset_version_1,
        )

        properties.add(
            file="properties_and_two_datasets.txt",
            properties={
                "name": "test with properties and datasets",
                "random": random_string,
            },
        )
        properties.add_to_dataset(
            file="properties_and_two_datasets.txt",
            dataset_version=dataset_version_1,
        )
        properties.add_to_dataset(
            file="properties_and_two_datasets.txt",
            dataset_version=dataset_version_2,
        )

    assert properties._files_properties.get("properties_and_dataset_version.txt") == {
        "foo": "bar",
        "valohai.dataset-versions": ["dataset://dataset-1/version"],
    }, "Should add both properties and dataset version metadata"
    assert properties._files_properties.get("only_dataset_version.txt") == {
        "valohai.dataset-versions": ["dataset://dataset-1/version"]
    }, "Should add dataset version metadata without any properties"
    assert properties._files_properties.get("properties_and_two_datasets.txt") == {
        "name": "test with properties and datasets",
        "random": random_string,
        "valohai.dataset-versions": list(
            {
                "dataset://dataset-1/version",
                "dataset://dataset-2/another-version",
            }
        ),
    }, "Should add both properties and multiple dataset versions"


def test_large_number_of_files(tmp_metadata_file, random_string):
    """Test handling metadata for a very large number of outputs."""
    test_properties = {
        "foo": "bar",
        "baz": "this is a longer metadata string",
        "random": random_string,
        "number": 42,
    }
    nr_of_files = 100_000

    start = time.perf_counter()
    with valohai.output_properties() as properties:
        properties.properties_file = tmp_metadata_file
        dataset_version = properties.dataset_version_uri("test-dataset", "v1")

        for i in range(nr_of_files):
            properties.add(
                file=f"file_{i}.txt",
                properties=test_properties,
            )
            properties.add_to_dataset(
                file=f"file_{i}.txt",
                dataset_version=dataset_version,
            )
    end = time.perf_counter()

    assert (
        len(properties.properties_file.read_bytes().splitlines()) == nr_of_files
    ), "Should have written all entries to file"

    elapsed_time = end - start
    logger.debug(f"File entries: {nr_of_files:,}; elapsed time: {elapsed_time:.2f} s")
    assert (
        elapsed_time < 2.0
    ), "Should actually be under 1 second; something has changed considerably"


def read_json_lines(properties_file: Path):
    """
    Read a saved properties JSON lines file back into a dictionary.
    Dictionary format: {file_path: metadata, ...}
    """
    return {
        entry["file"]: entry["metadata"]
        for entry in (
            json.loads(line) for line in properties_file.read_bytes().splitlines()
        )
    }


@pytest.fixture
def tmp_metadata_file(tmp_path) -> Path:
    return tmp_path / "valohai.metadata.jsonl"


@pytest.fixture
def random_string() -> str:
    length = 1000
    keyspace: str = string.ascii_letters + string.digits
    return "".join(random.choice(keyspace) for _ in range(length))
