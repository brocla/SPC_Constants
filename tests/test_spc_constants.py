# tests/test_spc_constants.py

import pytest
import math
from spc_constants import SPC_Constants
   

REFERENCE_VALUES = {
    'd2': {
        2: 1.128379,
        3: 1.692569,
        4: 2.058751,
        5: 2.325929,
        6: 2.534413,
        7: 2.704357,
        8: 2.847201,
        9: 2.970026,
       10: 3.077505,
    },
    'd3': {
        2: 0.852502,
        3: 0.888368,
        4: 0.879808,
        5: 0.864082,
        6: 0.848040,
        7: 0.833205,
        8: 0.819831,
        9: 0.807834,
       10: 0.797051,
    },
    'c4': {
        2:  0.797885,
        3:  0.886227,
        4:  0.921318,
        5:  0.939986,
        6:  0.951533,
        7:  0.959369,
        8:  0.965030,
        9:  0.969311,
        10: 0.972659,
    },

    'c5': {
         2: 0.602810,
         3: 0.463251,
         4: 0.388811,
         5: 0.341214,
         6: 0.307547,
         7: 0.282155,
         8: 0.262138,
         9: 0.245839,
        10: 0.232237,
    }
}

@pytest.mark.parametrize("n,expected", [
    (2, 1.128),
    (3, 1.693),
    (4, 2.059),
    (5, 2.326),
    (6, 2.534),
    (7, 2.704),
    (8, 2.847),
    (9, 2.970),
    (10, 3.078)
])
@pytest.mark.table_check
def test_d2_constant(n, expected):
    const = SPC_Constants(n)
    computed = const.d2
    assert computed == pytest.approx(expected, rel=1e-3), f"d2_constant({n}) should be approximately {expected}, got {computed}"

@pytest.mark.parametrize("n,expected", [
    (2, 0.853),
    (10, 0.797)
])
@pytest.mark.table_check
def test_d3_constant(n, expected):
    const = SPC_Constants(n)
    computed = const.d3
    assert computed == pytest.approx(expected, rel=1e-3), f"d3_constant({n}) should be approximately {expected}, got {computed}"

@pytest.mark.parametrize("n,expected", [
    (2,  0.797885),
    (3,  0.886227),
    (4,  0.921318),
    (5,  0.939986),
    (6,  0.951533),
    (7,  0.959369),
    (8,  0.965030),
    (9,  0.969311),
    (10, 0.972659),
])
@pytest.mark.table_check
def test_c4_constant(n, expected):
    const = SPC_Constants(n)
    computed = const.c4
    assert computed == pytest.approx(expected, rel=1e-4), f"c4_constant({n}) should be approximately {expected}, got {computed}"

@pytest.mark.parametrize("n,expected", [
    ( 2, 0.602810),
    ( 3, 0.463251),
    ( 4, 0.388811),
    ( 5, 0.341214),
    ( 6, 0.307547),
    ( 7, 0.282155),
    ( 8, 0.262138),
    ( 9, 0.245839),
    (10, 0.232237),
])
@pytest.mark.table_check
def test_c5_constant(n, expected):
    const = SPC_Constants(n)
    computed = const.c5
    assert computed == pytest.approx(expected, rel=1e-3), f"c5_constant({n}) should be approximately {expected}, got {computed}"

def test_constants_invalid_n():
    with pytest.raises(ValueError):
        const = SPC_Constants(1)

def test_non_positive_z_invalid():
    with pytest.raises(ValueError):
        SPC_Constants(2, -1)
    with pytest.raises(ValueError):
        SPC_Constants(2, z=0)

def test_read_only():
    const = SPC_Constants(2)
    with pytest.raises(AttributeError):
        const.n = 42
    with pytest.raises(AttributeError):
        const.z = 42
    with pytest.raises(AttributeError):
        const.c4 = 42
    with pytest.raises(AttributeError):
        const.c5 = 42
    with pytest.raises(AttributeError):
        const.d2 = 42
    with pytest.raises(AttributeError):
        const.d3 = 42
    with pytest.raises(AttributeError):
        const.A  = 42
    with pytest.raises(AttributeError):
        const.A2 = 42
    with pytest.raises(AttributeError):
        const.A3 = 42
    with pytest.raises(AttributeError):        
        const.B3 = 42
    with pytest.raises(AttributeError):        
        const.B4 = 42
    with pytest.raises(AttributeError):          
        const.B5 = 42
    with pytest.raises(AttributeError):
        const.B6 = 42
    with pytest.raises(AttributeError):
        const.D1 = 42
    with pytest.raises(AttributeError):
        const.D2 = 42
    with pytest.raises(AttributeError):
        const.D3 = 42
    with pytest.raises(AttributeError):
        const.D4 = 42
    with pytest.raises(AttributeError):
        const.E2 = 42
    with pytest.raises(AttributeError):
        const.E3 = 42


