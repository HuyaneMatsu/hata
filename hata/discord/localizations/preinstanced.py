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
    
    +-----------------------+-------------------------------+-----------+
    | Class attribute name  | name                          | value     |
    +=======================+===============================+===========+
    | bulgarian             | Bulgarian                     | bg        |
    +-----------------------+-------------------------------+-----------+
    | chinese_cn            | Chinese (China)               | zh-CN     |
    +-----------------------+-------------------------------+-----------+
    | chinese_tw            | Chinese (Taiwan)              | zh-TW     |
    +-----------------------+-------------------------------+-----------+
    | croatian              | Croatian                      | hr        |
    +-----------------------+-------------------------------+-----------+
    | czech                 | Czech                         | cs        |
    +-----------------------+-------------------------------+-----------+
    | danish                | Danish                        | da        |
    +-----------------------+-------------------------------+-----------+
    | dutch                 | Dutch                         | nl        |
    +-----------------------+-------------------------------+-----------+
    | english_gb            | English (Great Britain)       | en-GB     |
    +-----------------------+-------------------------------+-----------+
    | english_us            | English (United States)       | en-US     |
    +-----------------------+-------------------------------+-----------+
    | finnish               | Finnish                       | fi        |
    +-----------------------+-------------------------------+-----------+
    | french                | French                        | fr        |
    +-----------------------+-------------------------------+-----------+
    | german                | German                        | de        |
    +-----------------------+-------------------------------+-----------+
    | greek                 | Greek                         | el        |
    +-----------------------+-------------------------------+-----------+
    | hindi                 | Hindi                         | hi        |
    +-----------------------+-------------------------------+-----------+
    | hungarian             | Hungarian                     | hu        |
    +-----------------------+-------------------------------+-----------+
    | italian               | Italian                       | it        |
    +-----------------------+-------------------------------+-----------+
    | japanese              | Japanese                      | jp        |
    +-----------------------+-------------------------------+-----------+
    | korean                | Korean                        | ko        |
    +-----------------------+-------------------------------+-----------+
    | lithuanian            | Lithuanian                    | lt        |
    +-----------------------+-------------------------------+-----------+
    | norwegian             | Norwegian                     | no        |
    +-----------------------+-------------------------------+-----------+
    | polish                | Polish                        | pl        |
    +-----------------------+-------------------------------+-----------+
    | portuguese_br         | Portuguese (Brazil)           | pt-BR     |
    +-----------------------+-------------------------------+-----------+
    | romanian              | Romanian                      | ro        |
    +-----------------------+-------------------------------+-----------+
    | russian               | Russian                       | ru        |
    +-----------------------+-------------------------------+-----------+
    | spanish_sp            | Spanish (Spain)               | es-ES     |
    +-----------------------+-------------------------------+-----------+
    | swedish               | Swedish                       | sv-SE     |
    +-----------------------+-------------------------------+-----------+
    | thai                  | Thai                          | th        |
    +-----------------------+-------------------------------+-----------+
    | turkish               | Turkish                       | tr        |
    +-----------------------+-------------------------------+-----------+
    | ukrainian             | Ukrainian                     | uk        |
    +-----------------------+-------------------------------+-----------+
    | vietnamese            | Vietnamese                    | vi        |
    +-----------------------+-------------------------------+-----------+
    """
    INSTANCES = {}
    VALUE_TYPE = str
    
    __slots__ = ()
    
    # predefined
    bulgarian = P('bg', 'Bulgarian')
    chinese_cn = P('zh-CN', 'Chinese (China)')
    chinese_tw = P('zh-TW', 'Chinese (Taiwan)')
    croatian = P('hr', 'Croatian')
    czech = P('cs', 'Czech')
    danish = P('da', 'Danish')
    dutch = P('nl', 'Dutch')
    english_gb = P('en-GB', 'English (Great Britain)')
    english_us = P('en-US', 'English (United States)')
    finnish = P('fi', 'Finnish')
    french = P('fr', 'French')
    german = P('de', 'German')
    greek = P('el', 'Greek')
    hindi = P('hi', 'Hindi')
    hungarian = P('hu', 'Hungarian')
    italian = P('it', 'Italian')
    japanese = P('jp', 'Japanese')
    korean = P('ko', 'Korean')
    lithuanian = P('lt', 'Lithuanian')
    norwegian = P('no', 'Norwegian')
    polish = P('pl', 'Polish')
    portuguese_br = P('pt-BR', 'Portuguese (Brazil)')
    romanian = P('ro', 'Romanian')
    russian = P('ru', 'Russian')
    spanish_sp = P('es-ES', 'Spanish (Spain)')
    swedish = P('sv-SE', 'Swedish')
    thai = P('th', 'Thai')
    turkish = P('tr', 'Turkish')
    ukrainian = P('uk', 'Ukrainian')
    vietnamese = P('vi', 'Vietnamese')
