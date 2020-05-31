import re, pathlib
from ast import literal_eval
from setuptools import setup

HERE = pathlib.Path(__file__).parent

# Lookup version
version_search_pattern = re.compile('^__version__[ ]*=[ ]*((?:\'[^\']+\')|(?:\"[^\"]+\"))[ ]*$',re.M)
parsed = version_search_pattern.search((HERE / 'hata' / '__init__.py').read_text())
if parsed is None:
    raise RuntimeError('No version found at __init__.py')

version=literal_eval(parsed.group(1))

# Lookup readme
README = (HERE / 'README.md').read_text()

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
    long_description = README,
    long_description_content_type = 'text/markdown',
    classifiers = [
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation : PyPy',
            ],
    include_package_data = True,
    package_data = {
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
