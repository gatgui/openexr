#!/usr/bin/env python

from imath import *
from math import sqrt, pi, sin, cos
import math
import string, traceback, sys
import iex
import random



testList = []

# -----------------------------------------------------------------
# Test helper functions
# -----------------------------------------------------------------

ArrayBaseType = {}
ArrayBaseType[V2sArray] = V2s
ArrayBaseType[V2iArray] = V2i
ArrayBaseType[V2fArray] = V2f
ArrayBaseType[V2dArray] = V2d
ArrayBaseType[V3sArray] = V3s
ArrayBaseType[V3iArray] = V3i
ArrayBaseType[V3fArray] = V3f
ArrayBaseType[V3dArray] = V3d

VecBaseType = {}
VecBaseType[V2s] = int
VecBaseType[V2i] = int
VecBaseType[V2f] = float
VecBaseType[V2d] = float
VecBaseType[V3s] = int
VecBaseType[V3i] = int
VecBaseType[V3f] = float
VecBaseType[V3d] = float

eps = 10*FLT_EPS

def dimensions(baseType):
    if hasattr(baseType, 'dimensions'):
        return baseType.dimensions()
    else:
        return 1

def numNonZeroMaskEntries(mask):
    count = 0
    for i in range(0, len(mask)):
        if mask[i]:
            count += 1
    return count

def equalWithAbsErrorScalar(x1, x2, e):
    print("type x1({}) x2({}) e({}) -> scalar".format(type(x1), type(x2), type(e)))
    val = abs(x1 - x2)
    if val >= e:
        print ("Violation: val {} x1 {} x2 {} e {}".format(val, x1, x2, e))
    return abs(x1 - x2) < e

def make_range(start, end):
    num = end-start
    increment = 1
    if num < 0:
        num = -num;
        increment = -1

    retval = IntArray(num)
    val = start
    for i in range(0, num):
        retval[i] = val
        val += increment

    return retval

# We want to be able to use the test helper
# functions generically with different array types
# so we use hasattr to check if the arguments support
# [] operator.  This is sufficient to distinguish
# between vector and scalar types for our purposes here

def equalWithAbsError(x1, x2, e):
    if hasattr(x1, '__len__') and hasattr(x1, '__getitem__') and hasattr(x2, '__len__') and hasattr(x2, '__getitem__'):
        assert(len(x1) == len(x2))
        for i in range(0, len(x1)):
            if not equalWithAbsErrorScalar(x1[i], x2[i], e):
                return False
        return True
    elif isinstance(x1, int):
        return equalWithAbsErrorScalar(x1, int(x2), e)
    else:
        return equalWithAbsErrorScalar(x1, x2, e)

def equalWithRelErrorScalar(x1, x2, e):
    return abs(x1 - x2) <= e * abs(x1)

def equalWithRelError(x1, x2, e):
    if hasattr(x1, '__len__') and hasattr(x1, '__getitem__') and hasattr(x2, '__len__') and hasattr(x2, '__getitem__'):
        assert(len(x1) == len(x2))
        for i in range(0, len(x1)):
            if not equalWithRelErrorScalar(x1[i], x2[i], e):
                return False
        return True
    elif isinstance(x1, int):
        return equalWithRelErrorScalar(x1, int(x2), e)
    else:
        return equalWithRelErrorScalar(x1, x2, e)

def testVectorVectorArithmeticOps(f1, f2):
    f = f1 + f2
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(f[i] == f1[i] + f2[i])

    f = f1 - f2
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(f[i] == f1[i] - f2[i])

    f = f1 * f2
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(f[i] == f1[i] * f2[i])

    f = f1 / f2
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(equalWithAbsError(f[i], f1[i] / f2[i], eps))

    f = -f1
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(f[i] == -f1[i])

def testVectorScalarArithmeticOps(f1, v):
    f = f1 + v
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(f[i] == f1[i] + v)

    f = v + f1
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(f[i] == v + f1[i])

    f = f1 - v
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(f[i] == f1[i] - v)

    f = v - f1
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        if f[i] != v - f1[i]:
            assert(f[i] == v - f1[i])

    f = f1 * v
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(f[i] == f1[i] * v)

    f = v * f1
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(f[i] == v * f1[i])

    f = f1 / v
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(equalWithAbsError(f[i], f1[i] / v, eps))


def testVectorVectorInPlaceArithmeticOps(f1, f2):
    f = f1[:]
    f += f2

    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(f[i] == f1[i] + f2[i])

    f = f1[:]
    f -= f2
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(f[i] == f1[i] - f2[i])

    f = f1[:]
    f *= f2
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(f[i] == f1[i] * f2[i])

    f = f1[:]
    f /= f2
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(equalWithAbsError(f[i], f1[i] / f2[i], eps))

    f = f1[:]
    f = -f;
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(f[i] == -f1[i])

def testVectorScalarInPlaceArithmeticOps(f1, v):
    f = f1[:]
    f += v
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(f[i] == f1[i] + v)

    f = f1[:]
    f -= v
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(f[i] == f1[i] - v)

    f = f1[:]
    f *= v
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(f[i] == f1[i] * v)

    f = f1[:]
    f /= v
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(equalWithAbsError(f[i], f1[i] / v, eps))

def testPowFunctions(f1, f2):
    # vector-vector pow
    assert(len(f1) == len(f2))
    f = pow(f1, f2)
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(equalWithRelError(f[i], pow(f1[i], f2[i]), eps))

    f  = f1 ** f2
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(equalWithRelError(f[i], f1[i] ** f2[i], eps))

    # vector-scalar pow
    v = f2[0]
    f = pow(f1, v)
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(equalWithRelError(f[i], pow(f1[i], v), eps))

    # in-place vector-vector pow
    f = f1[:]
    f **= f2
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(equalWithRelError(f[i], pow(f1[i], f2[i]), eps))

    # in-place vector-scalar pow
    f = f1[:]
    v = f2[0]
    f **= v
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(equalWithRelError(f[i], f1[i] ** v, eps))

def testModOps(f1, f2):
    f = f1 % f2
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(f[i] == f1[i] % f2[i])

    v = f2[0]
    f = f1 % v
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(f[i] == f1[i] %v)

    f = f1[:]
    f %= f2
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(f[i] == f1[i] % f2[i])


def testVectorVectorComparisonOps(f1, f2):
    f = f1 == f2
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        if (f1[i] == f2[i]):
            assert(f[i] == 1)
        else:
            assert(f[i] == 0)

    f = f1 != f2
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        if (f1[i] != f2[i]):
            assert(f[i] == 1)
        else:
            assert(f[i] == 0)

def testVectorVectorInequalityOps(f1, f2):
    f = f1 < f2
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        if (f1[i] < f2[i]):
            assert(f[i] == 1)
        else:
            assert(f[i] == 0)

    f = f1 > f2
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        if (f1[i] > f2[i]):
            assert(f[i] == 1)
        else:
            assert(f[i] == 0)

    f = f1 <= f2
    for i in range(0, len(f)):
        if (f1[i] <= f2[i]):
            assert(f[i] == 1)
        else:
            assert(f[i] == 0)

    f = f1 >= f2
    for i in range(0, len(f)):
        if (f1[i] >= f2[i]):
            assert(f[i] == 1)
        else:
            assert(f[i] == 0)

def testVectorScalarComparisonOps(f1, v):
    f = f1 == v
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        if (f1[i] == v):
            assert(f[i] == 1)
        else:
            assert(f[i] == 0)

    f = v == f1
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        if (v == f1[i]):
            assert(f[i] == 1)
        else:
            assert(f[i] == 0)

    f = f1 != v
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        if (f1[i] != v):
            assert(f[i] == 1)
        else:
            assert(f[i] == 0)

    f = v != f1
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        if (v != f1[i]):
            assert(f[i] == 1)
        else:
            assert(f[i] == 0)

def testVectorScalarInequalityOps(f1, v):
    f = f1 < v
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        if (f1[i] < v):
            assert(f[i] == 1)
        else:
            assert(f[i] == 0)

    f = v < f1
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        if (v < f1[i]):
            assert(f[i] == 1)
        else:
            assert(f[i] == 0)

    f = f1 > v
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        if (f1[i] > v):
            assert(f[i] == 1)
        else:
            assert(f[i] == 0)

    f = v > f1
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        if (v > f1[i]):
            assert(f[i] == 1)
        else:
            assert(f[i] == 0)

    f = f1 <= v
    for i in range(0, len(f)):
        if (f1[i] <= v):
            assert(f[i] == 1)
        else:
            assert(f[i] == 0)

    f = v <= f1
    for i in range(0, len(f)):
        if (v <= f1[i]):
            assert(f[i] == 1)
        else:
            assert(f[i] == 0)

    f = f1 >= v
    for i in range(0, len(f)):
        if (f1[i] >= v):
            assert(f[i] == 1)
        else:
            assert(f[i] == 0)

    f = v >= f1
    for i in range(0, len(f)):
        if (v >= f1[i]):
            assert(f[i] == 1)
        else:
            assert(f[i] == 0)


# f1 and f2 are assumed to be unmasked arrays of the same length
def testVectorVectorMaskedInPlaceArithmeticOps(f1, f2, m):
    assert(len(f1) == len(f2))

    f = f1[:]
    f[m] += f2
    for i in range(0, len(m)):
        if m[i]: assert(f[i] == f1[i] + f2[i])

    f = f1[:]
    f[m] -= f2
    for i in range(0, len(m)):
        if m[i]: assert(f[i] == f1[i] - f2[i])

    f = f1[:]
    f[m] *= f2
    for i in range(0, len(m)):
        if m[i]: assert(f[i] == f1[i] * f2[i])

    f = f1[:]
    f[m] /= f2
    for i in range(0, len(m)):
        if m[i]: assert(equalWithAbsError(f[i], f1[i] / f2[i], eps))

    f = f1[:]
    f[m] = -f
    for i in range(0, len(m)):
        if m[i]: assert(f[i] == -f1[i])

# f1 is assumed to be an unmasked array and f2 is a masked
# or unmasked array such that len(f2) == len(f1[m])
def testVectorVectorMaskedInPlaceArithmeticOps2(f1, f2, m):
    assert(len(f1[m]) == len(f2))
    f = f1[:]
    f1m = f1[m]
    f[m] += f2
    fm = f[m]

    for i in range(0, len(fm)):
        assert(fm[i] == f1m[i] + f2[i])

    for i in range(0, len(m)):
        if m[i] == 0:
            assert(f[i] == f1[i])

    f = f1[:]
    f[m] -= f2
    fm = f[m]

    for i in range(0, len(fm)):
        assert(fm[i] == f1m[i] - f2[i])
    
    for i in range(0, len(m)):
        if m[i] == 0:
            assert(f[i] == f1[i])

    f = f1[:]
    f[m] *= f2
    fm = f[m]

    for i in range(0, len(fm)):
        assert(fm[i] == f1m[i] * f2[i])
    
    for i in range(0, len(m)):
        if m[i] == 0:
            assert(f[i] == f1[i])

    f = f1[:]
    f[m] /= f2
    fm = f[m]

    for i in range(0, len(fm)):
        assert(equalWithAbsError(fm[i], f1m[i] / f2[i], eps))
    
    for i in range(0, len(m)):
        if m[i] == 0:
            assert(f[i] == f1[i])

def testVectorVectorMaskedArithmeticOps(f1, f2, f3, m):
    f = f3[:]
    f[m] = f1[m] + f2[m]
    for i in range(0, len(m)):
        if m[i]: assert(f[i] == f1[i] + f2[i])
        else:    assert(f[i] == f3[i])

    f = f3[:]
    f[m] = f1[m] - f2[m]
    for i in range(0, len(m)):
        if m[i]: assert(f[i] == f1[i] - f2[i])
        else:    assert(f[i] == f3[i])

    f = f3[:]
    f[m] = f1[m] * f2[m]
    for i in range(0, len(m)):
        if m[i]: assert(f[i] == f1[i] * f2[i])
        else:    assert(f[i] == f3[i])

    f = f3[:]
    f[m] = f1[m] / f2[m]
    for i in range(0, len(m)):
        if m[i]: assert(equalWithRelError(f[i], f1[i] / f2[i], eps))
        else:    assert(f[i] == f3[i])


def testUnaryVecMethods(f):
    g = f.length()
    assert(len(g) == len(f))
    for i in range(0, len(f)):
        assert(equalWithRelError(g[i], f[i].length(), eps))

    g = f.length2()
    assert(len(g) == len(f))
    for i in range(0, len(f)):
        assert(g[i] == f[i].length2())

    # Normalization only makes sense for these types
    if type(f) in [V2fArray, V2dArray, V3fArray, V3dArray]:
        g = f[:]
        g.normalize()
        assert(len(g) == len(f))
        for i in range(0, len(f)):
            assert(g[i] == f[i].normalized())

        g = f.normalized()
        assert(len(g) == len(f))
        for i in range(0, len(f)):
            assert(g[i] == f[i].normalized())


def testBinaryVecMethods(f1, f2):
    f = f1.dot(f2)
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(f[i] == f1[i].dot(f2[i]))

    assert(f1.dot(f2) == f2.dot(f1))

    f = f1.cross(f2)
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(f[i] == f1[i].cross(f2[i]))

    assert(f1.cross(f2) == -f2.cross(f1))

    v = f2[0]
    f = f1.dot(v)
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(f[i] == f1[i].dot(v))

    assert(f1.dot(v) == v.dot(f1))

    f = f1.cross(v)
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(f[i] == f1[i].cross(v))

    assert(f1.cross(v) == -v.cross(f1))


def assertVectorVectorArithmeticOpFailures(f1, f2):
    try:
        f = f1 + f2
    except:
        pass
    else:
        assert(False)

    try:
        f = f1 - f2
    except:
        pass
    else:
        assert(False)

    try:
        f = f1 * f2
    except:
        pass
    else:
        assert(False)

    try:
        f = f1 / f2
    except:
        pass
    else:
        assert(False)

def assertVectorVectorInPlaceArithmeticOpFailures(f1, f2):
    try:
        f1 += f2
    except:
        pass
    else:
        assert(False)

    try:
        f1 -= f2
    except:
        pass
    else:
        assert(False)

    try:
        f1 *= f2
    except:
        pass
    else:
        assert(False)

    try:
        f1 /= f2
    except:
        pass
    else:
        assert(False)

def assertVectorVectorComparisonOpFailures(f1, f2):
    try:
        f1 == f2
    except:
        pass
    else:
        assert(False)

    try:
        f1 != f2
    except:
        pass
    else:
        assert(False)

    try:
        f1 < f2
    except:
        pass
    else:
        assert(False)

    try:
        f1 > f2
    except:
        pass
    else:
        assert(False)

    try:
        f1 <= f2
    except:
        pass
    else:
        assert(False)

    try:
        f1 >= f2
    except:
        pass
    else:
        assert(False)

def assertPowFunctionFailures(f1, f2):
    try:
        f1 ** f2
    except:
        pass
    else:
        assert(False)

    try:
        f1 **= f2
    except:
        pass
    else:
        assert(False)

def assertModOpFailures(f1, f2):
    try:
        f1 % f2
    except:
        pass
    else:
        assert(False)

    try:
        f1 %= f2
    except:
        pass
    else:
        assert(False)

# -----------------------------------------------------------------
# Begin main test definitions
# -----------------------------------------------------------------

def testNonMaskedFloatTypeArray(FloatTypeArray):
    f1 = FloatTypeArray(5)
    assert (len(f1) == 5)

    # Check for correct initialization
    for i in range(0, len(f1)):
        assert(f1[i] == 0)

    f1 = FloatTypeArray(1.25, 10)
    assert(len(f1) == 10)
    for i in range(0, len(f1)):
        assert(f1[i] == 1.25)

    # Ensure that an exception is thrown when
    # we exceed the bounds of the array
    try:
        print (f1[10])
    except:
        pass
    else:
        assert(False)

    # Check element assignment
    f1[0] = 1.5
    f1[1] = 2.0

    assert(f1[0] == 1.5)
    assert(f1[1] == 2.0)

    # Test copy construction
    f2 = FloatTypeArray(f1)
    assert(len(f2) == len(f1))
    for i in range(0, len(f1)):
        assert f1[i] == f2[i]

    # The same internal data is referenced by both arrays
    f2[3] = 4.5
    assert(f2[3] == 4.5)
    assert(f1[3] == 4.5)
    f1[4] = 5.5
    assert(f1[4] == 5.5)
    assert(f2[4] == 5.5)

    # Test negative indices
    assert(f2[-1] == f2[len(f2)-1])
    assert(f2[-2] == f2[len(f2)-2])

    # Test slice operations

    # Copy contents of f1
    f3 = f1[:]
    assert(len(f3) == len(f1))

    for i in range(0, len(f1)):
        assert(f3[i] == f1[i])

    f3[0] = 0.25
    assert(f3[0] != f1[0])

    f3 = f1[2:4]
    assert(len(f3) == 2)
    assert(f3[0] == f1[2] and f3[1] == f1[3])

    # Test array-array operations
    f1 = FloatTypeArray(5)
    f2 = FloatTypeArray(5)

    # These values were chosen to allow division operations
    # to return exact values that can be compared with '=='

    f1[0] = 1.25
    f1[1] = 2.0
    f1[2] = 3.0
    f1[3] = 1.0
    f1[4] = 3.75

    f2[0] = 5.0
    f2[1] = 2.0
    f2[2] = 1.5
    f2[3] = 2.0
    f2[4] = 10.0

    testVectorVectorArithmeticOps(f1, f2)
    testVectorVectorInPlaceArithmeticOps(f1, f2)

    # Test operations for arrays with scalars
    testVectorScalarArithmeticOps(f1, 1.75)
    testVectorScalarInPlaceArithmeticOps(f1, 0.25)
    testVectorScalarComparisonOps(f1, 3.5)
    testVectorScalarInequalityOps(f1, 3.5)

    # Make sure that operations fail when performed on arrays
    # of differing lengths
    f3 = FloatTypeArray(6)

    assertVectorVectorArithmeticOpFailures(f1, f3)
    assertVectorVectorInPlaceArithmeticOpFailures(f1, f3)
    assertVectorVectorComparisonOpFailures(f1, f3)
    assertPowFunctionFailures(f1, f3)

    testPowFunctions(f1, f2)

    print ("ok")

testList.append(('testNonMaskedFloatArray', lambda : testNonMaskedFloatTypeArray(FloatArray)))
testList.append(('testNonMaskedDoubleArray', lambda : testNonMaskedFloatTypeArray(DoubleArray)))

def testNonMaskedIntTypeArray(IntTypeArray):
    f1 = IntTypeArray(5)
    assert (len(f1) == 5)

    # Check for correct initialization
    for i in range(0, len(f1)):
        assert(f1[i] == 0)

    f1 = IntTypeArray(3, 10)
    assert(len(f1) == 10)
    for i in range(0, len(f1)):
        assert(f1[i] == 3)

    # Ensure that an exception is thrown when
    # we exceed the bounds of the array
    try:
        print (f1[10])
    except:
        pass
    else:
        assert(false)

    # Check element assignment
    f1[0] = 1
    f1[1] = 2

    assert(f1[0] == 1)
    assert(f1[1] == 2)

    # Test copy construction
    f2 = IntTypeArray(f1)
    assert(len(f2) == len(f1))
    for i in range(0, len(f1)):
        assert f1[i] == f2[i]

    # The same internal data is referenced by both arrays
    f2[3] = 4
    assert(f2[3] == 4)
    assert(f1[3] == 4)
    f1[4] = 5
    assert(f1[4] == 5)
    assert(f2[4] == 5)

    # Test negative indices
    assert(f2[-1] == f2[len(f2)-1])
    assert(f2[-2] == f2[len(f2)-2])

    # Test slice operations

    # Copy contents of f1
    f3 = f1[:]
    assert(len(f3) == len(f1))

    for i in range(0, len(f1)):
        assert(f3[i] == f1[i])

    f3[0] = 4
    assert(f3[0] != f1[0])

    f3 = f1[2:4]
    assert(len(f3) == 2)
    assert(f3[0] == f1[2] and f3[1] == f1[3])

    # Test array-array operations
    f1 = IntTypeArray(5)
    f2 = IntTypeArray(5)

    # These values were chosen to allow division operations
    # to return exact values that can be compared with '=='

    f1[0] = 1
    f1[1] = 2
    f1[2] = 3
    f1[3] = 1
    f1[4] = 7

    f2[0] = 5
    f2[1] = 2
    f2[2] = 1
    f2[3] = 2
    f2[4] = 10

    testVectorVectorArithmeticOps(f1, f2)
    testVectorVectorInPlaceArithmeticOps(f1, f2)
    testVectorVectorComparisonOps(f1, f2)
    testVectorVectorInequalityOps(f1, f2)

    # Test operations for arrays with scalars
    testVectorScalarArithmeticOps(f1, 2)
    testVectorScalarInPlaceArithmeticOps(f1, 4)
    testVectorScalarComparisonOps(f1, 7)
    testVectorScalarInequalityOps(f1, 7)

    testModOps(f1, f2)

    # Make sure that operations fail when performed on arrays
    # of differing lengths
    f3 = IntTypeArray(6)

    assertVectorVectorArithmeticOpFailures(f1, f3)
    assertVectorVectorInPlaceArithmeticOpFailures(f1, f3)
    assertVectorVectorComparisonOpFailures(f1, f3)
    assertModOpFailures(f1, f3)

    print ("ok")

testList.append(('testNonMaskedIntArray', lambda : testNonMaskedIntTypeArray(IntArray)))
testList.append(('testNonMaskedShortArray', lambda : testNonMaskedIntTypeArray(ShortArray)))
#testList.append(('testNonMaskedUnsignedCharArray', lambda : testNonMaskedIntTypeArray(UnsignedCharArray))) # arithmetic tests will fail this

def testMaskedFloatTypeArray(FloatTypeArray):
    f = FloatTypeArray(10)

    f[0] = 1.25
    f[1] = 2.5
    f[2] = 1.0
    f[3] = 1.75
    f[4] = 5.25
    f[5] = 7.0
    f[6] = 4.25
    f[7] = 1.0
    f[8] = 0.5
    f[9] = 3.5

    # Ensure we can't create a masked array if the indices don't match
    m1 = IntArray(9)
    try:
        mf = f[m1]
    except:
        pass
    else:
        assert(false)

    m1 = IntArray(len(f))
    m1[0] = 1
    m1[1] = 0
    m1[2] = 0
    m1[3] = 1
    m1[4] = 1
    m1[5] = 0
    m1[6] = 0
    m1[7] = 1
    m1[8] = 0
    m1[9] = 1

    # Ensure the masked array reports the correct reduced length
    mf = f[m1]
    assert(len(mf) == numNonZeroMaskEntries(m1))

    # Ensure the masked array holds the correct values
    assert(mf[0] == 1.25)
    assert(mf[1] == 1.75)
    assert(mf[2] == 5.25)
    assert(mf[3] == 1.0)
    assert(mf[4] == 3.5)

    # Masked arrays reference the same internal data
    f[9] = 1.75
    assert(mf[4] == 1.75)
    mf[3] = 10.5
    assert(f[7] == 10.5)

    # Test copy construction of masked references
    g = FloatTypeArray(mf)

    # Check slices of masks
    s = mf[1:3]
    assert(len(s) == 2)
    assert(s[0] == mf[1])
    assert(s[1] == mf[2])

    assert(mf[-1] == mf[len(mf)-1])
    assert(mf[-2] == mf[len(mf)-2])

    # Check that slices copy (not reference) array data
    s = mf[:]
    assert(len(s) == len(mf))
    for i in range(0, len(mf)):
        assert(s[i] == mf[i])

    s[0] = 0
    assert(s[0] != mf[0])

    # Test operations with masked arrays
    # Masked arrays should behave exactly as ordinary arrays

    m2 = IntArray(len(f))
    m2[0] = 1
    m2[1] = 0
    m2[2] = 1
    m2[3] = 0
    m2[4] = 1
    m2[5] = 1
    m2[6] = 0
    m2[7] = 0
    m2[8] = 1
    m2[9] = 1

    # m1 and m2 differ in the number of non-zero entries.
    # Ensure that arithmetic operations with masked arrays
    # cannot proceed if they have differing lengths

    mf1 = f[m1]
    mf2 = f[m2]

    assertVectorVectorInPlaceArithmeticOpFailures(mf1, mf2)

    # Test that the operations still fail when the number
    # of non-zero mask entries is the same

    m2[9] = 0

    assert(numNonZeroMaskEntries(m1) == numNonZeroMaskEntries(m2))

    mf2 = f[m2]
  
    # Aritmetic operations and comparison ops are supported
    testVectorVectorArithmeticOps(mf1, mf2)
    testVectorVectorComparisonOps(mf1, mf2)
    testVectorVectorInequalityOps(mf1, mf2)

    # Test operations between masked arrays and non-masked arrays
    assert(len(mf1) == 5);
    g = FloatTypeArray(5)
    g[0] = 0.25
    g[1] = 1.75
    g[2] = 3.0
    g[3] = 4.25
    g[4] = 5.75

    testVectorVectorArithmeticOps(g, mf1)
    testVectorVectorComparisonOps(g, mf1)
    testVectorVectorInequalityOps(g, mf1)

    assert(len(f) == 10)
    g = FloatTypeArray(10)
    g[0] = 0.75
    g[1] = 1.25
    g[2] = 6.0
    g[3] = 4.25
    g[4] = 1.5
    g[5] = 8.0
    g[6] = 3.5
    g[7] = 2.0
    g[8] = 1.75
    g[9] = 6.5

    testVectorVectorMaskedInPlaceArithmeticOps(f, g, m1)
    testVectorVectorMaskedInPlaceArithmeticOps2(f, g[m1], m1)
    testVectorVectorMaskedInPlaceArithmeticOps2(f, g[m2][:], m1)
    testVectorVectorMaskedArithmeticOps(f, g, f / 2.0, m1)

    print ("ok")

testList.append(('testMaskedFloatArray', lambda : testMaskedFloatTypeArray(FloatArray)))
testList.append(('testMaskedDoubleArray', lambda : testMaskedFloatTypeArray(DoubleArray)))


def testMaskedIntTypeArray(IntTypeArray):
    f = IntTypeArray(10)

    f[0] = 1
    f[1] = 2
    f[2] = 9
    f[3] = 1
    f[4] = 5
    f[5] = 7
    f[6] = 4
    f[7] = 1
    f[8] = 6
    f[9] = 3

    # Ensure we can't create a masked array if the indices don't match
    m1 = IntArray(9)
    try:
        mf = f[m1]
    except:
        pass
    else:
        assert(false)

    m1 = IntArray(len(f))
    m1[0] = 1
    m1[1] = 0
    m1[2] = 0
    m1[3] = 1
    m1[4] = 1
    m1[5] = 0
    m1[6] = 0
    m1[7] = 1
    m1[8] = 0
    m1[9] = 1

    # Ensure the masked array reports the correct reduced length
    mf = f[m1]
    assert(len(mf) == numNonZeroMaskEntries(m1))

    # Ensure the masked array holds the correct values
    assert(mf[0] == 1)
    assert(mf[1] == 1)
    assert(mf[2] == 5)
    assert(mf[3] == 1)
    assert(mf[4] == 3)

    # Masked arrays reference the same internal data
    f[9] = 4
    assert(mf[4] == 4)
    mf[3] = 5
    assert(f[7] == 5)

    # Test copy construction of masked references
    g = IntTypeArray(mf)

    # Check slices of masks
    s = mf[1:3]
    assert(len(s) == 2)
    assert(s[0] == mf[1])
    assert(s[1] == mf[2])

    assert(mf[-1] == mf[len(mf)-1])
    assert(mf[-2] == mf[len(mf)-2])

    # Check that slices copy (not reference) array data
    s = mf[:]
    assert(len(s) == len(mf))
    for i in range(0, len(mf)):
        assert(s[i] == mf[i])

    s[0] = 0
    assert(s[0] != mf[0])

    # Test operations with masked arrays
    # Masked arrays should behave exactly as ordinary arrays

    m2 = IntArray(len(f))
    m2[0] = 1
    m2[1] = 0
    m2[2] = 1
    m2[3] = 0
    m2[4] = 1
    m2[5] = 1
    m2[6] = 0
    m2[7] = 0
    m2[8] = 1
    m2[9] = 1

    # m1 and m2 differ in the number of non-zero entries.
    # Ensure that arithmetic operations with masked arrays
    # cannot proceed if they have differing lengths

    mf1 = f[m1]
    mf2 = f[m2]

    assertVectorVectorInPlaceArithmeticOpFailures(mf1, mf2)

    # Test that the operations still fail when the number
    # of non-zero mask entries is the same

    m2[9] = 0

    assert(numNonZeroMaskEntries(m1) == numNonZeroMaskEntries(m2))

    mf2 = f[m2]
  
    #assertVectorVectorInPlaceArithmeticOpFailures(mf1, mf2)

    # Aritmetic operations and comparison ops are supported
    testVectorVectorArithmeticOps(mf1, mf2)
    testVectorVectorComparisonOps(mf1, mf2)
    testVectorVectorInequalityOps(mf1, mf2)

    # Test operations between masked arrays and non-masked arrays
    assert(len(mf1) == 5);
    g = IntTypeArray(5)
    g[0] = 2
    g[1] = 1
    g[2] = 5
    g[3] = 4
    g[4] = 8

    testVectorVectorArithmeticOps(g, mf1)
    testVectorVectorComparisonOps(g, mf1)
    testVectorVectorInequalityOps(g, mf1)

    assert(len(f) == 10)
    g = IntTypeArray(10)
    g[0] = 5
    g[1] = 11
    g[2] = 3
    g[3] = 4
    g[4] = 1
    g[5] = 8
    g[6] = 6
    g[7] = 2
    g[8] = 1
    g[9] = 7

    testVectorVectorMaskedInPlaceArithmeticOps(f, g, m1)
    testVectorVectorMaskedInPlaceArithmeticOps2(f, g[m1], m1)
    testVectorVectorMaskedInPlaceArithmeticOps2(f, g[m2][:], m1)
    testVectorVectorMaskedArithmeticOps(f, g, f / 2, m1)

    print ("ok")

testList.append(('testMaskedIntArray', lambda : testMaskedIntTypeArray(IntArray)))
testList.append(('testMaskedShortArray', lambda : testMaskedIntTypeArray(ShortArray)))

