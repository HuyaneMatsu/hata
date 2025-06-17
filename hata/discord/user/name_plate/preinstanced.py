__all__ = ('Palette',)

from ...bases import Preinstance as P, PreinstancedBase
from ...color import Color


class Palette(PreinstancedBase, value_type = str):
    """
    Represents the dominant color of an asset.
        
    Attributes
    ----------
    color : ``Color``
        The dominant color of the palette.
    
    name : `str`
        The name of the name plate.
    
    value : `str`
        The Discord side identifier of the palette.
    
    Type Attributes
    ---------------
    Every predefined palette can also be accessed as type attribute:
    
    +---------------------------+---------------------------+-----------------------+-----------+
    | Type attribute name       | name                      | value                 | color     |
    +===========================+===========================+=======================+===========+
    | alice_blue                | alice blue                | aliceblue             | 0xf0f8ff  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | antique_white             | antique white             | antiquewhite          | 0xfaebd7  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | aqua                      | aqua                      | aqua                  | 0x00ffff  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | aquamarine                | aquamarine                | aquamarine            | 0x7fffd4  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | azure                     | azure                     | azure                 | 0xf0ffff  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | beige                     | beige                     | beige                 | 0xf5f5dc  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | bisque                    | bisque                    | bisque                | 0xffe4c4  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | black                     | black                     | black                 | 0x000000  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | blanched_almond           | blanched almond           | blanchedalmond        | 0xffebcd  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | blue                      | blue                      | blue                  | 0x0000ff  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | blue_violet               | blue violet               | blueviolet            | 0x8a2be2  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | brown                     | brown                     | brown                 | 0xa52a2a  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | burlywood                 | burlywood                 | burlywood             | 0xdeb887  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | cadet_blue                | cadet blue                | cadet blue            | 0x5f9ea0  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | chartreuse                | chartreuse                | chartreuse            | 0x7fff00  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | chocolate                 | chocolate                 | chocolate             | 0xd2691e  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | coral                     | coral                     | coral                 | 0xff7f50  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | cornflower                | cornflower                | cornflower            | 0x6495ed  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | cornflower_blue           | cornflower blue           | cornflowerblue        | 0x6495ed  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | cornsilk                  | cornsilk                  | cornsilk              | 0xfff8dc  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | crimson                   | crimson                   | crimson               | 0xdc143c  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | cyan                      | cyan                      | cyan                  | 0x00ffff  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | dark_blue                 | dark blue                 | darkblue              | 0x00008b  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | dark_cyan                 | dark cyan                 | darkcyan              | 0x008b8b  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | dark_goldenrod            | dark goldenrod            | darkgoldenrod         | 0xb8860b  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | dark_gray                 | dark gray                 | darkgray              | 0xa9a9a9  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | dark_green                | dark green                | darkgreen             | 0x006400  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | dark_grey                 | dark grey                 | darkgrey              | 0xa9a9a9  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | dark_khaki                | dark khaki                | darkkhaki             | 0xbdb76b  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | dark_magenta              | dark magenta              | darkmagenta           | 0x8b008b  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | dark_olive_green          | dark olive green          | darkolivegreen        | 0x556b2f  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | dark_orange               | dark orange               | darkorange            | 0xff8c00  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | dark_orchid               | dark orchid               | darkorchid            | 0x9932cc  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | dark_red                  | dark red                  | darkred               | 0x8b0000  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | dark_salmon               | dark salmon               | darksalmon            | 0xe9967a  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | dark_sea_green            | dark sea green            | darkseagreen          | 0x8fbc8f  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | dark_slate_blue           | dark slate blue           | darkslateblue         | 0x483d8b  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | dark_slate_gray           | dark slate gray           | darkslategray         | 0x2f4f4f  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | dark_slate_grey           | dark slate grey           | darkslategrey         | 0x2f4f4f  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | dark_turquoise            | dark turquoise            | darkturquoise         | 0x00ced1  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | dark_violet               | dark violet               | darkviolet            | 0x9400d3  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | deep_pink                 | deep pink                 | deeppink              | 0xff1493  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | deep_sky_blue             | deep sky blue             | deepskyblue           | 0x00bfff  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | dim_gray                  | dim gray                  | dimgray               | 0x696969  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | dim_grey                  | dim grey                  | dimgrey               | 0x696969  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | dodger_blue               | dodger blue               | dodgerblue            | 0x1e90ff  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | firebrick                 | firebrick                 | firebrick             | 0xb22222  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | floral_white              | floral white              | floralwhite           | 0xfffaf0  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | forest_green              | forest green              | forestgreen           | 0x228b22  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | fuchsia                   | fuchsia                   | fuchsia               | 0xff00ff  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | gainsboro                 | gainsboro                 | gainsboro             | 0xdcdcdc  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | ghost_white               | ghost white               | ghostwhite            | 0xf8f8ff  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | gold                      | gold                      | gold                  | 0xffd700  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | goldenrod                 | goldenrod                 | goldenrod             | 0xdaa520  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | gray                      | gray                      | gray                  | 0x808080  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | green                     | green                     | green                 | 0x008000  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | green_yellow              | green yellow              | greenyellow           | 0xadff2f  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | grey                      | grey                      | grey                  | 0x808080  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | honeydew                  | honeydew                  | honeydew              | 0xf0fff0  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | hot_pink                  | hot pink                  | hotpink               | 0xff69b4  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | indian_red                | indian red                | indianred             | 0xcd5c5c  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | indigo                    | indigo                    | indigo                | 0x4b0082  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | ivory                     | ivory                     | ivory                 | 0xfffff0  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | khaki                     | khaki                     | khaki                 | 0xf0e68c  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | laser_lemon               | laser lemon               | laserlemon            | 0xffff54  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | lavender                  | lavender                  | lavender              | 0xe6e6fa  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | lavender_blush            | lavender blush            | lavenderblush         | 0xfff0f5  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | lawn_green                | lawn green                | lawngreen             | 0x7cfc00  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | lemon_chiffon             | lemon chiffon             | lemonchiffon          | 0xfffacd  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | light_blue                | light blue                | lightblue             | 0xadd8e6  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | light_coral               | light coral               | lightcoral            | 0xf08080  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | light_cyan                | light cyan                | lightcyan             | 0xe0ffff  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | light_goldenrod           | light goldenrod           | lightgoldenrod        | 0xfafad2  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | light_goldenrod_yellow    | light goldenrod yellow    | lightgoldenrodyellow  | 0xfafad2  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | light_gray                | light gray                | lightgray             | 0xd3d3d3  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | light_green               | light green               | lightgreen            | 0x90ee90  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | light_grey                | light grey                | lightgrey             | 0xd3d3d3  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | light_pink                | light pink                | lightpink             | 0xffb6c1  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | light_salmon              | light salmon              | lightsalmon           | 0xffa07a  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | light_sea_green           | light sea green           | lightseagreen         | 0x20b2aa  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | light_sky_blue            | light sky blue            | lightskyblue          | 0x87cefa  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | light_slate_gray          | light slate gray          | lightslategray        | 0x778899  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | light_slate_grey          | light slate grey          | lightslategrey        | 0x778899  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | light_steel_blue          | light steel blue          | lightsteelblue        | 0xb0c4de  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | light_yellow              | light yellow              | lightyellow           | 0xffffe0  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | lime                      | lime                      | lime                  | 0x00ff00  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | lime_green                | lime green                | limegreen             | 0x32cd32  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | linen                     | linen                     | linen                 | 0xfaf0e6  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | magenta                   | magenta                   | magenta               | 0xff00ff  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | maroon                    | maroon                    | maroon                | 0x800000  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | maroon_2                  | maroon 2                  | maroon2               | 0x7f0000  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | maroon_3                  | maroon 3                  | maroon3               | 0xb03060  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | medium_aquamarine         | medium aquamarine         | mediumaquamarine      | 0x66cdaa  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | medium_blue               | medium blue               | mediumblue            | 0x0000cd  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | medium_orchid             | medium orchid             | mediumorchid          | 0xba55d3  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | medium_purple             | medium purple             | mediumpurple          | 0x9370db  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | medium_sea_green          | medium sea green          | mediumseagreen        | 0x3cb371  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | medium_slate_blue         | medium slate blue         | mediumslateblue       | 0x7b68ee  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | medium_spring_green       | medium spring green       | mediumspringgreen     | 0x00fa9a  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | medium_turquoise          | medium turquoise          | mediumturquoise       | 0x48d1cc  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | medium_violet_red         | medium violet red         | mediumvioletred       | 0xc71585  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | midnight_blue             | midnight blue             | midnightblue          | 0x191970  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | mint_cream                | mint cream                | mintcream             | 0xf5fffa  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | misty_rose                | misty rose                | mistyrose             | 0xffe4e1  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | moccasin                  | moccasin                  | moccasin              | 0xffe4b5  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | navajo_white              | navajo white              | navajowhite           | 0xffdead  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | navy                      | navy                      | navy                  | 0x000080  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | old_lace                  | old lace                  | oldlace               | 0xfdf5e6  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | olive                     | olive                     | olive                 | 0x808000  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | olive_drab                | olive drab                | olivedrab             | 0x6b8e23  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | orange                    | orange                    | orange                | 0xffa500  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | orange_red                | orange red                | orangered             | 0xff4500  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | orchid                    | orchid                    | orchid                | 0xda70d6  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | pale_goldenrod            | pale goldenrod            | palegoldenrod         | 0xeee8aa  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | pale_green                | pale green                | palegreen             | 0x98fb98  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | pale_turquoise            | pale turquoise            | paleturquoise         | 0xafeeee  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | pale_violet_red           | pale violet red           | palevioletred         | 0xdb7093  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | papaya_whip               | papaya whip               | papayawhip            | 0xffefd5  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | peach_puff                | peach puff                | peachpuff             | 0xffdab9  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | peru                      | peru                      | peru                  | 0xcd853f  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | pink                      | pink                      | pink                  | 0xffc0cb  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | plum                      | plum                      | plum                  | 0xdda0dd  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | powder_blue               | powder blue               | powderblue            | 0xb0e0e6  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | purple                    | purple                    | purple                | 0x800080  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | purple_2                  | purple 2                  | purple2               | 0x7f007f  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | purple_3                  | purple 3                  | purple3               | 0xa020f0  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | rebecca_purple            | rebecca purple            | rebeccapurple         | 0x663399  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | red                       | red                       | red                   | 0xff0000  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | rosy_brown                | rosy brown                | rosybrown             | 0xbc8f8f  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | royal_blue                | royal blue                | royalblue             | 0x4169e1  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | saddle_brown              | saddle brown              | saddlebrown           | 0x8b4513  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | salmon                    | salmon                    | salmon                | 0xfa8072  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | sandy_brown               | sandy brown               | sandybrown            | 0xf4a460  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | sea_green                 | sea green                 | seagreen              | 0x2e8b57  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | seashell                  | seashell                  | seashell              | 0xfff5ee  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | sienna                    | sienna                    | sienna                | 0xa0522d  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | silver                    | silver                    | silver                | 0xc0c0c0  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | sky_blue                  | sky blue                  | skyblue               | 0x87ceeb  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | slate_blue                | slate blue                | slateblue             | 0x6a5acd  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | slate_gray                | slate gray                | slategray             | 0x708090  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | slate_grey                | slate grey                | slategrey             | 0x708090  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | snow                      | snow                      | snow                  | 0xfffafa  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | spring_green              | spring green              | springgreen           | 0x00ff7f  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | steel_blue                | steel blue                | steelblue             | 0x4682b4  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | tan                       | tan                       | tan                   | 0xd2b48c  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | teal                      | teal                      | teal                  | 0x008080  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | thistle                   | thistle                   | thistle               | 0xd8bfd8  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | tomato                    | tomato                    | tomato                | 0xff6347  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | turquoise                 | turquoise                 | turquoise             | 0x40e0d0  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | violet                    | violet                    | violet                | 0xee82ee  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | wheat                     | wheat                     | wheat                 | 0xf5deb3  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | white                     | white                     | white                 | 0xffffff  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | white_smoke               | white smoke               | whitesmoke            | 0xf5f5f5  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | yellow                    | yellow                    | yellow                | 0xffff00  |
    +---------------------------+---------------------------+-----------------------+-----------+
    | yellow_green              | yellow green              | yellowgreen           | 0x9acd32  |
    +---------------------------+---------------------------+-----------------------+-----------+
    """
    __slots__ = ('color',)
    
    def __new__(cls, value, name = None, color = Color(0)):
        """
        Creates a palette instance.
        
        Parameters
        ----------
        value : `str`
            The unique identifier of the palette.
        
        name : `None | str` = `None`, Optional
            The palette's name.
        
        color : ``Color``
            The dominant color of the palette.
        """
        self = PreinstancedBase.__new__(cls, value, name)
        self.color = color
        return self        
    
    
    # predefined
    alice_blue = P('aliceblue', 'alice blue', Color(0xf0f8ff))
    antique_white = P('antiquewhite', 'antique white', Color(0xfaebd7))
    aqua = P('aqua', 'aqua', Color(0x00ffff))
    aquamarine = P('aquamarine', 'aquamarine', Color(0x7fffd4))
    azure = P('azure', 'azure', Color(0xf0ffff))
    beige = P('beige', 'beige', Color(0xf5f5dc))
    bisque = P('bisque', 'bisque', Color(0xffe4c4))
    black = P('black', 'black', Color(0x000000))
    blanched_almond = P('blanchedalmond', 'blanched almond', Color(0xffebcd))
    blue = P('blue', 'blue', Color(0x0000ff))
    blue_violet = P('blueviolet', 'blue violet', Color(0x8a2be2))
    brown = P('brown', 'brown', Color(0xa52a2a))
    burlywood = P('burlywood', 'burlywood', Color(0xdeb887))
    cadet_blue = P('cadetblue', 'cadet blue', Color(0x5f9ea0))
    chartreuse = P('chartreuse', 'chartreuse', Color(0x7fff00))
    chocolate = P('chocolate', 'chocolate', Color(0xd2691e))
    coral = P('coral', 'coral', Color(0xff7f50))
    cornflower = P('cornflower', 'cornflower', Color(0x6495ed))
    cornflower_blue = P('cornflower blue', 'cornflower blue', Color(0x6495ed))
    cornsilk = P('cornsilk', 'cornsilk', Color(0xfff8dc))
    crimson = P('crimson', 'crimson', Color(0xdc143c))
    cyan = P('cyan', 'cyan', Color(0x00ffff))
    dark_blue = P('darkblue', 'dark blue', Color(0x00008b))
    dark_cyan = P('darkcyan', 'dark cyan', Color(0x008b8b))
    dark_goldenrod = P('darkgoldenrod', 'dark goldenrod', Color(0xb8860b))
    dark_gray = P('darkgray', 'dark gray', Color(0xa9a9a9))
    dark_green = P('darkgreen', 'dark green', Color(0x006400))
    dark_grey = P('darkgrey', 'dark grey', Color(0xa9a9a9))
    dark_khaki = P('darkkhaki', 'dark khaki', Color(0xbdb76b))
    dark_magenta = P('darkmagenta', 'dark magenta', Color(0x8b008b))
    dark_olivegreen = P('darkolivegreen', 'dark olive green', Color(0x556b2f))
    dark_orange = P('darkorange', 'dark orange', Color(0xff8c00))
    dark_orchid = P('darkorchid', 'dark orchid', Color(0x9932cc))
    dark_red = P('darkred', 'dark red', Color(0x8b0000))
    dark_salmon = P('darksalmon', 'dark salmon', Color(0xe9967a))
    dark_seagreen = P('darkseagreen', 'dark sea green', Color(0x8fbc8f))
    dark_slateblue = P('darkslateblue', 'dark slate blue', Color(0x483d8b))
    dark_slate_gray = P('darkslategray', 'dark slate gray', Color(0x2f4f4f))
    dark_slate_grey = P('darkslategrey', 'dark slate grey', Color(0x2f4f4f))
    dark_turquoise = P('darkturquoise', 'dark turquoise', Color(0x00ced1))
    dark_violet = P('darkviolet', 'dark violet', Color(0x9400d3))
    deep_pink = P('deeppink', 'deep pink', Color(0xff1493))
    deep_skyblue = P('deepskyblue', 'deep sky blue', Color(0x00bfff))
    dim_gray = P('dimgray', 'dim gray', Color(0x696969))
    dim_grey = P('dimgrey', 'dim grey', Color(0x696969))
    dodger_blue = P('dodgerblue', 'dodger blue', Color(0x1e90ff))
    firebrick = P('firebrick', 'firebrick', Color(0xb22222))
    floral_white = P('floralwhite', 'floral white', Color(0xfffaf0))
    forest_green = P('forestgreen', 'forest green', Color(0x228b22))
    fuchsia = P('fuchsia', 'fuchsia', Color(0xff00ff))
    gainsboro = P('gainsboro', 'gainsboro', Color(0xdcdcdc))
    ghost_white = P('ghostwhite', 'ghost white', Color(0xf8f8ff))
    gold = P('gold', 'gold', Color(0xffd700))
    goldenrod = P('goldenrod', 'goldenrod', Color(0xdaa520))
    gray = P('gray', 'gray', Color(0x808080))
    green = P('green', 'green', Color(0x008000))
    green_yellow = P('greenyellow', 'green yellow', Color(0xadff2f))
    grey = P('grey', 'grey', Color(0x808080))
    honeydew = P('honeydew', 'honeydew', Color(0xf0fff0))
    hot_pink = P('hotpink', 'hot pink', Color(0xff69b4))
    indian_red = P('indianred', 'indian red', Color(0xcd5c5c))
    indigo = P('indigo', 'indigo', Color(0x4b0082))
    ivory = P('ivory', 'ivory', Color(0xfffff0))
    khaki = P('khaki', 'khaki', Color(0xf0e68c))
    laser_lemon = P('laserlemon', 'laser lemon', Color(0xffff54))
    lavender = P('lavender', 'lavender', Color(0xe6e6fa))
    lavender_blush = P('lavenderblush', 'lavender blush', Color(0xfff0f5))
    lawn_green = P('lawngreen', 'lawn green', Color(0x7cfc00))
    lemon_chiffon = P('lemonchiffon', 'lemon chiffon', Color(0xfffacd))
    light_blue = P('lightblue', 'light blue', Color(0xadd8e6))
    light_coral = P('lightcoral', 'light coral', Color(0xf08080))
    light_cyan = P('lightcyan', 'light cyan', Color(0xe0ffff))
    light_goldenrod = P('lightgoldenrod', 'light goldenrod', Color(0xfafad2))
    light_goldenrod_yellow = P('lightgoldenrodyellow', 'light goldenrod yellow', Color(0xfafad2))
    light_gray = P('lightgray', 'light gray', Color(0xd3d3d3))
    light_green = P('lightgreen', 'light green', Color(0x90ee90))
    light_grey = P('lightgrey', 'light grey', Color(0xd3d3d3))
    light_pink = P('lightpink', 'light pink', Color(0xffb6c1))
    light_salmon = P('lightsalmon', 'light salmon', Color(0xffa07a))
    light_sea_green = P('lightseagreen', 'light sea green', Color(0x20b2aa))
    light_sky_blue = P('lightskyblue', 'light sky blue', Color(0x87cefa))
    light_slate_gray = P('lightslategray', 'light slate gray', Color(0x778899))
    light_slate_grey = P('lightslategrey', 'light slate grey', Color(0x778899))
    light_steel_blue = P('lightsteelblue', 'light steel blue', Color(0xb0c4de))
    light_yellow = P('lightyellow', 'light yellow', Color(0xffffe0))
    lime = P('lime', 'lime', Color(0x00ff00))
    lime_green = P('limegreen', 'lime green', Color(0x32cd32))
    linen = P('linen', 'linen', Color(0xfaf0e6))
    magenta = P('magenta', 'magenta', Color(0xff00ff))
    maroon = P('maroon', 'maroon', Color(0x800000))
    maroon_2 = P('maroon2', 'maroon 2', Color(0x7f0000))
    maroon_3 = P('maroon3', 'maroon 3', Color(0xb03060))
    medium_aquamarine = P('mediumaquamarine', 'medium aquamarine', Color(0x66cdaa))
    medium_blue = P('mediumblue', 'medium blue', Color(0x0000cd))
    medium_orchid = P('mediumorchid', 'medium orchid', Color(0xba55d3))
    medium_purple = P('mediumpurple', 'medium purple', Color(0x9370db))
    medium_sea_green = P('mediumseagreen', 'medium sea green', Color(0x3cb371))
    medium_slate_blue = P('mediumslateblue', 'medium slate blue', Color(0x7b68ee))
    medium_spring_green = P('mediumspringgreen', 'medium spring green', Color(0x00fa9a))
    medium_turquoise = P('mediumturquoise', 'medium turquoise', Color(0x48d1cc))
    medium_violet_red = P('mediumvioletred', 'medium violet red', Color(0xc71585))
    midnight_blue = P('midnightblue', 'midnight blue', Color(0x191970))
    mint_cream = P('mintcream', 'mint cream', Color(0xf5fffa))
    misty_rose = P('mistyrose', 'misty rose', Color(0xffe4e1))
    moccasin = P('moccasin', 'moccasin', Color(0xffe4b5))
    navajo_white = P('navajowhite', 'navajo white', Color(0xffdead))
    navy = P('navy', 'navy', Color(0x000080))
    old_lace = P('oldlace', 'old lace', Color(0xfdf5e6))
    olive = P('olive', 'olive', Color(0x808000))
    olive_drab = P('olivedrab', 'olive drab', Color(0x6b8e23))
    orange = P('orange', 'orange', Color(0xffa500))
    orange_red = P('orangered', 'orange red', Color(0xff4500))
    orchid = P('orchid', 'orchid', Color(0xda70d6))
    pale_goldenrod = P('palegoldenrod', 'pale goldenrod', Color(0xeee8aa))
    pale_green = P('palegreen', 'pale green', Color(0x98fb98))
    pale_turquoise = P('paleturquoise', 'pale turquoise', Color(0xafeeee))
    pale_violet_red = P('palevioletred', 'pale violet red', Color(0xdb7093))
    papaya_whip = P('papayawhip', 'papaya whip', Color(0xffefd5))
    peach_puff = P('peachpuff', 'peach puff', Color(0xffdab9))
    peru = P('peru', 'peru', Color(0xcd853f))
    pink = P('pink', 'pink', Color(0xffc0cb))
    plum = P('plum', 'plum', Color(0xdda0dd))
    powder_blue = P('powderblue', 'powder blue', Color(0xb0e0e6))
    purple = P('purple', 'purple', Color(0x800080))
    purple_2 = P('purple2', 'purple 2', Color(0x7f007f))
    purple_3 = P('purple3', 'purple 3', Color(0xa020f0))
    rebecca_purple = P('rebeccapurple', 'rebecca purple', Color(0x663399))
    red = P('red', 'red', Color(0xff0000))
    rosy_brown = P('rosybrown', 'rosy brown', Color(0xbc8f8f))
    royal_blue = P('royalblue', 'royal blue', Color(0x4169e1))
    saddle_brown = P('saddlebrown', 'saddle brown', Color(0x8b4513))
    salmon = P('salmon', 'salmon', Color(0xfa8072))
    sandy_brown = P('sandybrown', 'sandy brown', Color(0xf4a460))
    sea_green = P('seagreen', 'sea green', Color(0x2e8b57))
    seashell = P('seashell', 'seashell', Color(0xfff5ee))
    sienna = P('sienna', 'sienna', Color(0xa0522d))
    silver = P('silver', 'silver', Color(0xc0c0c0))
    sky_blue = P('skyblue', 'sky blue', Color(0x87ceeb))
    slate_blue = P('slateblue', 'slate blue', Color(0x6a5acd))
    slate_gray = P('slategray', 'slate gray', Color(0x708090))
    slate_grey = P('slategrey', 'slate grey', Color(0x708090))
    snow = P('snow', 'snow', Color(0xfffafa))
    spring_green = P('springgreen', 'spring green', Color(0x00ff7f))
    steel_blue = P('steelblue', 'steel blue', Color(0x4682b4))
    tan = P('tan', 'tan', Color(0xd2b48c))
    teal = P('teal', 'teal', Color(0x008080))
    thistle = P('thistle', 'thistle', Color(0xd8bfd8))
    tomato = P('tomato', 'tomato', Color(0xff6347))
    turquoise = P('turquoise', 'turquoise', Color(0x40e0d0))
    violet = P('violet', 'violet', Color(0xee82ee))
    wheat = P('wheat', 'wheat', Color(0xf5deb3))
    white = P('white', 'white', Color(0xffffff))
    white_smoke = P('whitesmoke', 'white smoke', Color(0xf5f5f5))
    yellow = P('yellow', 'yellow', Color(0xffff00))
    yellow_green = P('yellowgreen', 'yellow green', Color(0x9acd32))


Palette.INSTANCES[''] = Palette.black
