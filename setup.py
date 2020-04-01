import os, re
from ast import literal_eval
from setuptools import setup

version_search_pattern=re.compile('^__version__[ ]*=[ ]*((?:\'[^\']+\')|(?:\"[^\"]+\"))[ ]*$',re.M)
with open(os.path.join(os.path.split(__file__)[0],'hata','__init__.py')) as file:
    parsed=version_search_pattern.search(file.read())

if parsed is None:
    raise RuntimeError('No version found at __init__.py')

version=literal_eval(parsed.group(1))

setup(
    name        = 'hata',
    version     = version,
    packages    = [
        'hata',
        'hata.backend',
        'hata.discord',
        'hata.discord.bin',
        'hata.ext.commands',
        'hata.ext.extension_loader',
        'hata.ext.kokoro_sqlalchemy',
        'hata.ext.prettyprint',
            ],
    url         = 'https://github.com/HuyaneMatsu/hata',
    license     = 'Apache 2.0',
    author      = 'HuyaneMatsu',
    author_email= 're.ism.tm@gmail.com',
    description = 'Discord API wrapper in Python',
    classifiers = [
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
            ],
    include_package_data = True,
    package_data = {
        'hata.discord': [
            'emojis.dnd',
                ],
        'hata.discord.bin' : [
            'libopus-0.x64.dll',
            'libopus-0.x86.dll',
                ],
            },
    python_requires = '>=3.6',
    install_requires = [
        'chardet>=2.0,<4.0',
            ],
    extras_require = {
        'voice' : [
            'PyNaCl==1.3.0',
                ],
        'relativedelta' : [
            'python-dateutil>=2.0',
                ],
        'cpythonspeedups': [
            'cchardet',
                ],
            },
        )