def testNonMaskedVecTypeArray(VecTypeArray):
    base_type = ArrayBaseType[VecTypeArray]
    vec_base_type = VecBaseType[base_type]

    f1 = VecTypeArray(5)
    assert (len(f1) == 5)

    # Check for correct initialization
    for i in range(0, len(f1)):
        assert(f1[i] == base_type(0))

    v = None
    if dimensions(base_type) == 2:
        v = base_type(1.25, 3.75)
    elif base_type.dimensions() == 3:
        v = base_type(1.25, 3.75, 2.0)
    else:
        assert(False)

    f1 = VecTypeArray(v, 10)
    assert(len(f1) == 10)
    for i in range(0, len(f1)):
        assert(f1[i] == v)

    # Ensure that an exception is thrown when
    # we exceed the bounds of the array
    try:
        print (f1[10])
    except:
        pass
    else:
        assert(False)

    # Check element assignment

    v1 = None
    v2 = None

    if dimensions(base_type) == 2:
        v1 = base_type(1.5, 0.75)
        v2 = base_type(4.25, 7.5)
    elif dimensions(base_type) == 3:
        v1 = base_type(1.5, 0.75, 5.0)
        v2 = base_type(4.25, 7.5, 2.25)
    else:
        assert(False)

    f1[0] = v1
    f1[1] = v2

    assert(f1[0] == v1)
    assert(f1[1] == v2)

    # Test copy construction
    f2 = VecTypeArray(f1)
    assert(len(f2) == len(f1))
    for i in range(0, len(f1)):
        assert f1[i] == f2[i]

    # The same internal data is referenced by both arrays
    v = None
    if dimensions(base_type) == 2:
        v = base_type(4.5, 1.75)
    elif base_type.dimensions() == 3:
        v = base_type(4.5, 1.75, 6.0)
    else:
        assert(False)

    f2[3] = v
    assert(f2[3] == v)
    assert(f1[3] == v)

    f1[4] = 2*v
    assert(f1[4] == 2*v)
    assert(f2[4] == 2*v)

    # Test negative indices
    assert(f2[-1] == f2[len(f2)-1])
    assert(f2[-2] == f2[len(f2)-2])

    # Test slice operations

    # Copy contents of f1
    f3 = f1[:]
    assert(len(f3) == len(f1))

    for i in range(0, len(f1)):
        assert(f3[i] == f1[i])

    v = None
    if dimensions(base_type) == 2:
        v = base_type(0.25, 5.25)
    elif base_type.dimensions() == 3:
        v = base_type(0.25, 5.25, 1.0)

    assert(v is not None)

    f3[0] = v
    assert(f3[0] != f1[0])

    f3 = f1[2:4]
    assert(len(f3) == 2)
    assert(f3[0] == f1[2] and f3[1] == f1[3])

    # Test array-array operations
    f1 = VecTypeArray(5)
    f2 = VecTypeArray(5)

    # These values were chosen to allow division operations
    # to return exact values that can be compared with '=='

    if dimensions(base_type) == 2:
        f1[0] = base_type(1.25, 2.5)
        f1[1] = base_type(2.0, 7.25)
        f1[2] = base_type(3.0, 9.0)
        f1[3] = base_type(1.0, 8.5)
        f1[4] = base_type(3.75, 3.25)

        f2[0] = base_type(5.0, 4.25)
        f2[1] = base_type(2.0, 3.5)
        f2[2] = base_type(1.5, 6.0)
        f2[3] = base_type(2.0, 7.25)
        f2[4] = base_type(10.0, 11.0)

    elif dimensions(base_type) == 3:
        f1[0] = base_type(1.25, 2.5, 11.75)
        f1[1] = base_type(2.0, 7.25, 4.0)
        f1[2] = base_type(3.0, 9.0, 12.25)
        f1[3] = base_type(1.0, 8.5, 6.5)
        f1[4] = base_type(3.75, 0.25, 5.25)

        f2[0] = base_type(5.0, 4.25, 5.75)
        f2[1] = base_type(2.0, 3.5, 8.0)
        f2[2] = base_type(1.5, 6.0, 12.5)
        f2[3] = base_type(2.0, 7.25, 15.0)
        f2[4] = base_type(10.0, 11.0, 1.25)

    testVectorVectorArithmeticOps(f1, f2)
    testVectorVectorInPlaceArithmeticOps(f1, f2)
    testUnaryVecMethods(f1)
    testBinaryVecMethods(f1, f2)

    if dimensions(base_type) == 2:
        v = base_type(1.25, 5.25)
    elif dimensions(base_type) == 3:
        v = base_type(1.25, 5.25, 1.0)
    else:
        assert(False)

    assert(v is not None)

    # Test operations for arrays with scalars
    testVectorScalarArithmeticOps(f1, v)
    testVectorScalarInPlaceArithmeticOps(f1, v)
    testVectorScalarComparisonOps(f1, v)

    # Test multiplication and division by vector base types
    v = vec_base_type(4.25)
    
    f = f1 * v
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(f[i] == f1[i] * v)

    f = v * f1
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(f[i] == v * f1[i])

    f = f1 / v
    assert(len(f) == len(f1))
    for i in range(0, len(f)):
        assert(equalWithAbsError(f[i], f1[i] / v, eps))


    # Make sure that operations fail when performed on arrays
    # of differing lengths
    f3 = VecTypeArray(6)

    assertVectorVectorArithmeticOpFailures(f1, f3)
    assertVectorVectorInPlaceArithmeticOpFailures(f1, f3)

    print ("ok")

testList.append(('testNonMaskedV2sArray', lambda : testNonMaskedVecTypeArray(V2sArray)))
testList.append(('testNonMaskedV2iArray', lambda : testNonMaskedVecTypeArray(V2iArray)))
testList.append(('testNonMaskedV2fArray', lambda : testNonMaskedVecTypeArray(V2fArray)))
testList.append(('testNonMaskedV2dArray', lambda : testNonMaskedVecTypeArray(V2dArray)))
testList.append(('testNonMaskedV3sArray', lambda : testNonMaskedVecTypeArray(V3sArray)))
testList.append(('testNonMaskedV3iArray', lambda : testNonMaskedVecTypeArray(V3iArray)))
testList.append(('testNonMaskedV3fArray', lambda : testNonMaskedVecTypeArray(V3fArray)))
testList.append(('testNonMaskedV3dArray', lambda : testNonMaskedVecTypeArray(V3dArray)))


def testMaskedVecTypeArray(VecTypeArray):
    base_type = ArrayBaseType[VecTypeArray]
    vec_base_type = VecBaseType[base_type]

    f = VecTypeArray(10)

    if dimensions(base_type) == 2:
        f[0] = base_type(1.25, 5.25)
        f[1] = base_type(2.5, 6.0)
        f[2] = base_type(1.0, 3.75)
        f[3] = base_type(1.75, 11.25)
        f[4] = base_type(5.25, 12.0)
        f[5] = base_type(7.0, 4.5)
        f[6] = base_type(4.25, 6.5)
        f[7] = base_type(1.0, 2.25)
        f[8] = base_type(1.5, 1.75)
        f[9] = base_type(3.5, 4.0)
    elif dimensions(base_type) == 3:
        f[0] = base_type(1.25, 5.25, 8.5)
        f[1] = base_type(2.5, 6.0, 7.25)
        f[2] = base_type(1.0, 3.75, 15.5)
        f[3] = base_type(1.75, 11.25, 10.0)
        f[4] = base_type(5.25, 12.0, 16.5)
        f[5] = base_type(7.0, 4.5, 1.25)
        f[6] = base_type(4.25, 6.5, 9.25)
        f[7] = base_type(1.0, 2.25, 5.0)
        f[8] = base_type(1.5, 1.75, 7.5)
        f[9] = base_type(3.5, 4.0, 5.75)

    # Ensure we can't create a masked array if the indices don't match
    m1 = IntArray(9)
    try:
        mf = f[m1]
    except:
        pass
    else:
        assert(false)

    m1 = IntArray(len(f))
    m1[0] = 1
    m1[1] = 0
    m1[2] = 0
    m1[3] = 1
    m1[4] = 1
    m1[5] = 0
    m1[6] = 0
    m1[7] = 1
    m1[8] = 0
    m1[9] = 1

    # Ensure the masked array reports the correct reduced length
    mf = f[m1]
    assert(len(mf) == numNonZeroMaskEntries(m1))

    # Ensure the masked array holds the correct values
    assert(mf[0] == f[0])
    assert(mf[1] == f[3])
    assert(mf[2] == f[4])
    assert(mf[3] == f[7])
    assert(mf[4] == f[9])

    # Masked arrays reference the same internal data
    v = None
    if dimensions(base_type) == 2:
        v = base_type(1.75, 2.5)
    elif dimensions(base_type) == 3:
        v = base_type(1.75, 2.5, 9.25)
    else:
        assert(False)

    f[9] = v
    assert(mf[4] == v)

    mf[3] = 2*v
    assert(f[7] == 2*v)

    # Test copy construction of masked references
    g = VecTypeArray(mf)

    # Check slices of masks
    s = mf[1:3]
    assert(len(s) == 2)
    assert(s[0] == mf[1])
    assert(s[1] == mf[2])

    assert(mf[-1] == mf[len(mf)-1])
    assert(mf[-2] == mf[len(mf)-2])

    # Check that slices copy (not reference) array data
    s = mf[:]
    assert(len(s) == len(mf))
    for i in range(0, len(mf)):
        assert(s[i] == mf[i])

    s[0] = base_type(0)
    assert(s[0] != mf[0])

    # Test operations with masked arrays
    # Masked arrays should behave exactly as ordinary arrays

    m2 = IntArray(len(f))
    m2[0] = 1
    m2[1] = 0
    m2[2] = 1
    m2[3] = 0
    m2[4] = 1
    m2[5] = 1
    m2[6] = 0
    m2[7] = 0
    m2[8] = 1
    m2[9] = 1

    # m1 and m2 differ in the number of non-zero entries.
    # Ensure that arithmetic operations with masked arrays
    # cannot proceed if they have differing lengths

    mf1 = f[m1]
    mf2 = f[m2]

    assertVectorVectorInPlaceArithmeticOpFailures(mf1, mf2)

    # Test that the operations still fail when the number
    # of non-zero mask entries is the same

    m2[9] = 0

    assert(numNonZeroMaskEntries(m1) == numNonZeroMaskEntries(m2))

    mf2 = f[m2]
  
    # Aritmetic operations and comparison ops are supported
    testVectorVectorArithmeticOps(mf1, mf2)
    testVectorVectorComparisonOps(mf1, mf2)

    # Test operations between masked arrays and non-masked arrays
    assert(len(mf1) == 5);
    g = VecTypeArray(5)

    if dimensions(base_type) == 2:
        g[0] = base_type(5.25, 2.75)
        g[1] = base_type(1.75, 11.5)
        g[2] = base_type(3.0, 8.25)
        g[3] = base_type(4.25, 6.75)
        g[4] = base_type(5.75, 12.0)
    elif dimensions(base_type) == 3:
        g[0] = base_type(5.25, 2.75, 1.0)
        g[1] = base_type(1.75, 11.5, 15.25)
        g[2] = base_type(3.0, 8.25, 9.0)
        g[3] = base_type(4.25, 6.75, 1.25)
        g[4] = base_type(5.75, 12.0, 7.5)
    else:
        assert(False)

    testVectorVectorArithmeticOps(g, mf1)
    testVectorVectorComparisonOps(g, mf1)

    testUnaryVecMethods(g)
    testBinaryVecMethods(g, mf1)
    testBinaryVecMethods(mf1, mf2)

    assert(len(f) == 10)
    g = VecTypeArray(10)

    if dimensions(base_type) == 2:
        g[0] = base_type(5.25, 2.75)
        g[1] = base_type(1.75, 11.5)
        g[2] = base_type(3.0, 8.25)
        g[3] = base_type(4.25, 6.75)
        g[4] = base_type(5.75, 12.0)
        g[5] = base_type(8.0, 5.25)
        g[6] = base_type(3.5, 4.0)
        g[7] = base_type(2.0, 12.5)
        g[8] = base_type(1.75, 6.75)
        g[9] = base_type(6.5, 8.0)
    elif dimensions(base_type) == 3:
        g[0] = base_type(5.25, 2.75, 1.0)
        g[1] = base_type(1.75, 11.5, 15.25)
        g[2] = base_type(3.0, 8.25, 9.0)
        g[3] = base_type(4.25, 6.75, 1.25)
        g[4] = base_type(5.75, 12.0, 7.5)
        g[5] = base_type(8.0, 5.25, 12.25)
        g[6] = base_type(3.5, 4.0, 6.0)
        g[7] = base_type(2.0, 12.5, 16.5)
        g[8] = base_type(1.75, 6.75, 4.25)
        g[9] = base_type(6.5, 8.0, 7.75)
    else:
        assert(False)

    testVectorVectorMaskedInPlaceArithmeticOps(f, g, m1)
    testVectorVectorMaskedInPlaceArithmeticOps2(f, g[m1], m1)
    testVectorVectorMaskedInPlaceArithmeticOps2(f, g[m2][:], m1)

    v = None
    if dimensions(base_type) == 2:
        v = base_type(1.25, 3.75)
    elif base_type.dimensions() == 3:
        v = base_type(1.25, 3.75, 2.0)
    else:
        assert(False)

    assert(v is not None)

    # Test operations for arrays with scalars
    testVectorScalarArithmeticOps(g, v)
    testVectorScalarInPlaceArithmeticOps(g, v)
    testVectorScalarComparisonOps(g, v)

    testVectorVectorMaskedArithmeticOps(f, f, f, m1)

    # Test multiplication and division by vector base types
    v = vec_base_type(4.25)
    
    f = g * v
    assert(len(f) == len(g))
    for i in range(0, len(f)):
        assert(f[i] == g[i] * v)

    f = v * g
    assert(len(f) == len(g))
    for i in range(0, len(f)):
        assert(f[i] == v * g[i])

    f = g / v
    assert(len(f) == len(g))
    for i in range(0, len(f)):
        assert(equalWithAbsError(f[i], g[i] / v, eps))

    testVectorVectorMaskedArithmeticOps

    print ("ok")

testList.append(('testMaskedV2sArray', lambda : testMaskedVecTypeArray(V2sArray)))
testList.append(('testMaskedV2iArray', lambda : testMaskedVecTypeArray(V2iArray)))
testList.append(('testMaskedV2fArray', lambda : testMaskedVecTypeArray(V2fArray)))
testList.append(('testMaskedV2dArray', lambda : testMaskedVecTypeArray(V2dArray)))
testList.append(('testMaskedV3fArray', lambda : testMaskedVecTypeArray(V3fArray)))
testList.append(('testMaskedV3dArray', lambda : testMaskedVecTypeArray(V3dArray)))


# -------------------------------------------------------------------------
# Tests for exceptions defined in imath module

def testExceptions():

    # Verify that the exception classes defined in imath
    # are subclasses of the exception classes in iex:
    # NullVecExc should be caught by "except NullVecExc",
    # "except iex.MathExc", "except iex.BaseExc" and
    # "except iex.std_exception".

    try:
        raise NullVecExc
    except NullVecExc:
        pass
    else:
        assert 0

    try:
        raise NullVecExc
    except iex.MathExc:
        pass
    else:
        assert 0

    try:
        raise NullVecExc
    except iex.BaseExc:
        pass
    else:
        assert 0

    try:
        raise NullVecExc
    except RuntimeError:
        pass
    else:
        assert 0

    try:
        raise NullQuatExc
    except RuntimeError:
        pass
    else:
        assert 0

    try:
        raise SingMatrixExc
    except RuntimeError:
        pass
    else:
        assert 0
    try:
        raise ZeroScaleExc
    except RuntimeError:
        pass
    else:
        assert 0

    try:
        raise IntVecNormalizeExc
    except RuntimeError:
        pass
    else:
        assert 0

    print ("ok")
    return


testList.append (('testExceptions',testExceptions))


# -------------------------------------------------------------------------
# Tests for functions

def testFun ():

    assert sign(5)    ==  1    
    assert sign(5.0)  ==  1    
    assert sign(-5)   == -1    
    assert sign(-5.0) == -1    

    assert log(math.e) ==  1    
    assert log(1)      ==  0    

    assert log10(10)   ==  1    
    assert log10(1)    ==  0    

    assert lerp(1, 2, 0.5)     == 1.5
    assert lerp(1.0, 2.0, 0.5) == 1.5
    assert lerp(2, 1, 0.5)     == 1.5
    assert lerp(2.0, 1.0, 0.5) == 1.5

    assert lerpfactor(1.5, 1, 2)     == 0.5
    assert lerpfactor(1.5, 1.0, 2.0) == 0.5

    assert clamp(0, 1, 2)       == 1
    assert clamp(3, 1, 2)       == 2
    assert clamp(0.0, 1.0, 2.0) == 1
    assert clamp(3.0, 1.0, 2.0) == 2

    assert cmp(1, 2)     == -1
    assert cmp(2, 2)     ==  0
    assert cmp(3, 2)     ==  1
    assert cmp(1.0, 2.0) == -1
    assert cmp(2.0, 2.0) ==  0
    assert cmp(3.0, 2.0) ==  1

    assert cmpt(1.0, 1.5, 0.1) == -1
    assert cmpt(1.5, 1.5, 0.1) ==  0
    assert cmpt(2.0, 1.5, 0.1) ==  1
    assert cmpt(1.0, 1.5, 0.6) ==  0
    assert cmpt(1.5, 1.5, 0.6) ==  0
    assert cmpt(2.0, 1.5, 0.6) ==  0

    assert iszero(0, 0)        == 1
    assert iszero(0, 0.1)      == 1
    assert iszero(0.01, 0.1)   == 1
    assert iszero(0.01, 0.001) == 0

    assert equal(5, 5, 0)        == 1
    assert equal(5, 6, 0)        == 0
    assert equal(5, 5.01, 0.1)   == 1
    assert equal(5, 5.01, 0.001) == 0

    assert trunc(1.1)  ==  1
    assert trunc(-1.1) == -1
    assert trunc(1)    ==  1

    assert divs( 4,  2) ==  2
    assert divs(-4,  2) == -2
    assert divs( 4, -2) == -2
    assert divs(-4, -2) ==  2
    assert mods( 3,  2) ==  1
    assert mods(-3,  2) == -1
    assert mods( 3, -2) ==  1
    assert mods(-3, -2) == -1

    assert divp( 4,  2) ==  2
    assert divp(-4,  2) == -2
    assert divp( 4, -2) == -2
    assert divp(-4, -2) ==  2
    assert modp( 3,  2) ==  1
    assert modp(-3,  2) ==  1
    assert modp( 3, -2) ==  1
    assert modp(-3, -2) ==  1

    print ("ok")

    return

testList.append (('testFun',testFun))


# -------------------------------------------------------------------------
# Tests for V2x

def testV2x (Vec):
    
    # Constructors (and element access).

    v = Vec()
    assert v[0] == 0 and v[1] == 0

    v = Vec(1)
    assert v[0] == 1 and v[1] == 1

    v = Vec(0, 1)
    assert v[0] == 0 and v[1] == 1

    v = Vec((0, 1))
    assert v[0] == 0 and v[1] == 1

    v = Vec([0, 1])
    assert v[0] == 0 and v[1] == 1

    v = Vec()
    v.setValue(0, 1)
    assert v[0] == 0 and v[1] == 1

    # Repr.

    v = Vec(1/9., 2/9.)
    assert v == eval(repr(v))

    # Sequence length.

    v = Vec()
    assert len(v) == 2

    # Element setting.

    v = Vec()
    v[0] = 10
    v[1] = 11
    assert v[0] == 10 and v[1] == 11

    try:
        v[-3] = 0  # This should raise an exception.
    except:
        pass
    else:
        assert 0   # We shouldn't get here.   

    try:
        v[3] = 0   # This should raise an exception.
    except:
        pass
    else:
        assert 0   # We shouldn't get here.

    try:
        v[1] = "a" # This should raise an exception.
    except:
        pass
    else:
        assert 0   # We shouldn't get here.

    # Assignment.

    v1 = Vec(1)
    
    v2 = v1
    assert v2[0] == 1 and v2[1] == 1
    v1[0] = 2
    assert v2[0] == 2 and v2[1] == 1
    
    # Comparison operators.

    v1 = Vec(20, 20)
    v2 = Vec(20, 20)
    v3 = Vec(20, 21)

    assert v1 == v2
    assert v1 != v3
    assert not (v1 < v2)
    assert v1 < v3
    assert v1 <= v2
    assert v1 <= v3
    assert not (v3 <= v1)
    assert not (v2 > v1)
    assert v3 > v1
    assert v2 >= v1
    assert v3 >= v1
    assert not (v1 >= v3)
    
    # Epsilon equality.

    e = 0.005
    v1 = Vec(1)
    v2 = Vec(1 + e)

    assert v1.equalWithAbsError(v2, e)
    assert v2.equalWithAbsError(v1, e)

    e = 0.003
    v1 = Vec(10)
    v2 = Vec(10 + 10 * e)

    assert v1.equalWithRelError(v2, e)
    assert v2.equalWithRelError(v1, e)

    # Dot products.

    v1 = Vec(0, 1)
    v2 = Vec(1, 0)
    v3 = Vec(1, 1)

    assert v1.dot(v2) == 0
    assert v1.dot(v3) == 1
    assert v1 ^ v2 == v1.dot(v2)
    assert v1 ^ v3 == v1.dot(v3)

    # Cross products.

    v1 = Vec(1, 0)
    v2 = Vec(0, 1)

    assert v1.cross(v2) == 1
    assert v2.cross(v1) == -1
    assert v1 % v2 == v1.cross(v2)
    assert v2 % v1 == v2.cross(v1)

    # Addition.

    v1 = Vec(10, 20)
    v2 = Vec(30, 40)

    assert v1 + v2 == Vec(40, 60)
    assert v2 + v1 == v1 + v2
    assert v1 + 1 == Vec(11, 21)
    assert 1 + v1 == v1 + 1

    # (with the switch to python2, we now allow ops between vectors and tuples)
    assert v1 + (1, 2) == Vec(11, 22)
    assert (1, 2) + v1 == v1 + (1, 2)

    # Subtraction and negation.

    v1 = Vec(10, 20)
    v2 = Vec(30, 40)

    assert v2 - v1 == Vec(20, 20)
    assert v1 - 1 == Vec(9, 19)
    assert 1 - v1 == - (v1 - 1)

    # (with the switch to python2, we now allow ops between vectors and tuples)
    assert v1 - (1, 2) == Vec(9, 18)
    assert (1, 2) - v1 == - (v1 - (1, 2))

    assert v1.negate() == Vec(-10, -20)

    # Multiplication.

    v1 = Vec(1, 2)
    v2 = Vec(3, 4)
    
    assert v1 * v2 == Vec(3, 8)
    assert v2 * v1 == v1 * v2
    assert 2 * v1 == Vec(2, 4)
    assert v1 * 2 == 2 * v1

    assert v1 * V2i(3, 4) == Vec(3, 8)
    assert v1 * V2f(3, 4) == Vec(3, 8)
    assert v1 * V2d(3, 4) == Vec(3, 8)

    v1 *= 2
    assert v1 == Vec(2, 4)
    v1 = Vec(1, 2)
    
    # (with the switch to python2, we now allow ops between vectors and tuples)
    assert v1 * (1, 2) == Vec(1, 4)
    assert (1, 2) * v1 == v1 * (1, 2)

    # Division.

    v1 = Vec(10, 20)
    v2 = Vec(2, 4)
    
    assert v1 / v2 == Vec(10/2, 20/4)
    assert v1 / 2 == Vec(10/2, 20/2)
    assert Vec(40) / v1 == Vec(40/10, 40/20)

    # (with the switch to python2, we now allow ops between vectors and tuples)
    assert v1 / (1, 2) == Vec(10/1, 20/2)
    assert Vec(30, 40) / v1 == Vec(30/10, 40/20)

    assert v1 / V2i (2, 4) == Vec(10/2, 20/4)
    assert v1 / V2f (2, 4) == Vec(10/2, 20/4)
    assert v1 / V2d (2, 4) == Vec(10/2, 20/4)
    assert v1 / (2, 4) == Vec(10/2, 20/4)
    assert v1 / [2, 4] == Vec(10/2, 20/4)

    v1 = Vec(10, 20)
    v1 /= 2
    assert v1 == Vec(10/2, 20/2)
    
    v1 = Vec(10, 20)
    v1 /= V2i (2, 4)
    assert v1 == Vec(10/2, 20/4)
    
    v1 = Vec(10, 20)
    v1 /= V2f (2, 4)
    assert v1 == Vec(10/2, 20/4)

    v1 = Vec(10, 20)
    v1 /= V2d (2, 4)
    assert v1 == Vec(10/2, 20/4)

    v1 = Vec(10, 20)
    v1 /= (2, 4)
    assert v1 == Vec(10/2, 20/4)

    v1 = Vec(10, 20)
    v1 /= [2, 4]
    assert v1 == Vec(10/2, 20/4)

    # Length.

    if (Vec != V2i):
       v = Vec(1, 2)
       assert equal(v.length(), sqrt(1*1 + 2*2), v.baseTypeEpsilon())
    else:
        v = Vec(1, 2)
        assert v.length() == round(sqrt(1*1 + 2*2))
        v = Vec(2, 3)
        assert v.length() == round(sqrt(2*2 + 3*3))

    v = Vec(1, 2)
    assert v.length2() == 1*1 + 2*2

    # Normalizing.

    if (Vec != V2i):
       v = Vec(1, 2)
       v.normalize()
       assert equal(v.length(), 1, v.baseTypeEpsilon())

       v = Vec(1, 2)
       v.normalizeExc()
       assert equal(v.length(), 1, v.baseTypeEpsilon())
       v = Vec(0)
       try:
           v.normalizeExc()        # This should raise an exception.
       except:
           pass
       else:
           assert 0                # We shouldn't get here.
       
       v = Vec(1, 2)
       v.normalizeNonNull()
       assert equal(v.length(), 1, v.baseTypeEpsilon())

       v = Vec(1, 2)
       assert equal(v.normalized().length(), 1, v.baseTypeEpsilon())

       v = Vec(1, 2)
       assert equal(v.normalizedExc().length(), 1, v.baseTypeEpsilon())
       v = Vec(0)
       try:
           v.normalizedExc()        # This should raise an exception.
       except:
           pass
       else:
           assert 0                # We shouldn't get here.
       
       v = Vec(1, 2)
       assert equal(v.normalizedNonNull().length(), 1, v.baseTypeEpsilon())

    else:
       v = Vec(0, 1)
       v.normalize()
       assert v.length() == 1

       v = Vec(1, 2)
       try:
           v.normalize()        # This should raise an exception.
       except:
           pass
       else:
           assert 0                # We shouldn't get here.
        
       v = Vec(0, 1)
       v.normalizeExc()
       assert v.length() == 1

       v = Vec(1, 2)
       try:
           v.normalizeExc()        # This should raise an exception.
       except:
           pass
       else:
           assert 0                # We shouldn't get here.
        
       v = Vec(0, 1)
       v.normalizeNonNull()
       assert v.length() == 1

       v = Vec(1, 2)
       try:
           v.normalizeNonNull()        # This should raise an exception.
       except:
           pass
       else:
           assert 0                # We shouldn't get here.
        
       v = Vec(0, 1)
       assert v.normalized().length() == 1

       v = Vec(1, 2)
       try:
           v.normalized()        # This should raise an exception.
       except:
           pass
       else:
           assert 0                # We shouldn't get here.
        
       v = Vec(0, 1)
       assert v.normalizedExc().length() == 1

       v = Vec(1, 2)
       try:
           v.normalizedExc()        # This should raise an exception.
       except:
           pass
       else:
           assert 0                # We shouldn't get here.
        
       v = Vec(0, 1)
       assert v.normalizeNonNull().length() == 1

       v = Vec(1, 2)
       try:
           v.normalizedNonNull()  # This should raise an exception.
       except:
           pass
       else:
           assert 0                         # We shouldn't get here.
        

    # Projection.

    if (Vec != V2i):
        s = Vec(2, 0)
        t = Vec(1, 1)
        assert t.project(s) == Vec(1, 0)

    # Orthogonal.

    if (Vec != V2i):
        s = Vec(2, 0)
        t = Vec(1, 1)
        o = s.orthogonal(t)
        assert iszero(o ^ s, s.baseTypeEpsilon())

    # Reflect.

    if (Vec != V2i):
        s = Vec(1, 1)
        t = Vec(2, 0)
        r = s.reflect(t)
        assert equal(abs(s ^ t), abs(r ^ t), s.baseTypeEpsilon())

    # Closest vertex.

    v0 = Vec(0, 0)
    v1 = Vec(5, 0)
    v2 = Vec(0, 5)
    
    p = Vec(1, 1)
    assert p.closestVertex(v0, v1, v2) == v0

    p = Vec(4, 1)
    assert p.closestVertex(v0, v1, v2) == v1

    p = Vec(1, 4)
    assert p.closestVertex(v0, v1, v2) == v2


    print ("ok")

    return

def testV2 ():

    print ("V2i")
    testV2x (V2i)
    print ("V2f")
    testV2x (V2f)
    print ("V2d")
    testV2x (V2d)

testList.append (('testV2',testV2))


# -------------------------------------------------------------------------
# Tests for V2xArray

