import os
import numpy as np
import pytest
from gaussed.bandpasses import Bandpass

filename = os.path.join(os.getcwd(), "tests/test_files/lsst-r.dat")


@pytest.mark.parametrize(
    "filename,name,dlambda,exception",
    [
        (1, "N", 1, ValueError("filename should be a string")),
        ("filename", "N", 1, OSError("Cannot find bandpass file 'filename'")),
        (filename, 1, 1, ValueError("name should be a string")),
        (filename, "N", "a", ValueError("dlambda should be a number")),
        (filename, "N", -2, ValueError("dlambda must be a positive number")),
    ],
)
def test_bandpass_bad_inputs(filename, name, dlambda, exception):
    try:
        Bandpass(filename, name=name, dlambda=dlambda)
    except (ValueError, OSError) as err:
        pass
        assert isinstance(err, type(exception))
        assert err.args == exception.args
    else:
        pytest.fail("Expected error but found none")


def test_bandpass_creation():
    # check auto-naming
    bandpass = Bandpass(filename)
    assert bandpass.name == "lsst-r"

    # check specified name and dlambda
    name = "Name"
    dlambda = 1
    bandpass = Bandpass(filename, dlambda=dlambda, name=name)
    assert bandpass.name == name
    diff = np.diff(bandpass.wavelen)
    assert all([d == dlambda for d in diff])

    # check that T and R are sensible
    assert isinstance(bandpass.T, np.ndarray)
    assert isinstance(bandpass.R, np.ndarray)
    Rsum = (bandpass.R * np.diff(bandpass.wavelen)[0]).sum()
    assert np.isclose(Rsum, 1)

    # check mean wavelen and eff width against known values
    r_mean_wavelen = 6257.74
    assert np.isclose(bandpass.mean_wavelen, r_mean_wavelen)
    r_eff_width = 1206.92
    assert np.isclose(bandpass.eff_width, r_eff_width)

    assert bandpass.__repr__() == "Bandpass(Name)"