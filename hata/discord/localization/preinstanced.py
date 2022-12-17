__all__ = ('Locale',)

from ..bases import Preinstance as P, PreinstancedBase


class Locale(PreinstancedBase):
    """
    Represents Discord's locale.
    
    Attributes
    ----------
    value : `str`
        The Discord side identifier value of the locale.
    name : `str`
        The default name of the locale.
    native_name : `str`
        The native name of the language.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`str`, ``Locale``) items
        Stores the predefined locales. This container is accessed when translating a Discord side
        identifier of a locale. The identifier value is used as a key to get it's wrapper side
        representation.
    VALUE_TYPE : `type` = `str`
        The locales' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the locales.
    
    Every predefined locale is also stored as a class attribute:
    
    +-----------------------+-------------------------------+-----------+---------------------------------------+
    | Class attribute name  | Name                          | Value     | Native name                           |
    +=======================+===============================+===========+=======================================+
    | bulgarian             | Bulgarian                     | bg        | български                             |
    +-----------------------+-------------------------------+-----------+---------------------------------------+
    | chinese_cn            | Chinese (China)               | zh-CN     | \u4e2d\u6587                          |
    +-----------------------+-------------------------------+-----------+---------------------------------------+
    | chinese_tw            | Chinese (Taiwan)              | zh-TW     | \u7e41\u9ad4\u4e2d\u6587              |
    +-----------------------+-------------------------------+-----------+---------------------------------------+
    | croatian              | Croatian                      | hr        | Hrvatski                              |
    +-----------------------+-------------------------------+-----------+---------------------------------------+
    | czech                 | Czech                         | cs        | Čeština                               |
    +-----------------------+-------------------------------+-----------+---------------------------------------+
    | danish                | Danish                        | da        | Dansk                                 |
    +-----------------------+-------------------------------+-----------+---------------------------------------+
    | dutch                 | Dutch                         | nl        | Nederlands                            |
    +-----------------------+-------------------------------+-----------+---------------------------------------+
    | english_gb            | English (Great Britain)       | en-GB     | English, UK                           |
    +-----------------------+-------------------------------+-----------+---------------------------------------+
    | english_us            | English (United States)       | en-US     | English, US                           |
    +-----------------------+-------------------------------+-----------+---------------------------------------+
    | finnish               | Finnish                       | fi        | Suomi                                 |
    +-----------------------+-------------------------------+-----------+---------------------------------------+
    | french                | French                        | fr        | Français                              |
    +-----------------------+-------------------------------+-----------+---------------------------------------+
    | german                | German                        | de        | Deutsch                               |
    +-----------------------+-------------------------------+-----------+---------------------------------------+
    | greek                 | Greek                         | el        | Ελληνικά                              |
    +-----------------------+-------------------------------+-----------+---------------------------------------+
    | hindi                 | Hindi                         | hi        | \u0939\u093f\u0928\u094d\u0926\u0940  |
    +-----------------------+-------------------------------+-----------+---------------------------------------+
    | hungarian             | Hungarian                     | hu        | Magyar                                |
    +-----------------------+-------------------------------+-----------+---------------------------------------+
    | indonesian            | Indonesian                    | id        | Bahasa Indonesia                      |
    +-----------------------+-------------------------------+-----------+---------------------------------------+
    | italian               | Italian                       | it        | Italiano                              |
    +-----------------------+-------------------------------+-----------+---------------------------------------+
    | japanese              | Japanese                      | jp        | \u65e5\u672c\u8a9e                    |
    +-----------------------+-------------------------------+-----------+---------------------------------------+
    | korean                | Korean                        | ko        | \ud55c\uad6d\uc5b4                    |
    +-----------------------+-------------------------------+-----------+---------------------------------------+
    | lithuanian            | Lithuanian                    | lt        | Lietuviškai                           |
    +-----------------------+-------------------------------+-----------+---------------------------------------+
    | norwegian             | Norwegian                     | no        | Norsk                                 |
    +-----------------------+-------------------------------+-----------+---------------------------------------+
    | polish                | Polish                        | pl        | Polski                                |
    +-----------------------+-------------------------------+-----------+---------------------------------------+
    | portuguese            | Portuguese, Brazilian         | pt-BR     | Português do Brasil                   |
    +-----------------------+-------------------------------+-----------+---------------------------------------+
    | romanian              | Romanian, Romania             | ro        | Română                                |
    +-----------------------+-------------------------------+-----------+---------------------------------------+
    | russian               | Russian                       | ru        | Pусский                               |
    +-----------------------+-------------------------------+-----------+---------------------------------------+
    | spanish               | Spanish                       | es-ES     | Español                               |
    +-----------------------+-------------------------------+-----------+---------------------------------------+
    | swedish               | Swedish                       | sv-SE     | Svenska                               |
    +-----------------------+-------------------------------+-----------+---------------------------------------+
    | thai                  | Thai                          | th        | \u0e44\u0e17\u0e22                    |
    +-----------------------+-------------------------------+-----------+---------------------------------------+
    | turkish               | Turkish                       | tr        | Türkçe                                |
    +-----------------------+-------------------------------+-----------+---------------------------------------+
    | ukrainian             | Ukrainian                     | uk        | Українська                            |
    +-----------------------+-------------------------------+-----------+---------------------------------------+
    | vietnamese            | Vietnamese                    | vi        | Tiếng Việt                            |
    +-----------------------+-------------------------------+-----------+---------------------------------------+
    """
    INSTANCES = {}
    VALUE_TYPE = str
    
    __slots__ = ('native_name',)
    

    @classmethod
    def _from_value(cls, value):
        """
        Creates a new locale with the given value.
        
        Parameters
        ----------
        value : `int`
            The locale's identifier value.
        
        Returns
        -------
        self : ``Locale``
            The created instance.
        """
        self = object.__new__(cls)
        self.name = cls.DEFAULT_NAME
        self.value = value
        self.native_name = value
        
        return self
    
    
    def __init__(self, value, name, native_name):
        """
        Creates an ``Locale`` and stores it at the class's `.INSTANCES` class attribute as well.
        
        Parameters
        ----------
        value : `int`
            The Discord side identifier value of the locale.
        name : `str`
            The default name of the locale.
        native_name : `str`
            The native name of the locale.
        """
        self.value = value
        self.name = name
        self.native_name = native_name
        
        self.INSTANCES[value] = self
    
    # predefined
    bulgarian = P('bg', 'Bulgarian', 'български')
    chinese_cn = P('zh-CN', 'Chinese China', '\u4e2d\u6587')
    chinese_tw = P('zh-TW', 'Chinese Taiwan', '\u7e41\u9ad4\u4e2d\u6587')
    croatian = P('hr', 'Croatian', 'Hrvatski')
    czech = P('cs', 'Czech', 'Čeština')
    danish = P('da', 'Danish', 'Dansk')
    dutch = P('nl', 'Dutch', 'Nederlands',)
    english_gb = P('en-GB', 'English, UK', 'English, UK')
    english_us = P('en-US', 'English, US', 'English, US')
    finnish = P('fi', 'Finnish', 'Suomi')
    french = P('fr', 'French', 'Français')
    german = P('de', 'German', 'Deutsch')
    greek = P('el', 'Greek', 'Ελληνικά')
    hindi = P('hi', 'Hindi', '\u0939\u093f\u0928\u094d\u0926\u0940')
    hungarian = P('hu', 'Hungarian', 'Magyar')
    indonesian = P('id', 'Indonesian', 'Bahasa Indonesia')
    italian = P('it', 'Italian', 'Italiano')
    japanese = P('jp', 'Japanese', '\u65e5\u672c\u8a9e')
    korean = P('ko', 'Korean', '\ud55c\uad6d\uc5b4')
    lithuanian = P('lt', 'Lithuanian', 'Lietuviškai')
    norwegian = P('no', 'Norwegian', 'Norsk')
    polish = P('pl', 'Polish', 'Polski')
    portuguese = P('pt-BR', 'Portuguese, Brazilian', 'Português do Brasil')
    romanian = P('ro', 'Romanian, Romania', 'Română')
    russian = P('ru', 'Russian', 'Pусский')
    spanish = P('es-ES', 'Spanish', 'Español')
    swedish = P('sv-SE', 'Swedish', 'Svenska')
    thai = P('th', 'Thai', '\u0e44\u0e17\u0e22')
    turkish = P('tr', 'Turkish', 'Türkçe')
    ukrainian = P('uk', 'Ukrainian', 'Українська')
    vietnamese = P('vi', 'Vietnamese', 'Tiếng Việt')
