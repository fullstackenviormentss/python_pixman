"""A Python 3 wrapper for the Pixman pixel-manipulation library <http://www.pixman.org/>.
"""
#+
# Copyright 2015 Lawrence D'Oliveiro <ldo@geek-central.gen.nz>.
# Licensed under the GNU Lesser General Public License v2.1 or later.
#-

from numbers import \
    Number
import ctypes as ct
import qahirah

pixman = ct.cdll.LoadLibrary("libpixman-1.so.0")

class PIXMAN :
    "useful definitions adapted from pixman-1/pixman.h. You will need to use the" \
    " constants, but apart from that, see the more Pythonic wrappers defined outside" \
    " this class in preference to accessing low-level structures directly."

    # General ctypes gotcha: when passing addresses of ctypes-constructed objects
    # to routine calls, do not construct the objects directly in the call. Otherwise
    # the refcount goes to 0 before the routine is actually entered, and the object
    # can get prematurely disposed. Always store the object reference into a local
    # variable, and pass the value of the variable instead.

    fixed_32_32_t = ct.c_long
    fixed_48_16_t = ct.c_long
    fixed_1_31_t = ct.c_uint
    fixed_1_16_t = ct.c_uint
    fixed_16_16_t = ct.c_int
    fixed_t = fixed_16_16_t

    fixed_to_int = lambda f : round(f / 65536)
    int_to_fixed = lambda i : i * 65536
    fixed_to_double = lambda f : f / 65536
    double_to_fixed = lambda f : f * 65536
    fixed_e = 1 # closest nonzero value to zero
    fixed_1 = 1 << 16
    fixed_1_minus_e = fixed_1 - fixed_e
    fixed_minus_1 = - fixed_1
    fixed_frac = lambda f : f & fixed_1_minus_e
    fixed_floor = lambda f : f & ~fixed_1_minus_e
    fixed_ceil = lambda f : fixed_floor(f + fixed_1_minus_e)
    fixed_fraction = fixed_frac
    fixed_mod_2 = lambda f : f & (fixed_1 | fixed_1_minus_e)
    max_fixed_48_16 = 0x7fffffff # huh?
    min_fixed_48_16 = - max_fixed_48_16 - 1

    class color_t(ct.Structure) :
        _fields_ = \
            [
                ("red", ct.c_ushort),
                ("green", ct.c_ushort),
                ("blue", ct.c_ushort),
                ("alpha", ct.c_ushort),
            ]
    #end color_t
    color_t_ptr = ct.POINTER(color_t)

    class point_fixed_t(ct.Structure) :
        pass
    point_fixed_t._fields_ = \
        [
            ("x", fixed_t),
            ("y", fixed_t),
        ]
    #end point_fixed_t

    class line_fixed_t(ct.Structure) :
        pass
    line_fixed_t._fields_ = \
        [
            ("p1", point_fixed_t),
            ("p2", point_fixed_t),
        ]
    #end line_fixed_t

    class vector(ct.Structure) :
        pass
    vector._fields_ = \
        [
            ("vector", fixed_t * 3),
        ]
    #end vector

    class transform(ct.Structure) :
        pass
    transform._fields_ = \
        [
            ("matrix", fixed_t * 3 * 3),
        ]
    #end transform

    class f_vector(ct.Structure) :
        pass
    f_vector._fields_ = \
        [
            ("vector", ct.c_double * 3),
        ]
    #end f_vector

    class f_transform(ct.Structure) :
        pass
    f_transform._fields_ = \
        [
            ("matrix", ct.c_double * 3 * 3),
        ]
    #end f_transform

    repeat_t = ct.c_uint
    # values for repeat_t:
    REPEAT_NONE = 0
    REPEAT_NORMAL = 1
    REPEAT_PAD = 2
    REPEAT_REFLECT = 3

    filter_t = ct.c_uint
    # values for filter_t:
    FILTER_FAST = 0
    FILTER_GOOD = 1
    FILTER_BEST = 2
    FILTER_NEAREST = 3
    FILTER_BILINEAR = 4
    FILTER_CONVOLUTION = 5
    FILTER_SEPARABLE_CONVOLUTION = 6

    op_t = ct.c_uint
    # values for op_t:
    OP_CLEAR = 0x00
    OP_SRC = 0x01
    OP_DST = 0x02
    OP_OVER = 0x03
    OP_OVER_REVERSE = 0x04
    OP_IN = 0x05
    OP_IN_REVERSE = 0x06
    OP_OUT = 0x07
    OP_OUT_REVERSE = 0x08
    OP_ATOP = 0x09
    OP_ATOP_REVERSE = 0x0a
    OP_XOR = 0x0b
    OP_ADD = 0x0c
    OP_SATURATE = 0x0d
    OP_DISJOINT_CLEAR = 0x10
    OP_DISJOINT_SRC = 0x11
    OP_DISJOINT_DST = 0x12
    OP_DISJOINT_OVER = 0x13
    OP_DISJOINT_OVER_REVERSE = 0x14
    OP_DISJOINT_IN = 0x15
    OP_DISJOINT_IN_REVERSE = 0x16
    OP_DISJOINT_OUT = 0x17
    OP_DISJOINT_OUT_REVERSE = 0x18
    OP_DISJOINT_ATOP = 0x19
    OP_DISJOINT_ATOP_REVERSE = 0x1a
    OP_DISJOINT_XOR = 0x1b

    OP_CONJOINT_CLEAR = 0x20
    OP_CONJOINT_SRC = 0x21
    OP_CONJOINT_DST = 0x22
    OP_CONJOINT_OVER = 0x23
    OP_CONJOINT_OVER_REVERSE = 0x24
    OP_CONJOINT_IN = 0x25
    OP_CONJOINT_IN_REVERSE = 0x26
    OP_CONJOINT_OUT = 0x27
    OP_CONJOINT_OUT_REVERSE = 0x28
    OP_CONJOINT_ATOP = 0x29
    OP_CONJOINT_ATOP_REVERSE = 0x2a
    OP_CONJOINT_XOR = 0x2b

    OP_MULTIPLY = 0x30
    OP_SCREEN = 0x31
    OP_OVERLAY = 0x32
    OP_DARKEN = 0x33
    OP_LIGHTEN = 0x34
    OP_COLOR_DODGE = 0x35
    OP_COLOR_BURN = 0x36
    OP_HARD_LIGHT = 0x37
    OP_SOFT_LIGHT = 0x38
    OP_DIFFERENCE = 0x39
    OP_EXCLUSION = 0x3a
    OP_HSL_HUE = 0x3b
    OP_HSL_SATURATION = 0x3c
    OP_HSL_COLOR = 0x3d
    OP_HSL_LUMINOSITY = 0x3e

    region_overlap_t = ct.c_uint
    # values for region_overlap_t:
    REGION_OUT = 0
    REGION_IN = 1
    REGION_PART = 2

    # TODO: region16

    class region32_data_t(ct.Structure) :
        _fields_ = \
            [
                ("size", ct.c_long),
                ("numRects", ct.c_long),
              # ("rects", box32_t * size),
            ]
    #end region32_data_t
    region32_data_t_ptr = ct.POINTER(region32_data_t)

    class rectangle32_t(ct.Structure) :
        _fields_ = \
            [
                ("x", ct.c_int),
                ("y", ct.c_int),
                ("width", ct.c_int),
                ("height", ct.c_int),
            ]
    #end rectangle32_t

    class box32_t(ct.Structure) :
        _fields_ = \
            [
                ("x1", ct.c_int),
                ("y1", ct.c_int),
                ("x2", ct.c_int),
                ("y2", ct.c_int),
            ]
    #end box32_t
    box32_t_ptr = ct.POINTER(box32_t)

    class region32_t(ct.Structure) :
        pass
    region32_t._fields_ = \
        [
            ("extents", box32_t),
            ("data", region32_data_t_ptr),
        ]
    #end region32_t

    # Images

    MAX_INDEXED = 256
    index_type = ct.c_uint

    class indexed_t(ct.Structure) :
        pass
    indexed_t._fields_ = \
        [
            ("color", ct.c_bool),
            ("rgba", ct.c_uint * MAX_INDEXED),
            ("ent", index_type * 32768),
        ]
    #end indexed_t

    class gradient_stop_t(ct.Structure) :
        pass
    gradient_stop_t._fields_ = \
        [
            ("x", fixed_t),
            ("color", color_t),
        ]
    #end gradient_stop_t

    read_memory_func_t = ct.CFUNCTYPE(ct.c_uint, ct.c_void_p, ct.c_int)
    write_memory_func_t = ct.CFUNCTYPE(None, ct.c_void_p, ct.c_uint, ct.c_int)
    image_destroy_func_t = ct.CFUNCTYPE(None, ct.c_void_p, ct.c_void_p)

    def FORMAT(bpp, type, a, r, g, b) :
        "generates a Pixman format code from the specified components."
        return \
            (
                bpp << 24
            |
                type << 16
            |
                a << 12
            |
                r << 8
            |
                g << 4
            |
                b
            )
    #end FORMAT

    FORMAT_BPP = lambda f : f >> 24
    FORMAT_TYPE = lambda f : f >> 16 & 0xff
    FORMAT_A = lambda f : f >> 12 & 0x0f
    FORMAT_R = lambda f : f >> 8 & 0x0f
    FORMAT_G = lambda f : f >> 4 & 0x0f
    FORMAT_B = lambda f : f & 0x0f
    FORMAT_RGB = lambda f : f & 0xfff
    FORMAT_VIS = lambda f : f & 0xffff
    FORMAT_DEPTH = lambda f : FORMAT_A(f) + FORMAT_R(f) + FORMAT_G(f) + FORMAT_B(f)

    TYPE_OTHER = 0
    TYPE_A = 1
    TYPE_ARGB = 2
    TYPE_ABGR = 3
    TYPE_COLOR = 4
    TYPE_GRAY = 5
    TYPE_YUY2 = 6
    TYPE_YV12 = 7
    TYPE_BGRA = 8
    TYPE_RGBA = 9
    TYPE_ARGB_SRGB = 10

    FORMAT_COLOR = lambda f : FORMAT_TYPE(f) in (TYPE_ARGB, TYPE_ABGR, TYPE_BGRA, TYPE_RGBA)

    format_code_t = ct.c_uint
    # values for format_code_t -- 32 bits per pixel
    a8r8g8b8 = FORMAT(32,TYPE_ARGB,8,8,8,8)
    x8r8g8b8 = FORMAT(32,TYPE_ARGB,0,8,8,8)
    a8b8g8r8 = FORMAT(32,TYPE_ABGR,8,8,8,8)
    x8b8g8r8 = FORMAT(32,TYPE_ABGR,0,8,8,8)
    b8g8r8a8 = FORMAT(32,TYPE_BGRA,8,8,8,8)
    b8g8r8x8 = FORMAT(32,TYPE_BGRA,0,8,8,8)
    r8g8b8a8 = FORMAT(32,TYPE_RGBA,8,8,8,8)
    r8g8b8x8 = FORMAT(32,TYPE_RGBA,0,8,8,8)
    x14r6g6b6 = FORMAT(32,TYPE_ARGB,0,6,6,6)
    x2r10g10b10 = FORMAT(32,TYPE_ARGB,0,10,10,10)
    a2r10g10b10 = FORMAT(32,TYPE_ARGB,2,10,10,10)
    x2b10g10r10 = FORMAT(32,TYPE_ABGR,0,10,10,10)
    a2b10g10r10 = FORMAT(32,TYPE_ABGR,2,10,10,10)

    # sRGB
    a8r8g8b8_sRGB = FORMAT(32,TYPE_ARGB_SRGB,8,8,8,8)

    # values for format_code_t -- 24 bits per pixel
    r8g8b8 = FORMAT(24,TYPE_ARGB,0,8,8,8)
    b8g8r8 = FORMAT(24,TYPE_ABGR,0,8,8,8)

    # values for format_code_t -- 16 bits per pixel
    r5g6b5 = FORMAT(16,TYPE_ARGB,0,5,6,5)
    b5g6r5 = FORMAT(16,TYPE_ABGR,0,5,6,5)

    a1r5g5b5 = FORMAT(16,TYPE_ARGB,1,5,5,5)
    x1r5g5b5 = FORMAT(16,TYPE_ARGB,0,5,5,5)
    a1b5g5r5 = FORMAT(16,TYPE_ABGR,1,5,5,5)
    x1b5g5r5 = FORMAT(16,TYPE_ABGR,0,5,5,5)
    a4r4g4b4 = FORMAT(16,TYPE_ARGB,4,4,4,4)
    x4r4g4b4 = FORMAT(16,TYPE_ARGB,0,4,4,4)
    a4b4g4r4 = FORMAT(16,TYPE_ABGR,4,4,4,4)
    x4b4g4r4 = FORMAT(16,TYPE_ABGR,0,4,4,4)

    # values for format_code_t -- 8 bits per pixel
    a8 = FORMAT(8,TYPE_A,8,0,0,0)
    r3g3b2 = FORMAT(8,TYPE_ARGB,0,3,3,2)
    b2g3r3 = FORMAT(8,TYPE_ABGR,0,3,3,2)
    a2r2g2b2 = FORMAT(8,TYPE_ARGB,2,2,2,2)
    a2b2g2r2 = FORMAT(8,TYPE_ABGR,2,2,2,2)

    c8 = FORMAT(8,TYPE_COLOR,0,0,0,0)
    g8 = FORMAT(8,TYPE_GRAY,0,0,0,0)

    x4a4 = FORMAT(8,TYPE_A,4,0,0,0)

    x4c4 = FORMAT(8,TYPE_COLOR,0,0,0,0)
    x4g4 = FORMAT(8,TYPE_GRAY,0,0,0,0)

    # values for format_code_t -- 4 bits per pixel
    a4 = FORMAT(4,TYPE_A,4,0,0,0)
    r1g2b1 = FORMAT(4,TYPE_ARGB,0,1,2,1)
    b1g2r1 = FORMAT(4,TYPE_ABGR,0,1,2,1)
    a1r1g1b1 = FORMAT(4,TYPE_ARGB,1,1,1,1)
    a1b1g1r1 = FORMAT(4,TYPE_ABGR,1,1,1,1)

    c4 = FORMAT(4,TYPE_COLOR,0,0,0,0)
    g4 = FORMAT(4,TYPE_GRAY,0,0,0,0)

    # values for format_code_t -- 1 bit per pixel
    a1 = FORMAT(1,TYPE_A,1,0,0,0)

    g1 = FORMAT(1,TYPE_GRAY,0,0,0,0)

    # values for format_code_t -- YUV
    yuy2 = FORMAT(16,TYPE_YUY2,0,0,0,0)
    yv12 = FORMAT(12,TYPE_YV12,0,0,0,0)

    kernel_t = ct.c_uint
    # values for kernel_t:
    KERNEL_IMPULSE = 0
    KERNEL_BOX = 1
    KERNEL_LINEAR = 2
    KERNEL_CUBIC = 3
    KERNEL_GAUSSIAN = 4
    KERNEL_LANCZOS2 = 5
    KERNEL_LANCZOS3 = 6
    KERNEL_LANCZOS3_STRETCHED = 7

    # TODO: glyphs