def testV2xArray (Array, Vec, Arrayx):
    
    # Constructors (and element access).

    a = Array (3)

    a[0] = Vec(0)
    a[1] = Vec(1)
    a[2] = Vec(2)

    assert a[0] == Vec(0)
    assert a[1] == Vec(1)
    assert a[2] == Vec(2)

    a[0].setValue(10,10)
    a[1].setValue(11,11)
    a[2].setValue(12,12)

    assert a[0] == Vec(10)
    assert a[1] == Vec(11)
    assert a[2] == Vec(12)

    # Element setting.

    a = Array(2)

    try:
        a[-3] = Vec(0)        # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.   

    try:
        a[3] = Vec(0)   # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    try:
        a[1] = "a"         # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    # Assignment.

    a = Array(2)
    a[0] = Vec(0)
    a[1] = Vec(1)
    
    b = Array(2)
    b[0] = Vec(0)
    b[1] = Vec(1)
    
    c = Array(2)
    c[0] = Vec(10)
    c[1] = Vec(11)

    # TODO: make equality work correctly.
    #assert a == b
    assert a != c
    
    # Dot products.

    a = Array(2)
    a[0] = Vec(1, 2)
    a[1] = Vec(3, 4)

    b = Array(2)
    b[0] = Vec(5, 6)
    b[1] = Vec(7, 8)

    r = a.dot(b)
    assert r[0] == 1*5 + 2*6
    assert r[1] == 3*7 + 4*8

    c = Vec(5, 6)
    r = a.dot(c)
    assert r[0] == 1*5 + 2*6
    assert r[1] == 3*5 + 4*6

    d = Array(3)
    try:
        a.dot(d)        # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.   
    
    
    # Cross products.

    a = Array(2)
    a[0] = Vec(1, 2)
    a[1] = Vec(3, 4)

    b = Array(2)
    b[0] = Vec(5, 6)
    b[1] = Vec(7, 8)

    r = a.cross(b)
    assert r[0] == 1*6 - 2*5
    assert r[1] == 3*8 - 4*7

    c = Vec(5, 6)
    r = a.cross(c)
    assert r[0] == 1*6 - 2*5
    assert r[1] == 3*6 - 4*5

    d = Array(3)
    try:
        a.cross(d)        # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.   

    # Addition.

    a = Array(2)
    a[0] = Vec(1, 2)
    a[1] = Vec(3, 4)

    b = Array(2)
    b[0] = Vec(5, 6)
    b[1] = Vec(7, 8)

    r = a + b
    assert r[0] == Vec(1+5, 2+6)
    assert r[1] == Vec(3+7, 4+8)

    r = a + Vec(10)
    assert r[0] == Vec(1+10, 2+10)
    assert r[1] == Vec(3+10, 4+10)

    v = Vec(11)
    r = v + a 
    assert r[0] == Vec(11+1, 11+2)
    assert r[1] == Vec(11+3, 11+4)

    a += b
    assert a[0] == Vec(1+5, 2+6)
    assert a[1] == Vec(3+7, 4+8)

    a[0] = Vec(1, 2)
    a[1] = Vec(3, 4)

    a += Vec(10)
    assert a[0] == Vec(1+10, 2+10)
    assert a[1] == Vec(3+10, 4+10)

    c = Array(3)

    try:
        a + c                # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.   

    try:
        a += c                # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.   

    # Subtraction.

    a = Array(2)
    a[0] = Vec(1, 2)
    a[1] = Vec(3, 4)

    b = Array(2)
    b[0] = Vec(5, 6)
    b[1] = Vec(7, 8)

    r = a - b
    assert r[0] == Vec(1-5, 2-6)
    assert r[1] == Vec(3-7, 4-8)

    r = a - Vec(10)
    assert r[0] == Vec(1-10, 2-10)
    assert r[1] == Vec(3-10, 4-10)

    r = Vec(10) - a
    assert r[0] == Vec(10-1, 10-2)
    assert r[1] == Vec(10-3, 10-4)

    v = Vec(11)
    r = v - a 
    assert r[0] == Vec(11-1, 11-2)
    assert r[1] == Vec(11-3, 11-4)

    a -= b
    assert a[0] == Vec(1-5, 2-6)
    assert a[1] == Vec(3-7, 4-8)

    a[0] = Vec(1, 2)
    a[1] = Vec(3, 4)

    a -= Vec(10)
    assert a[0] == Vec(1-10, 2-10)
    assert a[1] == Vec(3-10, 4-10)

    c = Array(3)

    try:
        a - c                # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.   

    try:
        a -= c                # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.   

    # Negation.

    a = Array(2)
    a[0] = Vec(1, 2)
    a[1] = Vec(3, 4)

    r = -a
    assert r[0] == Vec(-1, -2)
    assert r[1] == Vec(-3, -4)

    # Multiplication.

    a = Array(2)
    a[0] = Vec(1, 2)
    a[1] = Vec(3, 4)

    r = a * 10
    assert r[0] == Vec(1, 2) * 10
    assert r[1] == Vec(3, 4) * 10

    b = Arrayx(2)
    b[0] = 10
    b[1] = 11

    r = a * b
    assert r[0] == Vec(1, 2) * 10
    assert r[1] == Vec(3, 4) * 11
    
    a *= 10
    assert a[0] == Vec(1, 2) * 10
    assert a[1] == Vec(3, 4) * 10

    a[0] = Vec(1, 2)
    a[1] = Vec(3, 4)

    a *= b
    assert a[0] == Vec(1, 2) * 10
    assert a[1] == Vec(3, 4) * 11

    a[0] = Vec(1, 2)
    a[1] = Vec(3, 4)

    b = Array(2)
    b[0] = Vec(5, 6)
    b[1] = Vec(7, 8)

    r = a * b
    assert r[0] == Vec(1*5, 2*6)
    assert r[1] == Vec(3*7, 4*8)

    v = Vec(9, 10)

    r = a * v
    assert r[0] == Vec(1*9, 2*10)
    assert r[1] == Vec(3*9, 4*10)

    r = v * a
    assert r[0] == Vec(1*9, 2*10)
    assert r[1] == Vec(3*9, 4*10)

    a *= b
    assert a[0] == Vec(1*5, 2*6)
    assert a[1] == Vec(3*7, 4*8)

    a[0] = Vec(1, 2)
    a[1] = Vec(3, 4)

    a *= v
    assert a[0] == Vec(1*9, 2*10)
    assert a[1] == Vec(3*9, 4*10)

    d = Array(3)
    try:
        a * d                # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.   

    try:
        a *= d                # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.   

    # Division.

    a = Array(2)
    a[0] = Vec(1.0, 2.0)
    a[1] = Vec(3.0, 4.0)

    r = a / 10
    assert r[0] == Vec(1.0, 2.0) / 10
    assert r[1] == Vec(3.0, 4.0) / 10

    b = Arrayx(2)
    b[0] = 10
    b[1] = 11

    r = a / b
    assert r[0] == Vec(1.0, 2.0) / 10
    assert r[1] == Vec(3.0, 4.0) / 11
    
    a /= 10
    assert a[0] == Vec(1.0, 2.0) / 10
    assert a[1] == Vec(3.0, 4.0) / 10

    a[0] = Vec(1.0, 2.0)
    a[1] = Vec(3.0, 4.0)

    a /= b
    assert a[0] == Vec(1.0, 2.0) / 10
    assert a[1] == Vec(3.0, 4.0) / 11

    a[0] = Vec(1.0, 2.0)
    a[1] = Vec(3.0, 4.0)

    b = Array(2)
    b[0] = Vec(5, 6)
    b[1] = Vec(7, 8)

    r = a / b
    assert r[0] == Vec(1.0/5, 2.0/6)
    assert r[1] == Vec(3.0/7, 4.0/8)

    v = Vec(9, 10)

    r = a / v
    assert r[0] == Vec(1.0/9, 2.0/10)
    assert r[1] == Vec(3.0/9, 4.0/10)

    # TODO: Figure out why "v / a" is illegal, even though the
    # add_arithmetic_math_functions() routine in PyImathFixedArray.h
    # should make it possible.
    #r = v / a
    #assert r[0] == Vec(1.0/9, 2.0/10)
    #assert r[1] == Vec(3.0/9, 4.0/10)

    a /= b
    assert a[0] == Vec(1.0/5, 2.0/6)
    assert a[1] == Vec(3.0/7, 4.0/8)

    a[0] = Vec(1.0, 2.0)
    a[1] = Vec(3.0, 4.0)

    a /= v
    assert a[0] == Vec(1.0/9, 2.0/10)
    assert a[1] == Vec(3.0/9, 4.0/10)

    d = Array(3)
    try:
        a / d                # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.   

    try:
        a /= d                # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.   

    # Length.

    v0 = Vec(1, 2)
    v1 = Vec(3, 4)

    a = Array(2)
    a[0] = v0
    a[1] = v1

    l = a.length()
    assert (l[0] == v0.length())
    assert (l[1] == v1.length())

    l = a.length2()
    assert (l[0] == v0.length2())
    assert (l[1] == v1.length2())
    
    # Normalizing.

    if (Vec != V2i):

        a[0] = Vec(1, 2)
        a[1] = Vec(3, 4)

        r = a.normalized();
        assert r[0] == Vec(1, 2).normalized()
        assert r[1] == Vec(3, 4).normalized()

        a.normalize();
        assert a[0] == Vec(1, 2).normalized()
        assert a[1] == Vec(3, 4).normalized()

    print ("ok")

    return

def testV2Array ():

    print ("V2iArray")
    testV2xArray (V2iArray, V2i, IntArray)
    print ("V2fArray")
    testV2xArray (V2fArray, V2f, FloatArray)
    print ("V2dArray")
    testV2xArray (V2dArray, V2d, DoubleArray)

testList.append (('testV2Array',testV2Array))


# -------------------------------------------------------------------------
# Tests for V3x

def testV3x (Vec):
    
    # Constructors (and element access).

    v = Vec()
    assert v[0] == 0 and v[1] == 0 and v[2] == 0

    v = Vec(1)
    assert v[0] == 1 and v[1] == 1 and v[2] == 1

    v = Vec(0, 1, 2)
    assert v[0] == 0 and v[1] == 1 and v[2] == 2

    v = Vec((0, 1, 2))
    assert v[0] == 0 and v[1] == 1 and v[2] == 2

    v = Vec([0, 1, 2])
    assert v[0] == 0 and v[1] == 1 and v[2] == 2

    v = Vec()
    v.setValue(0, 1, 2)
    assert v[0] == 0 and v[1] == 1 and v[2] == 2

    # Repr.

    v = Vec(1/9., 2/9., 3/9.)
    assert v == eval(repr(v))

    # Sequence length.

    v = Vec()
    assert len(v) == 3

    # Element setting.

    v = Vec()
    v[0] = 10
    v[1] = 11
    v[2] = 12
    assert v[0] == 10 and v[1] == 11 and v[2] == 12

    try:
        v[-4] = 0           # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    try:
        v[3] = 0           # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    try:
        v[1] = "a"           # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    # Assignment.

    v1 = Vec(1)
    
    v2 = v1
    assert v2[0] == 1 and v2[1] == 1 and v2[2] == 1
    v1[0] = 2
    assert v2[0] == 2 and v2[1] == 1 and v2[2] == 1
    
    # Comparison operators.

    v1 = Vec(20, 20, 0)
    v2 = Vec(20, 20, 0)
    v3 = Vec(20, 21, 0)

    assert v1 == v2
    assert v1 != v3
    assert not (v1 < v2)
    assert v1 < v3
    assert v1 <= v2
    assert v1 <= v3
    assert not (v3 <= v1)
    assert not (v2 > v1)
    assert v3 > v1
    assert v2 >= v1
    assert v3 >= v1
    assert not (v1 >= v3)
    
    # Epsilon equality.

    e = 0.005
    v1 = Vec(1)
    v2 = Vec(1 + e)

    assert v1.equalWithAbsError(v2, e)
    assert v2.equalWithAbsError(v1, e)

    e = 0.003
    v1 = Vec(10)
    v2 = Vec(10 + 10 * e)

    assert v1.equalWithRelError(v2, e)
    assert v2.equalWithRelError(v1, e)

    # Dot products.

    v1 = Vec(0, 1, 0)
    v2 = Vec(1, 0, 0)
    v3 = Vec(1, 1, 0)

    assert v1.dot(v2) == 0
    assert v1.dot(v3) == 1
    assert v1 ^ v2 == v1.dot(v2)
    assert v1 ^ v3 == v1.dot(v3)

    # Cross products.

    v1 = Vec(1, 0, 0)
    v2 = Vec(0, 1, 0)

    assert v1.cross(v2) == Vec(0, 0, 1)
    assert v2.cross(v1) == Vec(0, 0, -1)
    assert v1 % v2 == v1.cross(v2)
    assert v2 % v1 == v2.cross(v1)

    # Addition.

    v1 = Vec(10, 20, 30)
    v2 = Vec(30, 40, 50)

    assert v1 + v2 == Vec(40, 60, 80)
    assert v2 + v1 == v1 + v2
    assert v1 + 1 == Vec(11, 21, 31)
    assert 1 + v1 == v1 + 1

    # (with the switch to python2, we now allow ops between vectors and tuples)
    assert v1 + (1, 2, 3) == Vec(11, 22, 33)
    assert (1, 2, 3) + v1 == v1 + (1, 2, 3)

    # Subtraction and negation.

    v1 = Vec(10, 20, 30)
    v2 = Vec(30, 40, 50)

    assert v2 - v1 == Vec(20, 20, 20)
    assert v1 - 1 == Vec(9, 19, 29)
    assert 1 - v1 == - (v1 - 1)
    
    # (with the switch to python2, we now allow ops between vectors and tuples)
    assert v1 - (1, 2, 3) == Vec(9, 18, 27)
    assert (1, 2, 3) - v1 == - (v1 - (1, 2, 3))

    assert v1.negate() == Vec(-10, -20, -30)

    # Multiplication.

    v1 = Vec(1, 2, 3)
    v2 = Vec(3, 4, 5)
    
    assert v1 * v2 == Vec(3, 8, 15)
    assert v2 * v1 == v1 * v2
    assert 2 * v1 == Vec(2, 4, 6)
    assert v1 * 2 == 2 * v1

    assert v1 * V3i(3, 4, 5) == Vec(3, 8, 15)
    assert v1 * V3f(3, 4, 5) == Vec(3, 8, 15)
    assert v1 * V3d(3, 4, 5) == Vec(3, 8, 15)

    v1 *= 2
    assert v1 == Vec(2, 4, 6)
    v1 = Vec(1, 2, 3)

    # (with the switch to python2, we now allow ops between vectors and tuples)
    assert v1 * (1, 2, 3) == Vec(1, 4, 9)
    assert (1, 2, 3) * v1 == v1 * (1, 2, 3)

    # Division.

    v1 = Vec(10, 20, 40)
    v2 = Vec(2, 4, 8)
    
    assert v1 / v2 == Vec(10/2, 20/4, 40/8)
    assert v1 / 2 == Vec(10/2, 20/2, 40/2)
    assert Vec(40) / v1 == Vec(40/10, 40/20, 40/40)

    # (with the switch to python2, we now allow ops between vectors and tuples)
    assert v1 / (1, 2, 4) == Vec(10, 10, 10)
    assert Vec(50, 40, 80) / v1 == Vec(5, 2, 2)

    assert v1 / V3i (2, 4, 8) == Vec(10/2, 20/4, 40/8)
    assert v1 / V3f (2, 4, 8) == Vec(10/2, 20/4, 40/8)
    assert v1 / V3d (2, 4, 8) == Vec(10/2, 20/4, 40/8)
    assert v1 / (2, 4, 8) == Vec(10/2, 20/4, 40/8)
    assert v1 / [2, 4, 8] == Vec(10/2, 20/4, 40/8)

    v1 = Vec(10, 20, 40)
    v1 /= 2
    assert v1 == Vec(10/2, 20/2, 40/2)
    
    v1 = Vec(10, 20, 40)
    v1 /= V3i (2, 4, 8)
    assert v1 == Vec(10/2, 20/4, 40/8)
    
    v1 = Vec(10, 20, 40)
    v1 /= V3f (2, 4, 8)
    assert v1 == Vec(10/2, 20/4, 40/8)

    v1 = Vec(10, 20, 40)
    v1 /= V3d (2, 4, 8)
    assert v1 == Vec(10/2, 20/4, 40/8)

    v1 = Vec(10, 20, 40)
    v1 /= (2, 4, 8)
    assert v1 == Vec(10/2, 20/4, 40/8)

    v1 = Vec(10, 20, 40)
    v1 /= [2, 4, 8]
    assert v1 == Vec(10/2, 20/4, 40/8)

    # Length.

    if (Vec != V3i):
       v = Vec(1, 2, 3)
       assert equal(v.length(), sqrt(1*1 + 2*2 + 3*3), v.baseTypeEpsilon())
    else:
        v = Vec(1, 2, 3)
        assert v.length() == round(sqrt(1*1 + 2*2 + 3*3))
        v = Vec(2, 3, 4)
        assert v.length() == round(sqrt(2*2 + 3*3 + 4*4))

    v = Vec(1, 2, 3)
    assert v.length2() == 1*1 + 2*2 + 3*3

    # Normalizing.

    if (Vec != V3i):
       v = Vec(1, 2, 3)
       v.normalize()
       assert equal(v.length(), 1, v.baseTypeEpsilon())

       v = Vec(1, 2, 3)
       v.normalizeExc()
       assert equal(v.length(), 1, v.baseTypeEpsilon())
       v = Vec(0)
       try:
           v.normalizeExc()        # This should raise an exception.
       except:
           pass
       else:
           assert 0                # We shouldn't get here.
       
       v = Vec(1, 2, 3)
       v.normalizeNonNull()
       assert equal(v.length(), 1, v.baseTypeEpsilon())

       v = Vec(1, 2, 3)
       assert equal(v.normalized().length(), 1, v.baseTypeEpsilon())

       v = Vec(1, 2, 3)
       assert equal(v.normalizedExc().length(), 1, v.baseTypeEpsilon())
       v = Vec(0)
       try:
           v.normalizedExc()  # This should raise an exception.
       except:
           pass
       else:
           assert 0              # We shouldn't get here.
       
       v = Vec(1, 2, 3)
       assert equal(v.normalizedNonNull().length(), 1, v.baseTypeEpsilon())

    else:
       v = Vec(0, 1, 0)
       v.normalize()
       assert v.length() == 1

       v = Vec(1, 2, 3)
       try:
           v.normalize()        # This should raise an exception.
       except:
           pass
       else:
           assert 0                # We shouldn't get here.
        
       v = Vec(0, 1, 0)
       v.normalizeExc()
       assert v.length() == 1

       v = Vec(1, 2, 3)
       try:
           v.normalizeExc()        # This should raise an exception.
       except:
           pass
       else:
           assert 0                # We shouldn't get here.
        
       v = Vec(0, 1, 0)
       v.normalizeNonNull()
       assert v.length() == 1

       v = Vec(1, 2, 3)
       try:
           v.normalizeNonNull()        # This should raise an exception.
       except:
           pass
       else:
           assert 0                # We shouldn't get here.
        
       v = Vec(0, 1, 0)
       assert v.normalized().length() == 1

       v = Vec(1, 2, 3)
       try:
           v.normalized()        # This should raise an exception.
       except:
           pass
       else:
           assert 0                # We shouldn't get here.
        
       v = Vec(0, 1, 0)
       assert v.normalizedExc().length() == 1

       v = Vec(1, 2, 3)
       try:
           v.normalizedExc()        # This should raise an exception.
       except:
           pass
       else:
           assert 0                # We shouldn't get here.
        
       v = Vec(0, 1, 0)
       assert v.normalizeNonNull().length() == 1

       v = Vec(1, 2, 3)
       try:
           v.normalizedNonNull()  # This should raise an exception.
       except:
           pass
       else:
           assert 0                  # We shouldn't get here.
        
    # Projection.

    if (Vec != V3i):
        s = Vec(2, 0, 0)
        t = Vec(1, 1, 0)
        assert t.project(s) == Vec(1, 0, 0)

    # Orthogonal.

    if (Vec != V3i):
        s = Vec(2, 0, 0)
        t = Vec(1, 1, 0)
        o = s.orthogonal(t)
        assert iszero(o ^ s, s.baseTypeEpsilon())

    # Reflect.

    if (Vec != V3i):
        s = Vec(1, 1, 0)
        t = Vec(2, 0, 0)
        r = s.reflect(t)
        assert equal(abs(s ^ t), abs(r ^ t), s.baseTypeEpsilon())

    # Closest vertex.

    v0 = Vec(0, 0, 0)
    v1 = Vec(5, 0, 0)
    v2 = Vec(0, 5, 0)
    
    p = Vec(1, 1, 0)
    assert p.closestVertex(v0, v1, v2) == v0

    p = Vec(4, 1, 0)
    assert p.closestVertex(v0, v1, v2) == v1

    p = Vec(1, 4, 0)
    assert p.closestVertex(v0, v1, v2) == v2


    print ("ok")

    return

def testV3 ():

    print ("V3i")
    testV3x (V3i)
    print ("V3f")
    testV3x (V3f)
    print ("V3d")
    testV3x (V3d)

testList.append (('testV3',testV3))


# -------------------------------------------------------------------------
# Tests for V3xArray

def testV3xArray (Array, Vec, Arrayx):
    
    # Constructors (and element access).

    a = Array (3)

    a[0] = Vec(0)
    a[1] = Vec(1)
    a[2] = Vec(2)

    assert a[0] == Vec(0)
    assert a[1] == Vec(1)
    assert a[2] == Vec(2)

    a[0].setValue(10,10,10)
    a[1].setValue(11,11,11)
    a[2].setValue(12,12,12)

    assert a[0] == Vec(10)
    assert a[1] == Vec(11)
    assert a[2] == Vec(12)

    # explicit constructors across types
    af = V3fArray(a)
    assert a[0] == Vec(af[0])
    assert a[1] == Vec(af[1])
    assert a[2] == Vec(af[2])
    ad = V3dArray(a)
    assert a[0] == Vec(ad[0])
    assert a[1] == Vec(ad[1])
    assert a[2] == Vec(ad[2])
    ai = V3iArray(a)
    assert a[0] == Vec(ai[0])
    assert a[1] == Vec(ai[1])
    assert a[2] == Vec(ai[2])


    # Element setting.

    a = Array(2)

    try:
        a[-3] = Vec(0)        # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.   

    try:
        a[3] = Vec(0)   # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    try:
        a[1] = "a"         # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    # Assignment.

    a = Array(2)
    a[0] = Vec(0)
    a[1] = Vec(1)
    
    b = Array(2)
    b[0] = Vec(0)
    b[1] = Vec(1)
    
    c = Array(2)
    c[0] = Vec(10)
    c[1] = Vec(11)

    # TODO: make equality work correctly.
    #assert a == b
    assert a != c
    
    # Dot products.

    a = Array(2)
    a[0] = Vec(1, 2, 3)
    a[1] = Vec(4, 5, 6)

    b = Array(2)
    b[0] = Vec(7, 8, 9)
    b[1] = Vec(10, 11, 12)

    r = a.dot(b)
    assert r[0] == 1*7 + 2*8 + 3*9
    assert r[1] == 4*10 + 5*11 + 6*12

    c = Vec(13, 14, 15)
    r = a.dot(c)
    assert r[0] == 1*13 + 2*14 + 3*15
    assert r[1] == 4*13 + 5*14 + 6*15

    d = Array(3)
    try:
        a.dot(d)        # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.   
    
    
    # Cross products.

    a = Array(2)
    a[0] = Vec(1, 2, 3)
    a[1] = Vec(4, 5, 6)

    b = Array(2)
    b[0] = Vec(7, 8, 9)
    b[1] = Vec(10, 11, 12)

    r = a.cross(b)
    assert r[0] == Vec(1, 2, 3) % Vec(7, 8, 9)
    assert r[1] == Vec(4, 5, 6) % Vec(10, 11, 12)

    c = Vec(13, 14, 15)
    r = a.cross(c)
    assert r[0] == Vec(1, 2, 3) % Vec(13, 14, 15)
    assert r[1] == Vec(4, 5, 6) % Vec(13, 14, 15)

    d = Array(3)
    try:
        a.cross(d)        # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.   

    # Addition.

    a = Array(2)
    a[0] = Vec(1, 2, 3)
    a[1] = Vec(4, 5, 6)

    b = Array(2)
    b[0] = Vec(7, 8, 9)
    b[1] = Vec(10, 11, 12)

    r = a + b
    assert r[0] == Vec(1+7, 2+8, 3+9)
    assert r[1] == Vec(4+10, 5+11, 6+12)

    r = a + Vec(10)
    assert r[0] == Vec(1+10, 2+10, 3+10)
    assert r[1] == Vec(4+10, 5+10, 6+10)

    v = Vec(11)
    r = v + a 
    assert r[0] == Vec(11+1, 11+2, 11+3)
    assert r[1] == Vec(11+4, 11+5, 11+6)

    a += b
    assert a[0] == Vec(1+7, 2+8, 3+9)
    assert a[1] == Vec(4+10, 5+11, 6+12)

    a[0] = Vec(1, 2, 3)
    a[1] = Vec(4, 5, 6)

    a += Vec(10)
    assert a[0] == Vec(1+10, 2+10, 3+10)
    assert a[1] == Vec(4+10, 5+10, 6+10)

    c = Array(3)

    try:
        a + c                # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.   

    try:
        a += c                # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.   

    # Subtraction.

    a = Array(2)
    a[0] = Vec(1, 2, 3)
    a[1] = Vec(4, 5, 6)

    b = Array(2)
    b[0] = Vec(7, 8, 9)
    b[1] = Vec(10, 11, 12)

    r = a - b
    assert r[0] == Vec(1-7, 2-8, 3-9)
    assert r[1] == Vec(4-10, 5-11, 6-12)

    r = a - Vec(10)
    assert r[0] == Vec(1-10, 2-10, 3-10)
    assert r[1] == Vec(4-10, 5-10, 6-10)

    v = Vec(11)
    r = v - a 
    assert r[0] == Vec(11-1, 11-2, 11-3)
    assert r[1] == Vec(11-4, 11-5, 11-6)

    a -= b
    assert a[0] == Vec(1-7, 2-8, 3-9)
    assert a[1] == Vec(4-10, 5-11, 6-12)

    a[0] = Vec(1, 2, 3)
    a[1] = Vec(4, 5, 6)

    a -= Vec(10)
    assert a[0] == Vec(1-10, 2-10, 3-10)
    assert a[1] == Vec(4-10, 5-10, 6-10)

    c = Array(3)

    try:
        a - c                # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.   

    try:
        a -= c                # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.   

    # Negation.

    a = Array(2)
    a[0] = Vec(1, 2, 3)
    a[1] = Vec(4, 5, 6)

    r = -a
    assert r[0] == Vec(-1, -2, -3)
    assert r[1] == Vec(-4, -5, -6)

    # Multiplication.

    a = Array(2)
    a[0] = Vec(1, 2, 3)
    a[1] = Vec(4, 5, 6)

    r = a * 10
    assert r[0] == Vec(1, 2, 3) * 10
    assert r[1] == Vec(4, 5, 6) * 10

    b = Arrayx(2)
    b[0] = 10
    b[1] = 11

    r = a * b
    assert r[0] == Vec(1, 2, 3) * 10
    assert r[1] == Vec(4, 5, 6) * 11
    
    a *= 10
    assert a[0] == Vec(1, 2, 3) * 10
    assert a[1] == Vec(4, 5, 6) * 10

    a[0] = Vec(1, 2, 3)
    a[1] = Vec(4, 5, 6)

    a *= b
    assert a[0] == Vec(1, 2, 3) * 10
    assert a[1] == Vec(4, 5, 6) * 11

    a[0] = Vec(1, 2, 3)
    a[1] = Vec(4, 5, 6)

    b = Array(2)
    b[0] = Vec(7, 8, 9)
    b[1] = Vec(10, 11, 12)

    r = a * b
    assert r[0] == Vec(1*7, 2*8, 3*9)
    assert r[1] == Vec(4*10, 5*11, 6*12)

    v = Vec(13, 14, 15)

    r = a * v
    assert r[0] == Vec(1*13, 2*14, 3*15)
    assert r[1] == Vec(4*13, 5*14, 6*15)

    r = v * a
    assert r[0] == Vec(1*13, 2*14, 3*15)
    assert r[1] == Vec(4*13, 5*14, 6*15)

    a *= b
    assert a[0] == Vec(1*7, 2*8, 3*9)
    assert a[1] == Vec(4*10, 5*11, 6*12)

    a[0] = Vec(1, 2, 3)
    a[1] = Vec(4, 5, 6)

    a *= v
    assert a[0] == Vec(1*13, 2*14, 3*15)
    assert a[1] == Vec(4*13, 5*14, 6*15)

    d = Array(3)
    try:
        a * d                # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.   

    try:
        a *= d                # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.   

    # Division.

    a = Array(2)
    a[0] = Vec(1.0, 2.0, 3.0)
    a[1] = Vec(4.0, 5.0, 6.0)

    r = a / 10
    assert r[0] == Vec(1.0, 2.0, 3.0) / 10
    assert r[1] == Vec(4.0, 5.0, 6.0) / 10

    b = Arrayx(2)
    b[0] = 10
    b[1] = 11

    r = a / b
    assert r[0] == Vec(1.0, 2.0, 3.0) / 10
    assert r[1] == Vec(4.0, 5.0, 6.0) / 11
    
    a /= 10
    assert a[0] == Vec(1.0, 2.0, 3.0) / 10
    assert a[1] == Vec(4.0, 5.0, 6.0) / 10

    a[0] = Vec(1.0, 2.0, 3.0)
    a[1] = Vec(4.0, 5.0, 6.0)

    a /= b
    assert a[0] == Vec(1.0, 2.0, 3.0) / 10
    assert a[1] == Vec(4.0, 5.0, 6.0) / 11

    a[0] = Vec(1.0, 2.0, 3.0)
    a[1] = Vec(4.0, 5.0, 6.0)

    b = Array(2)
    b[0] = Vec(7.0, 8.0, 9.0)
    b[1] = Vec(10.0, 11.0, 12.0)

    r = a / b
    assert r[0] == Vec(1.0/7, 2.0/8, 3.0/9)
    assert r[1] == Vec(4.0/10, 5.0/11, 6.0/12)

    v = Vec(13.0, 14.0, 15.0)

    r = a / v
    assert r[0] == Vec(1.0/13, 2.0/14, 3.0/15)
    assert r[1] == Vec(4.0/13, 5.0/14, 6.0/15)

    # TODO: Figure out why "v / a" is illegal, even though the
    # add_arithmetic_math_functions() routine in PyImathFixedArray.h
    # should make it possible.
    #r = v / a
    #assert r[0] == Vec(1.0/13, 2.0/14, 3.0/15)
    #assert r[1] == Vec(4.0/13, 5.0/14, 6.0/15)

    a /= b
    assert a[0] == Vec(1.0/7, 2.0/8, 3.0/9)
    assert a[1] == Vec(4.0/10, 5.0/11, 6.0/12)

    a[0] = Vec(1.0, 2.0, 3.0)
    a[1] = Vec(4.0, 5.0, 6.0)

    a /= v
    assert a[0] == Vec(1.0/13, 2.0/14, 3.0/15)
    assert a[1] == Vec(4.0/13, 5.0/14, 6.0/15)

    d = Array(3)
    try:
        a / d                # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.   

    try:
        a /= d                # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.   

    # Length.

    v0 = Vec(1, 2, 3)
    v1 = Vec(4, 5, 6)

    a = Array(2)
    a[0] = v0
    a[1] = v1

    l = a.length()
    assert (l[0] == v0.length())
    assert (l[1] == v1.length())

    l = a.length2()
    assert (l[0] == v0.length2())
    assert (l[1] == v1.length2())
    
    # Normalizing.

    if (Vec != V3i):

        a[0] = Vec(1, 2, 3)
        a[1] = Vec(4, 5, 6)

        r = a.normalized();
        assert r[0] == Vec(1, 2, 3).normalized()
        assert r[1] == Vec(4, 5, 6).normalized()

        a.normalize();
        assert a[0] == Vec(1, 2, 3).normalized()
        assert a[1] == Vec(4, 5, 6).normalized()

    print ("ok")

    return

def testV3Array ():

    print ("V3iArray")
    testV3xArray (V3iArray, V3i, IntArray)
    print ("V3fArray")
    testV3xArray (V3fArray, V3f, FloatArray)
    print ("V3dArray")
    testV3xArray (V3dArray, V3d, DoubleArray)

