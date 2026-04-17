__all__ = ()

from hata.env import EnvGetter


with EnvGetter() as env:
    JACKET_TOKEN = env.get_str('JACKET_TOKEN', raise_if_missing_or_empty = True)
    LABEL_TOKEN = env.get_str('LABEL_TOKEN', raise_if_missing_or_empty = True)
