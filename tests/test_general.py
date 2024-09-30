import pymetatree


def test_version():
    version = pymetatree.__version__

    assert version is not None