testList.append (('testV3Array',testV3Array))


# -------------------------------------------------------------------------
# Tests for Vec --> Vec conversions

def testV2xConversions (Vec):

    # Assignment
    
    v1 = Vec(0, 1)

    v2 = V2i (v1)
    assert v2[0] == 0 and v2[1] == 1

    v2 = V2f (v1)
    assert v2[0] == 0 and v2[1] == 1

    v2 = V2d (v1)
    assert v2[0] == 0 and v2[1] == 1

    # The += operator
    
    v2 = Vec (1, 2)
    v2 += V2i (v1)
    assert v2[0] == 1 and v2[1] == 3

    v2 = Vec (1, 2)
    v2 += V2f (v1)
    assert v2[0] == 1 and v2[1] == 3

    v2 = Vec (1, 2)
    v2 += V2d (v1)
    assert v2[0] == 1 and v2[1] == 3

    # The -= operator
    
    v2 = Vec (1, 2)
    v2 -= V2i (v1)
    assert v2[0] == 1 and v2[1] == 1

    v2 = Vec (1, 2)
    v2 -= V2f (v1)
    assert v2[0] == 1 and v2[1] == 1

    v2 = Vec (1, 2)
    v2 -= V2d (v1)
    assert v2[0] == 1 and v2[1] == 1

    # The *= operator
    
    v2 = Vec (1, 2)
    v2 *= V2i (v1)
    assert v2[0] == 0 and v2[1] == 2

    v2 = Vec (1, 2)
    v2 *= V2f (v1)
    assert v2[0] == 0 and v2[1] == 2

    v2 = Vec (1, 2)
    v2 *= V2d (v1)
    assert v2[0] == 0 and v2[1] == 2

    print ("ok")
    return


def testV3xConversions (Vec):

    # Assignment
    
    v1 = Vec(0, 1, 2)

    v2 = V3i (v1)
    assert v2[0] == 0 and v2[1] == 1 and v2[2] == 2

    v2 = V3f (v1)
    assert v2[0] == 0 and v2[1] == 1 and v2[2] == 2

    v2 = V3d (v1)
    assert v2[0] == 0 and v2[1] == 1 and v2[2] == 2

    # The += operator

    v2 = Vec (1, 2, 3)
    v2 += V3i (v1)
    assert v2[0] == 1 and v2[1] == 3 and v2[2] == 5
    
    v2 = Vec (1, 2, 3)
    v2 += V3f (v1)
    assert v2[0] == 1 and v2[1] == 3 and v2[2] == 5
    
    v2 = Vec (1, 2, 3)
    v2 += V3d (v1)
    assert v2[0] == 1 and v2[1] == 3 and v2[2] == 5

    # The -= operator

    v2 = Vec (1, 2, 3)
    v2 -= V3i (v1)
    assert v2[0] == 1 and v2[1] == 1 and v2[2] == 1
    
    v2 = Vec (1, 2, 3)
    v2 -= V3f (v1)
    assert v2[0] == 1 and v2[1] == 1 and v2[2] == 1
    
    v2 = Vec (1, 2, 3)
    v2 -= V3d (v1)
    assert v2[0] == 1 and v2[1] == 1 and v2[2] == 1

    # The *= operator
    
    v2 = Vec (1, 2, 3)
    v2 *= V3i (v1)
    assert v2[0] == 0 and v2[1] == 2 and v2[2] == 6
    
    v2 = Vec (1, 2, 3)
    v2 *= V3f (v1)
    assert v2[0] == 0 and v2[1] == 2 and v2[2] == 6
    
    v2 = Vec (1, 2, 3)
    v2 *= V3d (v1)
    assert v2[0] == 0 and v2[1] == 2 and v2[2] == 6
    
    print ("ok")
    return

# -------------------------------------------------------------------------
# Tests for V4x

def testV4x (Vec):
    
    # Constructors (and element access).

    v = Vec()
    assert v[0] == 0 and v[1] == 0 and v[2] == 0 and v[3] == 0

    v = Vec(1)
    assert v[0] == 1 and v[1] == 1 and v[2] == 1 and v[3] == 1

    v = Vec(0, 1, 2, 3)
    assert v[0] == 0 and v[1] == 1 and v[2] == 2 and v[3] == 3

    v = Vec((0, 1, 2, 3))
    assert v[0] == 0 and v[1] == 1 and v[2] == 2 and v[3] == 3

    v = Vec([0, 1, 2, 3])
    assert v[0] == 0 and v[1] == 1 and v[2] == 2 and v[3] == 3

    v = Vec()
    v.setValue(0, 1, 2, 3)
    assert v[0] == 0 and v[1] == 1 and v[2] == 2 and v[3] == 3

    # Repr.

    v = Vec(1/9., 2/9., 3/9., 4./9.)
    assert v == eval(repr(v))

    # Sequence length.

    v = Vec()
    assert len(v) == 4

    # Element setting.

    v = Vec()
    v[0] = 10
    v[1] = 11
    v[2] = 12
    v[3] = 13
    assert v[0] == 10 and v[1] == 11 and v[2] == 12 and v[3] == 13

    try:
        # TODO why does this have to be -5 and not -4?
        v[-5] = 0           # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    try:
        v[4] = 0           # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    try:
        v[1] = "a"           # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    # Assignment.

    v1 = Vec(1)
    
    v2 = v1
    assert v2[0] == 1 and v2[1] == 1 and v2[2] == 1 and v2[3] == 1
    v1[0] = 2
    assert v2[0] == 2 and v2[1] == 1 and v2[2] == 1 and v2[3] == 1
    
    # Comparison operators.

    v1 = Vec(20, 20, 20, 20)
    v2 = Vec(20, 20, 20, 20)
    v3 = Vec(20, 20, 20, 21)

    assert v1 == v2
    assert v1 != v3
    assert not (v1 < v2)
    assert v1 < v3
    assert v1 <= v2
    assert v1 <= v3
    assert not (v3 <= v1)
    assert not (v2 > v1)
    assert v3 > v1
    assert v2 >= v1
    assert v3 >= v1
    assert not (v1 >= v3)
    
    # Epsilon equality.

    e = 0.005
    v1 = Vec(1)
    v2 = Vec(1 + e)

    assert v1.equalWithAbsError(v2, e)
    assert v2.equalWithAbsError(v1, e)

    e = 0.003
    v1 = Vec(10)
    v2 = Vec(10 + 10 * e)

    assert v1.equalWithRelError(v2, e)
    assert v2.equalWithRelError(v1, e)

    # Dot products.

    v1 = Vec(0, 1, 0, 1)
    v2 = Vec(1, 0, 0, 0)
    v3 = Vec(1, 1, 1, 1)

    assert v1.dot(v2) == 0
    assert v1.dot(v3) == 2
    assert v1 ^ v2 == v1.dot(v2)
    assert v1 ^ v3 == v1.dot(v3)

    # Addition.

    v1 = Vec(10, 20, 30, 40)
    v2 = Vec(30, 40, 50, 60)

    assert v1 + v2 == Vec(40, 60, 80, 100)
    assert v2 + v1 == v1 + v2
    assert v1 + 1 == Vec(11, 21, 31, 41)
    assert 1 + v1 == v1 + 1

    # (with the switch to python2, we now allow ops between vectors and tuples)
    assert v1 + (1, 2, 3, 4) == Vec(11, 22, 33, 44)
    assert (1, 2, 3, 4) + v1 == v1 + (1, 2, 3, 4)

    # Subtraction and negation.

    v1 = Vec(10, 20, 30, 40)
    v2 = Vec(30, 40, 50, 60)

    assert v2 - v1 == Vec(20, 20, 20, 20)
    assert v1 - 1 == Vec(9, 19, 29, 39)
    assert 1 - v1 == - (v1 - 1)
    
    # (with the switch to python2, we now allow ops between vectors and tuples)
    assert v1 - (1, 2, 3, 4) == Vec(9, 18, 27, 36)
    assert (1, 2, 3, 4) - v1 == - (v1 - (1, 2, 3, 4))

    assert v1.negate() == Vec(-10, -20, -30, -40)

    # Multiplication.

    v1 = Vec(1, 2, 3, 4)
    v2 = Vec(3, 4, 5, 6)
    
    assert v1 * v2 == Vec(3, 8, 15, 24)
    assert v2 * v1 == v1 * v2
    assert 2 * v1 == Vec(2, 4, 6, 8)
    assert v1 * 2 == 2 * v1

    assert v1 * V4i(3, 4, 5, 6) == Vec(3, 8, 15, 24)
    assert v1 * V4f(3, 4, 5, 6) == Vec(3, 8, 15, 24)
    assert v1 * V4d(3, 4, 5, 6) == Vec(3, 8, 15, 24)

    v1 *= 2
    assert v1 == Vec(2, 4, 6, 8)
    v1 = Vec(1, 2, 3, 4)

    # (with the switch to python2, we now allow ops between vectors and tuples)
    assert v1 * (1, 2, 3, 4) == Vec(1, 4, 9, 16)
    assert (1, 2, 3, 4) * v1 == v1 * (1, 2, 3, 4)

    # Division.

    v1 = Vec(10, 20, 40, 80)
    v2 = Vec(2, 4, 8, 10)
    
    assert v1 / v2 == Vec(10/2, 20/4, 40/8, 80/10)
    assert v1 / 2 == Vec(10/2, 20/2, 40/2, 80/2)
    assert Vec(80) / v1 == Vec(80/10, 80/20, 80/40, 80/80)

    # (with the switch to python2, we now allow ops between vectors and tuples)
    assert v1 / (1, 2, 4, 8) == Vec(10, 10, 10, 10)
    assert Vec(50, 40, 80, 160) / v1 == Vec(5, 2, 2, 2)

    assert v1 / V4i (2, 4, 8, 10) == Vec(10/2, 20/4, 40/8, 80/10)
    assert v1 / V4f (2, 4, 8, 10) == Vec(10/2, 20/4, 40/8, 80/10)
    assert v1 / V4d (2, 4, 8, 10) == Vec(10/2, 20/4, 40/8, 80/10)
    assert v1 / (2, 4, 8, 10) == Vec(10/2, 20/4, 40/8, 80/10)
    assert v1 / [2, 4, 8, 10] == Vec(10/2, 20/4, 40/8, 80/10)

    v1 = Vec(10, 20, 40, 80)
    v1 /= 2
    assert v1 == Vec(10/2, 20/2, 40/2, 80/2)
    
    v1 = Vec(10, 20, 40, 80)
    v1 /= V4i (2, 4, 8, 10)
    assert v1 == Vec(10/2, 20/4, 40/8, 80/10)
    
    v1 = Vec(10, 20, 40, 80)
    v1 /= V4f (2, 4, 8, 10)
    assert v1 == Vec(10/2, 20/4, 40/8, 80/10)

    v1 = Vec(10, 20, 40, 80)
    v1 /= V4d (2, 4, 8, 10)
    assert v1 == Vec(10/2, 20/4, 40/8, 80/10)

    v1 = Vec(10, 20, 40, 80)
    v1 /= (2, 4, 8, 10)
    assert v1 == Vec(10/2, 20/4, 40/8, 80/10)

    v1 = Vec(10, 20, 40, 80)
    v1 /= [2, 4, 8, 10]
    assert v1 == Vec(10/2, 20/4, 40/8, 80/10)

    # Length.

    if (Vec != V4i):
       v = Vec(1, 2, 3, 4)
       assert equal(v.length(), sqrt(1*1 + 2*2 + 3*3 + 4*4), 10.0*v.baseTypeEpsilon())
    else:
        v = Vec(1, 2, 3, 4)
        assert v.length() == round(sqrt(1*1 + 2*2 + 3*3 + 4*4))
        v = Vec(2, 3, 4, 5)
        assert v.length() == round(sqrt(2*2 + 3*3 + 4*4 + 5*5))

    v = Vec(1, 2, 3, 4)
    assert v.length2() == 1*1 + 2*2 + 3*3 + 4*4

    # Normalizing.

    if (Vec != V4i):
       v = Vec(1, 2, 3, 4)
       v.normalize()
       assert equal(v.length(), 1, v.baseTypeEpsilon())

       v = Vec(1, 2, 3, 4)
       v.normalizeExc()
       assert equal(v.length(), 1, v.baseTypeEpsilon())
       v = Vec(0)
       try:
           v.normalizeExc()        # This should raise an exception.
       except:
           pass
       else:
           assert 0                # We shouldn't get here.
       
       v = Vec(1, 2, 3, 4)
       v.normalizeNonNull()
       assert equal(v.length(), 1, v.baseTypeEpsilon())

       v = Vec(1, 2, 3, 4)
       assert equal(v.normalized().length(), 1, v.baseTypeEpsilon())

       v = Vec(1, 2, 3, 4)
       assert equal(v.normalizedExc().length(), 1, v.baseTypeEpsilon())
       v = Vec(0)
       try:
           v.normalizedExc()  # This should raise an exception.
       except:
           pass
       else:
           assert 0              # We shouldn't get here.
       
       v = Vec(1, 2, 3, 4)
       assert equal(v.normalizedNonNull().length(), 1, v.baseTypeEpsilon())

    else:
       v = Vec(0, 0, 0, 1)
       v.normalize()
       assert v.length() == 1

       v = Vec(1, 2, 3, 4)
       try:
           v.normalize()        # This should raise an exception.
       except:
           pass
       else:
           assert 0                # We shouldn't get here.
        
       v = Vec(0, 0, 0, 1)
       v.normalizeExc()
       assert v.length() == 1

       v = Vec(1, 2, 3, 4)
       try:
           v.normalizeExc()        # This should raise an exception.
       except:
           pass
       else:
           assert 0                # We shouldn't get here.
        
       v = Vec(0, 0, 0, 1)
       v.normalizeNonNull()
       assert v.length() == 1

       v = Vec(1, 2, 3, 4)
       try:
           v.normalizeNonNull()        # This should raise an exception.
       except:
           pass
       else:
           assert 0                # We shouldn't get here.
        
       v = Vec(0, 0, 0, 1)
       assert v.normalized().length() == 1

       v = Vec(1, 2, 3, 4)
       try:
           v.normalized()        # This should raise an exception.
       except:
           pass
       else:
           assert 0                # We shouldn't get here.
        
       v = Vec(0, 0, 0, 1)
       assert v.normalizedExc().length() == 1

       v = Vec(1, 2, 3, 4)
       try:
           v.normalizedExc()        # This should raise an exception.
       except:
           pass
       else:
           assert 0                # We shouldn't get here.
        
       v = Vec(0, 0, 0, 1)
       assert v.normalizeNonNull().length() == 1

       v = Vec(1, 2, 3, 4)
       try:
           v.normalizedNonNull()  # This should raise an exception.
       except:
           pass
       else:
           assert 0                  # We shouldn't get here.
        
    # Projection.

    if (Vec != V4i):
        s = Vec(0, 0, 0, 2)
        t = Vec(1, 1, 1, 1)
        assert t.project(s) == Vec(0, 0, 0, 1)

    # Orthogonal.

    if (Vec != V4i):
        s = Vec(0, 0, 0, 2)
        t = Vec(1, 1, 1, 1)
        o = s.orthogonal(t)
        assert iszero(o ^ s, s.baseTypeEpsilon())

    # Reflect.

    if (Vec != V4i):
        s = Vec(1, 1, 1, 1)
        t = Vec(0, 0, 0, 2)
        r = s.reflect(t)
        assert equal(abs(s ^ t), abs(r ^ t), s.baseTypeEpsilon())

    print ("ok")

    return

def testV4 ():

    print ("V4i")
    testV4x (V4i)
    print ("V4f")
    testV4x (V4f)
    print ("V4d")
    testV4x (V4d)

testList.append (('testV4',testV4))


# -------------------------------------------------------------------------
# Tests for V4xArray

def testV4xArray (Array, Vec, Arrayx):
    
    # Constructors (and element access).

    a = Array (4)

    a[0] = Vec(0)
    a[1] = Vec(1)
    a[2] = Vec(2)
    a[3] = Vec(3)

    assert a[0] == Vec(0)
    assert a[1] == Vec(1)
    assert a[2] == Vec(2)
    assert a[3] == Vec(3)

    a[0].setValue(10,10,10,10)
    a[1].setValue(11,11,11,11)
    a[2].setValue(12,12,12,12)
    a[3].setValue(13,13,13,13)

    assert a[0] == Vec(10)
    assert a[1] == Vec(11)
    assert a[2] == Vec(12)
    assert a[3] == Vec(13)

    # Element setting.

    a = Array(2)

    try:
        a[-3] = Vec(0)        # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.   

    try:
        a[4] = Vec(0)   # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    try:
        a[1] = "a"         # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    # Assignment.

    a = Array(2)
    a[0] = Vec(0)
    a[1] = Vec(1)
    
    b = Array(2)
    b[0] = Vec(0)
    b[1] = Vec(1)
    
    c = Array(2)
    c[0] = Vec(10)
    c[1] = Vec(11)

    # TODO: make equality work correctly.
    #assert a == b
    assert a != c
    
    # Dot products.

    a = Array(2)
    a[0] = Vec(1, 2, 3, 4)
    a[1] = Vec(4, 5, 6, 7)

    b = Array(2)
    b[0] = Vec(7, 8, 9, 10)
    b[1] = Vec(10, 11, 12, 13)

    r = a.dot(b)
    assert r[0] == 1*7 + 2*8 + 3*9 + 4*10
    assert r[1] == 4*10 + 5*11 + 6*12 + 7*13

    c = Vec(13, 14, 15, 16)
    r = a.dot(c)
    assert r[0] == 1*13 + 2*14 + 3*15 + 4*16
    assert r[1] == 4*13 + 5*14 + 6*15 + 7*16

    d = Array(3)
    try:
        a.dot(d)        # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.   
    
    # Addition.

    a = Array(2)
    a[0] = Vec(1, 2, 3, 4)
    a[1] = Vec(4, 5, 6, 7)

    b = Array(2)
    b[0] = Vec(7, 8, 9, 10)
    b[1] = Vec(10, 11, 12, 13)

    r = a + b
    assert r[0] == Vec(1+7, 2+8, 3+9, 4+10)
    assert r[1] == Vec(4+10, 5+11, 6+12, 7+13)

    r = a + Vec(10)
    assert r[0] == Vec(1+10, 2+10, 3+10, 4+10)
    assert r[1] == Vec(4+10, 5+10, 6+10, 7+10)

    v = Vec(11)
    r = v + a 
    assert r[0] == Vec(11+1, 11+2, 11+3, 11+4)
    assert r[1] == Vec(11+4, 11+5, 11+6, 11+7)

    a += b
    assert a[0] == Vec(1+7, 2+8, 3+9, 4+10)
    assert a[1] == Vec(4+10, 5+11, 6+12, 7+13)

    a[0] = Vec(1, 2, 3, 4)
    a[1] = Vec(4, 5, 6, 7)

    a += Vec(10)
    assert a[0] == Vec(1+10, 2+10, 3+10, 4+10)
    assert a[1] == Vec(4+10, 5+10, 6+10, 7+10)

    c = Array(3)

    try:
        a + c                # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.   

    try:
        a += c                # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.   

    # Subtraction.

    a = Array(2)
    a[0] = Vec(1, 2, 3, 4)
    a[1] = Vec(4, 5, 6, 7)

    b = Array(2)
    b[0] = Vec(7, 8, 9, 10)
    b[1] = Vec(10, 11, 12, 13)

    r = a - b
    assert r[0] == Vec(1-7, 2-8, 3-9, 4-10)
    assert r[1] == Vec(4-10, 5-11, 6-12, 7-13)

    r = a - Vec(10)
    assert r[0] == Vec(1-10, 2-10, 3-10, 4-10)
    assert r[1] == Vec(4-10, 5-10, 6-10, 7-10)

    v = Vec(11)
    r = v - a 
    assert r[0] == Vec(11-1, 11-2, 11-3, 11-4)
    assert r[1] == Vec(11-4, 11-5, 11-6, 11-7)

    a -= b
    assert a[0] == Vec(1-7, 2-8, 3-9, 4-10)
    assert a[1] == Vec(4-10, 5-11, 6-12, 7-13)

    a[0] = Vec(1, 2, 3, 4)
    a[1] = Vec(4, 5, 6, 7)

    a -= Vec(10)
    assert a[0] == Vec(1-10, 2-10, 3-10, 4-10)
    assert a[1] == Vec(4-10, 5-10, 6-10, 7-10)

    c = Array(3)

    try:
        a - c                # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.   

    try:
        a -= c                # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.   

    # Negation.

    a = Array(2)
    a[0] = Vec(1, 2, 3, 4)
    a[1] = Vec(4, 5, 6, 7)

    r = -a
    assert r[0] == Vec(-1, -2, -3, -4)
    assert r[1] == Vec(-4, -5, -6, -7)

    # Multiplication.

    a = Array(2)
    a[0] = Vec(1, 2, 3, 4)
    a[1] = Vec(4, 5, 6, 7)

    r = a * 10
    assert r[0] == Vec(1, 2, 3, 4) * 10
    assert r[1] == Vec(4, 5, 6, 7) * 10

    b = Arrayx(2)
    b[0] = 10
    b[1] = 11

    r = a * b
    assert r[0] == Vec(1, 2, 3, 4) * 10
    assert r[1] == Vec(4, 5, 6, 7) * 11
    
    a *= 10
    assert a[0] == Vec(1, 2, 3, 4) * 10
    assert a[1] == Vec(4, 5, 6, 7) * 10

    a[0] = Vec(1, 2, 3, 4)
    a[1] = Vec(4, 5, 6, 7)

    a *= b
    assert a[0] == Vec(1, 2, 3, 4) * 10
    assert a[1] == Vec(4, 5, 6, 7) * 11

    a[0] = Vec(1, 2, 3, 4)
    a[1] = Vec(4, 5, 6, 7)

    b = Array(2)
    b[0] = Vec(7, 8, 9, 10)
    b[1] = Vec(10, 11, 12, 13)

    r = a * b
    assert r[0] == Vec(1*7, 2*8, 3*9, 4*10)
    assert r[1] == Vec(4*10, 5*11, 6*12, 7*13)

    v = Vec(13, 14, 15, 16)

    r = a * v
    assert r[0] == Vec(1*13, 2*14, 3*15, 4*16)
    assert r[1] == Vec(4*13, 5*14, 6*15, 7*16)

    r = v * a
    assert r[0] == Vec(1*13, 2*14, 3*15, 4*16)
    assert r[1] == Vec(4*13, 5*14, 6*15, 7*16)

    a *= b
    assert a[0] == Vec(1*7, 2*8, 3*9, 4*10)
    assert a[1] == Vec(4*10, 5*11, 6*12, 7*13)

    a[0] = Vec(1, 2, 3, 4)
    a[1] = Vec(4, 5, 6, 7)

    a *= v
    assert a[0] == Vec(1*13, 2*14, 3*15, 4*16)
    assert a[1] == Vec(4*13, 5*14, 6*15, 7*16)

    d = Array(3)
    try:
        a * d                # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.   

    try:
        a *= d                # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.   

    # Division.

    a = Array(2)
    a[0] = Vec(1.0, 2.0, 3.0, 4.0)
    a[1] = Vec(4.0, 5.0, 6.0, 7.0)

    r = a / 10
    assert r[0] == Vec(1.0, 2.0, 3.0, 4.0) / 10
    assert r[1] == Vec(4.0, 5.0, 6.0, 7.0) / 10

    b = Arrayx(2)
    b[0] = 10
    b[1] = 11

    r = a / b
    assert r[0] == Vec(1.0, 2.0, 3.0, 4.0) / 10
    assert r[1] == Vec(4.0, 5.0, 6.0, 7.0) / 11
    
    a /= 10
    assert a[0] == Vec(1.0, 2.0, 3.0, 4.0) / 10
    assert a[1] == Vec(4.0, 5.0, 6.0, 7.0) / 10

    a[0] = Vec(1.0, 2.0, 3.0, 4.0)
    a[1] = Vec(4.0, 5.0, 6.0, 7.0)

    a /= b
    assert a[0] == Vec(1.0, 2.0, 3.0, 4.0) / 10
    assert a[1] == Vec(4.0, 5.0, 6.0, 7.0) / 11

    a[0] = Vec(1.0, 2.0, 3.0, 4.0)
    a[1] = Vec(4.0, 5.0, 6.0, 7.0)

    b = Array(2)
    b[0] = Vec(7.0, 8.0, 9.0, 10.0)
    b[1] = Vec(10.0, 11.0, 12.0, 13.0)

    r = a / b
    assert r[0] == Vec(1.0/7, 2.0/8, 3.0/9, 4.0/10)
    assert r[1] == Vec(4.0/10, 5.0/11, 6.0/12, 7.0/13)

    v = Vec(13.0, 14.0, 15.0, 16)

    r = a / v
    assert r[0] == Vec(1.0/13, 2.0/14, 3.0/15, 4.0/16)
    assert r[1] == Vec(4.0/13, 5.0/14, 6.0/15, 7.0/16)

    # TODO: Figure out why "v / a" is illegal, even though the
    # add_arithmetic_math_functions() routine in PyImathFixedArray.h
    # should make it possible.
    #r = v / a
    #assert r[0] == Vec(1.0/13, 2.0/14, 3.0/15)
    #assert r[1] == Vec(4.0/13, 5.0/14, 6.0/15)

    a /= b
    assert a[0] == Vec(1.0/7, 2.0/8, 3.0/9, 4.0/10)
    assert a[1] == Vec(4.0/10, 5.0/11, 6.0/12, 7.0/13)

    a[0] = Vec(1.0, 2.0, 3.0, 4.0)
    a[1] = Vec(4.0, 5.0, 6.0, 7.0)

    a /= v
    assert a[0] == Vec(1.0/13, 2.0/14, 3.0/15, 4.0/16)
    assert a[1] == Vec(4.0/13, 5.0/14, 6.0/15, 7.0/16)

    d = Array(3)
    try:
        a / d                # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.   

    try:
        a /= d                # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.   

    # Length.

    v0 = Vec(1, 2, 3, 4)
    v1 = Vec(4, 5, 6, 7)

    a = Array(2)
    a[0] = v0
    a[1] = v1

    l = a.length()
    assert (l[0] == v0.length())
    assert (l[1] == v1.length())

    l = a.length2()
    assert (l[0] == v0.length2())
    assert (l[1] == v1.length2())
    
    # Normalizing.

    if (Vec != V4i):

        a[0] = Vec(1, 2, 3, 4)
        a[1] = Vec(4, 5, 6, 7)

        r = a.normalized();
        assert r[0] == Vec(1, 2, 3, 4).normalized()
        assert r[1] == Vec(4, 5, 6, 7).normalized()

        a.normalize();
        assert a[0] == Vec(1, 2, 3, 4).normalized()
        assert a[1] == Vec(4, 5, 6, 7).normalized()

    print ("ok")

    return

def testV4Array ():

    print ("V4iArray")
    testV4xArray (V4iArray, V4i, IntArray)
    print ("V4fArray")
    testV4xArray (V4fArray, V4f, FloatArray)
    print ("V4dArray")
    testV4xArray (V4dArray, V4d, DoubleArray)

testList.append (('testV4Array',testV4Array))

def testV4xConversions (Vec):

    # Assignment
    
    v1 = Vec(0, 1, 2, 3)

    v2 = V4i (v1)
    assert v2[0] == 0 and v2[1] == 1 and v2[2] == 2 and v2[3] == 3

    v2 = V4f (v1)
    assert v2[0] == 0 and v2[1] == 1 and v2[2] == 2 and v2[3] == 3

    v2 = V4d (v1)
    assert v2[0] == 0 and v2[1] == 1 and v2[2] == 2 and v2[3] == 3

    # The += operator

    v2 = Vec (1, 2, 3, 4)
    v2 += V4i (v1)
    assert v2[0] == 1 and v2[1] == 3 and v2[2] == 5 and v2[3] == 7
    
    v2 = Vec (1, 2, 3, 4)
    v2 += V4f (v1)
    assert v2[0] == 1 and v2[1] == 3 and v2[2] == 5  and v2[3] == 7
    
    v2 = Vec (1, 2, 3, 4)
    v2 += V4d (v1)
    assert v2[0] == 1 and v2[1] == 3 and v2[2] == 5  and v2[3] == 7

    # The -= operator

    v2 = Vec (1, 2, 3, 4)
    v2 -= V4i (v1)
    assert v2[0] == 1 and v2[1] == 1 and v2[2] == 1 and v2[3] == 1
    
    v2 = Vec (1, 2, 3, 4)
    v2 -= V4f (v1)
    assert v2[0] == 1 and v2[1] == 1 and v2[2] == 1 and v2[3] == 1
    
    v2 = Vec (1, 2, 3, 4)
    v2 -= V4d (v1)
    assert v2[0] == 1 and v2[1] == 1 and v2[2] == 1 and v2[3] == 1

    # The *= operator
    
    v2 = Vec (1, 2, 3, 4)
    v2 *= V4i (v1)
    assert v2[0] == 0 and v2[1] == 2 and v2[2] == 6 and v2[3] == 12
    
    v2 = Vec (1, 2, 3, 4)
    v2 *= V4f (v1)
    assert v2[0] == 0 and v2[1] == 2 and v2[2] == 6 and v2[3] == 12
    
    v2 = Vec (1, 2, 3, 4)
    v2 *= V4d (v1)
    assert v2[0] == 0 and v2[1] == 2 and v2[2] == 6 and v2[3] == 12
    
    print ("ok")
    return


def testV2xV3xConversion (VecA, VecB):

    try:
        v = VecA();
        v1 = VecB (v);           # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.


def testVecConversions ():

    print ("V2i")
    testV2xConversions (V2i)
    print ("V2f")
    testV2xConversions (V2f)
    print ("V2d")
    testV2xConversions (V2d)

    print ("V3i")
    testV3xConversions (V3i)
    print ("V3f")
    testV3xConversions (V3f)
    print ("V3d")
    testV3xConversions (V3d)

    print ("V4i")
    testV4xConversions (V4i)
    print ("V4f")
    testV4xConversions (V4f)
    print ("V4d")
    testV4xConversions (V4d)


    print ("invalid conversions")
    # Deliberatly not exhaustive, just representative.
    testV2xV3xConversion (V2i, V3f)
    testV2xV3xConversion (V3f, V2d)

    print ("ok")
    return


testList.append (('testVecConversions',testVecConversions))



# -------------------------------------------------------------------------
# Tests for Shear6x

