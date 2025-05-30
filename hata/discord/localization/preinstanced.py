__all__ = ('Locale',)

from ..bases import Preinstance as P, PreinstancedBase


class Locale(PreinstancedBase, value_type = str):
    """
    Represents Discord's locale.
    
    Attributes
    ----------
    name : `str`
        The default name of the locale.
    
    native_name : `str`
        The native name of the language.
    
    value : `str`
        The Discord side identifier value of the locale.
    
    Type Attributes
    ---------------
    Every predefined locale is also stored as a type attribute:
    
    +-----------------------+-------------------------------+-----------+---------------------------------------+
    | Type attribute name   | Name                          | Value     | Native name                           |
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
    | spanish_la            | Spanish (Latin America)       | es-419    | Español, LATAM                        |
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
    __slots__ = ('native_name',)
    
    def __new__(cls, value, name = None, native_name = None):
        """
        Creates new locale.
        
        Parameters
        ----------
        value : `str`
            The Discord side identifier value of the locale.
        
        name : `None | str` = `None`, Optional
            The default name of the locale.
        
        native_name : `None | str` = `None`, Optional
            The native name of the locale.
        """
        if name is None:
            name = value
        
        if native_name is None:
            native_name = name
        
        self = PreinstancedBase.__new__(cls, value, name)
        self.native_name = native_name
        return self
    
    
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
    spanish_la = P('es-419', 'Spanish (Latin America)', 'Español, LATAM')
    
    swedish = P('sv-SE', 'Swedish', 'Svenska')
    thai = P('th', 'Thai', '\u0e44\u0e17\u0e22')
    turkish = P('tr', 'Turkish', 'Türkçe')
    ukrainian = P('uk', 'Ukrainian', 'Українська')
    vietnamese = P('vi', 'Vietnamese', 'Tiếng Việt')