#end PIXMAN

# TODO: fixed-point and floating-point transformations
# TODO: 16-bit regions?

pixman.pixman_region32_init.restype = None
pixman.pixman_region32_init.argtypes = (ct.c_void_p,)
pixman.pixman_region32_init_rect.restype = None
pixman.pixman_region32_init_rect.argtypes = (ct.c_void_p, ct.c_int, ct.c_int, ct.c_uint, ct.c_uint)
pixman.pixman_region32_init_rects.restype = ct.c_bool
pixman.pixman_region32_init_rects.argtypes = (ct.c_void_p, ct.c_void_p, ct.c_int)
pixman.pixman_region32_init_with_extents.restype = None
pixman.pixman_region32_init_with_extents.argtypes = (ct.c_void_p, ct.c_void_p)
pixman.pixman_region32_init_from_image.restype = None
pixman.pixman_region32_init_from_image.argtypes = (ct.c_void_p, ct.c_void_p)
pixman.pixman_region32_fini.restype = None
pixman.pixman_region32_fini.argtypes = (ct.c_void_p,)
pixman.pixman_region32_translate.restype = None
pixman.pixman_region32_translate.argtypes = (ct.c_void_p, ct.c_int, ct.c_int)
pixman.pixman_region32_copy.restype = ct.c_bool
pixman.pixman_region32_copy.argtypes = (ct.c_void_p, ct.c_void_p)
pixman.pixman_region32_intersect.restype = ct.c_bool
pixman.pixman_region32_intersect.argtypes = (ct.c_void_p, ct.c_void_p, ct.c_void_p)
pixman.pixman_region32_union.restype = ct.c_bool
pixman.pixman_region32_union.argtypes = (ct.c_void_p, ct.c_void_p, ct.c_void_p)
pixman.pixman_region32_intersect_rect.restype = ct.c_bool
pixman.pixman_region32_intersect_rect.argtypes = (ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int, ct.c_uint, ct.c_uint)
pixman.pixman_region32_union_rect.restype = ct.c_bool
pixman.pixman_region32_union_rect.argtypes = (ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int, ct.c_uint, ct.c_uint)
pixman.pixman_region32_subtract.restype = ct.c_bool
pixman.pixman_region32_subtract.argtypes = (ct.c_void_p, ct.c_void_p, ct.c_void_p)
pixman.pixman_region32_inverse.restype = ct.c_bool
pixman.pixman_region32_inverse.argtypes = (ct.c_void_p, ct.c_void_p, ct.c_void_p)
pixman.pixman_region32_contains_point.restype = ct.c_bool
pixman.pixman_region32_contains_point.argtypes = (ct.c_void_p, ct.c_int, ct.c_int, ct.c_void_p)
pixman.pixman_region32_contains_rectangle.restype = PIXMAN.region_overlap_t
pixman.pixman_region32_contains_rectangle.argtypes = (ct.c_void_p, ct.c_void_p)
pixman.pixman_region32_not_empty.restype = ct.c_bool
pixman.pixman_region32_not_empty.argtypes = (ct.c_void_p,)
pixman.pixman_region32_extents.restype = PIXMAN.box32_t_ptr
pixman.pixman_region32_extents.argtypes = (ct.c_void_p,)
pixman.pixman_region32_n_rects.restype = ct.c_int
pixman.pixman_region32_n_rects.argtypes = (ct.c_void_p,)
pixman.pixman_region32_rectangles.restype = ct.c_void_p
pixman.pixman_region32_rectangles.argtypes = (ct.c_void_p, ct.c_void_p)
pixman.pixman_region32_equal.restype = ct.c_bool
pixman.pixman_region32_equal.argtypes = (ct.c_void_p, ct.c_void_p)
pixman.pixman_region32_selfcheck.restype = ct.c_bool
pixman.pixman_region32_selfcheck.argtypes = (ct.c_void_p,)
pixman.pixman_region32_reset.restype = None
pixman.pixman_region32_reset.argtypes = (ct.c_void_p, ct.c_void_p)
pixman.pixman_region32_clear.restype = None
pixman.pixman_region32_clear.argtypes = (ct.c_void_p,)

