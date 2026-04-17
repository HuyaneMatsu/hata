__all__ = ('Jacket',)

from hata import Client

from ..constants import JACKET_TOKEN


Jacket = Client(
    JACKET_TOKEN,
    extensions = ['slash'],
)