def test_A_constant():
    # A = z / sqrt(n)
    for z in [2.5, 3.0, 3.5]:
        for n in [2, 3, 4, 5, 10]:
            expected = z / math.sqrt(n)
            const = SPC_Constants(n, z=z)
            computed = const.A
            assert computed == pytest.approx(expected, rel=1e-8), f"A_constant({n}) with z={z} should be approximately {expected}, got {computed}"

def test_A2_constant():
    # A2 = z / (d2 * sqrt(n))
    for z in [2.5, 3.0, 3.5]:
        for n in [2, 3, 4, 5, 10]:
            const = SPC_Constants(n, z=z)
            expected = z / (const.d2 * math.sqrt(n))
            computed = const.A2
            assert computed == pytest.approx(expected, rel=1e-8), f"A2_constant({n}) with z={z} should be approximately {expected}, got {computed}"

def test_A3_constant():
    # A3 = z / (c4 * sqrt(n))
    for z in [2.5, 3.0, 3.5]:
        for n in [2, 3, 4, 5, 10]:
            const = SPC_Constants(n, z=z)
            computed = const.A3
            expected = z / (const.c4 * math.sqrt(n))
            assert computed == pytest.approx(expected, rel=1e-8), f"A3_constant({n}) with z={z} should be approximately {expected}, got {computed}"

@pytest.mark.parametrize("n,z,expected_lower", [
    (2, 3.0, max(0, 1 - (3.0 / REFERENCE_VALUES['c4'][2]) * math.sqrt(1 - REFERENCE_VALUES['c4'][2]**2))),
    (3, 3.0, max(0, 1 - (3.0 / REFERENCE_VALUES['c4'][3]) * math.sqrt(1 - REFERENCE_VALUES['c4'][3]**2))),
    (9, 3.0, max(0, 1 - (3.0 / REFERENCE_VALUES['c4'][9]) * math.sqrt(1 - REFERENCE_VALUES['c4'][9]**2))),
    (10, 3.0, max(0, 1 - (3.0 / REFERENCE_VALUES['c4'][10]) * math.sqrt(1 - REFERENCE_VALUES['c4'][10]**2))),
    (10, 8.0, max(0, 1 - (8.0 / REFERENCE_VALUES['c4'][10]) * math.sqrt(1 - REFERENCE_VALUES['c4'][10]**2))),

])
def test_B3_constant(n, z, expected_lower):
    const = SPC_Constants(n, z=z)
    computed = const.B3
    assert computed == pytest.approx(expected_lower, rel=1e-4), f"B3_constant({n}, z={z}) should be approximately {expected_lower}, got {computed}"

@pytest.mark.parametrize("n,z,expected_upper", [
    (2, 3.0, 1 + (3.0 / REFERENCE_VALUES['c4'][2]) * math.sqrt(1 - REFERENCE_VALUES['c4'][2]**2)),
    (3, 3.0, 1 + (3.0 / REFERENCE_VALUES['c4'][3]) * math.sqrt(1 - REFERENCE_VALUES['c4'][3]**2)),
    (9, 2.0, 1 + (2.0 / REFERENCE_VALUES['c4'][9]) * math.sqrt(1 - REFERENCE_VALUES['c4'][9]**2)),
])
def test_B4_constant(n, z, expected_upper):
    const = SPC_Constants(n, z=z)
    computed = const.B4
    assert computed == pytest.approx(expected_upper, rel=1e-5), f"B4_constant({n}, z={z}) should be approximately {expected_upper}, got {computed}"

@pytest.mark.parametrize("n,z,expected_lower", [
    (2, 3.0, REFERENCE_VALUES['c4'][2] - 3.0 * math.sqrt(1 - REFERENCE_VALUES['c4'][2]**2)),
    (3, 3.0, REFERENCE_VALUES['c4'][3] - 3.0 * math.sqrt(1 - REFERENCE_VALUES['c4'][3]**2)),
    (9, 4.0, REFERENCE_VALUES['c4'][9] - 4.0 * math.sqrt(1 - REFERENCE_VALUES['c4'][9]**2)),
])
def test_B5_constant(n, z, expected_lower):
    const = SPC_Constants(n, z=z)
    computed = const.B5
    expected = max(0, expected_lower)
    assert computed == pytest.approx(expected, rel=1e-5), f"B5_constant({n}, z={z}) should be approximately {expected}, got {computed}"

