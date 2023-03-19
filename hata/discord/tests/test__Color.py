import vampytest

from ..color import Color


def test__Color__new__0():
    """
    Tests whether ``Color.__new__`` works as intended.
    
    Case: No value given.
    """
    color = Color()
    vampytest.assert_instance(color, Color)
    vampytest.assert_eq(color, 0)


def test__Color__new__1():
    """
    Tests whether ``Color.__new__`` works as intended.
    
    Case: Value given.
    """
    value = 795464
    
    color = Color(value)
    vampytest.assert_instance(color, Color)
    vampytest.assert_eq(color, value)


def test__Color__repr():
    """
    Tests whether ``Color.__repr__`` works as intended.
    
    Case: Value given.
    """
    value = 795464
    
    color = Color(value)
    vampytest.assert_instance(repr(color), str)


def test__Color__str():
    """
    Tests whether ``Color.__str__`` works as intended.
    
    Case: Value given.
    """
    value = 0xffffff
    
    color = Color(value)
    vampytest.assert_instance(str(color), str)


def test__Color__from_html__0():
    """
    Tests whether ``Color.from_html`` works as intended.
    
    Case: Passing.
    """
    for input_value, expected_output in (
        ('#0c2348', 795464),
        ('0c2348', 795464),
        ('#acd', 11193565),
        ('acd', 11193565),
    ):
        output = Color.from_html(input_value)
        vampytest.assert_instance(output, Color)
        vampytest.assert_eq(output, expected_output)


def test__Color__from_html__1():
    """
    Tests whether ``Color.from_html`` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        '#c231482', 
        '#22222',
        'c341812',
        '#aaa4',
        '#aa',
        'a4aa',
        'zzz',
        '#zzz'
        'zzzzzzz',
        '#zzzzzzz',
    ):
        with vampytest.assert_raises(ValueError):
            Color.from_html(input_value)


def test__Color__as_html__0():
    """
    Tests whether ``Color.as_html`` works as intended.
    
    Case: Passing.
    """
    for input_value, expected_output in (
        (795464, '#0C2348'),
        (11193565, '#AACCDD'),
    ):
        output = Color(input_value).as_html
        vampytest.assert_instance(output, str)
        vampytest.assert_eq(output, expected_output)


def test__Color__from_rgb_tuple__0():
    """
    Tests whether ``Color.from_rgb_tuple`` works as intended.
    
    Case: Passing.
    """
    for input_value, expected_output in (
        ((+ 12, + 35, + 72), 795464),
        ((- 10, + 35, + 72), 9032),
        ((+ 12, - 10, + 72), 786504),
        ((+ 12, + 35, - 72), 795392),
        ((+300, + 35, + 72), 16720712),
        ((+ 12, +300, + 72), 851784),
        ((+ 12, + 35, +300), 795647),
    ):
        output = Color.from_rgb_tuple(input_value)
        vampytest.assert_instance(output, Color)
        vampytest.assert_eq(output, expected_output)


def test__Color__from_rgb_tuple__1():
    """
    Tests whether ``Color.from_rgb_tuple`` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        (1, 2),
        (1, 2, 3, 4),
    ):
        with vampytest.assert_raises(ValueError):
            Color.from_rgb_tuple(input_value)


def test__Color__as_rgb_tuple__0():
    """
    Tests whether ``Color.as_rgb_tuple`` works as intended.
    
    Case: Passing.
    """
    for input_value, expected_output in (
        (795464, (12, 35, 72)),
    ):
        output = Color(input_value).as_rgb_tuple
        vampytest.assert_instance(output, tuple)
        vampytest.assert_eq(output, expected_output)


