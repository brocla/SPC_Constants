"""
Calculate SPC constants from scratch. No values taken from a table.

The advantages are:
- more decimal places than commonly available in tables
- available for any value of n>=2
- The +/- limits are adjustable to values other than 3 sigma.
- some comfort in knowing whence come these constants.


USAGE
>>> from spc_constants import SPC_Constants
>>> const = SPC_Constants(2, z=3)
>>> const.A2
np.float64(1.8799712059732498)
>>> str(const)
'n=2 z=3 A=2.1213203435596424 A2=1.8799712059732498 A3=2.6586807763582736 c4=0.7978845608028655 B3=0 B4=3.2665319192886 B5=0 B6=2.6063153857701256 d2=1.1283791670955128 d3=0.8525024664464096 D1=0 D2=3.6858865664347413 D3=0 D4=3.266531919339083'


GLOSSARY
Constant   Description
--------   -----------------------------------------------------------------
c4	       unbiased estimator of the population standard deviation
c5         unbiased estimator for the standard deviation of the moving range
d2	       unbiased estimator of the sample standard deviation
d3	       unbiased estimator of the standard deviation of the range
A          X̄ limits based on standard sigma (rare). Pairs with <D1 and D2> or <B5 and B6>.
A2	       X̄ limits based on calculated R-bar. Pairs with D3 and D4. (Common)
A3	       X̄ limits based on calculated s-bar. Pairs with B3 and B4.
B3	       LCL on s chart, given s-bar
B4	       UCL on s chart, given s-bar
B5         LCL on s chart, given standard sigma 
B6         UCL on s chart, given standard sigma
D1	       LCL on R chart when Standards given for sigma (rare). 
D2	       UCL on R chart when Standards given for sigma (rare)
D3	       LCL on R Chart. No standard given. Data used to estimate sigma. (common)
D4	       UCL on R Chart. No standard given. Data used to estimate sigma. (common)
E2	       I-MR Chart
E3         I-Ms Chart

where `n` is the sample size,
and `z` is the multiplier of standard error. The default is a 3 sigma limit.

Note: All the constants are read-only. 
      And the arguments, n and z are read-only.

Note: `n` is traditionally an integer because sample size is a counting number, 
but the equations don't require it, so float values of `n` are allowed.
I don't know what an application might be.

References:
- "Statistical Quality Control" by Montgomery. See table 6.9
- SAS documentation. https://support.sas.com/en/documentation.html

The calculation of d2 and d3 is a bit slow
as it involves integration from -infinity to infinity, so
a cache was added to speed up their repeated use.
"""

import numpy as np
from scipy.stats import norm
from scipy.integrate import quad
from scipy.special import gammaln
from functools import wraps, cached_property, cache
import dbm


def persistent_cache(db_path):
    """
    A decorator that caches method results using a persistent dbm-based cache.
    """
    db = dbm.open(db_path, "c")

    def _encode(item):
        """Encode as a string."""
        return f"{item}"

    def _decode(_bytes):
        """Decode dbm bytes back to a float."""
        return float(_bytes.decode())

    def decorator(func):
        @wraps(func)
        def wrapper(self):
            key = self.n
            encoded_key = _encode(key)

            if encoded_key in db:
                # cache hit
                return _decode(db[encoded_key])

            value = func(self)

            # Cache the result
            db[encoded_key] = _encode(value)
            return value

        return wrapper

    return decorator