pixman.pixman_blt.restype = ct.c_bool
pixman.pixman_blt.argtypes = (ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int, ct.c_int, ct.c_int, ct.c_int, ct.c_int, ct.c_int, ct.c_int, ct.c_int, ct.c_int)
pixman.pixman_fill.restype = ct.c_bool
pixman.pixman_fill.argtypes = (ct.c_void_p, ct.c_int, ct.c_int, ct.c_int, ct.c_int, ct.c_int, ct.c_int, ct.c_uint)
pixman.pixman_version.restype = ct.c_int
pixman.pixman_version_string.restype = ct.c_char_p

pixman.pixman_format_supported_destination.restype = ct.c_bool
pixman.pixman_format_supported_destination.argtypes = (ct.c_uint,)
pixman.pixman_format_supported_source.restype = ct.c_bool
pixman.pixman_format_supported_source.argtypes = (ct.c_uint,)

pixman.pixman_image_create_solid_fill.restype = ct.c_void_p
pixman.pixman_image_create_solid_fill.argtypes = (ct.c_void_p,)
pixman.pixman_image_create_linear_gradient.restype = ct.c_void_p
pixman.pixman_image_create_linear_gradient.argtypes = (ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_int)
pixman.pixman_image_create_radial_gradient.restype = ct.c_void_p
pixman.pixman_image_create_radial_gradient.argtypes = (ct.c_void_p, ct.c_void_p, PIXMAN.fixed_t, PIXMAN.fixed_t, ct.c_void_p, ct.c_int)
pixman.pixman_image_create_conical_gradient.restype = ct.c_void_p
pixman.pixman_image_create_conical_gradient.argtypes = (ct.c_void_p, PIXMAN.fixed_t, ct.c_void_p, ct.c_int)
pixman.pixman_image_create_bits.restype = ct.c_void_p
pixman.pixman_image_create_bits.argtypes = (PIXMAN.format_code_t, ct.c_int, ct.c_int, ct.c_void_p, ct.c_int)
pixman.pixman_image_create_bits_no_clear.restype = ct.c_void_p
pixman.pixman_image_create_bits_no_clear.argtypes = (PIXMAN.format_code_t, ct.c_int, ct.c_int, ct.c_void_p, ct.c_int)
pixman.pixman_image_ref.restype = ct.c_void_p
pixman.pixman_image_ref.argtypes = (ct.c_void_p,)
pixman.pixman_image_unref.restype = ct.c_bool
pixman.pixman_image_unref.argtypes = (ct.c_void_p,)
pixman.pixman_image_set_destroy_function.restype = None
pixman.pixman_image_set_destroy_function.argtypes = (ct.c_void_p, PIXMAN.image_destroy_func_t, ct.c_void_p)
pixman.pixman_image_get_destroy_data.restype = ct.c_void_p
pixman.pixman_image_get_destroy_data.argtypes = (ct.c_void_p,)
pixman.pixman_image_set_clip_region.restype = ct.c_bool
pixman.pixman_image_set_clip_region.argtypes = (ct.c_void_p, ct.c_void_p)
pixman.pixman_image_set_clip_region32.restype = ct.c_bool
pixman.pixman_image_set_clip_region32.argtypes = (ct.c_void_p, ct.c_void_p)
pixman.pixman_image_set_has_client_clip.restype = None
pixman.pixman_image_set_has_client_clip.argtypes = (ct.c_void_p, ct.c_bool)
pixman.pixman_image_set_transform.restype = ct.c_bool
pixman.pixman_image_set_transform.argtypes = (ct.c_void_p, ct.c_void_p)
pixman.pixman_image_set_repeat.restype = None
pixman.pixman_image_set_repeat.argtypes = (ct.c_void_p, PIXMAN.repeat_t)
pixman.pixman_image_set_filter.restype = ct.c_bool
pixman.pixman_image_set_filter.argtypes = (ct.c_void_p, PIXMAN.filter_t, ct.c_void_p, ct.c_int)
pixman.pixman_image_set_source_clipping.restype = None
pixman.pixman_image_set_source_clipping.argtypes = (ct.c_void_p, ct.c_bool)
pixman.pixman_image_set_alpha_map.restype = None
pixman.pixman_image_set_alpha_map.argtypes = (ct.c_void_p, ct.c_void_p, ct.c_short, ct.c_short)
pixman.pixman_image_set_component_alpha.restype = None
pixman.pixman_image_set_component_alpha.argtypes = (ct.c_void_p, ct.c_bool)
pixman.pixman_image_get_component_alpha.restype = ct.c_bool
pixman.pixman_image_get_component_alpha.argtypes = (ct.c_void_p,)
pixman.pixman_image_set_accessors.restype = None
pixman.pixman_image_set_accessors.argtypes = (ct.c_void_p, PIXMAN.read_memory_func_t, PIXMAN.write_memory_func_t)
pixman.pixman_image_set_indexed.restype = None
pixman.pixman_image_set_indexed.argtypes = (ct.c_void_p, ct.c_void_p)
pixman.pixman_image_get_data.restype = ct.c_void_p
pixman.pixman_image_get_data.argtypes = (ct.c_void_p,)
pixman.pixman_image_get_width.restype = ct.c_int
pixman.pixman_image_get_width.argtypes = (ct.c_void_p,)
pixman.pixman_image_get_height.restype = ct.c_int
pixman.pixman_image_get_height.argtypes = (ct.c_void_p,)
pixman.pixman_image_get_stride.restype = ct.c_int
pixman.pixman_image_get_stride.argtypes = (ct.c_void_p,)
pixman.pixman_image_get_depth.restype = ct.c_int
pixman.pixman_image_get_depth.argtypes = (ct.c_void_p,)
pixman.pixman_image_get_format.restype = PIXMAN.format_code_t
pixman.pixman_image_get_format.argtypes = (ct.c_void_p,)
pixman.pixman_filter_create_separable_convolution.restype = ct.c_void_p
pixman.pixman_filter_create_separable_convolution.argtypes = (ct.c_void_p, PIXMAN.fixed_t, PIXMAN.fixed_t, PIXMAN.kernel_t, PIXMAN.kernel_t, PIXMAN.kernel_t, PIXMAN.kernel_t, ct.c_int, ct.c_int)
pixman.pixman_image_fill_rectangles.restype = ct.c_bool
pixman.pixman_image_fill_rectangles.argtypes = (PIXMAN.op_t, ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_void_p)
pixman.pixman_image_fill_boxes.restype = ct.c_bool
pixman.pixman_image_fill_boxes.argtypes = (PIXMAN.op_t, ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_void_p)
pixman.pixman_compute_composite_region.restype = ct.c_bool
pixman.pixman_compute_composite_region.argtypes = (ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_short, ct.c_short, ct.c_short, ct.c_short, ct.c_short, ct.c_short, ct.c_short, ct.c_short)
pixman.pixman_image_composite.restype = None
pixman.pixman_image_composite.argtypes = (PIXMAN.op_t, ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_short, ct.c_short, ct.c_short, ct.c_short, ct.c_short, ct.c_short, ct.c_short, ct.c_short)
pixman.pixman_image_composite32.restype = None
pixman.pixman_image_composite32.argtypes = (PIXMAN.op_t, ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int, ct.c_int, ct.c_int, ct.c_int, ct.c_int, ct.c_int, ct.c_int)

