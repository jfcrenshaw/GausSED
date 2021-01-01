import numpy as np
from numbers import Number
import os


class Bandpass:
    """
    Class to handle instrument filter bandpass.

    Parameters
    ----------
    filename : str
        Location and name of file where bandpass is stored
        Must be a file with two columns: wavelength and bandpass throughput
    name : str
        Name of bandpass
    dlambda : float
        Width of wavelength grid on which bandpass will be sampled
        Default = 10

    Attributes
    ----------
    wavelen : numpy.ndarray
        Bandpass wavelength grid
        Range determined from the wavelengths in the provided file
        Resampled on wavelength grid with width dlambda
    T : numpy.ndarray
        Bandpass throughput from the provided file
    R : numpy.ndarray
        Bandpass normalized response function, defined
        :math:`R = \lambda T(\lambda) / \int(\lambda T(\lambda) d\lambda)`
    mean_wavelen: float
        Mean wavelength of the bandpass, defined
        :math:`\lambda_{\mathrm{mean}} = `\int \lambda R(\lambda) d\lambda`
    eff_width: float
        Effective width of the bandpass, defined
        :math:`W_{\mathrm{eff}} = \max{[R(\lambda)]}^{-1}`

    Methods
    -------
    flux(seds)
        Return flux through the bandpass for the provided sed(s)
        NEED TO IMPLEMENT

    """

    def __init__(self, filename: str, name: str = None, dlambda: float = 10):
        # validate inputs
        if not isinstance(filename, str):
            raise ValueError("filename should be a string")
        if not os.path.isfile(filename):
            raise OSError(f"Cannot find bandpass file '{filename}'")
        if name is not None and not isinstance(name, str):
            raise ValueError("name should be a string")
        if not isinstance(dlambda, Number):
            raise ValueError("dlambda should be a number")
        elif dlambda <= 0:
            raise ValueError("dlambda must be a positive number")

        # load system response from file
        wavelen, T = np.loadtxt(filename, unpack=True)

        # resample wavelen and calculate R
        self.wavelen = np.arange(min(wavelen), max(wavelen) + dlambda, dlambda)
        self.T = np.interp(self.wavelen, wavelen, T, left=0, right=0)
        self.R = self.T * self.wavelen
        self.R /= (self.R * dlambda).sum()
        del wavelen, T

        # calculate mean wavelength and effective width
        self.mean_wavelen = (self.wavelen * self.R * dlambda).sum()
        self.eff_width = (self.R * dlambda).sum() / max(self.R)

        # set the name
        name = filename.split("/")[-1].split(".")[0] if name is None else name
        self.name = name

    def flux(self, seds) -> np.ndarray:
        """
        Return flux through the bandpass for the provided sed(s)

        Parameters
        ----------
        seds : SED or iterable of SEDs

        Returns
        -------
        np.ndarray
            Array of fluxes
            If only a single SED is given, array is squeezed
        """
        raise NotImplementedError

    def __repr__(self):
        return f"Bandpass({self.name})"