def testShear6x (Shear):
    
    # Constructors (and element access).

    h = Shear()
    assert h[0] == 0 and h[1] == 0 and h[2] == 0 and \
           h[3] == 0 and h[4] == 0 and h[5] == 0

    h = Shear(1)
    assert h[0] == 1 and h[1] == 1 and h[2] == 1 and \
           h[3] == 1 and h[4] == 1 and h[5] == 1

    h = Shear(0, 1, 2)
    assert h[0] == 0 and h[1] == 1 and h[2] == 2 and \
           h[3] == 0 and h[4] == 0 and h[5] == 0

    h = Shear((0, 1, 2))
    assert h[0] == 0 and h[1] == 1 and h[2] == 2 and \
           h[3] == 0 and h[4] == 0 and h[5] == 0

    h = Shear(0, 1, 2, 3, 4, 5)
    assert h[0] == 0 and h[1] == 1 and h[2] == 2 and \
           h[3] == 3 and h[4] == 4 and h[5] == 5

    h = Shear((0, 1, 2, 3, 4, 5))
    assert h[0] == 0 and h[1] == 1 and h[2] == 2 and \
           h[3] == 3 and h[4] == 4 and h[5] == 5

    h = Shear()
    h.setValue(0, 1, 2, 3, 4, 5) 
    assert h[0] == 0 and h[1] == 1 and h[2] == 2 and \
           h[3] == 3 and h[4] == 4 and h[5] == 5

    # Repr.

    h = Shear(1/9., 2/9., 3/9., 4/9., 5/9., 6/9.)
    assert h == eval(repr(h))

    # Sequence length.

    h = Shear()
    assert len(h) == 6

    # Element setting.

    h = Shear()
    h[0] = 10
    h[1] = 11
    h[2] = 12
    h[3] = 13
    h[4] = 14
    h[5] = 15
    assert h[0] == 10 and h[1] == 11 and h[2] == 12 and \
           h[3] == 13 and h[4] == 14 and h[5] == 15

    try:
        h[-7] = 0           # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    try:
        h[6] = 0           # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    try:
        h[1] = "a"           # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    # Assignment.

    h1 = Shear(1)
    
    h2 = h1
    assert h2[0] == 1 and h2[1] == 1 and h2[2] == 1 and \
           h2[3] == 1 and h2[4] == 1 and h2[5] == 1
    h1[0] = 2
    assert h2[0] == 2 and h2[1] == 1 and h2[2] == 1 and \
           h2[3] == 1 and h2[4] == 1 and h2[5] == 1
    
    # Comparison operators.

    h1 = Shear(20, 20, 20, 20, 20, 0)
    h2 = Shear(20, 20, 20, 20, 20, 0)
    h3 = Shear(20, 20, 20, 20, 21, 0)

    assert h1 == h2
    assert h1 != h3
    assert not (h1 < h2)
    assert h1 < h3
    assert h1 <= h2
    assert h1 <= h3
    assert not (h3 <= h1)
    assert not (h2 > h1)
    assert h3 > h1
    assert h2 >= h1
    assert h3 >= h1
    assert not (h1 >= h3)
    
    # Epsilon equality.

    e = 0.005
    h1 = Shear(1)
    h2 = Shear(1 + e)

    assert h1.equalWithAbsError(h2, e)
    assert h2.equalWithAbsError(h1, e)

    e = 0.003
    h1 = Shear(10)
    h2 = Shear(10 + 10 * e)

    assert h1.equalWithRelError(h2, e)
    assert h2.equalWithRelError(h1, e)

    # Addition.

    h1 = Shear(10, 20, 30, -10, -20, -30)
    h2 = Shear(30, 40, 50, -30, -40, -50)

    assert h1 + h2 == Shear(40, 60, 80, -40, -60, -80)
    assert h2 + h1 == h1 + h2
    assert h1 + 1 == Shear(11, 21, 31, -9, -19, -29)
    assert 1 + h1 == h1 + 1

    # (with the switch to python2, we now allow ops between vectors and tuples)
    assert h1 + (1, 2, 3, 4, 5, 6) == Shear(11, 22, 33, -6, -15, -24)
    assert (1, 2, 3, 4, 5, 6) + h1 == h1 + (1, 2, 3, 4, 5, 6)

    # Subtraction and negation.

    h1 = Shear(10, 20, 30, -10, -20, -30)
    h2 = Shear(30, 40, 50, -30, -40, -50)

    assert h2 - h1 == Shear(20, 20, 20, -20, -20, -20)
    assert h1 - 1 == Shear(9, 19, 29, -11, -21, -31)
    assert 1 - h1 == - (h1 - 1)
    
    # (with the switch to python2, we now allow ops between vectors and tuples)
    assert h1 - (1, 2, 3, 4, 5, 6) == Shear(9, 18, 27, -14, -25, -36)
    assert (1, 2, 3, 4, 5, 6) - h1 == - (h1 - (1, 2, 3, 4, 5, 6))

    assert h1.negate() == Shear(-10, -20, -30, 10, 20, 30)

    # Multiplication.

    h1 = Shear(1, 2, 3, -1, -2, -3)
    h2 = Shear(3, 4, 5, -3, -4, -5)
    
    assert h1 * h2 == Shear(3, 8, 15, 3, 8, 15)
    assert h2 * h1 == h1 * h2
    assert 2 * h1 == Shear(2, 4, 6, -2, -4, -6)
    assert h1 * 2 == 2 * h1

    # (with the switch to python2, we now allow ops between vectors and tuples)
    assert h1 * (1, 2, 3, 4, 5, 6) == Shear(1, 4, 9, -4, -10, -18)
    assert (1, 2, 3, 4, 5, 6) * h1 == h1 * (1, 2, 3, 4, 5, 6)

    # Division.

    h1 = Shear(10, 20, 40, -10, -20, -40)
    h2 = Shear(2, 4, 8, -2, -4, -8)
    
    assert h1 / h2 == Shear(10/2, 20/4, 40/8, -10/-2, -20/-4, -40/-8)
    assert h1 / 2 == Shear(10/2, 20/2, 40/2, -10/2, -20/2, -40/2)
    assert Shear(40) / h1 == Shear(40/10, 40/20, 40/40, 40/-10, 40/-20, 40/-40)

    # (with the switch to python2, we now allow ops between vectors and tuples)
    assert h1 / (1, 2, 4, -1, -2, -4) == Shear(10, 10, 10, 10, 10, 10)
    assert Shear(50, 40, 80, -50, -40, -80) / h1 == Shear(5, 2, 2, 5, 2, 2)

    print ("ok")

    return

def testShear6 ():

    print ("Shear6f")
    testShear6x (Shear6f)
    print ("Shear6d")
    testShear6x (Shear6d)

testList.append (('testShear6',testShear6))


# -------------------------------------------------------------------------
# Tests for Shear --> Shear conversions

def testShearV3xConversions (Vec):

    v = Vec (0, 1, 2)

    h = Shear6f (v)
    assert h[0] == 0 and h[1] == 1 and h[2] == 2 and \
           h[3] == 0 and h[4] == 0 and h[5] == 0

    h = Shear6d (v)
    assert h[0] == 0 and h[1] == 1 and h[2] == 2 and \
           h[3] == 0 and h[4] == 0 and h[5] == 0

    print ("ok")
    return


def testShear6xConversions (Shear):

    h1 = Shear(0, 1, 2, 3, 4, 5)

    h2 = Shear6f (h1)
    assert h2[0] == 0 and h2[1] == 1 and h2[2] == 2 and \
           h2[3] == 3 and h2[4] == 4 and h2[5] == 5

    h2 = Shear6d (h1)
    assert h2[0] == 0 and h2[1] == 1 and h2[2] == 2 and \
           h2[3] == 3 and h2[4] == 4 and h2[5] == 5

    print ("ok")
    return


def testShearConversions ():

    print ("V3f")
    testShearV3xConversions (V3f)
    print ("V3d")
    testShearV3xConversions (V3d)

    print ("Shear6f")
    testShear6xConversions (Shear6f)
    print ("Shear6d")
    testShear6xConversions (Shear6d)

    print ("ok")
    return


testList.append (('testShearConversions',testShearConversions))



# -------------------------------------------------------------------------
# Tests for M33x

def testM33x (Mat, Vec, Vec3):
    
    # Constructors (and element access).

    m = Mat()
    assert m[0][0] == 1 and m[0][1] == 0 and m[0][2] == 0 and \
           m[1][0] == 0 and m[1][1] == 1 and m[1][2] == 0 and \
           m[2][0] == 0 and m[2][1] == 0 and m[2][2] == 1

    m = Mat(1)
    assert m[0][0] == 1 and m[0][1] == 1 and m[0][2] == 1 and \
           m[1][0] == 1 and m[1][1] == 1 and m[1][2] == 1 and \
           m[2][0] == 1 and m[2][1] == 1 and m[2][2] == 1

    m = Mat((0, 1, 2), (3, 4, 5), (6, 7, 8))
    assert m[0][0] == 0 and m[0][1] == 1 and m[0][2] == 2 and \
           m[1][0] == 3 and m[1][1] == 4 and m[1][2] == 5 and \
           m[2][0] == 6 and m[2][1] == 7 and m[2][2] == 8


    m = Mat(0, 1, 2, 3, 4, 5, 6, 7, 8)
    assert m[0][0] == 0 and m[0][1] == 1 and m[0][2] == 2 and \
           m[1][0] == 3 and m[1][1] == 4 and m[1][2] == 5 and \
           m[2][0] == 6 and m[2][1] == 7 and m[2][2] == 8

    # Repr.

    m = Mat(0/9., 1/9., 2/9., 3/9., 4/9., 5/9., 6/9., 7/9., 8/9.)
    assert m == eval(repr(m))

    # Sequence length.

    m = Mat()
    assert len(m) == 3

    # Element setting.

    m = Mat()
    m[0][0] = 10
    m[1][2] = 11
    assert m[0][0] == 10 and m[1][2] == 11

    try:
        m[-4][0] = 0           # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    try:
        v[3][0] = 0           # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    try:
        m[0][-4] = 0           # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    try:
        v[0][3] = 0           # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    try:
        v[1] = (1,2,3)           # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    # Assignment.

    m1 = Mat(1)
    
    m2 = m1
    assert m2[0][0] == 1 and m2[0][1] == 1 and m2[0][2] == 1 and \
           m2[1][0] == 1 and m2[1][1] == 1 and m2[1][2] == 1 and \
           m2[2][0] == 1 and m2[2][1] == 1 and m2[2][2] == 1
    m1[0][0] = 2
    assert m2[0][0] == 2 and m2[0][1] == 1 and m2[0][2] == 1 and \
           m2[1][0] == 1 and m2[1][1] == 1 and m2[1][2] == 1 and \
           m2[2][0] == 1 and m2[2][1] == 1 and m2[2][2] == 1
    
    # Identity.

    m = Mat(2)

    m.makeIdentity()
    assert m[0][0] == 1 and m[0][1] == 0 and m[0][2] == 0 and \
           m[1][0] == 0 and m[1][1] == 1 and m[1][2] == 0 and \
           m[2][0] == 0 and m[2][1] == 0 and m[2][2] == 1

    # Comparison operators.

    m1 = Mat()
    m1[1][1] = 2
    m2 = Mat()
    m2[1][1] = 2
    m3 = Mat()
    m3[1][1] = 3

    assert m1 == m2
    assert m1 != m3
    assert not (m1 < m2)
    assert m1 < m3
    assert m1 <= m2
    assert m1 <= m3
    assert not (m3 <= m1)
    assert not (m2 > m1)
    assert m3 > m1
    assert m2 >= m1
    assert m3 >= m1
    assert not (m1 >= m3)

    # Epsilon equality.

    e = 0.005
    m1 = Mat(1)
    m2 = Mat(1 + e)

    assert m1.equalWithAbsError(m2, e)
    assert m2.equalWithAbsError(m1, e)

    e = 0.003
    m1 = Mat(10)
    m2 = Mat(10 + 10 * e)

    assert m1.equalWithRelError(m2, e)
    assert m2.equalWithRelError(m1, e)

    # Addition.

    m1 = Mat(1)
    m2 = Mat(2)

    assert m1 + m2 == Mat(3)
    assert m2 + m1 == m1 + m2
    assert m1 + 1 == Mat(2)
    assert 1 + m1 == m1 + 1

    # Subtraction and negation.

    m1 = Mat(2)
    m2 = Mat(3)

    assert m2 - m1 == Mat(1)
    assert m1 - 1 == Mat(1)
    assert 1 - m1 == - (m1 - 1)
    assert m1.negate() == Mat(-2)

    # Multiplication.

    m1 = Mat(1)
    # (Translates by (1,2).)
    m2 = Mat()
    m2[2][0] = 1
    m2[2][1] = 2
    # (Scales by (3, 4).)
    m3 = Mat()
    m3[0][0] = 3
    m3[1][1] = 4
    v = Vec(1, 2)

    assert m1 * 2 == Mat(2)
    assert m1 * 2 == 2 * m1
    assert m2 * m3 == Mat((3,0,0),(0,4,0),(3,8,1))
    assert m3 * m2 == Mat((3,0,0),(0,4,0),(1,2,1))
    assert v * m2 == Vec(2, 4)
    try:
        m1 * v                   # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    m2f = M33f()
    m2f[2][0] = 1
    m2f[2][1] = 2
    v = Vec(1, 2)
    v *= m2f
    assert v == Vec(2, 4)

    m2d = M33d()
    m2d[2][0] = 1
    m2d[2][1] = 2
    v = Vec(1, 2)
    v *= m2d
    assert v == Vec(2, 4)

    # (Rotates by 45 degrees, then translates by (1,2).)
    m3 = Mat()
    m3[0][0] = 0
    m3[0][1] = 1
    m3[1][0] = -1
    m3[1][1] = 0    
    m4 = m3 * m2
    v1 = Vec(1, 0)
    v2 = Vec()
    
    m4.multVecMatrix(v1,v2)
    assert v2.equalWithAbsError((1, 3), v2.baseTypeEpsilon())
    v2 = m4.multVecMatrix(v1)
    assert v2.equalWithAbsError((1, 3), v2.baseTypeEpsilon())
    v1a = V2fArray(1)
    v1a[:] = V2f(v1)
    v2a = m4.multVecMatrix(v1a)
    assert v2a[0].equalWithAbsError((1, 3), v2a[0].baseTypeEpsilon())
    v1a = V2dArray(1)
    v1a[:] = V2d(v1)
    v2a = m4.multVecMatrix(v1a)
    assert v2a[0].equalWithAbsError((1, 3), v2a[0].baseTypeEpsilon())
    

    m4.multDirMatrix(v1,v2)
    assert v2.equalWithAbsError((0, 1), v2.baseTypeEpsilon())
    v2 = m4.multDirMatrix(v1)
    assert v2.equalWithAbsError((0, 1), v2.baseTypeEpsilon())
    v1a = V2fArray(1)
    v1a[:] = V2f(v1)
    v2a = m4.multDirMatrix(v1a)
    assert v2a[0].equalWithAbsError((0, 1), v2a[0].baseTypeEpsilon())
    v1a = V2dArray(1)
    v1a[:] = V2d(v1)
    v2a = m4.multDirMatrix(v1a)
    assert v2a[0].equalWithAbsError((0, 1), v2a[0].baseTypeEpsilon())
    
    # Division.

    m = Mat(4)

    assert m / 2 == Mat(2)
    try:
        4 / m                   # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    # Transpose.

    m = Mat(1, 2, 3, 4, 5, 6, 7, 8, 9)

    assert m.transpose() == Mat(1, 4, 7, 2, 5, 8, 3, 6, 9)
    m.transposed()
    assert m == Mat(1, 4, 7, 2, 5, 8, 3, 6, 9)
    
    # Invert.

    # (Translates by (1,2).)
    m1 = Mat()
    m1[2][0] = 1
    m1[2][1] = 2
    
    m1I = m1.inverse()
    assert m1 * m1I == Mat()
    m1I = m1.gjInverse()
    assert m1 * m1I == Mat()

    m2 = Mat(m1)
    m2.invert()
    assert m1 * m2 == Mat()
    m2 = Mat(m1)
    m2.gjInvert()
    assert m1 * m2 == Mat()

    # Rotation (in radians).

    v1 = Vec(1, 0)

    m = Mat()
    m.setRotation(-pi / 2)

    v2 = v1 * m
    assert v2.equalWithAbsError((0, -1), v2.baseTypeEpsilon())

    m.rotate(-pi / 2)

    v2 = v1 * m
    assert v2.equalWithAbsError((-1, 0), v2.baseTypeEpsilon())

    # Scaling.

    v1 = Vec(1, 2)

    m = Mat()
    m.setScale(2)

    v2 = v1 * m
    assert v2.equalWithAbsError((2, 4), v2.baseTypeEpsilon())

    m.scale(3)

    v2 = v1 * m
    assert v2.equalWithAbsError((6, 12), v2.baseTypeEpsilon())

    m = Mat()
    m.setScale((1, 2))

    v2 = v1 * m
    assert v2.equalWithAbsError((1, 4), v2.baseTypeEpsilon())

    m.scale((2, 3))

    v2 = v1 * m
    assert v2.equalWithAbsError((2, 12), v2.baseTypeEpsilon())

    # It is not essential for correctness that the following exceptions
    # occur.  Instead, these tests merely document the way the Python
    # wrappings currently work.
    try:
        m.setScale(1, 2)        # This should raise an exception.
    except:
        pass
    else:
        assert 0                   # We shouldn't get here.

    # Shearing.

    v1 = Vec(1, 2)

    m = Mat()
    m.setShear(2)

    v2 = v1 * m
    assert v2.equalWithAbsError((5, 2), v2.baseTypeEpsilon())

    m.shear(3)

    v2 = v1 * m
    assert v2.equalWithAbsError((11, 2), v2.baseTypeEpsilon())

    m = Mat()
    m.setShear((2, 1))

    v2 = v1 * m
    assert v2.equalWithAbsError((5, 3), v2.baseTypeEpsilon())

    m.shear((3, 2))

    v2 = v1 * m
    assert v2.equalWithAbsError((15, 11), v2.baseTypeEpsilon())

    m = Mat()
    m.setShear((1, 2))

    v2 = v1 * m
    assert v2.equalWithAbsError((3, 4), v2.baseTypeEpsilon())

    m.shear((2, 3))

    v2 = v1 * m
    assert v2.equalWithAbsError((10, 15), v2.baseTypeEpsilon())

    # It is not essential for correctness that the following exceptions
    # occur.  Instead, these tests merely document the way the Python
    # wrappings currently work.
    try:
        m.setShear(1, 2)        # This should raise an exception.
    except:
        pass
    else:
        assert 0                   # We shouldn't get here.

    # Translation.

    v1 = Vec(1, 0)

    m = Mat()
    m.setTranslation((3, 2))

    v2 = v1 * m
    assert v2.equalWithAbsError((4, 2), v2.baseTypeEpsilon())

    m.translate((1, 2))

    v2 = v1 * m
    assert v2.equalWithAbsError((5, 4), v2.baseTypeEpsilon())

    v3 = m.translation()
    assert v3.equalWithAbsError((4, 4), v2.baseTypeEpsilon())

    # Extract scaling.

    m = Mat()
    s = Vec(4, 5)
    m.translate((1, 2))
    m.shear(7)
    m.scale(s)

    sM = Vec()
    m.extractScaling(sM)
    assert sM.equalWithAbsError(s, s.baseTypeEpsilon())

    # Sans scaling / Remove scaling.

    m1 = Mat()
    m1.translate((1, 2))
    m1.shear(7)
    m1.scale((4, 5))

    m2 = m1.sansScaling()
    assert m2[0][0] == 1 and m2[1][1] == 1 and \
           abs (m2[1][0] - 7) <= 4 * m2.baseTypeEpsilon () and \
           abs (m2[0][1])     <= 4 * m2.baseTypeEpsilon () and \
           m2[2][0] == 1 and m2[2][1] == 2 

    m1 = Mat()
    m1.translate((1, 2))
    m1.shear(7)
    m1.scale((0, 0))

    try:
        m2 = m1.sansScaling()  # This should raise an exception.
    except:
        pass
    else:
        assert 0               # We shouldn't get here.   

    m1 = Mat()
    m1.translate((1, 2))
    m1.shear(7)
    m2 = Mat(m1)
    m1.scale((4, 5))

    r = m1.removeScaling()
    assert r == 1 and m1.equalWithAbsError(m2, 4 * m1.baseTypeEpsilon())

    m = Mat()
    m.translate((1, 2))
    m.shear(7)
    m.scale((0, 0))

    try:
        r = m.removeScaling()  # This should raise an exception.
    except:
        pass
    else:
        assert 0               # We shouldn't get here.   

    m = Mat()
    m.translate((1, 2))
    m.shear(7)
    m.scale((0, 0))

    r = m.removeScaling(0)
    assert r == 0

    # Sans scaling and shear / Remove scaling and shear.

    m1 = Mat()
    m1.translate((1, 2))
    m1.shear(7)
    m1.scale((4, 5))

    m2 = m1.sansScalingAndShear()
    assert m2[0][0] == 1 and m2[1][1] == 1 and \
           m2[1][0] == 0 and m2[0][1] == 0 and \
           m2[2][0] == 1 and m2[2][1] == 2 

    m1 = Mat()
    m1.translate((1, 2))
    m1.shear(7)
    m1.scale((0, 0))

    try:
        m2 = m1.sansScalingAndShear()  # This should raise an exception.
    except:
        pass
    else:
        assert 0               # We shouldn't get here.   

    m1 = Mat()
    m1.translate((1, 2))
    m2 = Mat(m1)
    m1.shear(7)
    m1.scale((4, 5))

    r = m1.removeScalingAndShear()
    assert r == 1 and m1.equalWithAbsError(m2, m1.baseTypeEpsilon())

    m = Mat()
    m.translate((1, 2))
    m.scale((0, 0))

    try:
        r = m.removeScalingAndShear()  # This should raise an exception.
    except:
        pass
    else:
        assert 0               # We shouldn't get here.   

    m = Mat()
    m.translate((1, 2))
    m.shear(7)
    m.scale((0, 0))

    r = m.removeScalingAndShear(0)
    assert r == 0

    # Extract and remove scaling and shear.

    m = Mat()
    s = Vec(4, 5)
    h = Vec(7, 0)
    m.translate((1, 2))
    m2 = Mat(m)
    m.shear(h)
    m.scale(s)

    sM = Vec()
    hM = Vec()
    m.extractScalingAndShear(sM, hM)
    assert sM.equalWithAbsError(s, s.baseTypeEpsilon())
    assert hM.equalWithAbsError(h, 4 * h.baseTypeEpsilon())

    sM = Vec()
    hM = Vec()
    m.extractAndRemoveScalingAndShear(sM, hM)
    assert sM.equalWithAbsError(s, s.baseTypeEpsilon())
    assert hM.equalWithAbsError(h, 4 * h.baseTypeEpsilon())
    assert m2.equalWithAbsError(m, m.baseTypeEpsilon())

    # Extract Euler.

    m = Mat()
    a = pi/4
    # (Rotation by -a around Z axis.)
    m[0][0] = cos(a)
    m[0][1] = -sin(a)
    m[1][0] = sin(a)
    m[1][1] = cos(a)
    v = Vec()

    m.extractEuler(v)
    assert v.equalWithAbsError((-a, 0), v.baseTypeEpsilon())

    # Extract scale, shear, rotation, translation.

    s = Vec(1, 2)
    h = Vec(0.5, 0)
    a = pi/4
    t = Vec(4, 5)

    mS = Mat()
    mS.scale(s)
    mH = Mat()
    # (Shear by XY, XZ, YZ shear factors.)
    mH.shear(h)
    mR = Mat()
    # (Rotation by -a around Z axis.)
    mR[0][0] = cos(a)
    mR[0][1] = -sin(a)
    mR[1][0] = sin(a)
    mR[1][1] = cos(a)
    mT = Mat()
    mT.translate(t)
    m = mS * mH * mR * mT

    sInq = Vec()
    hInq = Vec()
    rInq = Vec()
    tInq = Vec()

    b = m.extractSHRT(sInq, hInq, rInq, tInq)

    assert sInq.equalWithAbsError(s, 2 * sInq.baseTypeEpsilon())
    assert hInq.equalWithAbsError(h, hInq.baseTypeEpsilon())
    assert rInq.equalWithAbsError((-a, 0), 2 * rInq.baseTypeEpsilon())
    assert tInq.equalWithAbsError(t, tInq.baseTypeEpsilon())

    # Matrix minors

    a = Mat(1,2,3,4,5,6,7,8,9)
    assert a.minorOf(0,0) == a.fastMinor(1,2,1,2)
    assert a.minorOf(0,1) == a.fastMinor(1,2,0,2)
    assert a.minorOf(0,2) == a.fastMinor(1,2,0,1)
    assert a.minorOf(1,0) == a.fastMinor(0,2,1,2)
    assert a.minorOf(1,1) == a.fastMinor(0,2,0,2)
    assert a.minorOf(1,2) == a.fastMinor(0,2,0,1)
    assert a.minorOf(2,0) == a.fastMinor(0,1,1,2)
    assert a.minorOf(2,1) == a.fastMinor(0,1,0,2)
    assert a.minorOf(2,2) == a.fastMinor(0,1,0,1)

    # Determinants (by building a random singular value decomposition)

    u = Mat()
    v = Mat()
    s = Mat()

    u.setRotation( random.random() )
    v.setRotation( random.random() )
    s[0][0] = random.random()
    s[1][1] = random.random()
    s[2][2] = random.random()

    c = u * s * v.transpose()
    assert abs(c.determinant() - s[0][0]*s[1][1]*s[2][2]) <= u.baseTypeEpsilon()

    # Outer product of two 3D vectors

    a = Vec3(1,2,3)
    b = Vec3(4,5,6)
    p = Mat()

    p.outerProduct(a,b)
    for i in range(3):
        for j in range(3):
            assert p[i][j] == a[i]*b[j]

    print ("ok")
    return

def testM33 ():

    print ("M33f")
    testM33x (M33f, V2f, V3f)
    print ("M33d")
    testM33x (M33d, V2d, V3d)

testList.append (('testM33',testM33))


# -------------------------------------------------------------------------
# Tests for M44x