# TODO: glyphs

#+
# Higher-level stuff follows
#-

def version() :
    "returns the integer Pixman version."
    return \
        pixman.pixman_version()
#end version

def version_string() :
    "returns the Pixman version string."
    return \
        pixman.pixman_version_string()
#end version_string

class Point(qahirah.Vector) :
    "augment Vector with additional Pixman-specific functionality."

    __slots__ = () # to forestall typos

    @staticmethod
    def from_pixman_fixed(p) :
        return \
            Point \
              (
                x = PIXMAN.fixed_t_double(p.x),
                y = PIXMAN.fixed_t_double(p.y),
              )
    #end from_pixman_fixed

    def to_pixman_fixed(self) :
        return \
            PIXMAN.point_fixed_t \
              (
                x = PIXMAN.double_to_fixed(self.x),
                y = PIXMAN.double_to_fixed(self.y),
              )
    #end to_pixman_fixed

#end Point

class Rect(qahirah.Rect) :
    "augment Rect with additional Pixman-specific functionality."

    __slots__ = () # to forestall typos

    @staticmethod
    def from_pixman_box(b) :
        return \
            Rect.from_corners((b.x1, b.y1), (b.x2, b.y2))
    #end from_pixman_box

    def to_pixman_box(self) :
        return \
            PIXMAN.box32_t(self.left, self.top, self.right, self.bottom)
    #end to_pixman_box

