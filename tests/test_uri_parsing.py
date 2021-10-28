from valohai.internals.utils import uri_to_filename


def test_uri_to_filename():
    assert uri_to_filename("https://joo.jee.com/asdf.txt") == "asdf.txt"
    assert uri_to_filename("https://joo.jee.com/herp/derp/asdf.txt") == "asdf.txt"
    assert (
        uri_to_filename("https://joo.jee.com/asdf.txt?xyz=foobar&zyx=1232345345")
        == "asdf.txt"
    )