def testM44x (Mat, Vec):
    
    # Constructors (and element access).

    m = Mat()
    assert \
      m[0][0] == 1 and m[0][1] == 0 and m[0][2] == 0 and m[0][3] == 0 and \
      m[1][0] == 0 and m[1][1] == 1 and m[1][2] == 0 and m[1][3] == 0 and \
      m[2][0] == 0 and m[2][1] == 0 and m[2][2] == 1 and m[2][3] == 0 and \
      m[3][0] == 0 and m[3][1] == 0 and m[3][2] == 0 and m[3][3] == 1

    m = Mat(1)
    assert \
      m[0][0] == 1 and m[0][1] == 1 and m[0][2] == 1 and m[0][3] == 1 and \
      m[1][0] == 1 and m[1][1] == 1 and m[1][2] == 1 and m[1][3] == 1 and \
      m[2][0] == 1 and m[2][1] == 1 and m[2][2] == 1 and m[2][3] == 1 and \
      m[3][0] == 1 and m[3][1] == 1 and m[3][2] == 1 and m[3][3] == 1

    m = Mat((0,1,2,3), (4,5,6,7), (8,9,10,11), (12,13,14,15))
    assert \
      m[0][0] == 0 and m[0][1] == 1 and m[0][2] == 2 and m[0][3] == 3 and \
      m[1][0] == 4 and m[1][1] == 5 and m[1][2] == 6 and m[1][3] == 7 and \
      m[2][0] == 8 and m[2][1] == 9 and m[2][2] ==10 and m[2][3] ==11 and \
      m[3][0] ==12 and m[3][1] ==13 and m[3][2] ==14 and m[3][3] ==15

    # Repr.

    m = Mat((0/9.,1/9.,2/9.,3/9.),
            (4/9.,5/9.,6/9.,7/9.),
            (8/9.,9/9.,10/9.,11/9.),
            (12/9.,13/9.,14/9.,15/9.))
    assert m == eval(repr(m))

    # Sequence length.

    m = Mat()
    assert len(m) == 4

    # Element setting.

    m = Mat()
    m[0][0] = 10
    m[1][2] = 11
    assert m[0][0] == 10 and m[1][2] == 11

    try:
        m[-5][0] = 0           # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    try:
        m[4][0] = 0           # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    try:
        m[0][-5] = 0           # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    try:
        m[0][4] = 0           # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    try:
        m[1] = (1,2,3,4)   # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    # Assignment.

    m1 = Mat(1)
    
    m2 = m1
    assert \
      m2[0][0] ==1 and m2[0][1] ==1 and m2[0][2] ==1 and m2[0][3] ==1 and \
      m2[1][0] ==1 and m2[1][1] ==1 and m2[1][2] ==1 and m2[1][3] ==1 and \
      m2[2][0] ==1 and m2[2][1] ==1 and m2[2][2] ==1 and m2[2][3] ==1 and \
      m2[3][0] ==1 and m2[3][1] ==1 and m2[3][2] ==1 and m2[3][3] ==1

    m1[0][0] = 2
    assert \
      m2[0][0] ==2 and m2[0][1] ==1 and m2[0][2] ==1 and m2[0][3] ==1 and \
      m2[1][0] ==1 and m2[1][1] ==1 and m2[1][2] ==1 and m2[1][3] ==1 and \
      m2[2][0] ==1 and m2[2][1] ==1 and m2[2][2] ==1 and m2[2][3] ==1 and \
      m2[3][0] ==1 and m2[3][1] ==1 and m2[3][2] ==1 and m2[3][3] ==1
    
    # Identity.

    m = Mat(2)

    m.makeIdentity()
    assert \
      m[0][0] == 1 and m[0][1] == 0 and m[0][2] == 0 and m[0][3] == 0 and \
      m[1][0] == 0 and m[1][1] == 1 and m[1][2] == 0 and m[1][3] == 0 and \
      m[2][0] == 0 and m[2][1] == 0 and m[2][2] == 1 and m[2][3] == 0 and \
      m[3][0] == 0 and m[3][1] == 0 and m[3][2] == 0 and m[3][3] == 1

    # Comparison operators.

    m1 = Mat()
    m1[1][1] = 2
    m2 = Mat()
    m2[1][1] = 2
    m3 = Mat()
    m3[1][1] = 3

    assert m1 == m2
    assert m1 != m3
    assert not (m1 < m2)
    assert m1 < m3
    assert m1 <= m2
    assert m1 <= m3
    assert not (m3 <= m1)
    assert not (m2 > m1)
    assert m3 > m1
    assert m2 >= m1
    assert m3 >= m1
    assert not (m1 >= m3)

    # Epsilon equality.

    e = 0.005
    m1 = Mat(1)
    m2 = Mat(1 + e)

    assert m1.equalWithAbsError(m2, e)
    assert m2.equalWithAbsError(m1, e)

    e = 0.003
    m1 = Mat(10)
    m2 = Mat(10 + 10 * e)

    assert m1.equalWithRelError(m2, e)
    assert m2.equalWithRelError(m1, e)

    # Addition.

    m1 = Mat(1)
    m2 = Mat(2)

    assert m1 + m2 == Mat(3)
    assert m2 + m1 == m1 + m2
    assert m1 + 1 == Mat(2)
    assert 1 + m1 == m1 + 1

    # Subtraction and negation.

    m1 = Mat(2)
    m2 = Mat(3)

    assert m2 - m1 == Mat(1)
    assert m1 - 1 == Mat(1)
    assert 1 - m1 == - (m1 - 1)
    assert m1.negate() == Mat(-2)

    # Multiplication.

    m1 = Mat(1)
    # (Translates by (1, 2, 0).)
    m2 = Mat()
    m2[3][0] = 1
    m2[3][1] = 2
    # (Scales by (3, 4, 1).)
    m3 = Mat()
    m3[0][0] = 3
    m3[1][1] = 4
    v = Vec(1, 2, 0)

    assert m1 * 2 == Mat(2)
    assert m1 * 2 == 2 * m1
    assert m2 * m3 == Mat((3,0,0,0),(0,4,0,0),(0,0,1,0),(3,8,0,1))
    assert m3 * m2 == Mat((3,0,0,0),(0,4,0,0),(0,0,1,0),(1,2,0,1))
    assert v * m2 == Vec(2, 4, 0)
    try:
        m1 * v                   # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    m2f = M44f()
    m2f[3][0] = 1
    m2f[3][1] = 2
    v = Vec(1, 2, 0)
    v *= m2f
    assert v == Vec(2, 4, 0)

    m2d = M44d()
    m2d[3][0] = 1
    m2d[3][1] = 2
    v = Vec(1, 2, 0)
    v *= m2d
    assert v == Vec(2, 4, 0)

    # (Rotates by 45 degrees around Z, then translates by (1, 2, 0).)
    m3 = Mat()
    m3[0][0] = 0
    m3[0][1] = 1
    m3[1][0] = -1
    m3[1][1] = 0    
    m4 = m3 * m2
    v1 = Vec(1, 0, 0)
    v2 = Vec()
    
    m4.multVecMatrix(v1,v2)
    assert v2.equalWithAbsError((1, 3, 0), v2.baseTypeEpsilon())
    v2 = m4.multVecMatrix(v1)
    assert v2.equalWithAbsError((1, 3, 0), v2.baseTypeEpsilon())
    v1a = V3fArray(1)
    v1a[:] = V3f(v1)
    v2a = m4.multVecMatrix(v1a)
    assert v2a[0].equalWithAbsError((1, 3, 0), v2a[0].baseTypeEpsilon())
    v1a = V3dArray(1)
    v1a[:] = V3d(v1)
    v2a = m4.multVecMatrix(v1a)
    assert v2a[0].equalWithAbsError((1, 3, 0), v2a[0].baseTypeEpsilon())
    
    m4.multDirMatrix(v1,v2)
    assert v2.equalWithAbsError((0, 1, 0), v2.baseTypeEpsilon())
    v2 = m4.multDirMatrix(v1)
    assert v2.equalWithAbsError((0, 1, 0), v2.baseTypeEpsilon())
    v1a = V3fArray(1)
    v1a[:] = V3f(v1)
    v2a = m4.multDirMatrix(v1a)
    assert v2a[0].equalWithAbsError((0, 1, 0), v2a[0].baseTypeEpsilon())
    v1a = V3dArray(1)
    v1a[:] = V3d(v1)
    v2a = m4.multDirMatrix(v1a)
    assert v2a[0].equalWithAbsError((0, 1, 0), v2a[0].baseTypeEpsilon())
    
    # Division.

    m = Mat(4)

    assert m / 2 == Mat(2)
    try:
        4 / m                   # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    # Transpose.

    m = Mat((0,1,2,3), (4,5,6,7), (8,9,10,11), (12,13,14,15))

    assert m.transpose() == Mat((0,4,8,12), (1,5,9,13), (2,6,10,14), (3,7,11,15))
    m.transposed()
    assert m == Mat((0,4,8,12), (1,5,9,13), (2,6,10,14), (3,7,11,15))
    
    # Invert.

    # (Translates by (1,2).)
    m1 = Mat()
    m1[3][0] = 1
    m1[3][1] = 2
    
    m1I = m1.inverse()
    assert m1 * m1I == Mat()
    m1I = m1.gjInverse()
    assert m1 * m1I == Mat()

    m2 = Mat(m1)
    m2.invert()
    assert m1 * m2 == Mat()
    m2 = Mat(m1)
    m2.gjInvert()
    assert m1 * m2 == Mat()

    # Scaling.

    v1 = Vec(1, 2, 0)

    m = Mat()
    m.setScale(2)

    v2 = v1 * m
    assert v2.equalWithAbsError((2, 4, 0), v2.baseTypeEpsilon())

    m.scale(3)

    v2 = v1 * m
    assert v2.equalWithAbsError((6, 12, 0), v2.baseTypeEpsilon())

    m = Mat()
    m.setScale((1, 2, 1))

    v2 = v1 * m
    assert v2.equalWithAbsError((1, 4, 0), v2.baseTypeEpsilon())

    m.scale((2, 3, 1))

    v2 = v1 * m
    assert v2.equalWithAbsError((2, 12, 0), v2.baseTypeEpsilon())

    # It is not essential for correctness that the following exceptions
    # occur.  Instead, these tests merely document the way the Python
    # wrappings currently work.
    try:
        m.setScale(1, 2)        # This should raise an exception.
    except:
        pass
    else:
        assert 0                   # We shouldn't get here.

    # Shearing.

    v1 = Vec((1, 2, 3))

    m = Mat()
    m.setShear((2, 3, 4))

    v2 = v1 * m
    assert v2.equalWithAbsError((14, 14, 3), v2.baseTypeEpsilon())

    m.shear((1, 2, 3))

    v2 = v1 * m
    assert v2.equalWithAbsError((40, 23, 3), v2.baseTypeEpsilon())

    m = Mat()
    m.setShear((4, 3, 2, -4, -3, -2))

    v2 = v1 * m
    assert v2.equalWithAbsError((18, 4, -4), v2.baseTypeEpsilon())

    m.shear((3, 2, 1, -3, -2, -1))

    v2 = v1 * m
    assert v2.equalWithAbsError((18, -52, -44), v2.baseTypeEpsilon())

    # It is not essential for correctness that the following exceptions
    # occur.  Instead, these tests merely document the way the Python
    # wrappings currently work.
    try:
        m.setShear(1, 2, 3)        # This should raise an exception.
    except:
        pass
    else:
        assert 0                   # We shouldn't get here.

    # It is not essential for correctness that the following exceptions
    # occur.  Instead, these tests merely document the way the Python
    # wrappings currently work.
    try:
        m.shear(1, 2, 3, 4, 5, 6)        # This should raise an exception.
    except:
        pass
    else:
        assert 0                   # We shouldn't get here.

    # Translation.

    v1 = Vec(1, 0, 0)

    m = Mat()
    m.setTranslation((3, 2, 0))

    v2 = v1 * m
    assert v2.equalWithAbsError((4, 2, 0), v2.baseTypeEpsilon())

    m.translate((1, 2, 0))

    v2 = v1 * m
    assert v2.equalWithAbsError((5, 4, 0), v2.baseTypeEpsilon())

    v3 = m.translation()
    assert v3.equalWithAbsError((4, 4, 0), v3.baseTypeEpsilon())

    # Extract scaling.

    m = Mat()
    s = Vec(4, 5, 6)
    m.translate((1, 2, 3))
    m.shear((7, 8, 9))
    m.scale(s)

    sM = Vec()
    m.extractScaling(sM)
    assert sM.equalWithAbsError(s, s.baseTypeEpsilon())

    # Sans scaling / Remove scaling.

    m1 = Mat()
    m1.translate((1, 2, 3))
    m1.shear((7, 8, 9))
    m1.scale((4, 5, 6))

    m2 = m1.sansScaling()
    assert m2[0][0] == 1 and m2[1][1] == 1 and m2[2][2] == 1 and \
           m2[1][0] == 7 and m2[2][0] == 8 and m2[2][1] == 9 and \
           m2[0][1] == 0 and m2[0][2] == 0 and m2[1][2] == 0 and \
           m2[3][0] == 1 and m2[3][1] == 2 and m2[3][2] == 3

    m1 = Mat()
    m1.translate((1, 2, 3))
    m1.shear((7, 8, 9))
    m1.scale((0, 0, 0))

    try:
        m2 = m1.sansScaling()  # This should raise an exception.
    except:
        pass
    else:
        assert 0               # We shouldn't get here.   

    m1 = Mat()
    m1.translate((1, 2, 3))
    m1.shear((7, 8, 9))
    m2 = Mat(m1)
    m1.scale((4, 5, 6))

    r = m1.removeScaling()
    assert r == 1 and m1.equalWithAbsError(m2, m1.baseTypeEpsilon())

    m = Mat()
    m.translate((1, 2, 3))
    m.shear((7, 8, 9))
    m.scale((0, 0, 0))

    try:
        r = m.removeScaling()  # This should raise an exception.
    except:
        pass
    else:
        assert 0               # We shouldn't get here.   

    m = Mat()
    m.translate((1, 2, 3))
    m.shear((7, 8, 9))
    m.scale((0, 0, 0))

    r = m.removeScaling(0)
    assert r == 0

    # Sans scaling and shear / Remove scaling and shear.

    m1 = Mat()
    m1.translate((1, 2, 3))
    m1.shear((7, 8, 9))
    m1.scale((4, 5, 6))

    m2 = m1.sansScalingAndShear()
    assert m2[0][0] == 1 and m2[1][1] == 1 and m2[2][2] == 1 and \
           m2[1][0] == 0 and m2[2][0] == 0 and m2[2][1] == 0 and \
           m2[0][1] == 0 and m2[0][2] == 0 and m2[1][2] == 0 and \
           m2[3][0] == 1 and m2[3][1] == 2 and m2[3][2] == 3

    m1 = Mat()
    m1.translate((1, 2, 3))
    m1.shear((7, 8, 9))
    m1.scale((0, 0, 0))

    try:
        m2 = m1.sansScalingAndShear()  # This should raise an exception.
    except:
        pass
    else:
        assert 0               # We shouldn't get here.   

    m1 = Mat()
    m1.translate((1, 2, 3))
    m2 = Mat(m1)
    m1.shear((7, 8, 9))
    m1.scale((4, 5, 6))

    r = m1.removeScalingAndShear()
    assert r == 1 and m1.equalWithAbsError(m2, m1.baseTypeEpsilon())

    m = Mat()
    m.translate((1, 2, 3))
    m.scale((0, 0, 0))

    try:
        r = m.removeScalingAndShear()  # This should raise an exception.
    except:
        pass
    else:
        assert 0               # We shouldn't get here.   

    m = Mat()
    m.translate((1, 2, 3))
    m.shear((7, 8, 9))
    m.scale((0, 0, 0))

    r = m.removeScalingAndShear(0)
    assert r == 0

    # Extract and remove scaling and shear.

    m = Mat()
    s = Vec(4, 5, 6)
    h = Vec(7, 8, 9)
    m.translate((1, 2, 3))
    m2 = Mat(m)
    m.shear(h)
    m.scale(s)

    sM = Vec()
    hM = Vec()
    m.extractScalingAndShear(sM, hM)
    assert sM.equalWithAbsError(s, s.baseTypeEpsilon())
    assert hM.equalWithAbsError(h, h.baseTypeEpsilon())

    sM = Vec()
    hM = Vec()
    m.extractAndRemoveScalingAndShear(sM, hM)
    assert sM.equalWithAbsError(s, s.baseTypeEpsilon())
    assert hM.equalWithAbsError(h, h.baseTypeEpsilon())
    assert m2.equalWithAbsError(m, m.baseTypeEpsilon())

    # Extract Euler.

    m = Mat()
    a = pi/4
    # (Rotation by -a around Z axis.)
    m[0][0] = cos(a)
    m[0][1] = -sin(a)
    m[1][0] = sin(a)
    m[1][1] = cos(a)
    v = Vec()

    m.extractEulerZYX(v)
    assert v.equalWithAbsError((-a, 0, 0), v.baseTypeEpsilon())

    m.extractEulerXYZ(v)
    assert v.equalWithAbsError((0, 0, -a), v.baseTypeEpsilon())

    # Extract scale, shear, rotation, translation.

    s = Vec(1, 2, 3)
    h = Vec(0.5, 1, 0.75)
    a = pi/4
    t = Vec(4, 5, 6)

    mS = Mat()
    mS.scale(s)
    mH = Mat()
    # (Shear by XY, XZ, YZ shear factors.)
    mH.shear(h)
    mR = Mat()
    # (Rotation by -a around Z axis.)
    mR[0][0] = cos(a)
    mR[0][1] = -sin(a)
    mR[1][0] = sin(a)
    mR[1][1] = cos(a)
    mT = Mat()
    mT.translate(t)
    m = mS * mH * mR * mT

    sInq = Vec()
    hInq = Vec()
    rInq = Vec()
    tInq = Vec()

    b = m.extractSHRT(sInq, hInq, rInq, tInq)

    assert sInq.equalWithAbsError(s, sInq.baseTypeEpsilon())
    assert hInq.equalWithAbsError(h, hInq.baseTypeEpsilon())
    assert rInq.equalWithAbsError((0, 0, -a), 2 * rInq.baseTypeEpsilon())
    assert tInq.equalWithAbsError(t, tInq.baseTypeEpsilon())

    # From-to rotation matrix.

    fromDir = Vec(1, 1, 0)
    fromDir.normalize()
    toDir = Vec(0, 1, 1)
    toDir.normalize()
    m = Mat()
    m.rotationMatrix(fromDir, toDir)

    v = fromDir * m
    assert v.equalWithAbsError(toDir, 2 * v.baseTypeEpsilon())

    fromDirTup = (fromDir[0], fromDir[1], fromDir[2])
    toDirTup = (toDir[0], toDir[1], toDir[2])

    m = Mat()
    m.rotationMatrix(fromDirTup, toDirTup)

    v = fromDir * m
    assert v.equalWithAbsError(toDir, 2 * v.baseTypeEpsilon())

    m = Mat()
    m.rotationMatrix(fromDir, toDirTup)

    v = fromDir * m
    assert v.equalWithAbsError(toDir, 2 * v.baseTypeEpsilon())

    m = Mat()
    m.rotationMatrix(fromDirTup, toDir)

    v = fromDir * m
    assert v.equalWithAbsError(toDir, 2 * v.baseTypeEpsilon())

    fromDir = V3f(1, 1, 0)
    fromDir.normalize()
    toDir = V3f(0, 1, 1)
    toDir.normalize()
    m = Mat()
    m.rotationMatrix(fromDir, toDir)

    v = fromDir * m
    assert v.equalWithAbsError(toDir, 2 * V3f.baseTypeEpsilon())

    fromDir = V3d(1, 1, 0)
    fromDir.normalize()
    toDir = V3d(0, 1, 1)
    toDir.normalize()
    m = Mat()
    m.rotationMatrix(fromDir, toDir)

    v = fromDir * m
    assert v.equalWithAbsError(toDir, 2 * V3f.baseTypeEpsilon())

    # From-to rotation matrix with up dir.

    upDir = Vec(1, 0, 1)
    upDir.normalize()
    fromDir = Vec(1, 1, 0)
    fromDir.normalize()
    toDir = Vec(0, 1, 1)
    toDir.normalize()
    m = Mat()
    m.rotationMatrixWithUpDir(fromDir, toDir, upDir)

    v = fromDir * m
    assert v.equalWithAbsError(toDir, v.baseTypeEpsilon())

    fromDirTup = (fromDir[0], fromDir[1], fromDir[2])
    toDirTup = (toDir[0], toDir[1], toDir[2])
    upDirTup = (upDir[0], upDir[1], upDir[2])

    m = Mat()
    m.rotationMatrixWithUpDir(fromDirTup, toDirTup, upDirTup)

    v = fromDir * m
    assert v.equalWithAbsError(toDir, 2 * v.baseTypeEpsilon())

    m = Mat()
    m.rotationMatrixWithUpDir(fromDir, toDirTup, upDirTup)

    v = fromDir * m
    assert v.equalWithAbsError(toDir, 2 * v.baseTypeEpsilon())

    m = Mat()
    m.rotationMatrixWithUpDir(fromDirTup, toDir, upDirTup)

    v = fromDir * m
    assert v.equalWithAbsError(toDir, 2 * v.baseTypeEpsilon())

    m = Mat()
    m.rotationMatrixWithUpDir(fromDirTup, toDirTup, upDir)

    v = fromDir * m
    assert v.equalWithAbsError(toDir, 2 * v.baseTypeEpsilon())

    upDir = V3f(1, 0, 1)
    upDir.normalize()
    fromDir = V3f(1, 1, 0)
    fromDir.normalize()
    toDir = V3f(0, 1, 1)
    toDir.normalize()
    m = Mat()
    m.rotationMatrixWithUpDir(fromDir, toDir, upDir)

    v = fromDir * m
    assert v.equalWithAbsError(toDir, V3f.baseTypeEpsilon())

    upDir = V3d(1, 0, 1)
    upDir.normalize()
    fromDir = V3d(1, 1, 0)
    fromDir.normalize()
    toDir = V3d(0, 1, 1)
    toDir.normalize()
    m = Mat()
    m.rotationMatrixWithUpDir(fromDir, toDir, upDir)

    v = fromDir * m
    assert v.equalWithAbsError(toDir, V3f.baseTypeEpsilon())

    # Determinants (by building a random singular value decomposition)

    u = Mat()
    v = Mat()
    s = Mat()

    u.rotationMatrix( V3f(random.random(),random.random(),random.random()).normalize(),
                      V3f(random.random(),random.random(),random.random()).normalize() )
    v.rotationMatrix( V3f(random.random(),random.random(),random.random()).normalize(),
                      V3f(random.random(),random.random(),random.random()).normalize() )
    s[0][0] = random.random()
    s[1][1] = random.random()
    s[2][2] = random.random()
    s[3][3] = random.random()

    c = u * s * v.transpose()
    assert abs(c.determinant() - s[0][0]*s[1][1]*s[2][2]*s[3][3]) <= u.baseTypeEpsilon()

    # Matrix minors

    a = Mat(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)
    assert a.minorOf(0,0) == a.fastMinor(1,2,3,1,2,3)
    assert a.minorOf(0,1) == a.fastMinor(1,2,3,0,2,3)
    assert a.minorOf(0,2) == a.fastMinor(1,2,3,0,1,3)
    assert a.minorOf(0,3) == a.fastMinor(1,2,3,0,1,2)
    assert a.minorOf(1,0) == a.fastMinor(0,2,3,1,2,3)
    assert a.minorOf(1,1) == a.fastMinor(0,2,3,0,2,3)
    assert a.minorOf(1,2) == a.fastMinor(0,2,3,0,1,3)
    assert a.minorOf(1,3) == a.fastMinor(0,2,3,0,1,2)
    assert a.minorOf(2,0) == a.fastMinor(0,1,3,1,2,3)
    assert a.minorOf(2,1) == a.fastMinor(0,1,3,0,2,3)
    assert a.minorOf(2,2) == a.fastMinor(0,1,3,0,1,3)
    assert a.minorOf(2,3) == a.fastMinor(0,1,3,0,1,2)
    assert a.minorOf(3,0) == a.fastMinor(0,1,2,1,2,3)
    assert a.minorOf(3,1) == a.fastMinor(0,1,2,0,2,3)
    assert a.minorOf(3,2) == a.fastMinor(0,1,2,0,1,3)
    assert a.minorOf(3,3) == a.fastMinor(0,1,2,0,1,2)

    print ("ok")
    return

def testM44 ():

    print ("M44f")
    testM44x (M44f, V3f)
    print ("M44d")
    testM44x (M44d, V3d)

testList.append (('testM44',testM44))


# -------------------------------------------------------------------------
# Tests for Mat --> Mat conversions

def testM33xConversions (Mat):

    # Assignment
    
    m1 = Mat(0,1,2, 3,4,5, 6,7,8)

    m2 = M33f (m1)
    assert m2[0][0] == 0 and m2[0][1] == 1

    m2 = M33d (m1)
    assert m2[0][0] == 0 and m2[0][1] == 1

    # The += operator

    m2 = Mat(0,1,2, 3,4,5, 6,7,8)
    m2 += M33f (m1)
    assert m2[0][0] == 0 and m2[0][1] == 2
    
    m2 = Mat(0,1,2, 3,4,5, 6,7,8)
    m2 += M33d (m1)
    assert m2[0][0] == 0 and m2[0][1] == 2
    
    # The -= operator

    m2 = Mat(0,1,2, 3,4,5, 6,7,8)
    m2 -= M33f (m1)
    assert m2[0][0] == 0 and m2[0][1] == 0
    
    m2 = Mat(0,1,2, 3,4,5, 6,7,8)
    m2 -= M33d (m1)
    assert m2[0][0] == 0 and m2[0][1] == 0

    # The *= operator

    m2 = Mat(0,1,2, 3,4,5, 6,7,8)
    m2 *= M33f (m1)
    assert m2[0][0] == 0*0 + 1*3 + 2*6
    assert m2[0][1] == 0*1 + 1*4 + 2*7
        
    m2 = Mat(0,1,2, 3,4,5, 6,7,8)
    m2 *= M33d (m1)
    assert m2[0][0] == 0*0 + 1*3 + 2*6
    assert m2[0][1] == 0*1 + 1*4 + 2*7
        
    print ("ok")
    return


def testM44xConversions (Mat):

    # Assignment
    
    m1 = Mat((0,1,2,3), (4,5,6,7), (8,9,10,11), (12,13,14,15))

    m2 = M44f (m1)
    assert m2[0][0] == 0 and m2[0][1] == 1 and m2[0][2] == 2

    m2 = M44d (m1)
    assert m2[0][0] == 0 and m2[0][1] == 1 and m2[0][2] == 2

    # The += operator

    m2 = Mat((0,1,2,3), (4,5,6,7), (8,9,10,11), (12,13,14,15))
    m2 += M44f (m1)
    assert m2[0][0] == 0 and m2[0][1] == 2
    
    m2 = Mat((0,1,2,3), (4,5,6,7), (8,9,10,11), (12,13,14,15))
    m2 += M44d (m1)
    assert m2[0][0] == 0 and m2[0][1] == 2
    
    # The -= operator

    m2 = Mat((0,1,2,3), (4,5,6,7), (8,9,10,11), (12,13,14,15))
    m2 -= M44f (m1)
    assert m2[0][0] == 0 and m2[0][1] == 0
    
    m2 = Mat((0,1,2,3), (4,5,6,7), (8,9,10,11), (12,13,14,15))
    m2 -= M44d (m1)
    assert m2[0][0] == 0 and m2[0][1] == 0
    
    # The *= operator

    m2 = Mat((0,1,2,3), (4,5,6,7), (8,9,10,11), (12,13,14,15))
    m2 *= M44f (m1)
    assert m2[0][0] == 0*0 + 1*4 + 2*8 + 3*12
    assert m2[0][1] == 0*1 + 1*5 + 2*9 + 3*13
        
    m2 = Mat((0,1,2,3), (4,5,6,7), (8,9,10,11), (12,13,14,15))
    m2 *= M44d (m1)
    assert m2[0][0] == 0*0 + 1*4 + 2*8 + 3*12
    assert m2[0][1] == 0*1 + 1*5 + 2*9 + 3*13
                
    print ("ok")
    return


def testM33xM44xConversion (MatA, MatB):

    try:
        m = MatA();
        m1 = MatB (m);           # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.


def testMatConversions ():

    print ("M33f")
    testM33xConversions (M33f)
    print ("M33d")
    testM33xConversions (M33d)

    print ("M44f")
    testM44xConversions (M44f)
    print ("M44d")
    testM44xConversions (M44d)

    print ("invalid conversions")
    # Deliberatly not exhaustive, just representative.
    testM33xM44xConversion (M33f, M44d)
    testM33xM44xConversion (M44f, M33d)

    print ("ok")
    return


testList.append (('testMatConversions',testMatConversions))


# -------------------------------------------------------------------------
# Tests for Box2x

def testBox2x (Box, Vec):

    # constructors

    b = Box()
    assert b.isEmpty() and (not b.hasVolume())

    b = Box (Vec (1, 2))
    assert (not b.isEmpty()) and (not b.hasVolume())
    assert b.min() == Vec (1, 2) and b.max() == Vec (1, 2)

    b = Box (Vec (4, 5), Vec (7, 8))
    assert (not b.isEmpty()) and b.hasVolume()
    assert b.min() == Vec (4, 5) and b.max() == Vec (7, 8)

    b1 = Box (b)
    assert b1.min() == Vec (4, 5) and b1.max() == Vec (7, 8)

    b = Box (((1, 2), (4, 5)))
    assert b.min() == Vec (1, 2) and b.max() == Vec (4, 5)

    # setMin(), setMax()

    b = Box()
    b.setMin (Vec (1, 2))
    b.setMax (Vec (3, 6))
    assert b.min() == Vec (1, 2) and b.max() == Vec (3, 6)
    assert b.size() == Vec (2, 4)
    assert b.center() == Vec (2, 4)

    # makeEmpty()

    b.makeEmpty()
    assert b.isEmpty()

    # extendBy()

    b.extendBy (Vec (1, 2))
    assert b.min() == Vec (1, 2) and b.max() == Vec (1, 2)

    b.extendBy (Vec (0, 2))
    assert b.min() == Vec (0, 2) and b.max() == Vec (1, 2)

    b.extendBy (Box (Vec (0, 0), Vec (4, 4)))
    assert b.min() == Vec (0, 0) and b.max() == Vec (4, 4)

    # intersects()

    b = Box (Vec (0, 0), Vec (4, 4))
    assert b.intersects (Vec (1, 2))
    assert not b.intersects (Vec (6, 7))
    assert b.intersects (Box (Vec (-2, -2), Vec (1, 1)))
    assert not b.intersects (Box (Vec (-2, -2), Vec (-1, -1)))

    # majorAxis()

    assert 0 == Box(Vec (0, 0), Vec (2, 1)).majorAxis()
    assert 1 == Box(Vec (0, 0), Vec (1, 2)).majorAxis()

    # repr

    b = Box (Vec (1/9., 2/9.), Vec (4/9., 5/9.))
    assert b == eval (repr (b))

    print ("ok")
    return


def testBox2():

    print ("Box2i")
    testBox2x (Box2i, V2i)
    print ("Box2f")
    testBox2x (Box2f, V2f)
    print ("Box2d")
    testBox2x (Box2d, V2d)


testList.append (('testBox2',testBox2))


# -------------------------------------------------------------------------
# Tests for Box3x

def testBox3x (Box, Vec):

    # constructors

    b = Box()
    assert b.isEmpty() and (not b.hasVolume())

    b = Box (Vec (1, 2, 3))
    assert (not b.isEmpty()) and (not b.hasVolume())
    assert b.min() == Vec (1, 2, 3) and b.max() == Vec (1, 2, 3)

    b = Box (Vec (4, 5, 6), Vec (7, 8, 9))
    assert (not b.isEmpty()) and b.hasVolume()
    assert b.min() == Vec (4, 5, 6) and b.max() == Vec (7, 8, 9)

    b1 = Box (b)
    assert b1.min() == Vec (4, 5, 6) and b1.max() == Vec (7, 8, 9)

    b = Box (((1, 2, 3), (4, 5, 6)))
    assert b.min() == Vec (1, 2, 3) and b.max() == Vec (4, 5, 6)

    # setMin(), setMax()

    b = Box()
    b.setMin (Vec (1, 2, 3))
    b.setMax (Vec (3, 6, 11))
    assert b.min() == Vec (1, 2, 3) and b.max() == Vec (3, 6, 11)
    assert b.size() == Vec (2, 4, 8)
    assert b.center() == Vec (2, 4, 7)

    # makeEmpty()

    b.makeEmpty()
    assert b.isEmpty()

    # extendBy()

    b.extendBy (Vec (1, 2, 3))
    assert b.min() == Vec (1, 2, 3) and b.max() == Vec (1, 2, 3)

    b.extendBy (Vec (0, 2, 4))
    assert b.min() == Vec (0, 2, 3) and b.max() == Vec (1, 2, 4)

    b.extendBy (Box (Vec (0, 0, 0), Vec (4, 4, 4)))
    assert b.min() == Vec (0, 0, 0) and b.max() == Vec (4, 4, 4)

    # intersects()

    b = Box (Vec (0, 0, 0), Vec (4, 4, 4))
    assert b.intersects (Vec (1, 2, 3))
    assert not b.intersects (Vec (6, 7, 8))
    assert b.intersects (Box (Vec (-2, -2, -2), Vec (1, 1, 1)))
    assert not b.intersects (Box (Vec (-2, -2, -2), Vec (-1, -1, -1)))

    # majorAxis()

    assert 0 == Box(Vec (0, 0, 0), Vec (2, 1, 1)).majorAxis()
    assert 1 == Box(Vec (0, 0, 0), Vec (1, 2, 1)).majorAxis()
    assert 2 == Box(Vec (0, 0, 0), Vec (1, 1, 2)).majorAxis()

    # repr

    b = Box (Vec (1/9., 2/9., 3/9.), Vec (4/9., 5/9., 6/9.))
    assert b == eval (repr (b))

    # tranform

    b = Box (Vec (1, 1, 1), Vec (2, 2, 2))

    mf = M44f ()
    mf.setTranslation (Vec (10, 11, 12))

    b2 = b * mf
    assert b2.min() == Vec (11, 12, 13)
    assert b2.max() == Vec (12, 13, 14)
    
    b *= mf
    assert b.min() == Vec (11, 12, 13)
    assert b.max() == Vec (12, 13, 14)
    
    b = Box (Vec (1, 1, 1), Vec (2, 2, 2))

    md = M44d ()
    md.setTranslation (Vec (10, 11, 12))

    b2 = b * md
    assert b2.min() == Vec (11, 12, 13)
    assert b2.max() == Vec (12, 13, 14)
    
    b *= md
    assert b.min() == Vec (11, 12, 13)
    assert b.max() == Vec (12, 13, 14)
    
    print ("ok")
    return


def testBox3():

    print ("Box3i")
    testBox3x (Box3i, V3i)
    print ("Box3f")
    testBox3x (Box3f, V3f)
    print ("Box3d")
    testBox3x (Box3d, V3d)


testList.append (('testBox3',testBox3))


# -------------------------------------------------------------------------
# Tests for Box --> Box conversions