@pytest.mark.parametrize("n,z,expected_upper", [
    (2, 3.0, REFERENCE_VALUES['c4'][2] + 3.0 * math.sqrt(1 - REFERENCE_VALUES['c4'][2]**2)),
    (3, 3.0, REFERENCE_VALUES['c4'][3] + 3.0 * math.sqrt(1 - REFERENCE_VALUES['c4'][3]**2)),
])
def test_B6_constant(n, z, expected_upper):
    const = SPC_Constants(n, z=z)
    computed = const.B6
    expected = REFERENCE_VALUES['c4'][n] + z * math.sqrt(1 - REFERENCE_VALUES['c4'][n]**2)
    assert computed == pytest.approx(expected_upper, rel=1e-5), f"B6_constant({n}, z={z}) should be approximately {expected}, got {computed}"

@pytest.mark.parametrize("n,z,expected_lower", [
    (2, 3.0, max(0, REFERENCE_VALUES['d2'][2] - 3.0 * REFERENCE_VALUES['d3'][2])),
    (3, 3.0, max(0, REFERENCE_VALUES['d2'][3] - 3.0 * REFERENCE_VALUES['d3'][3])),
    (9, 2.0, max(0, REFERENCE_VALUES['d2'][9] - 2.0 * REFERENCE_VALUES['d3'][9])),
])
def test_D1_constant(n, z, expected_lower):
    const = SPC_Constants(n, z=z)
    computed = const.D1
    expected = max(0, const.d2 - z * const.d3)
    assert computed == pytest.approx(expected, rel=1e-5), f"D1_constant({n}, z={z}) should be approximately {expected}, got {computed}"

@pytest.mark.parametrize("n,z,expected_upper", [
    (2, 3.0, REFERENCE_VALUES['d2'][2] + 3.0 * REFERENCE_VALUES['d3'][2]),
    (3, 3.0, REFERENCE_VALUES['d2'][3] + 3.0 * REFERENCE_VALUES['d3'][3]),
])
def test_D2_constant(n, z, expected_upper):
    const = SPC_Constants(n, z=z)
    computed = const.D2
    expected = const.d2 + z * const.d3
    assert computed == pytest.approx(expected, rel=1e-8), f"D2_constant({n}, z={z}) should be approximately {expected}, got {computed}"

@pytest.mark.parametrize("n,z,expected_lower", [
    (2, 3.0, max(0, 1 - 3.0 * REFERENCE_VALUES['d3'][2] / REFERENCE_VALUES['d2'][2])),
    (3, 3.0, max(0, 1 - 3.0 * REFERENCE_VALUES['d3'][3] / REFERENCE_VALUES['d2'][3])),
    (6, 3.0, max(0, 1 - 3.0 * REFERENCE_VALUES['d3'][6] / REFERENCE_VALUES['d2'][6])),
    (7, 3.0, max(0, 1 - 3.0 * REFERENCE_VALUES['d3'][7] / REFERENCE_VALUES['d2'][7])),
    (8, 3.0, max(0, 1 - 3.0 * REFERENCE_VALUES['d3'][8] / REFERENCE_VALUES['d2'][8])),
    (9, 3.0, max(0, 1 - 3.0 * REFERENCE_VALUES['d3'][9] / REFERENCE_VALUES['d2'][9])),
    (9, 4.0, max(0, 1 - 4.0 * REFERENCE_VALUES['d3'][9] / REFERENCE_VALUES['d2'][9])),
    (9, 2.0, max(0, 1 - 2.0 * REFERENCE_VALUES['d3'][9] / REFERENCE_VALUES['d2'][9])),
])
def test_D3_constant(n, z, expected_lower):
    const = SPC_Constants(n, z=z)
    computed = const.D3
    expected = max(0, 1 - z * const.d3 / const.d2)
    assert computed == pytest.approx(expected, rel=1e-8), f"D3_constant({n}, z={z}) should be approximately {expected}, got {computed}"

@pytest.mark.parametrize("n,z,expected_upper", [
    (2, 3.0, 1 + 3.0 * REFERENCE_VALUES['d3'][2] / REFERENCE_VALUES['d2'][2]),
    (3, 3.0, 1 + 3.0 * REFERENCE_VALUES['d3'][3] / REFERENCE_VALUES['d2'][3]),
])
def test_D4_constant(n, z, expected_upper):
    const = SPC_Constants(n, z=z)
    computed = const.D4
    expected = 1 + z * const.d3 / const.d2
    assert computed == pytest.approx(expected, rel=1e-8), f"D4_constant({n}, z={z}) should be approximately {expected}, got {computed}"

def test_E2_constant():
    # E2 = z / d2
    for z in [2.5, 3.0, 3.5]:
        for n in [2, 3, 4, 5, 10]:
            const = SPC_Constants(n, z=z)
            computed = const.E2
            d2 = const.d2
            expected = z / d2
            assert computed == pytest.approx(expected, rel=1e-6), f"E2_constant({n}, z={z}) should be approximately {expected}, got {computed}"