#end Rect

class Region :
    "wrapper for a Pixman region32_t. Do not instantiate directly; use one of the create methods."

    __slots__ = ("_region",) # to forestall typos

    def __init__(self) :
        self._region = PIXMAN.region32_t()
    #end __init__

    @staticmethod
    def create() :
        result = Region()
        pixman.pixman_region32_init(ct.byref(result._region))
        return \
            result
    #end create

    @staticmethod
    def create_rect(rect) :
        result = Region()
        assert rect.isint()
        pixman.pixman_region32_init_rect(ct.byref(result._region), rect.left, rect.top, rect.width, rect.height)
        return \
            result
    #end create_rect

    @staticmethod
    def create_rects(rects) :
        result = Region()
        nr_rects = len(rects)
        c_rects = (PIXMAN.box32_t * nr_rects)()
        for i in range(nr_rects) :
            assert rects[i].isint()
            c_rects[i] = rects[i].to_pixman_box()
        #end for
        validated = pixman.pixman_region32_init_rects(ct.byref(result._region), ct.byref(c_rects), nr_rects)
        return \
            (result, validated)
    #end create_rects

    @staticmethod
    def create_with_extents(extents) :
        result = Region()
        assert extents.isint()
        c_extents = extents.to_pixman_box()
        pixman.pixman_region32_init_with_extents(ct.byref(result._region), ct.byref(c_extents))
        return \
            result
    #end create_with_extents

    @staticmethod
    def create_from_image(image) :
        if not isinstance(image, Image) :
            raise TypeError("image must be an Image")
        #end if
        result = Region()
        pixman.pixman_region32_init_from_image(ct.byref(result._region), image._pmobj)
        return \
            result
    #end create_from_image

    def __del__(self) :
        if self._region != None :
            pixman.pixman_region32_fini(ct.byref(self._region))
            self._region = None
        #end if
    #end __del__

    def translate(offset) :
        offset = Vector.from_tuple(offset)
        assert offset.isint()
        pixman.pixman_region32_translate(ct.byref(self._region), offset.x, offset.y)
        return \
            self
    #end translate

    def copy(self, dest) :
        if not isinstance(dest, Region) :
            raise TypeError("dest must be a Region")
        #end if
        if not pixman.pixman_region32_copy(ct.byref(dest._region), ct.byref(self._region)) :
            raise MemoryError("Pixman couldn’t copy region")
        #end if
        return \
            self
    #end copy

    def intersect(reg1, reg2, new_reg) :
        if not isinstance(reg1, Region) or not isinstance(new_reg, Region) :
            raise TypeError("args must be Regions")
        #end if
        if not pixman.pixman_region32_intersect(ct.byref(new_reg._region), ct.byref(reg1._region), ct.byref(reg2._region)) :
            raise MemoryError("Pixman couldn’t intersect regions")
        #end if
        return \
            self
    #end intersect

    def union(reg1, reg2, new_reg) :
        if not isinstance(reg1, Region) or not isinstance(new_reg, Region) :
            raise TypeError("args must be Regions")
        #end if
        if not pixman.pixman_region32_union(ct.byref(new_reg._region), ct.byref(reg1._region), ct.byref(reg2._region)) :
            raise MemoryError("Pixman couldn’t union regions")
        #end if
        return \
            self
    #end intersect

    def intersect_rect(self, rect, dest) :
        if not isinstance(dest, Region) :
            raise TypeError("dest must be a Region")
        #end if
        assert rect.isint()
        if not pixman.pixman_region32_intersect_rect(ct.byref(dest._region), ct.byref(self._region), rect.left, rect.top, rect.width, rect.height) :
            raise MemoryError("Pixman couldn’t intersect region")
        #end if
        return \
            self
    #end intersect_rect

    def union_rect(self, rect, dest) :
        if not isinstance(dest, Region) :
            raise TypeError("dest must be a Region")
        #end if
        assert rect.isint()
        if not pixman.pixman_region32_union_rect(ct.byref(dest._region), ct.byref(self._region), rect.left, rect.top, rect.width, rect.height) :
            raise MemoryError("Pixman couldn’t union region")
        #end if
        return \
            self
    #end union_rect

    def subtract(reg1, reg2, new_reg) :
        if not isinstance(reg1, Region) or not isinstance(new_reg, Region) :
            raise TypeError("args must be Regions")
        #end if
        if not pixman.pixman_region32_subtract(ct.byref(new_reg._region), ct.byref(reg1._region), ct.byref(reg2._region)) :
            raise MemoryError("Pixman couldn’t subtract regions")
        #end if
        return \
            self
    #end subtract

    def inverse(self, inv_rect, new_reg) :
        if not isinstance(new_reg, Region) :
            raise TypeError("new_reg must be Region")
        #end if
        assert inv_rect.isint()
        c_inv_rect = inv_rect.to_pixman_box()
        if not pixman.pixman_region32_inverse(ct.byref(self._region), ct.byref(c_inv_rect), ct.byref(new_reg._region)) :
            raise MemoryError("Pixman couldn’t invert region")
        #end if
        return \
            self
    #end inverse

    def contains_point(self, point, want_box = False) :
        point = Vector.from_tuple(point)
        assert point.isint()
        if want_box :
            box = ct.pointer(PIXMAN.box32_t())
        else :
            box = None
        #end if
        contains = pixman.pixman_region32_contains_point(ct.byref(self._region), point.x, point.y, box)
        if want_box :
            result = (contains, Rect.from_pixman_box(box.contents))
        else :
            result = contains
        #end if
        return \
            result
    #end contains_point

    def contains_rectangle(self, prect) :
        c_prect = prect.to_pixman_box()
        return \
            pixman.pixman_region32_contains_rectangle(ct.byref(self._region), ct.byref(c_prect))
    #end contains_rectangle

    @property
    def not_empty(self) :
        return \
            pixman.pixman_region32_not_empty(ct.byref(self._region))
    #end not_empty

    @property
    def extents(self) :
        return \
            Rect.from_pixman_box(pixman.pixman_region32_extents(ct.byref(self._region)).contents)
    #end extents

    @property
    def n_rects(self) :
        "the number of rectangles making up the Region."
        return \
            pixman.pixman_region32_n_rects(ct.byref(self._region))
    #end n_rects

    def rectangles(self) :
        "iterates over the rectangles making up the Region."
        nr_rects = ct.c_int()
        rects = pixman.pixman_region32_rectangles(ct.byref(self._region), ct.byref(nr_rects))
        nr_rects = nr_rects.value
        rects = ct.cast(rects, PIXMAN.box32_t_ptr)
        for i in range(nr_rects) :
            yield Rect.from_pixman_box(rects[i])
        #end for
    #end rectangles

    def __eq__(rgn1, rgn2) :
        "equality of two Regions."
        if not isinstance(rgn2, Region) :
            raise TypeError("args must be Regions")
        #end if
        return \
            pixman.pixman_region32_equal(ct.byref(rgn1._region), ct.byref(rgn2._region))
    #end __eq__

    def selfcheck(self) :
        if not pixman.pixman_region32_selfcheck(ct.byref(self._region)) :
            raise RuntimeError("Region failed Pixman selfcheck")
        #end if
        return \
            self
    #end selfcheck

    def reset(self, box) :
        "resets the Region to a simple rectangle."
        c_box = box.to_pixman_box()
        pixman.pixman_region32_reset(ct.byref(self._region), ct.byref(c_box))
        return \
            self
    #end reset

    def clear(self) :
        pixman.pixman_region32_clear(ct.byref(self._region))
    #end clear