def testBox2Conversions (Box, Vec):

    b1 = Box (Vec (1, 2), Vec (4, 5))

    b2 = Box2i (b1)
    assert b2.min() == V2i (1, 2) and b2.max() == V2i (4, 5)

    b2 = Box2f (b1)
    assert b2.min() == V2f (1, 2) and b2.max() == V2f (4, 5)

    b2 = Box2d (b1)
    assert b2.min() == V2d (1, 2) and b2.max() == V2d (4, 5)

    print ("ok")
    return


def testBox3Conversions (Box, Vec):

    b1 = Box (Vec (1, 2, 3), Vec (4, 5, 6))

    b2 = Box3i (b1)
    assert b2.min() == V3i (1, 2, 3) and b2.max() == V3i (4, 5, 6)

    b2 = Box3f (b1)
    assert b2.min() == V3f (1, 2, 3) and b2.max() == V3f (4, 5, 6)

    b2 = Box3d (b1)
    assert b2.min() == V3d (1, 2, 3) and b2.max() == V3d (4, 5, 6)

    print ("ok")
    return


def testBox2Box3Conversion (Box1, Box2):

    try:
        b = Box1();
        b1 = Box2 (b);           # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.


def testBoxConversions ():

    print ("Box2i")
    testBox2Conversions (Box2i, V2i)
    print ("Box2f")
    testBox2Conversions (Box2f, V2f)
    print ("Box2d")
    testBox2Conversions (Box2d, V2d)

    print ("Box3i")
    testBox3Conversions (Box3i, V3i)
    print ("Box3f")
    testBox3Conversions (Box3f, V3f)
    print ("Box3d")
    testBox3Conversions (Box3d, V3d)

    print ("invalid conversions")
    testBox2Box3Conversion (Box2i, Box3i)
    testBox2Box3Conversion (Box2i, Box3f)
    testBox2Box3Conversion (Box3d, Box2i)
    testBox2Box3Conversion (Box3f, Box2f)

    print ("ok")
    return


testList.append (('testBoxConversions',testBoxConversions))


# -------------------------------------------------------------------------
# Tests for Quatx

def testQuatx (Quat, Vec, M33, M44):

    # constructors, r(), v()
    e = 4 * Vec.baseTypeEpsilon()

    q = Quat()
    assert q.r() == 1 and q.v() == Vec (0, 0, 0)

    q = Quat (2, 3, 4, 5)
    assert q.r() == 2 and q.v() == Vec (3, 4, 5)

    q = Quat (6, Vec (7, 8, 9))
    assert q.r() == 6 and q.v() == Vec (7, 8, 9)

    q1 = Quat (q)
    assert q1.r() == 6 and q1.v() == Vec (7, 8, 9)

    # setR(), setV()

    q.setR (1)
    q.setV (Vec (2, 3, 4))
    assert q.r() == 1 and q.v() == Vec (2, 3, 4)

    # invert(), inverse()

    q = Quat (1, 0, 0, 1)
    assert q.inverse() == Quat (0.5, 0, 0, -0.5)
    q.invert()
    assert q == Quat (0.5, 0, 0, -0.5)

    # normalize(), normalized()

    q = Quat (2, Vec (0, 0, 0))
    assert q.normalized() == Quat (1, 0, 0, 0)
    q.normalize()
    assert q == Quat (1, 0, 0, 0)

    q = Quat (0, Vec (0, 2, 0))
    assert q.normalized() == Quat (0, 0, 1, 0)
    q.normalize()
    assert q == Quat (0, 0, 1, 0)

    # length()

    q = Quat (3, 0, 4, 0)
    assert q.length() == 5

    # setAxisAngle(), angle(), axis()

    q.setAxisAngle (Vec (0, 0, 1), pi/2)
    v = q.axis()
    a = q.angle()
    assert v.equalWithAbsError (Vec (0, 0, 1), e)
    assert equal(a, pi/2, e)

    # setRotation()

    q.setRotation (Vec (1, 0, 0), Vec (0, 1, 0))
    v = q.axis()
    a = q.angle()
    assert v.equalWithAbsError (Vec (0, 0, 1), e)
    assert equal(a, pi/2, e)

    # slerp()

    q = Quat()
    q.setAxisAngle (Vec (0, 0, 1), pi/2)
    p = Quat()
    p.setAxisAngle (Vec (1, 0, 0), pi/2)
    
    r = q.slerp (p, 0)

    assert equal (r.r(), sqrt(2) / 2, e)

    assert r.v().equalWithAbsError (Vec (0, 0, sqrt(2) / 2), e)
    r = q.slerp (p, 1)

    assert equal (r.r(), sqrt(2) / 2, e)

    assert r.v().equalWithAbsError (Vec (sqrt(2) / 2, 0, 0), e)

    # toMatrix33(), toMatrix44()

    q.setRotation (Vec (1, 0, 0), Vec (0, 1, 0))

    m = q.toMatrix33()

    assert m.equalWithAbsError (M33 (0, 1, 0,
                                    -1, 0, 0,
                                     0, 0, 1),
                                m.baseTypeEpsilon())
    m = q.toMatrix44()

    assert m.equalWithAbsError (M44 (( 0, 1, 0, 0),
                                     (-1, 0, 0, 0),
                                     ( 0, 0, 1, 0),
                                     ( 0, 0, 0, 1)),
                                m.baseTypeEpsilon())

    # +, - (unary and binary), ~ *, /, ^

    assert Quat (1, 2, 3, 4) + Quat (5, 6, 7, 8) == Quat (6, 8, 10, 12)

    assert Quat (-1, -2, -3, -4) - Quat (5, 6, 7, 8) == Quat (-6, -8, -10, -12)
    assert -Quat (1, 2, 3, 4) == Quat (-1, -2, -3, -4)
    
    assert ~Quat (1, 2, 3, 4) == Quat (1, -2, -3, -4)

    assert 2 * Quat (1, 2, 3, 4) == Quat (2, 4, 6, 8)
    assert Quat (1, 2, 3, 4) * 2 == Quat (2, 4, 6, 8)
    assert Quat (1, 0, 0, 1) * Quat (1, 1, 0, 0) == Quat (1, 1, 1, 1)
    assert Quat (1, 1, 0, 0) * Quat (1, 0, 0, 1) == Quat (1, 1, -1, 1)
    
    assert Quat (1, 0, 0, 1) / Quat (0.5, -0.5, 0, 0) == Quat (1, 1, 1, 1)
    assert Quat (2, 4, 6, 8) / 2 == Quat (1, 2, 3, 4)

    assert Quat (1, 2, 3, 4) ^ Quat (2, 2, 2, 2) == 20

    # repr

    q = Quat (1/9., 2/9., 3/9., 4/9.)
    assert q == eval (repr (q))

    # extract()

    m1 = M44 ()
    vFrom = Vec (1, 0, 0)
    vTo = Vec (0, 1, 1)
    m1.rotationMatrix(vFrom, vTo)
    q = Quat ()
    q.extract(m1)
    m2 = q.toMatrix44()
    assert m2.equalWithAbsError(m1, 2*m1.baseTypeEpsilon())

    print ("ok")
    return


def testQuatConversions ():

    q = Quatf (1, V3f (2, 3, 4))
    q1 = Quatd (q)
    assert q1.r() == 1 and q1.v() == V3d (2, 3, 4)

    q = Quatd (1, V3d (2, 3, 4))
    q1 = Quatf (q)
    assert q1.r() == 1 and q1.v() == V3f (2, 3, 4)

    print ("ok")
    return


def testQuat():

    print ("Quatf")
    testQuatx (Quatf, V3f, M33f, M44f)
    print ("Quatd")
    testQuatx (Quatd, V3d, M33d, M44d)
    print ("conversions")
    testQuatConversions()


testList.append (('testQuat',testQuat))


# -------------------------------------------------------------------------
# Tests for Eulerx

def testEulerx (Euler, Vec, M33, M44):

    # constructors, toXYZVector(), order()

    e = Euler()
    assert e.toXYZVector() == Vec (0, 0, 0) and e.order() == EULER_XYZ

    e = Euler (Vec (1, 2, 3))
    assert e.toXYZVector() == Vec (1, 2, 3) and e.order() == EULER_XYZ

    e = Euler (Vec (1, 2, 3), EULER_ZYX)
    assert e.toXYZVector() == Vec (3, 2, 1) and e.order() == EULER_ZYX

    e1 = Euler (e)
    assert e1.toXYZVector() == Vec (3, 2, 1) and e1.order() == EULER_ZYX

    e = Euler (4, 5, 6)
    assert e.toXYZVector() == Vec (4, 5, 6) and e.order() == EULER_XYZ

    e = Euler (4, 5, 6, EULER_ZXY)
    assert e.toXYZVector() == Vec (5, 6, 4) and e.order() == EULER_ZXY

    e = Euler (M33())
    assert e.toXYZVector() == Vec (0, 0, 0) and e.order() == EULER_XYZ

    e = Euler (M33(), EULER_ZYX)
    assert e.toXYZVector() == Vec (0, 0, 0) and e.order() == EULER_ZYX

    e = Euler (M44())
    assert e.toXYZVector() == Vec (0, 0, 0) and e.order() == EULER_XYZ

    e = Euler (M44(), EULER_ZYX)
    assert e.toXYZVector() == Vec (0, 0, 0) and e.order() == EULER_ZYX

    # comparison

    e = Euler (1, 2, 3, EULER_XYZ)

    e1 = e
    assert e1 == e

    e1 = Euler (1, 2, 3, EULER_XZY)
    assert e1 != e

    e1 = Euler (1, 1, 3, EULER_XYZ)
    assert e1 != e

    # setXYZVector(), setOrder()

    e.setXYZVector (Vec (7, 8, 9))

    e.setOrder (EULER_ZYX)
    assert e.order() == EULER_ZYX and e.toXYZVector() == Vec (9, 8, 7)

    e.setOrder (EULER_XYZ)
    assert e.order() == EULER_XYZ and e.toXYZVector() == Vec (7, 8, 9)

    # set(), frameStatic(), initialRepeated(), parityEven(), initialAxis()

    e.set (EULER_X_AXIS, 0, 0, 1)
    assert e.order() == EULER_XZX
    assert e.frameStatic() == 1
    assert e.initialRepeated() == 1
    assert e.parityEven() == 0
    assert e.initialAxis() == EULER_X_AXIS

    e.set (EULER_Y_AXIS, 1, 0, 1)
    assert e.order() == EULER_YZYr
    assert e.frameStatic() == 0
    assert e.initialRepeated() == 1
    assert e.parityEven() == 0
    assert e.initialAxis() == EULER_Y_AXIS

    e.set (EULER_Z_AXIS, 1, 1, 1)
    assert e.order() == EULER_XZXr
    assert e.frameStatic() == 0
    assert e.initialRepeated() == 1
    assert e.parityEven() == 1
    assert e.initialAxis() == EULER_Z_AXIS

    # extract()

    e = Euler (EULER_XYZ);

    m = M33 (( 0, 2, 0),        # 90-degree rotation around Z,
             (-2, 0, 0),        # scale by factor 2
             ( 0, 0, 2))

    e.extract (m);
    v = e.toXYZVector();

    assert v.equalWithAbsError (Vec (0, 0, pi/2), v.baseTypeEpsilon())

    m = M44 (( 0, 2, 0, 0),        # 90-degree rotation around Z
             (-2, 0, 0, 0),        # scale by factor 2
             ( 0, 0, 2, 0),
             ( 0, 0, 0, 1))

    e.extract (m);
    v = e.toXYZVector();

    assert v.equalWithAbsError (Vec (0, 0, pi/2), v.baseTypeEpsilon())

    # toMatrix33(), toMatrix44()

    m = e.toMatrix33();

    assert m.equalWithAbsError (M33 (0, 1, 0,
                                    -1, 0, 0,
                                     0, 0, 1),
                                m.baseTypeEpsilon())
    m = e.toMatrix44();

    assert m.equalWithAbsError (M44 (( 0, 1, 0, 0),
                                     (-1, 0, 0, 0),
                                     ( 0, 0, 1, 0),
                                     ( 0, 0, 0, 1)),
                                m.baseTypeEpsilon())
    # toQuat()

    q = e.toQuat();

    assert equal (q.r(), sqrt(2) / 2, Vec().baseTypeEpsilon())

    assert q.v().equalWithAbsError (Vec (0, 0, sqrt(2) / 2),
                                    Vec().baseTypeEpsilon())

    # angleOrder()

    e = Euler (EULER_XYZ)
    assert e.angleOrder() == (0, 1, 2)

    e = Euler (EULER_XZY)
    assert e.angleOrder() == (0, 2, 1)

    e = Euler (EULER_ZYX)
    assert e.angleOrder() == (2, 1, 0)

    # makeNear()

    e = Euler (0, 0, 0.1 + 2 * pi)
    e1 = Euler (0, 0, 0.1)

    e.makeNear (e1)
    v = e.toXYZVector()
    assert v.equalWithAbsError (Vec (0, 0, 0.1), v.baseTypeEpsilon())

    # repr

    e = Euler (1/9., 2/9., 3/9., EULER_XYZ)
    assert e == eval (repr (e))

    e = Euler (1/9., 2/9., 3/9., EULER_YXZ)
    assert e == eval (repr (e))

    e = Euler (1/9., 2/9., 3/9., EULER_XZXr)
    assert e == eval (repr (e))

    print ("ok")
    return


def testEulerConversions ():

    e = Eulerf (V3f (1, 2, 3), EULER_XYZ)
    e1 = Eulerd (e)
    assert e1.toXYZVector() == V3d (1, 2, 3) and e1.order() == EULER_XYZ

    e = Eulerd (V3d (1, 2, 3), EULER_XYZ)
    e1 = Eulerf (e)
    assert e1.toXYZVector() == V3f (1, 2, 3) and e1.order() == EULER_XYZ

    print ("ok")
    return


def testEuler():

    print ("Eulerf")
    testEulerx (Eulerf, V3f, M33f, M44f)
    print ("Eulerd")
    testEulerx (Eulerd, V3d, M33d, M44d)
    print ("conversions")
    testEulerConversions()


testList.append (('testEuler',testEuler))


# -------------------------------------------------------------------------
# Tests for Line3x

def testLine3x (Line, Vec, Mat):

    # constructors, pos(), dir()

    l = Line()
    assert l.pos() == Vec (0, 0, 0) and l.dir() == Vec (1, 0, 0)

    l = Line (Vec (1, 2, 3), Vec (1, 6, 3))
    assert l.pos() == Vec (1, 2, 3) and l.dir() == Vec (0, 1, 0)

    l1 = Line (l)
    assert l1.pos() == Vec (1, 2, 3) and l1.dir() == Vec (0, 1, 0)

    # comparison

    l = Line (Vec (1, 1, 1), Vec (2, 2, 2))
    l1 = Line (l)
    assert l == l1

    l = Line (Vec (1, 1, 1), Vec (2, 2, 3))
    assert l != l1

    l = Line (Vec (1, 1, 2), Vec (2, 2, 2))
    assert l != l1

    # setPos(), setDir(), set()

    l.setPos (Vec (4, 5, 6))
    l.setDir (Vec (0, 0, 4))
    assert l.pos() == Vec (4, 5, 6) and l.dir() == Vec (0, 0, 1)

    l.set (Vec (1, 2, 3), Vec (1, 6, 3))
    assert l.pos() == Vec (1, 2, 3) and l.dir() == Vec (0, 1, 0)

    # pointAt()

    l = Line (Vec (1, 2, 3), Vec (2, 2, 3))
    assert l.pointAt (2) == Vec (3, 2, 3)

    # distanceTo()

    l = Line (Vec (0, 0, 0), Vec (1, 0, 0))
    assert l.distanceTo (Vec (2, 3, 0)) == 3
    assert l.distanceTo (Line (Vec (0, 2, -1), Vec (0, 2, 1))) == 2

    # closestPointTo(), closestPoints()

    l = Line (Vec (1, 0, 0), Vec (2, 0, 0))
    assert l.closestPointTo (Vec (0, 1, 0)) == Vec (0, 0, 0)

    l1 = Line (Vec (0, 1, 1), Vec (0, 1, 2))
    assert l.closestPointTo (l1) == Vec (0, 0, 0)

    p = l.closestPoints (l1)
    assert p[0] == Vec (0, 0, 0) and p[1] == Vec (0, 1, 0)

    # closestTriangleVertex()

    l = Line (Vec (0, 0, 0), Vec (1, 0, 0))
    v = l.closestTriangleVertex (Vec (1, 1, 1), Vec (2, 0, 2), Vec (1, 2, 3))
    assert v == Vec (1, 1, 1)

    # intersectWithTriangle()

    l = Line (Vec (0, 0, 0), Vec (1, 0, 0))

    i = l.intersectWithTriangle (Vec (1, 1, 0), Vec (1, 2, 0), Vec (2, 2, 0))

    assert i == None

    i = l.intersectWithTriangle (Vec (4,-1,-1), Vec (4,-1, 2), Vec (4, 2,-1))

    assert i[0] == Vec (4, 0, 0)
    assert i[1].equalWithAbsError (Vec (1) / 3, i[1].baseTypeEpsilon())
    assert i[2] == 0

    # rotatePoint()

    l = Line (Vec (0, 0, 0), Vec (1, 0, 0))
    p = l.rotatePoint (Vec (2, 2, 0), pi/2)

    assert p.equalWithAbsError (Vec (2, 0, -2), p.baseTypeEpsilon())

    # line*matrix multiplication

    l = Line (Vec (0, 0, 0), Vec (1, 0, 0))

    m = Mat (( 0, 1, 0, 0),
             (-1, 0, 0, 0),
             ( 0, 0, 1, 0),
             ( 0, 0, 0, 1))

    l = l * m
    assert l.pos() == Vec (0, 0, 0) and l.dir() == Vec (0, 1, 0)

    try:
        l = m * l        # should raise TypeError
    except TypeError:
        pass
    else:
        assert 0

    # repr

    e = Line (V3f (1/9., 2/9., 3/9.), V3f (1/9., 3/9., 3/9.))
    assert e == eval (repr (e))

    print ("ok")
    return


def testLine3Conversions ():

    l = Line3f (V3f (1, 2, 3), V3f (1, 3, 3))
    l1 = Line3d (l)
    assert l1.pos() == V3d (1, 2, 3) and l1.dir() == V3d (0, 1, 0)

    l = Line3d (V3d (1, 2, 3), V3d (1, 3, 3))
    l1 = Line3f (l)
    assert l1.pos() == V3f (1, 2, 3) and l1.dir() == V3f (0, 1, 0)

    print ("ok")
    return


def testLine3():

    print ("Line3f")
    testLine3x (Line3f, V3f, M44f)
    print ("Line3d")
    testLine3x (Line3d, V3d, M44d)
    print ("conversions")
    testLine3Conversions()


testList.append (('testLine3',testLine3))


# -------------------------------------------------------------------------
# Tests for Plane3x

def testPlane3x (Plane, Vec, Mat, Line):

    # constructors, normal(), distance()

    p = Plane()
    assert p.normal() == Vec (1, 0, 0) and p.distance() == 0

    p = Plane (Vec (0, 4, 0), 3) # normal, distance
    assert p.normal() == Vec (0, 1, 0) and p.distance() == 3

    p = Plane (Vec (0, 4, 0), Vec (0, 1, 0)) # point, normal
    assert p.normal() == Vec (0, 1, 0) and p.distance() == 4

    p = Plane (Vec (0, 0, 1), Vec (2, 0, 1), Vec (0, 2, 1)) # three points
    assert p.normal() == Vec (0, 0, 1) and p.distance() == 1

    p1 = Plane (p)
    assert p1.normal() == Vec (0, 0, 1) and p1.distance() == 1

    # comparison

    p = Plane (Vec (1, 1, 1), 2)
    p1 = Plane (p)
    assert p == p1

    p = Plane (Vec (1, 1, 2), 2)
    assert p != p1

    p = Plane (Vec (1, 1, 1), 1)
    assert p != p1

    # setNormal(), setDistance()

    p = Plane(Vec (1, 1, 1), 3)
    p.setNormal (Vec (0, 0, 4))
    p.setDistance (5)
    assert p.normal() == Vec (0, 0, 1) and p.distance() == 5

    # set()

    p.set (Vec (0, 1, 0), 2) # normal, distance
    assert p.normal() == Vec (0, 1, 0) and p.distance() == 2

    p.set (Vec (0, 2, 0), Vec (0, 0, 1)) # point, normal
    assert p.normal() == Vec (0, 0, 1) and p.distance() == 0

    p.set (Vec (1, 0, 2), Vec (1, 2, 0), Vec (1, 0, 0)) # three points
    assert p.normal() == Vec (-1, 0, 0) and p.distance() == -1

    # intersect(), intersectT(), distanceTo(), reflectPoint(), reflectVector()

    p = Plane (Vec (2, 0, 2), Vec (2, 2, 0), Vec (2, 0, 0)) # three points

    l = Line (Vec (0, 0, 0), Vec (1, 0, 0))
    assert p.intersect(l) == Vec (2, 0, 0)
    assert p.intersectT(l) == 2

    assert p.distanceTo (Vec (1, 2, 3)) ==  1
    assert p.distanceTo (Vec (3, 2, 3)) == -1

    assert p.reflectPoint (Vec (1, 2, 3)) == Vec (3, 2, 3)
    assert p.reflectVector (Vec (1, 2, 3)) == Vec (1, -2, -3)

    # plane*matrix multiplication

    p = Plane (Vec (1, 0, 0), 4)

    m = Mat (( 0, 1, 0, 0),
             (-1, 0, 0, 0),
             ( 0, 0, 1, 0),
             ( 0, 0, 0, 1))

    p = p * m
    assert p.normal().equalWithAbsError (Vec (0, 1, 0), Vec().baseTypeEpsilon())
    assert equal (p.distance(), 4, Vec().baseTypeEpsilon())

    try:
        p = m * p        # should raise TypeError
    except TypeError:
        pass
    else:
        assert 0

    # unary minus operator

    assert -Plane (Vec (0, 1, 0), 4) == Plane (Vec (0, -1, 0), -4)

    # repr

    e = Plane (Vec (0/9., 1/9., 0/9.), 3/9.)
    assert e == eval (repr (e))

    print ("ok")
    return


def testPlane3Conversions ():

    p = Plane3f (V3f (1, 0, 0), 3)
    p1 = Plane3d (p)
    assert p1.normal() == V3d (1, 0, 0) and p1.distance() == 3

    p = Plane3d (V3d (1, 0, 0), 3)
    p1 = Plane3f (p)
    assert p1.normal() == V3f (1, 0, 0) and p1.distance() == 3

    print ("ok")
    return


def testPlane3():

    print ("Plane3f")
    testPlane3x (Plane3f, V3f, M44f, Line3f)
    print ("Plane3d with Line3f")
    testPlane3x (Plane3d, V3d, M44d, Line3f)
    print ("Plane3d with Line3d")
    testPlane3x (Plane3d, V3d, M44d, Line3d)
    print ("conversions")
    testPlane3Conversions()


testList.append (('testPlane3',testPlane3))


# -------------------------------------------------------------------------
# Tests for Color3x

def testColor3x (Color, maxComp):
    
    # Constructors (and element access).

    v = Color()
    assert v[0] == 0 and v[1] == 0 and v[2] == 0

    v = Color(1)
    assert v[0] == 1 and v[1] == 1 and v[2] == 1

    v = Color(0, 1, 2)
    assert v[0] == 0 and v[1] == 1 and v[2] == 2

    v = Color((0, 1, 2))
    assert v[0] == 0 and v[1] == 1 and v[2] == 2

    v = Color([0, 1, 2])
    assert v[0] == 0 and v[1] == 1 and v[2] == 2

    v = Color()
    v.setValue(0, 1, 2)
    assert v[0] == 0 and v[1] == 1 and v[2] == 2

    # Repr.

    v = Color(1/9., 2/9., 3/9.)
    assert v == eval(repr(v))

    # Sequence length.

    v = Color()
    assert len(v) == 3

    # Element setting.

    v = Color()
    v[0] = 10
    v[1] = 11
    v[2] = 12
    assert v[0] == 10 and v[1] == 11 and v[2] == 12

    try:
        v[-4] = 0           # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    try:
        v[3] = 0           # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    try:
        v[1] = "a"           # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    # Assignment.

    v1 = Color(1)
    
    v2 = v1
    assert v2[0] == 1 and v2[1] == 1 and v2[2] == 1
    v1[0] = 2
    assert v2[0] == 2 and v2[1] == 1 and v2[2] == 1
    
    # Comparison operators.

    v1 = Color(20, 20, 0)
    v2 = Color(20, 20, 0)
    v3 = Color(20, 21, 0)

    assert v1 == v2
    assert v1 != v3
    assert not (v1 < v2)
    assert v1 < v3
    assert v1 <= v2
    assert v1 <= v3
    assert not (v3 <= v1)
    assert not (v2 > v1)
    assert v3 > v1
    assert v2 >= v1
    assert v3 >= v1
    assert not (v1 >= v3)
    
    # Addition.

    v1 = Color(10, 20, 30)
    v2 = Color(30, 40, 50)

    assert v1 + v2 == Color(40, 60, 80)
    assert v2 + v1 == v1 + v2
    assert v1 + 1 == Color(11, 21, 31)
    assert 1 + v1 == v1 + 1

    # (with the switch to python2, we now allow ops between colors and tuples)
    assert v1 + (1, 2, 3) == Color(11, 22, 33)
    assert (1, 2, 3) + v1 == v1 + (1, 2, 3)

    # Subtraction and negation.

    v1 = Color(10, 20, 30)
    v2 = Color(30, 40, 50)

    assert v2 - v1 == Color(20, 20, 20)
    assert v1 - 1 == Color(9, 19, 29)
    assert 1 - v1 == - (v1 - 1)

    # (with the switch to python2, we now allow ops between colors and tuples)
    assert v1 - (1, 2, 3) == Color(9, 18, 27)
    assert (1, 2, 3) - v1 == - (v1 - (1, 2, 3))

    assert v1.negate() == Color(-10, -20, -30)

    # Multiplication.

    v1 = Color(1, 2, 3)
    v2 = Color(3, 4, 5)
    
    assert v1 * v2 == Color(3, 8, 15)
    assert v2 * v1 == v1 * v2
    assert 2 * v1 == Color(2, 4, 6)
    assert v1 * 2 == 2 * v1

    # (with the switch to python2, we now allow ops between colors and tuples)
    assert v1 * (1, 2, 3) == Color(1, 4, 9)
    assert (1, 2, 3) * v1 == v1 * (1, 2, 3)

    # Division.

    v1 = Color(10, 20, 40)
    v2 = Color(2, 4, 8)
    
    assert v1 / v2 == Color(10/2, 20/4, 40/8)
    assert v1 / 2 == Color(10/2, 20/2, 40/2)
    assert Color(40) / v1 == Color(40/10, 40/20, 40/40)

    # (with the switch to python2, we now allow ops between colors and tuples)
    assert v1 / (1, 4, 20) == Color(10/1, 20/4, 40/20)
    assert Color(20, 60, 160) / v1 == Color(20/10, 60/20, 160/40)
    
    # Color space conversion.

    c1 = Color(maxComp, 0, 0)

    c2 = c1.rgb2hsv()
    assert c2[0] == 0 and c2[1] == maxComp and c2[2] == maxComp

    c3 = c2.hsv2rgb()
    assert c3[0] == maxComp and c3[1] == 0 and c3[2] == 0    

    print ("ok")

    return

def testColor3 ():

    print ("Color3f")
    testColor3x (Color3f, 1.0)
    print ("Color3c")
    testColor3x (Color3c, 255)

testList.append (('testColor3',testColor3))


# -------------------------------------------------------------------------
# Tests for Color4x

def testColor4x (Color, maxComp):
    
    # Constructors (and element access).

    v = Color()
    assert v[0] == 0 and v[1] == 0 and v[2] == 0 and v[3] == 0

    v = Color(1)
    assert v[0] == 1 and v[1] == 1 and v[2] == 1 and v[3] == 1

    v = Color(0, 1, 2, 3)
    assert v[0] == 0 and v[1] == 1 and v[2] == 2 and v[3] == 3

    v = Color((0, 1, 2, 3))
    assert v[0] == 0 and v[1] == 1 and v[2] == 2 and v[3] == 3

    v = Color([0, 1, 2, 3])
    assert v[0] == 0 and v[1] == 1 and v[2] == 2 and v[3] == 3

    v = Color()
    v.setValue(0, 1, 2, 3)
    assert v[0] == 0 and v[1] == 1 and v[2] == 2 and v[3] == 3

    # Repr.

    v = Color(1/9., 2/9., 3/9., 4/9.)
    assert v == eval(repr(v))

    # Sequence length.

    v = Color()
    assert len(v) == 4

    # Element setting.

    v = Color()
    v[0] = 10
    v[1] = 11
    v[2] = 12
    v[3] = 13
    assert v[0] == 10 and v[1] == 11 and v[2] == 12 and v[3] == 13

    try:
        v[-5] = 0           # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    try:
        v[4] = 0           # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    try:
        v[1] = "a"           # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    # Assignment.

    v1 = Color(1)
    
    v2 = v1
    assert v2[0] == 1 and v2[1] == 1 and v2[2] == 1 and v2[3] == 1
    v1[0] = 2
    assert v2[0] == 2 and v2[1] == 1 and v2[2] == 1 and v2[3] == 1
    
    # Comparison operators.

    v1 = Color(20, 20, 0, 0)
    v2 = Color(20, 20, 0, 0)
    v3 = Color(20, 21, 0, 0)

    assert v1 == v2
    assert v1 != v3
    assert not (v1 < v2)
    assert v1 < v3
    assert v1 <= v2
    assert v1 <= v3
    assert not (v3 <= v1)
    assert not (v2 > v1)
    assert v3 > v1
    assert v2 >= v1
    assert v3 >= v1
    assert not (v1 >= v3)
    
    # Addition.

    v1 = Color(10, 20, 30, 0)
    v2 = Color(30, 40, 50, 0)

    assert v1 + v2 == Color(40, 60, 80, 0)
    assert v2 + v1 == v1 + v2
    assert v1 + 1 == Color(11, 21, 31, 1)
    assert 1 + v1 == v1 + 1

    # (with the switch to python2, we now allow ops between colors and tuples)
    assert v1 + (1, 2, 3, 4) == Color(11, 22, 33, 4)
    assert (1, 2, 3, 4) + v1 == v1 + (1, 2, 3, 4)

    # Subtraction and negation.

    v1 = Color(10, 20, 30, 0)
    v2 = Color(30, 40, 50, 0)

    assert v2 - v1 == Color(20, 20, 20, 0)
    assert v1 - 1 == Color(9, 19, 29, -1)
    assert 1 - v1 == - (v1 - 1)

    # (with the switch to python2, we now allow ops between colors and tuples)
    assert v1 - (1, 2, 3, 4) == Color(9, 18, 27, -4)
    assert (1, 2, 3, 4) - v1 == - (v1 - (1, 2, 3, 4))

    assert v1.negate() == Color(-10, -20, -30, 0)

    # Multiplication.

    v1 = Color(1, 2, 3, 0)
    v2 = Color(3, 4, 5, 0)
    
    assert v1 * v2 == Color(3, 8, 15, 0)
    assert v2 * v1 == v1 * v2
    assert 2 * v1 == Color(2, 4, 6, 0)
    assert v1 * 2 == 2 * v1

    # (with the switch to python2, we now allow ops between colors and tuples)
    assert v1 * (1, 2, 3, 4) == Color(1, 4, 9, 0)
    assert (1, 2, 3, 4) * v1 == v1 * (1, 2, 3, 4)

    # Division.

    v1 = Color(10, 20, 40, 40)
    v2 = Color(2, 4, 8, 8)
    
    assert v1 / v2 == Color(10/2, 20/4, 40/8, 40/8)
    assert v1 / 2 == Color(10/2, 20/2, 40/2, 40/2)
    assert Color(40) / v1 == Color(40/10, 40/20, 40/40, 40/40)

    # (with the switch to python2, we now allow ops between colors and tuples)
    assert v1 / (1, 4, 8, 20) == Color(10/1, 20/4, 40/8, 40/20)
    assert Color(20, 60, 160, 40) / v1 == Color(20/10, 60/20, 160/40, 40/40)

    # Color space conversion.

    c1 = Color(maxComp, 0, 0, 0)

    c2 = c1.rgb2hsv()
    assert c2[0] == 0 and c2[1] == maxComp and c2[2] == maxComp and c2[3] == 0

    c3 = c2.hsv2rgb()
    assert c3[0] == maxComp and c3[1] == 0 and c3[2] == 0 and c3[3] == 0

    print ("ok")

    return