def test__Color__from_rgb_float_tuple__0():
    """
    Tests whether ``Color.from_rgb_float_tuple`` works as intended.
    
    Case: Passing.
    """
    for input_value, expected_output in (
        ((+0.1, +0.3, +0.7), 1658034),
        ((-0.1, +0.3, +0.7), 19634),
        ((+0.1, -0.1, +0.7), 1638578),
        ((+0.1, +0.3, -0.1), 1657856),
        ((+1.1, +0.3, +0.7), 16731314),
        ((+0.1, +1.1, +0.7), 1703858),
        ((+0.1, +0.3, +1.1), 1658111),
    ):
        output = Color.from_rgb_float_tuple(input_value)
        vampytest.assert_instance(output, Color)
        vampytest.assert_eq(output, expected_output)


def test__Color__from_rgb_float_tuple__1():
    """
    Tests whether ``Color.from_rgb_float_tuple`` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        (1.0, 2.0),
        (1.0, 2.0, 3.0, 4.0),
    ):
        with vampytest.assert_raises(ValueError):
            Color.from_rgb_float_tuple(input_value)


def test__Color__as_rgb_float_tuple__0():
    """
    Tests whether ``Color.as_rgb_float_tuple`` works as intended.
    
    Case: Passing.
    """
    for input_value, expected_output in (
        (1658034, (0.1, 0.3, 0.7)),
    ):
        output = Color(input_value).as_rgb_float_tuple
        vampytest.assert_instance(output, tuple)
        vampytest.assert_eq((*(round(c, 2) for c in output),), expected_output)


def test__Color__from_rgb():
    """
    Tests whether ``Color.from_rgb`` works as intended.
    
    Case: Passing.
    """
    for input_values, expected_output in (
        ((+ 12, + 35, + 72), 795464),
        ((- 10, + 35, + 72), 9032),
        ((+ 12, - 10, + 72), 786504),
        ((+ 12, + 35, - 72), 795392),
        ((+300, + 35, + 72), 16720712),
        ((+ 12, +300, + 72), 851784),
        ((+ 12, + 35, +300), 795647),
    ):
        output = Color.from_rgb(*input_values)
        vampytest.assert_instance(output, Color)
        vampytest.assert_eq(output, expected_output)


def test__Color__from_rgb_float__0():
    """
    Tests whether ``Color.from_rgb_float`` works as intended.
    
    Case: Passing.
    """
    for input_values, expected_output in (
        ((+0.1, +0.3, +0.7), 1658034),
        ((-0.1, +0.3, +0.7), 19634),
        ((+0.1, -0.1, +0.7), 1638578),
        ((+0.1, +0.3, -0.1), 1657856),
        ((+1.1, +0.3, +0.7), 16731314),
        ((+0.1, +1.1, +0.7), 1703858),
        ((+0.1, +0.3, +1.1), 1658111),
    ):
        output = Color.from_rgb_float(*input_values)
        vampytest.assert_instance(output, Color)
        vampytest.assert_eq(output, expected_output)


def test__Color__from_hsl_tuple__0():
    """
    Tests whether ``Color.from_hsl_tuple`` works as intended.
    
    Case: Passing.
    """
    for input_value, expected_output in (
        ((+200, + 44, + 77), 11259358),
        ((+700, + 44, + 77), 14592956),
        ((+200, +120, + 77), 9099519),
        ((+200, + 44, +120), 16777215),
        ((- 80, + 44, + 77), 13478878),
        ((+200, - 20, + 77), 12895428),
        ((+200, + 44, - 20), 0),
    ):
        output = Color.from_hsl_tuple(input_value)
        vampytest.assert_instance(output, Color)
        vampytest.assert_eq(output, expected_output)

def test__Color__from_hsl__0():
    """
    Tests whether ``Color.from_hsl`` works as intended.
    
    Case: Passing.
    """
    for input_values, expected_output in (
        ((+200, + 44, + 77), 11259358),
        ((+700, + 44, + 77), 14592956),
        ((+200, +120, + 77), 9099519),
        ((+200, + 44, +120), 16777215),
        ((- 80, + 44, + 77), 13478878),
        ((+200, - 20, + 77), 12895428),
        ((+200, + 44, - 20), 0),
    ):
        output = Color.from_hsl(*input_values)
        vampytest.assert_instance(output, Color)
        vampytest.assert_eq(output, expected_output)


def test__Color__as_hsl_tuple__0():
    """
    Tests whether ``Color.as_hsl_tuple`` works as intended.
    
    Case: Passing.
    """
    for input_value, expected_output in (
        (11259358, (200, 44, 77)),
    ):
        output = Color(input_value).as_hsl_tuple
        vampytest.assert_instance(output, tuple)
        vampytest.assert_eq((*(round(c, 2) for c in output),), expected_output)


def test__Color__from_hsl_float_tuple__0():
    """
    Tests whether ``Color.from_hsl_float_tuple`` works as intended.
    
    Case: Passing.
    """
    for input_value, expected_output in (
        ((+200, + 44, + 77), 11259358),
        ((+700, + 44, + 77), 14592956),
        ((+200, +120, + 77), 9099519),
        ((+200, + 44, +120), 16777215),
        ((- 80, + 44, + 77), 13478878),
        ((+200, - 20, + 77), 12895428),
        ((+200, + 44, - 20), 0),
    ):
        input_value = (input_value[0] / 360, input_value[1] / 100, input_value[2] / 100)
        
        output = Color.from_hsl_float_tuple(input_value)
        vampytest.assert_instance(output, Color)
        vampytest.assert_eq(output, expected_output)


def test__Color__from_hsl_float_0():
    """
    Tests whether ``Color.from_hsl_float`` works as intended.
    
    Case: Passing.
    """
    for input_values, expected_output in (
        ((+200, + 44, + 77), 11259358),
        ((+700, + 44, + 77), 14592956),
        ((+200, +120, + 77), 9099519),
        ((+200, + 44, +120), 16777215),
        ((- 80, + 44, + 77), 13478878),
        ((+200, - 20, + 77), 12895428),
        ((+200, + 44, - 20), 0),
    ):
        input_values = (input_values[0] / 360, input_values[1] / 100, input_values[2] / 100)
        
        output = Color.from_hsl_float(*input_values)
        vampytest.assert_instance(output, Color)
        vampytest.assert_eq(output, expected_output)


def test__Color__as_hsl_float_tuple__0():
    """
    Tests whether ``Color.as_hsl_float_tuple`` works as intended.
    
    Case: Passing.
    """
    for input_value, expected_output in (
        (11259358, (round(200 / 360, 1), round(44 / 100, 1), round(77 / 100, 1))),
    ):
        output = Color(input_value).as_hsl_float_tuple
        vampytest.assert_instance(output, tuple)
        vampytest.assert_eq((*(round(c, 1) for c in output),), expected_output)



def test__Color__red():
    """
    Tests whether ``Color.red`` works as intended.
    """
    for input_value, expected_output in (
        (795464, 12),
    ):
        output = Color(input_value).red
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, expected_output)


def test__Color__green():
    """
    Tests whether ``Color.green`` works as intended.
    """
    for input_value, expected_output in (
        (795464, 35),
    ):
        output = Color(input_value).green
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, expected_output)


def test__Color__blue():
    """
    Tests whether ``Color.blue`` works as intended.
    """
    for input_value, expected_output in (
        (795464, 72),
    ):
        output = Color(input_value).blue
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, expected_output)


def test__Color__random():
    """
    Tests whether ``Color.random`` works as intended.
    """
    output = Color.random()
    vampytest.assert_instance(output, Color)
    vampytest.assert_eq((output & 0xffffff) ^ output, 0)


def test__Color__set_seed():
    """
    Tests whether ``Color.set_seed`` works as intended.
    """
    seed = 123
    
    Color.set_seed(seed)
    output_0 = Color.random()
    
    Color.set_seed(seed)
    output_1 = Color.random()
    
    vampytest.assert_eq(output_0, output_1)