#end Region

class Colour(qahirah.Colour) :
    "augment Colour with additional Pixman-specific functionality."

    __slots__ = () # to forestall typos

    @staticmethod
    def from_pixman(c) :
        return \
            Colour.from_rgba \
              ((
                c.red / 65535,
                c.green / 65535,
                c.blue / 65535,
                c.alpha / 65535,
              ))
    #end from_pixman

    def to_pixman(self) :
        return \
            PIXMAN.color_t \
              (
                red = round(self.r * 65535),
                green = round(self.g * 65535),
                blue = round(self.b * 65535),
                alpha = round(self.a * 65535),
              )
    #end to_pixman

#end Colour

class GradientStop :
    "representation of a Pixman gradient stop."

    def __init__(self, x, colour) :
        if not isinstance(x, Number) or not isinstance(colour, Colour) :
            raise TypeError("invalid arg types")
        #end if
        self.x = x
        self.colour = colour
    #end __init__

    @staticmethod
    def from_pixman(gs) :
        return \
            GradientStop(PIXMAN.fixed_to_double(gs.x), Colour.from_pixman(gs.color))
    #end from_pixman

    def to_pixman(self) :
        return \
            PIXMAN.gradient_stop_t(PIXMAN.double_to_fixed(self.x), self.colour.to_pixman())
    #end to_pixman

    @staticmethod
    def to_pixman_array(stops) :
        "given a sequence of GradientStop objects, returns an array of Pixman" \
        " gradient_stop_t values along with the length of the array."
        nr_stops = len(stops)
        c_stops = (PIXMAN.gradient_stop_t * nr_stops)()
        for i in range(nr_stops) :
            c_stops[i] = stops[i].to_pixman()
        #end for
        return \
            c_stops, nr_stops
    #end to_pixman_array

