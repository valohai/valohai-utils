import io
import os
import tarfile
import zipfile

from valohai.internals.vfs import VFS, find_files


def _add_binary_to_tar(tf: tarfile.TarFile, name: str, content: bytes):
    tarinfo = tarfile.TarInfo(name)
    tarinfo.size = len(content)
    tf.addfile(tarinfo, io.BytesIO(content))


expected_contents = {
    "0quux.txt": b"Maista uudet maut",
    "dir1/1hello.txt": b"Hernekeitto",
    "dir1/2world.txt": b"Viina",
    "dir2/3spam.txt": b"Teline",
    "dir2/4eggs.txt": b"Johannes",
}


def make_vfs_files(tmpdir):
    zip_path = tmpdir.join("dir1").mkdir().join("example.zip")
    tar_path = tmpdir.join("dir2").mkdir().join("esimerkki.tar")
    raw_path = tmpdir.join("0quux.txt")

    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("1hello.txt", b"Hernekeitto")
        zf.writestr("2world.txt", b"Viina")

    with tarfile.TarFile.open(tar_path, "w") as tf:
        _add_binary_to_tar(tf, "3spam.txt", b"Teline")
        _add_binary_to_tar(tf, "4eggs.txt", b"Johannes")

    with open(raw_path, "w") as outf:
        outf.write("Maista uudet maut")


def test_vfs(tmpdir):
    make_vfs_files(tmpdir)
    names_that_should_be_cleaned = set()
    with VFS() as vfs:
        find_files(vfs, tmpdir, process_archives=True)
        direct_contents = {}
        open_read_contents = {}
        concrete_contents = {}
        for file in vfs.files:
            direct_contents[file.name] = file.read()

            with file.open() as of:
                open_read_contents[file.name] = of.read()

            with file.open() if not file.parent_file else file.open_concrete() as cf:
                # If os.open() can read the file, it's a concrete disk file
                fd = os.open(cf.name, os.R_OK)
                concrete_contents[file.name] = os.read(fd, 10_000)
                os.close(fd)
                if file.parent_file:
                    names_that_should_be_cleaned.add(cf.name)
        assert direct_contents == expected_contents
        assert concrete_contents == expected_contents
        assert open_read_contents == expected_contents

    assert not any(os.path.isfile(name) for name in names_that_should_be_cleaned)
