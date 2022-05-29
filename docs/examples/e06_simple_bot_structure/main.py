from dotenv import dotenv_values
from hata import Client, wait_for_interruption
from hata.ext.plugin_loader import EXTENSION_LOADER

config = dotenv_values('.env')

Sakuya = Client(config['TOKEN'],
    extensions = 'commands_v2',
    prefix = '!',
)


@Sakuya.events
async def ready(client):
    print(f'{client:f} is connected!')

# Registered variables to extension loader, show up in each loaded extension file.
EXTENSION_LOADER.add_default_variables(Sakuya=Sakuya)
# Adds the extensions file or the extensions files recursive in the directory
EXTENSION_LOADER.add('modules')
# Loads all the added extension files.
EXTENSION_LOADER.load_all()


Sakuya.start()

wait_for_interruption()