class SPC_Constants:
    def __init__(self, n, z=3.0):
        if n < 2:
            raise ValueError(
                f"Sample size n must be greater than or equal to 2, not {n}"
            )
        self._sample_size = n

        if z <= 0:
            raise ValueError(f"z argument must be positive, not {z}")
        self._sigma_limit = z

    @property
    def n(self):
        return self._sample_size

    @property
    def z(self):
        return self._sigma_limit

    def __repr__(self):
        return f"{self.__class__.__name__}({self.n}, z={self.z})"

    def __str__(self):
        return (
            f"n={self.n} z={self.z} A={self.A:.8f} A2={self.A2:.8f} A3={self.A3:.8f} "
            f"c4={self.c4:.8f} B3={self.B3:.8f} B4={self.B4:.8f} B5={self.B5:.8f} "
            f"B6={self.B6:.8f} d2={self.d2:.8f} d3={self.d3:.8f} D1={self.D1:.8f} "
            f"D2={self.D2:.8f} D3={self.D3:.8f} D4={self.D4:.8f}"
        )

    @property
    @persistent_cache(".cache.d2.dbm")
    def d2(self):
        r"""
        Math equation for d2 (written in LaTex).
        d_2 = \int_{-\infty}^{\infty} [ 1- (1-\Phi(x))^n -(\Phi(x))^n ] \; dx
            where \Phi(\cdot) is the standard normal cumulative distribution function.
        Refer to Tippett (1925) ON THE EXTREME INDIVIDUALS AND THE RANGE OF SAMPLES TAKEN FROM A NORMAL POPULATION.
        see equation (3)

        https://documentation.sas.com/doc/en/pgmsascdc/9.4_3.5/qcug/qcug_functions_sect027.htm
        """
        n = self.n

        def integrand(x):
            return 1 - (1 - norm.cdf(x)) ** n - (norm.cdf(x)) ** n

        result, _ = quad(integrand, -np.inf, np.inf)
        return result

    @property
    @persistent_cache(".cache.d3.dbm")
    def d3(self):
        r"""
        Double integral Math equation for d3 (written in LaTex).
        The value d3 can be expressed as
        d_3 = \sqrt{ 2 \int_{-\infty}^{\infty} \int_{-\infty}^y f(x,y) \,dx\,dy - d_2^2 }
        Tippett (1925) see equation (10)

        Reference: https://documentation.sas.com/doc/en/pgmsascdc/9.4_3.5/qcug/qcug_functions_sect031.htm
        """

        # Perform the outer integration over y from -∞ to ∞
        outer_integral_value, _ = quad(
            lambda y: self.inner_integral(y), -np.inf, np.inf
        )

        result = np.sqrt(2 * outer_integral_value - self.d2**2)
        return result

    def f(self, x, y):
        r"""
        Math equation used in calculating d3
        f(x,y) = 1 - (\Phi(y))^n - (1-\Phi(x))^n + (\Phi(y) - \Phi(x))^n
            where \Phi(\cdot) is the standard normal cumulative distribution function and d2 is the expected range. Refer to Tippett (1925).
        """
        n = self.n
        Phi_x = norm.cdf(x)
        Phi_y = norm.cdf(y)
        return 1 - Phi_y**n - (1 - Phi_x) ** n + (Phi_y - Phi_x) ** n

    def inner_integral(self, y):
        """
        Perform the inner integration of f() over x from -∞ for a given y.
        """
        result, _ = quad(lambda x: self.f(x, y), -np.inf, y)
        return result

    @property
    @persistent_cache(".cache.c4.dbm")
    def c4(self):
        r"""
        Math equation for c4 (written in LaTex).
        Calculate the c4 constant for a sample of size n.
        \[ c_4 = \frac{\Gamma (\frac{n}{2}) \sqrt{2/(n-1) } }{\Gamma (\frac{n-1}{2}) } \]

        Reference: https://documentation.sas.com/doc/en/pgmsascdc/9.4_3.5/qcug/qcug_functions_sect019.htm
        """
        n = self.n

        # to avoid overflow, use gammaln() instead of gamma()
        # Compute the exponential of the difference of the logs
        gamma_ratio = np.exp(gammaln(n / 2) - gammaln((n - 1) / 2))
        return np.sqrt(2 / (n - 1)) * gamma_ratio

    @property
    @cache
    def c5(self):
        return np.sqrt(1 - self.c4**2)

    @property
    @cache
    def A(self):
        return self.z / np.sqrt(self.n)

    @property
    @cache
    def A2(self):
        return self.z / self.d2 / np.sqrt(self.n)

    @property
    @cache
    def A3(self):
        return self.z / self.c4 / np.sqrt(self.n)

    @property
    @cache
    def B3(self):
        return max(0, 1 - (self.z / self.c4) * np.sqrt(1 - self.c4**2))

    @property
    @cache
    def B4(self):
        return 1 + (self.z / self.c4) * np.sqrt(1 - self.c4**2)

    @property
    @cache
    def B5(self):
        return max(0, self.c4 - self.z * np.sqrt(1 - self.c4**2))

    @property
    @cache
    def B6(self):
        return self.c4 + self.z * np.sqrt(1 - self.c4**2)

    @property
    @cache
    def D1(self):
        return max(0, self.d2 - self.z * self.d3)

    @property
    @cache
    def D2(self):
        return self.d2 + self.z * self.d3

    @property
    @cache
    def D3(self):
        return max(0, 1 - self.z * self.d3 / self.d2)

    @property
    @cache
    def D4(self):
        return 1 + self.z * self.d3 / self.d2

    @property
    @cache
    def E2(self):
        return self.z / self.d2

    @property
    @cache
    def E3(self):
        return self.z / self.c4


if __name__ == "__main__":

    spc = SPC_Constants(2)
    print(repr(spc))
    print(spc)
    print()

    header = f"{'n':>6s}  {'z':<4s}  {'d2':8s}  {'d3':8s}  {'c4':8s}  {'A2':8s}  {'A3':8s}  {'B3':8s}  {'B4':8s}  {'D3':8s}  {'D4':8s}"
    print(header)
    for n in range(2, 16):
        spc = SPC_Constants(n)
        print(
            f"{n:6d}  {spc.z:4.2f}  {spc.d2:8f}  {spc.d3:8f}  {spc.c4:8f}  {spc.A2:8f}  {spc.A3:8f}  {spc.B3:8f}  {spc.B4:8f}  {spc.D3:8f}  {spc.D4:8f}"
        )
        if not n % 5:
            print()