def test_E3_constant():
    # E3 = z / c4
    for z in [2.5, 3.0, 3.5]:
        for n in [2, 3, 4, 5, 10]:
            const = SPC_Constants(n, z=z)
            computed = const.E3
            c4 = const.c4
            expected = z / c4
            assert computed == pytest.approx(expected, rel=1e-6), f"E3_constant({n}, z={z}) should be approximately {expected}, got {computed}"

### INVARIANTS ###
#
# For several pairs of constants, their sums and differences are invariants. This is used to test the code for consistency.
# The invariants do not hold if the constant was truncated to have a value of zero. This is checked, and skipped. 

@pytest.mark.invariant
def test_D1_D2_invariant_plus():
    for z in [ 1.5, 2, 3, 4, 4.5]:
        for n in [2, 5, 7, 10, 15, 25]:
            const = SPC_Constants(n, z=z)
            expected = 2
            D1 = const.D1
            D2 = const.D2
            if D1:
                computed = (D1 + D2)/const.d2
                assert computed == pytest.approx(expected, rel=1e-8), f"D1,D2 invariant. For n={n}, z={z} expected {expected}, got {computed}"

@pytest.mark.invariant
def test_D1_D2_invariant_minus():
    for z in [ 1.5, 2, 3, 4, 4.5]:
        for n in [2, 5, 7, 10, 15, 25]:
            const = SPC_Constants(n, z=z)
            expected = 2
            D1 = const.D1
            D2 = const.D2
            if D1:
                computed = (D2 - D1)/z/const.d3
                assert computed == pytest.approx(expected, rel=1e-8), f"D1,D2 invariant. For n={n}, z={z} expected {expected}, got {computed}"

@pytest.mark.invariant
def test_D3_D4_invariant_plus():
    for z in [ 1.5, 2, 3, 4, 4.5]:
        for n in [2, 5, 7, 10, 15, 25]:
            const = SPC_Constants(n, z=z)
            expected = 2.0
            D3 = const.D3
            D4 = const.D4
            if D3:
                computed = D3 + D4
                assert computed == pytest.approx(expected, rel=1e-8), f"D3,D4 invariant. For n={n}, z={z} expected {expected}, got {computed}"

@pytest.mark.invariant
def test_D3_D4_invariant_minus():
    for z in [ 1.5, 2, 3, 4, 4.5]:
        for n in [7, 10, 15, 25]:
            const = SPC_Constants(n, z=z)
            expected = 2
            D3 = const.D3
            D4 = const.D4
            if D3:
                computed = (D4 - D3)*const.d2/const.d3/z
                assert computed == pytest.approx(expected, rel=1e-8), f"D3,D4 invariant. For n={n}, z={z} expected {expected}, got {computed}"

@pytest.mark.invariant
def test_B3_B4_invariant_plus():
    for z in [ 1.5, 2, 3, 4, 4.5]:
        for n in [6, 7, 10, 15, 25]:
            const = SPC_Constants(n, z=z)
            expected = 2
            B3 = const.B3
            B4 = const.B4
            if B3:
                computed = B3 + B4
                assert computed == pytest.approx(expected, rel=1e-8), f"B3,B4 invariant. For n={n}, z={z} expected {expected}, got {computed}"

@pytest.mark.invariant
def test_B3_B4_invariant_minus():
    for z in [2.5, 3.0, 3.5]:
        for n in [6, 7, 10, 13, 15, 17, 23, 25, 50, 100]:
            const = SPC_Constants(n, z=z)
            expected = 2
            B3 = const.B3
            B4 = const.B4

            # invariant test does not work if B3 was set to zero. Skip
            if B3:
                computed = (B4 - B3) * const.c4 / const.c5 / z
                assert computed == pytest.approx(expected, rel=1e-8), f"B3,B4 invariant. For n={n}, z={z} expected {expected}, got {computed}"

@pytest.mark.invariant
def test_B5_B6_invariant_plus():
    for z in [ 1.5, 2, 3, 3.1, 4, 4.5]:
        for n in [6, 7, 10, 15, 25]:
            const = SPC_Constants(n, z=z)
            expected = 2
            B5 = const.B5
            B6 = const.B6
            if B5:
                computed = (const.B5 + const.B6)/const.c4
                assert computed == pytest.approx(expected, rel=1e-8), f"B5,B6 invariant. For n={n}, z={z} expected {expected}, got {computed}"

@pytest.mark.invariant
def test_B5_B6_invariant_minus():
    for z in [ 1.5, 2, 3, 3.1, 4, 4.5]:
        for n in [6, 7, 10, 15, 25]:
            const = SPC_Constants(n, z=z)
            expected = 2
            B5 = const.B5
            B6 = const.B6
            if B5:
                computed = (const.B6 - const.B5)/const.c5/z
                assert computed == pytest.approx(expected, rel=1e-8), f"B5,B6 invariant. For n={n}, z={z} expected {expected}, got {computed}"