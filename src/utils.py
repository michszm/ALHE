from math import sqrt


def vector(a, b):
    i, j, k = a
    p, q, r = b
    return p - i, q - j, r - k


def vector_length(v):
    x, y, z = v
    return sqrt((x ** 2) + (y ** 2) + (z ** 2))


def unit_vector(v):
    x, y, z = v
    length = vector_length(v)
    return x / length, y / length, z / length


def dot_product(v, u):
    i, j, k = v
    p, q, r = u
    return i * p + j * q + k * r


def translate_vector(v, t):
    x, y, z = v
    m, n, o = t
    return x + m, y + n, z + o


def scale_vector(v, s):
    x, y, z = v
    return x * s, y * s, z * s


def two_points_distance(a, b):
    return vector_length(vector(a, b))


def clamp(x):
    if x < 0.0:
        x = 0.0
    elif x > 1.0:
        x = 1.0
    return x


def nrst_pt_on_seg(x, a, b):
    segment_vec = vector(a, b)
    point_vec = vector(a, x)
    segment_vec_len = vector_length(segment_vec)
    segment_unit_vec = unit_vector(segment_vec)
    scaled_point_vec = scale_vector(point_vec, 1.0 / segment_vec_len)
    nearest_point_on_unit = dot_product(segment_unit_vec, scaled_point_vec)
    nearest_point_on_unit = clamp(nearest_point_on_unit)
    nearest_point = scale_vector(segment_vec, nearest_point_on_unit)
    distance_to_nearest_point = two_points_distance(nearest_point, point_vec)
    nearest_point = translate_vector(nearest_point, a)
    return nearest_point, distance_to_nearest_point
