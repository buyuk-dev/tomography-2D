import numpy


def compute(n):
    L = n * 2
    h = numpy.zeros(L)
    L2 = L // 2 + 1
    h[0] = 1/4.
    j = numpy.linspace(1, L2, L2//2, False)
    h[1:L2:2] = -1./(numpy.pi**2 * j**2)
    h[L2:] = numpy.copy(h[1:L2-1][::-1])
    _ramp = h * 2.0
    return numpy.abs(numpy.fft.fft(_ramp))


def filter(image, n):
    ramp = compute(n)
    filtered = numpy.fft.ifft(
        ramp * numpy.fft.fft(image, 2*n, axis=1),
        axis=1
    )[:,:n].real
    return filtered

