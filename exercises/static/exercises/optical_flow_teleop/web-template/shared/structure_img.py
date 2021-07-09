from ctypes import Structure, c_int32, c_int64

class MD(Structure):
    _fields_ = [
        ('shape_0', c_int32),
        ('shape_1', c_int32),
        ('shape_2', c_int32),
        ('size', c_int64)
    ]