#end GradientStop

def format_supported_destination(format) :
    return \
        pixman.pixman_format_supported_destination(format)
#end format_supported_destination

def format_supported_source(format) :
    return \
        pixman.pixman_format_supported_source(format)
#end format_supported_source

class Image :
    "wrapper for a Pixman image. Do not instantiate directly; use the create methods."

    __slots__ = ("_pmobj",) # to forestall typos

    def __init__(self, _pmobj) :
        self._pmobj = _pmobj
    #end __init__

    def __del__(self) :
        if self._pmobj != None :
            pixman.pixman_image_unref(self._pmobj)
            self._pmobj = None
        #end if
    #end __del__

    @staticmethod
    def create_solid_fill(colour) :
        "creates an image whose content consists of a single solid colour."
        c_colour = colour.to_pixman()
        return \
            Image(pixman.pixman_image_create_solid_fill(ct.byref(c_colour)))
    #end create_solid_fill

    @staticmethod
    def create_linear_gradient(p1, p2, stops) :
        c_p1 = p1.to_pixman_fixed()
        c_p2 = p2.to_pixman_fixed()
        c_stops, nr_stops = GradientStop.to_pixman_array(stops)
        return \
            Image(pixman.pixman_image_create_linear_gradient(ct.byref(c_p1), ct.byref(c_p2), ct.byref(c_stops), nr_stops))
    #end create_linear_gradient

    @staticmethod
    def create_radial_gradient(inner, outer, inner_radius, outer_radius, stops) :
        c_inner = inner.to_pixman_fixed()
        c_outer = outer.to_pixman_fixed()
        c_inner_radius = PIXMAN.double_to_fixed(inner_radius)
        c_outer_radius = PIXMAN.double_to_fixed(outer_radius)
        c_stops, nr_stops = GradientStop.to_pixman_array(stops)
        return \
            Image(pixman.pixman_image_create_radial_gradient(ct.byref(c_inner), ct.byref(c_outer), c_inner_radius, c_outer_radius, ct.byref(c_stops), nr_stops))
    #end create_radial_gradient

    @staticmethod
    def create_conical_gradient(centre, angle, stops) :
        # for consistency, I expect angle in radians, even though underlying
        # Pixman call wants it in degrees
        c_centre = centre.to_pixman_fixed()
        c_stops, nr_stops = GradientStop.to_pixman_array(stops)
        return \
            Image(pixman.pixman_image_create_conical_gradient(ct.byref(c_centre), PIXMAN.double_to_fixed(angle / qahirah.deg), ct.byref(stops), nr_stops))
    #end create_conical_gradient

    @staticmethod
    def create_bits(format, width, height, bits, rowstride_bytes, clear = True) :
        return \
            Image \
              (
                (pixman.pixman_image_create_bits_no_clear, pixman.pixman_image_create_bits)[clear]
                    (format, width, height, bits, rowstride_bytes)
              )
    #end create_bits

    # more TBD

#end Image

# more TBD
