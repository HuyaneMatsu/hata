import re, pathlib
from ast import literal_eval
from setuptools import setup

HERE = pathlib.Path(__file__).parent

# Lookup version
version_search_pattern = re.compile('^__version__[ ]*=[ ]*((?:\'[^\']+\')|(?:\"[^\"]+\"))[ ]*$', re.M)
parsed = version_search_pattern.search((HERE / 'hata' / '__init__.py').read_text())
if parsed is None:
    raise RuntimeError('No version found in `__init__.py`.')

version = literal_eval(parsed.group(1))

# Lookup readme
README = (HERE / 'README.md').read_text('utf-8')

setup(
    name = 'hata',
    version = version,
    packages = [
        'hata',
        'hata.backend',
        'hata.discord',
        'hata.discord.activity',
        'hata.discord.application',
        'hata.discord.bases',
        'hata.discord.bin',
        'hata.discord.channel',
        'hata.discord.client',
        'hata.discord.embed',
        'hata.discord.emoji',
        'hata.discord.events',
        'hata.discord.exceptions',
        'hata.discord.gateway',
        'hata.discord.guild',
        'hata.discord.http',
        'hata.discord.integration',
        'hata.discord.interaction',
        'hata.discord.invite',
        'hata.discord.message',
        'hata.discord.oauth2',
        'hata.discord.permission',
        'hata.discord.role',
        'hata.discord.stage',
        'hata.discord.sticker',
        'hata.discord.user',
        'hata.discord.voice',
        'hata.discord.webhook',
        'hata.ext',
        'hata.ext.asyncio',
        'hata.ext.command_utils',
        'hata.ext.commands',
        'hata.ext.commands.helps',
        'hata.ext.commands_v2',
        'hata.ext.commands_v2.helps',
        'hata.ext.extension_loader',
        'hata.ext.kokoro_sqlalchemy',
        'hata.ext.patchouli',
        'hata.ext.prettyprint',
        'hata.ext.slash',
        'hata.main',
    ],
    url = 'https://github.com/HuyaneMatsu/hata',
    license = 'MIT',
    author = 'HuyaneMatsu',
    author_email = 're.ism.tm@gmail.com',
    description = 'A powerful asynchronous library for creating Discord bots in Python.',
    long_description = README,
    long_description_content_type = 'text/markdown',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        
        'License :: OSI Approved :: MIT License',
        
        'Intended Audience :: Developers',
        
        'Operating System :: OS Independent',
        
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        #'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        
        'Topic :: Communications :: Chat',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
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
        'chardet>=2.0',
    ],
    extras_require = {
        'voice' : [
            'PyNaCl>=1.3.0',
        ],
        'relativedelta' : [
            'python-dateutil>=2.0',
        ],
        'cpythonspeedups': [
            'cchardet>=2.0',
        ],
    },
)
