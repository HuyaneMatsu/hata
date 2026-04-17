__all__ = ('Label',)

from hata import Client

from ..constants import LABEL_TOKEN


Label = Client(
    LABEL_TOKEN,
    extensions = ['slash'],
)