def testColor4 ():

    print ("Color4f")
    testColor4x (Color4f, 1.0)
    print ("Color4c")
    testColor4x (Color4c, 255)

testList.append (('testColor4',testColor4))


# -------------------------------------------------------------------------
# Tests for Color --> Color conversions

def testColor3xConversions (Color):

    v1 = Color(0, 1, 2)

    v2 = Color3c (v1)
    assert v2[0] == 0 and v2[1] == 1 and v2[2] == 2

    v2 = Color3f (v1)
    assert v2[0] == 0 and v2[1] == 1 and v2[2] == 2

    print ("ok")
    return


def testColor4xConversions (Color):

    v1 = Color(0, 1, 2, 3)

    v2 = Color4c (v1)
    assert v2[0] == 0 and v2[1] == 1 and v2[2] == 2 and v2[3] == 3

    v2 = Color4f (v1)
    assert v2[0] == 0 and v2[1] == 1 and v2[2] == 2 and v2[3] == 3

    print ("ok")
    return


def testColor3xColor4xConversion (ColorA, ColorB):

    try:
        v = ColorA ();
        v1 = ColorB (v);   # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.


def testColorConversions ():

    print ("Color3c")
    testColor3xConversions (Color3c)
    print ("Color3f")
    testColor3xConversions (Color3f)
    print ("V3i")
    testColor3xConversions (V3i)
    print ("V3f")
    testColor3xConversions (V3f)
    print ("V3d")
    testColor3xConversions (V3d)

    print ("Color4c")
    testColor4xConversions (Color4c)
    print ("Color4f")
    testColor4xConversions (Color4f)

    print ("invalid conversions")
    # Deliberatly not exhaustive, just representative.
    testColor3xColor4xConversion (Color3c, Color4f)
    testColor3xColor4xConversion (Color4c, Color3f)

    print ("ok")
    return


testList.append (('testColorConversions',testColorConversions))


# -------------------------------------------------------------------------
# Tests for Frustumx

def testFrustumx (Frustum, Vec3, Mat):
    
    # Constructors (and accessors).

    f = Frustum()

    nearPlane = 1
    farPlane = 1000
    left = -2
    right = 2
    top = 2
    bottom = -2
    ortho = 1

    f = Frustum(nearPlane, farPlane, left, right, top, bottom, ortho)
    assert f.nearPlane() == nearPlane and f.farPlane() == farPlane and \
           f.left() == left and f.right() == right and \
           f.bottom() == bottom and f.top() == top and \
           f.orthographic() == ortho

    # Repr.

    f = Frustum(nearPlane, farPlane, left, right, top, bottom, ortho)
    assert f.nearPlane() == nearPlane and f.farPlane() == farPlane and \
           f.left() == left and f.right() == right and \
           f.bottom() == bottom and f.top() == top and \
           f.orthographic() == ortho
    assert f.near() == nearPlane and f.far() == farPlane

    # Assignment.

    f1 = Frustum(nearPlane, farPlane, left, right, top, bottom, ortho)
    
    f2 = f1
    assert f2.nearPlane() == f1.nearPlane() and f2.farPlane() == f1.farPlane() and \
           f2.left() == f1.left() and f2.right() == f2.right() and \
           f2.bottom() == f1.bottom() and f2.top() == f1.top() and \
           f2.orthographic() == f1.orthographic()
    assert f2.near() == f1.nearPlane() and f2.far() == f1.farPlane()

    # Planes.

    nearPlane = 1
    farPlane = 2
    left = -1
    right = 1
    top = 1
    bottom = -1
    ortho = 0
    f = Frustum(nearPlane, farPlane, left, right, top, bottom, ortho)

    p1 = f.planes();
    
    topN    = Vec3( 0, 1, 1).normalized()
    rightN  = Vec3( 1, 0, 1).normalized()
    bottomN = Vec3( 0,-1, 1).normalized()
    leftN   = Vec3(-1, 0, 1).normalized()
    nearPlaneN   = Vec3( 0, 0, 1)
    farPlaneN    = Vec3( 0, 0,-1)
    assert p1[0].normal() == topN and p1[0].distance() == 0
    assert p1[1].normal() == rightN and p1[1].distance() == 0
    assert p1[2].normal() == bottomN and p1[2].distance() == 0
    assert p1[3].normal() == leftN and p1[3].distance() == 0
    assert p1[4].normal() == nearPlaneN and p1[4].distance() == -nearPlane
    assert p1[5].normal() == farPlaneN and p1[5].distance() == farPlane

    m = Mat()
    m.rotationMatrix(Vec3(0, 0,-1), (-1, 0, 0))
    p2 = f.planes(m)

    topN    = Vec3( 1, 1, 0).normalized()
    rightN  = Vec3( 1, 0,-1).normalized()
    bottomN = Vec3( 1,-1, 0).normalized()
    leftN   = Vec3( 1, 0, 1).normalized()
    nearPlaneN   = Vec3( 1, 0, 0)
    farPlaneN    = Vec3(-1, 0, 0)
    assert p2[0].normal().equalWithAbsError(topN, topN.baseTypeEpsilon())
    assert p2[0].distance() == 0
    assert p2[1].normal().equalWithAbsError(rightN, rightN.baseTypeEpsilon())
    assert p2[1].distance() == 0
    assert p2[2].normal().equalWithAbsError(bottomN, bottomN.baseTypeEpsilon())
    assert p2[2].distance() == 0
    assert p2[3].normal().equalWithAbsError(leftN, leftN.baseTypeEpsilon())
    assert p2[3].distance() == 0
    assert p2[4].normal().equalWithAbsError(nearPlaneN, nearPlaneN.baseTypeEpsilon())
    assert equal(p2[4].distance(), -nearPlane, 2 * nearPlaneN.baseTypeEpsilon())
    assert p2[5].normal().equalWithAbsError(farPlaneN, farPlaneN.baseTypeEpsilon())
    assert equal(p2[5].distance(), farPlane, 2 * farPlaneN.baseTypeEpsilon())

    # Fovy, aspect, projection matrix.

    nearPlane = 1
    farPlane = 2
    left = -1
    right = 1
    top = 1
    bottom = -1
    ortho = 0
    f = Frustum(nearPlane, farPlane, left, right, top, bottom, ortho)

    assert equal(f.fovx(), pi / 2.0, Vec3().baseTypeEpsilon())
    assert equal(f.aspect(), 1, Vec3().baseTypeEpsilon())

    m = f.projectionMatrix()
    C = -(farPlane + nearPlane) / (farPlane - nearPlane)
    D = (-2 * farPlane * nearPlane) / (farPlane - nearPlane)
    E = 2 * nearPlane / (right - left)
    F = 2 * nearPlane / (top - bottom)
    assert m[0][0] == E
    assert m[1][1] == F
    assert m[2][2] == C
    assert m[3][2] == D

    # Window.

    nearPlane = 2
    farPlane = 4
    left = -2
    right = 2
    top = 2
    bottom = -2
    ortho = 0
    f1 = Frustum(nearPlane, farPlane, left, right, top, bottom, ortho)

    left2 = -0.5
    right2 = 0.5
    top2 = 0.25
    bottom2 = -0.25
    f2 = f1.window(left2, right2, top2, bottom2)
    assert f2.left() == -1 and f2.right() == 1
    assert f2.top() == 0.5 and f2.bottom() == -0.5

    # Project screen to ray, point to screen.

    nearPlane = 1
    farPlane = 2
    left = -1
    right = 1
    top = 1
    bottom = -1
    ortho = 0
    f = Frustum(nearPlane, farPlane, left, right, top, bottom, ortho)

    s = 0.5
    t = 0.5
    l = f.projectScreenToRay((s, t))
    
    p3d = Vec3(left + (right - left) * (1 + s) / 2.0,
             bottom + (top - bottom) * (1 + t) / 2.0, -nearPlane)
    assert iszero(l.distanceTo(p3d), 2 * p3d.baseTypeEpsilon())

    p2d = f.projectPointToScreen(p3d)
    assert p2d.equalWithAbsError((s, t), p2d.baseTypeEpsilon())

    p3df = V3f (p3d)
    p2d = f.projectPointToScreen(p3df)
    assert p2d.equalWithAbsError((s, t), p2d.baseTypeEpsilon())

    p3dd = V3d (p3d)
    p2d = f.projectPointToScreen(p3dd)
    assert p2d.equalWithAbsError((s, t), p2d.baseTypeEpsilon())

    # Conversion between depth and Z.

    f = Frustum()
    zMin = 1
    zMax = 100
    
    assert round(f.ZToDepth(zMin, zMin, zMax)) == round(-f.nearPlane())
    assert round(f.ZToDepth(zMax, zMin, zMax)) == round(-f.farPlane())
    assert (f.near() == f.nearPlane())
    assert (f.far() == f.farPlane())

    assert round(f.normalizedZToDepth(-1)) == round(-f.nearPlane())
    assert round(f.normalizedZToDepth(1)) == round(-f.farPlane())

    assert f.DepthToZ(-f.nearPlane(), zMin, zMax) == zMin
    assert f.DepthToZ(-f.farPlane(), zMin, zMax) == zMax

    # Screen and world radius conversion.

    nearPlane = 1
    farPlane = 10
    left = -1
    right = 1
    top = 1
    bottom = -1
    ortho = 0
    f = Frustum(nearPlane, farPlane, left, right, top, bottom, ortho)

    d = 4
    s = 0.75
    r1 = f.screenRadius((0, 0, -d), d * s)
    assert equal(r1, s, Vec3().baseTypeEpsilon())

    r2 = f.worldRadius((0, 0, -d), r1)
    assert equal(r2, d * s, Vec3().baseTypeEpsilon())

    print ("ok")

    return

def testFrustum ():

    print ("Frustumf")
    testFrustumx (Frustumf, V3f, M44f)

testList.append (('testFrustum',testFrustum))


# -------------------------------------------------------------------------
# Tests for random number generators

def testRandomCompare (r1a, r1b, r1c, r2):
    n = 10
    nMatch1a1b = 0
    nMatch1a1c = 0
    nMatch1a2 = 0
    for i in range(n):
        a = r1a()
        b = r1b()
        c = r1c()
        d = r2()
        if (a == b): nMatch1a1b = nMatch1a1b + 1
        if (a == c): nMatch1a1c = nMatch1a1c + 1
        if (a == d): nMatch1a2 = nMatch1a2 + 1
    assert nMatch1a1b == n
    assert nMatch1a1c == n
    assert nMatch1a2 < n
    
def testRandomCompareSphere (r1a, r1b, r1c, r2, type):
    n = 10
    nMatch1a1b = 0
    nMatch1a1c = 0
    nMatch1a2 = 0
    for i in range(n):
        a = r1a(type)
        b = r1b(type)
        c = r1c(type)
        d = r2(type)
        if (a == b): nMatch1a1b = nMatch1a1b + 1
        if (a == c): nMatch1a1c = nMatch1a1c + 1
        if (a == d): nMatch1a2 = nMatch1a2 + 1
    assert nMatch1a1b == n
    assert nMatch1a1c == n
    assert nMatch1a2 < n
    
def testRandomx (Rand):

    # Same/different seeds produces same/different sequences.

    r1a = Rand(1)
    r1b = Rand(1)
    r1c = Rand(r1a)
    r2 = Rand(2)
    
    testRandomCompare(r1a.nextb, r1b.nextb, r1c.nextb, r2.nextb)
    testRandomCompare(r1a.nexti, r1b.nexti, r1c.nexti, r2.nexti)
    testRandomCompare(r1a.nextf, r1b.nextf, r1c.nextf, r2.nextf)
    testRandomCompareSphere(r1a.nextSolidSphere, r1b.nextSolidSphere, \
                            r1c.nextSolidSphere, r2.nextSolidSphere, V2f())
    testRandomCompareSphere(r1a.nextSolidSphere, r1b.nextSolidSphere, \
                            r1c.nextSolidSphere, r2.nextSolidSphere, V2d())
    testRandomCompareSphere(r1a.nextSolidSphere, r1b.nextSolidSphere, \
                            r1c.nextSolidSphere, r2.nextSolidSphere, V3f())
    testRandomCompareSphere(r1a.nextSolidSphere, r1b.nextSolidSphere, \
                            r1c.nextSolidSphere, r2.nextSolidSphere, V3f())
    testRandomCompareSphere(r1a.nextHollowSphere, r1b.nextHollowSphere, \
                            r1c.nextHollowSphere, r2.nextHollowSphere, V2f())
    testRandomCompareSphere(r1a.nextHollowSphere, r1b.nextHollowSphere, \
                            r1c.nextHollowSphere, r2.nextHollowSphere, V2d())
    testRandomCompareSphere(r1a.nextHollowSphere, r1b.nextHollowSphere, \
                            r1c.nextHollowSphere, r2.nextHollowSphere, V3f())
    testRandomCompareSphere(r1a.nextHollowSphere, r1b.nextHollowSphere, \
                            r1c.nextHollowSphere, r2.nextHollowSphere, V3f())
    testRandomCompare(r1a.nextGauss, r1b.nextGauss, r1c.nextGauss, \
                      r2.nextGauss)
    testRandomCompareSphere(r1a.nextGaussSphere, r1b.nextGaussSphere, \
                            r1c.nextGaussSphere, r2.nextGaussSphere, V2f())
    testRandomCompareSphere(r1a.nextGaussSphere, r1b.nextGaussSphere, \
                            r1c.nextGaussSphere, r2.nextGaussSphere, V2d())
    testRandomCompareSphere(r1a.nextGaussSphere, r1b.nextGaussSphere, \
                            r1c.nextGaussSphere, r2.nextGaussSphere, V3f())
    testRandomCompareSphere(r1a.nextGaussSphere, r1b.nextGaussSphere, \
                            r1c.nextGaussSphere, r2.nextGaussSphere, V3f())

    # Init (if it works for one type, it should work for all).

    r = Rand(10)
    seq = []
    n = 10
    for i in range(n):
        seq.append(r.nextb())
    r.init(10)
    for i in range(n):
        assert r.nextb() == seq[i]

    print ("ok")

    return

def testRandom ():

    print ("Rand32")
    testRandomx (Rand32)
    print ("Rand48")
    testRandomx (Rand48)
    
testList.append (('testRandom',testRandom))

# -------------------------------------------------------------------------
# Tests C4xArrays
def testC4xArray(Array, Color, Arrayx):
    a = Array (3)

    a[0] = Color(0)
    a[1] = Color(1)
    a[2] = Color(2)

    assert a[0] == Color(0)
    assert a[1] == Color(1)
    assert a[2] == Color(2)

    # Element setting.

    a = Array(2)

    try:
        a[-3] = Color(0) # This should raise an exception.
    except:
        pass
    else:
        assert 0            # We shouldn't get here.   

    try:
        a[3] = Color(0)   # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    try:
        a[1] = "a"         # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    # Assignment.

    a = Array(2)
    a[0] = Color(0)
    a[1] = Color(1)

    # Array Component access
    
    ar = Arrayx(2)
    ag = Arrayx(2)
    ab = Arrayx(2)
    aa = Arrayx(2)
    ar[:] = a.r
    ag[:] = a.g
    ab[:] = a.b
    aa[:] = a.a

    assert ar == a.r
    assert ag == a.g
    assert ab == a.b
    assert aa == a.a

    a.r[0] = 1
    assert ar != a.r

def testC4Array ():
    print ("C4fArray")
    testC4xArray (C4fArray, Color4f, FloatArray)
    print ("C4cArray")
    testC4xArray (C4cArray, Color4c, UnsignedCharArray)

testList.append (('testC4Array',testC4Array))

# -------------------------------------------------------------------------
# Verify that floating-point exceptions, both in Imath and in Python,
# raise Python exceptions rather than causing crashes.

def testFpExceptions():

    try:
        v = V3f (1, 1, 1)
        v = v / 0
        print (v)
    except iex.MathExc:
        pass
    else:
        assert 0

    try:
        f = sqrt (-1)
        print (f)
    except ValueError:
        pass
    except OverflowError:
        pass
    else:
        assert 0

    # The overflow exception may not masked properly on Windows?
    #try:
    #    v = V3d (1e200, 1e200, 1e200)
    #    v = v * v * v
    #    print (v)
    #except iex.MathExc:
    #    pass

    try:
        f = sqrt (-1)
        print (f)
    except ValueError:
        pass
    except OverflowError:
        pass
    else:
        assert 0

    try:
        f = 1 / 0
        print (f)
    except ZeroDivisionError:
        pass
    else:
        assert 0

    print ("ok")
    return


testList.append (('testFpExceptions',testFpExceptions))

def testProcrustes():
    m = M44d()
    m.translate (V3d(10, 5, 0))

    r = Eulerd (pi, pi/4.0, 0)
    m = m * r.toMatrix44()

    n = 8
    f = []
    t = []
    w = []
    for i in range (n):
        theta = 2.0 * pi * float(i)/float(n)
        fromVec = V3d(cos(theta), sin(theta), 0)
        w.append (1)
        f.append (fromVec)
        t.append (fromVec * m)

    result = procrustesRotationAndTranslation (f, t, None, False)
    for i in range(n):
        res = f[i] * result
        assert ((res - t[i]).length2() < 1e-5)

    # Test it with arrays:
    r = Rand48(145)
    f1 = V3dArray (n)
    t1 = V3dArray (n)
    for i in range(n):
        fromVec = V3d (r.nextf(), r.nextf(), r.nextf())
        f1[i] = fromVec
        t1[i] = fromVec * m
    result = procrustesRotationAndTranslation (f1, t1, None, False)
    for i in range(n):
        res = f1[i] * result
        assert ((res - t1[i]).length2() < 1e-5)

    # Verify weights:
    f.append (V3d(0,0,0))
    t.append (V3d(10000,10000,100))
    w.append (0.0)
    result = procrustesRotationAndTranslation (f, t, w, False)
    for i in range(n):
        res = f[i] * result
        assert ((res - t[i]).length2() < 1e-5)
   
testList.append (('testProcrustes',testProcrustes))

def testSVD():
    # We'll just test the Python wrapper here; for comprehensive SVD tests,
    # please see ImathToolboxTest.
    # 4x4
    m = M44d()
    [U, S, V] = m.singularValueDecomposition(False)

    eps = 1e-4
    def sameMatrix44 (m1, m2):
        for i in range(4):
            for j in range(4):
                if (abs(m1[i][j] - m2[i][j]) > eps):
                    return False
        return True

    def sameVector4 (v1, v2):
        for i in range(4):
            if (abs(v1[i] - v2[i]) > eps):
                return False
        return True

    assert (sameMatrix44(U, M44d()));
    assert (sameMatrix44(V, M44d()));
    assert (sameVector4(S, V4d(1,1,1,1)))

    def checkSVD44(m):
        [U, S, V] = m.singularValueDecomposition(True)
        assert (sameMatrix44(U*U.transposed(), M44d()))
        assert (sameMatrix44(V*V.transposed(), M44d()))
        for i in range(3):
            assert S[i] >= 0

        assert (U.determinant() > 0)
        assert (V.determinant() > 0)

        sDiag = M44d()
        for i in range(4):
            sDiag[i][i] = S[i]
        assert (sameMatrix44(U*sDiag*V.transposed(), m))

        [U2, S2, V2] = m.singularValueDecomposition(False)
        for i in range(4):
            assert (S2[i] >= 0)
        for i in range(3):
            assert (abs(S[i] - S2[i]) < eps)
        assert (abs(abs(S[3]) - S2[3]) < eps)

    scaleMatrix = M44d()
    scaleMatrix.setScale (V3d(1, 2, 3))
    m = m * scaleMatrix
    checkSVD44(m)

    e = Eulerd (20, 30, 40)
    m = m * e.toMatrix44()
    checkSVD44(m)

    scaleMatrix.setScale (V3d(-3, 2, 3))
    m = m * e.toMatrix44()
    checkSVD44(m)
    
    # 3x3
    m = M33d()
    [U, S, V] = m.singularValueDecomposition(False)

    eps = 1e-4
    def sameMatrix33 (m1, m2):
        for i in range(3):
            for j in range(3):
                if (abs(m1[i][j] - m2[i][j]) > eps):
                    return False
        return True

    def sameVector3 (v1, v2):
        for i in range(3):
            if (abs(v1[i] - v2[i]) > eps):
                return False
        return True

    assert (sameMatrix33(U, M33d()));
    assert (sameMatrix33(V, M33d()));
    assert (sameVector3(S, V3d(1,1,1)))

    def checkSVD33(m):
        [U, S, V] = m.singularValueDecomposition(True)
        assert (sameMatrix33(U*U.transposed(), M33d()))
        assert (sameMatrix33(V*V.transposed(), M33d()))
        for i in range(3):
            assert S[i] >= 0

        assert (U.determinant() > 0)
        assert (V.determinant() > 0)

        sDiag = M33d()
        for i in range(3):
            sDiag[i][i] = S[i]
        assert (sameMatrix33(U*sDiag*V.transposed(), m))

        [U2, S2, V2] = m.singularValueDecomposition(False)
        for i in range(2):
            assert (S2[i] >= 0)
        for i in range(2):
            assert (abs(S[i] - S2[i]) < eps)
        assert (abs(abs(S[2]) - S2[2]) < eps)

    scaleMatrix = M33d (1, 0, 0, 0, 2, 0, 0, 0, 3)
    m = m * scaleMatrix
    checkSVD33(m)

    e = Eulerd (20, 30, 40)
    m = m * e.toMatrix33()
    checkSVD33(m)

    scaleMatrix = M33d (-3, 0, 0, 0, 2, 0, 0, 0, 3)
    m = m * e.toMatrix33()
    checkSVD33(m)

testList.append (('testSVD',testSVD))

def testSymmetricEigensolve():
    # We'll just test the Python wrapper here; for comprehensive eigensolver tests,
    # please see ImathToolboxTest.
    # 4x4

    eps = 1e-4
    def sameMatrix44 (m1, m2):
        for i in range(4):
            for j in range(4):
                if (abs(m1[i][j] - m2[i][j]) > eps):
                    return False
        return True

    def sameVector4 (v1, v2):
        for i in range(4):
            if (abs(v1[i] - v2[i]) > eps):
                return False
        return True
    
    m = M44d()
    [Q, S] = m.symmetricEigensolve()
    assert (sameMatrix44 (Q, M44d()))
    assert (sameVector4 (S, V4d(1,1,1,1)))

    m = M44d(2, 4, 3,  6,
             4, 1, 9,  7,
             3, 9, 10, 13,
             6, 7, 13, 27);
    [Q, S] = m.symmetricEigensolve()
    assert (sameMatrix44(Q*Q.transposed(), M44d()))

    sDiag = M44d()
    for i in range(4):
        sDiag[i][i] = S[i]
    assert (sameMatrix44 (Q * sDiag * Q.transposed(), m))

    # Verify that it checks for symmetry:
    m[2][3] = 1000
    try:
        m.symmetricEigensolve()
    except iex.ArgExc:
        pass
    else:
        assert 0

    def sameMatrix33 (m1, m2):
        for i in range(3):
            for j in range(3):
                if (abs(m1[i][j] - m2[i][j]) > eps):
                    return False
        return True

    def sameVector3 (v1, v2):
        for i in range(3):
            if (abs(v1[i] - v2[i]) > eps):
                return False
        return True
    
    m = M33d()
    [Q, S] = m.symmetricEigensolve()
    assert (sameMatrix33 (Q, M33d()))
    assert (sameVector3 (S, V3d(1,1,1)))

    m = M33d(2, 4, 3,
             4, 1, 9, 
             3, 9, 10)
    [Q, S] = m.symmetricEigensolve()
    assert (sameMatrix33(Q*Q.transposed(), M33d()))

    sDiag = M33d()
    for i in range(3):
        sDiag[i][i] = S[i]
    assert (sameMatrix33 (Q * sDiag * Q.transposed(), m))

    # Verify that it checks for symmetry:
    m[1][2] = 1000
    try:
        m.symmetricEigensolve()
    except iex.ArgExc:
        pass
    else:
        assert 0



testList.append (('testSymmetricEigensolve',testSymmetricEigensolve))

# -------------------------------------------------------------------------
# Tests C4xArrays
def testMxArray(Array, Matrix):
    a = Array (3)

    a[0] = Matrix(0)
    a[1] = Matrix(1)
    a[2] = Matrix(2)

    assert a[0] == Matrix(0)
    assert a[1] == Matrix(1)
    assert a[2] == Matrix(2)

    # Element setting.

    a = Array(2)

    try:
        a[-3] = Matrix(0) # This should raise an exception.
    except:
        pass
    else:
        assert 0            # We shouldn't get here.   

    try:
        a[3] = Matrix(0)   # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    try:
        a[1] = "a"         # This should raise an exception.
    except:
        pass
    else:
        assert 0           # We shouldn't get here.

    # Assignment.

    a = Array(2)
    a[0] = Matrix(0)
    a[1] = Matrix(1)


def testMatrixArray ():
    print ("M44fArray")
    testMxArray (M44fArray, M44f)
    print ("M44dArray")
    testMxArray (M44dArray, M44d)
    print ("M33fArray")
    testMxArray (M33fArray, M33f)
    print ("M33dArray")
    testMxArray (M33dArray, M33d)

testList.append(("testMatrixArray",testMatrixArray))

def testStringArray():

    num = 10

    s = StringArray(num)
    s2 = StringArray(num)

    assert((s != '').reduce() == 0)
    assert((s == '').reduce() == num)

    assert(('' != s).reduce() == 0)
    assert(('' == s).reduce() == num)

    assert((s != s2).reduce() == 0)
    assert((s == s2).reduce() == num)
  
    id = IntArray(num)
    id[:] = make_range(0,num)

    s = StringArray('foo', num)
    s2 = StringArray('a', num)
    s2[:] = 'foo'

    assert((s != 'foo').reduce() == 0)
    assert((s == 'foo').reduce() == num)

    assert(('foo' != s).reduce() == 0)
    assert(('foo' == s).reduce() == num)
    assert((s != s2).reduce() == 0)
    assert((s == s2).reduce() == num)

    s[id < num//2] = 'bar'
    
    assert((s != 'foo').reduce() == num/2)
    assert((s == 'foo').reduce() == num/2)

    assert(('foo' != s).reduce() == num/2)
    assert(('foo' == s).reduce() == num/2)

    assert((s != 'bar').reduce() == num/2)
    assert((s == 'bar').reduce() == num/2)

    assert(('bar' != s).reduce() == num/2)
    assert(('bar' == s).reduce() == num/2)

    assert((s != s2).reduce() == num/2)
    assert((s == s2).reduce() == num/2)
    
    for i in range(0,num):
        s2[i] = str(i)

    for i in range(0,num):
        assert(int(s2[i]) == i)

    print ("should see %d 'bar' and %d 'foo'" % (num/2,num/2))
    for m in s:
        print (m)
    print ("should see '0' through '%d'" % (num-1))
    for m in s2:
        print (m)

    print ("ok")

testList.append(("testStringArray",testStringArray))


def testWstringArray():

    num = 10

    s = WstringArray(num)
    s2 = WstringArray(num)

    assert((s != '').reduce() == 0)
    assert((s == '').reduce() == num)

    assert(('' != s).reduce() == 0)
    assert(('' == s).reduce() == num)

    assert((s != s2).reduce() == 0)
    assert((s == s2).reduce() == num)
  
    id = IntArray(num)
    id[:] = make_range(0,num)

    s = WstringArray(u'foo', num)
    s2 = WstringArray(u'a', num)
    s2[:] = u'foo'

    assert((s != u'foo').reduce() == 0)
    assert((s == u'foo').reduce() == num)

    assert((u'foo' != s).reduce() == 0)
    assert((u'foo' == s).reduce() == num)
    assert((s != s2).reduce() == 0)
    assert((s == s2).reduce() == num)

    s[id < num//2] = u'bar'
    
    assert((s != u'foo').reduce() == num/2)
    assert((s == u'foo').reduce() == num/2)

    assert((u'foo' != s).reduce() == num/2)
    assert((u'foo' == s).reduce() == num/2)

    assert((s != u'bar').reduce() == num/2)
    assert((s == u'bar').reduce() == num/2)

    assert((u'bar' != s).reduce() == num/2)
    assert((u'bar' == s).reduce() == num/2)

    assert((s != s2).reduce() == num/2)
    assert((s == s2).reduce() == num/2)
    
    for i in range(0,num):
        s2[i] = str(i)

    for i in range(0,num):
        assert(int(s2[i]) == i)

    print ("should see %d 'bar' and %d 'foo'" % (num/2,num/2))
    for m in s:
        print (m)
    print ("should see '0' through '%d'" % (num-1))
    for m in s2:
        print (m)

    print ("ok")

testList.append(("testWstringArray",testWstringArray))


# -------------------------------------------------------------------------
# Main loop

random.seed (1567)

for test in testList:
    funcName = test[0]
    print ("")
    print ("Running %s" % funcName)
    test[1]()

print ("")

# Local Variables:
# mode:python
# End:
