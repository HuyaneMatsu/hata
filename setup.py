import pathlib, re
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
        'hata.discord.activity.fields',
        'hata.discord.activity.metadata',
        'hata.discord.application',
        'hata.discord.application.application',
        'hata.discord.application.application_entity',
        'hata.discord.application.application_executable',
        'hata.discord.application.application_install_parameters',
        'hata.discord.application.eula',
        'hata.discord.application.team',
        'hata.discord.application.team_member',
        'hata.discord.application.third_party_sku',
        'hata.discord.application_command',
        'hata.discord.auto_moderation',
        'hata.discord.auto_moderation.action',
        'hata.discord.auto_moderation.action_metadata',
        'hata.discord.auto_moderation.execution_event',
        'hata.discord.auto_moderation.rule',
        'hata.discord.auto_moderation.trigger_metadata',
        'hata.discord.bases',
        'hata.discord.bin',
        'hata.discord.channel',
        'hata.discord.channel.channel',
        'hata.discord.channel.channel_metadata',
        'hata.discord.channel.forum_tag',
        'hata.discord.client',
        'hata.discord.client.compounds',
        'hata.discord.component',
        'hata.discord.component.component',
        'hata.discord.component.component_metadata',
        'hata.discord.component.interaction_form',
        'hata.discord.component.string_select_option',
        'hata.discord.embed',
        'hata.discord.emoji',
        'hata.discord.events',
        'hata.discord.exceptions',
        'hata.discord.gateway',
        'hata.discord.guild',
        'hata.discord.guild.audit_logs',
        'hata.discord.guild.audit_logs.change_converters',
        'hata.discord.http',
        'hata.discord.integration',
        'hata.discord.integration.integration',
        'hata.discord.integration.integration_account',
        'hata.discord.integration.integration_application',
        'hata.discord.integration.integration_metadata',
        'hata.discord.interaction',
        'hata.discord.interaction.interaction_component',
        'hata.discord.interaction.interaction_event',
        'hata.discord.interaction.interaction_metadata',
        'hata.discord.interaction.interaction_option',
        'hata.discord.interaction.resolved',
        'hata.discord.interaction.responding',
        'hata.discord.invite',
        'hata.discord.localization',
        'hata.discord.message',
        'hata.discord.message.attachment',
        'hata.discord.oauth2',
        'hata.discord.oauth2.connection',
        'hata.discord.permission',
        'hata.discord.permission.permission_overwrite',
        'hata.discord.permission.permission_overwrite.fields',
        'hata.discord.role',
        'hata.discord.scheduled_event',
        'hata.discord.scheduled_event.metadata',
        'hata.discord.stage',
        'hata.discord.sticker',
        'hata.discord.user',
        'hata.discord.user.guild_profile',
        'hata.discord.voice',
        'hata.discord.webhook',
        'hata.ext',
        'hata.ext.asyncio',
        'hata.ext.command_utils',
        'hata.ext.commands_v2',
        'hata.ext.commands_v2.helps',
        'hata.ext.extension_loader',
        'hata.ext.patchouli',
        'hata.ext.plugin_loader',
        'hata.ext.plugin_loader.import_overwrite',
        'hata.ext.plugin_loader.snapshot',
        'hata.ext.plugin_loader.utils',
        'hata.ext.kokoro_sqlalchemy',
        'hata.ext.prettyprint',
        'hata.ext.slash',
        'hata.ext.slash.command',
        'hata.ext.slash.command.command_base',
        'hata.ext.slash.command.command_base_application_command',
        'hata.ext.slash.command.command_base_custom_id',
        'hata.ext.slash.command.component_command',
        'hata.ext.slash.command.context_command',
        'hata.ext.slash.command.form_submit_command',
        'hata.ext.slash.command.slash_command',
        'hata.ext.slash.menus',
        'hata.ext.solarlink',
        'hata.ext.top_gg',
        'hata.main',
        'hata.main.commands',
        'hata.main.commands.default',
        'hata.main.core',
        'hata.main.core.command',
        'hata.utils',
    ],
    url = 'https://github.com/HuyaneMatsu/hata',
    license = 'DBAD',
    author = 'HuyaneMatsu',
    author_email = 're.ism.tm@gmail.com',
    description = 'A powerful asynchronous library for creating Discord bots in Python.',
    long_description = README,
    long_description_content_type = 'text/markdown',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        
        'Intended Audience :: Developers',
        
        'Operating System :: OS Independent',
        
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        
        'Topic :: Communications :: Chat',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    include_package_data = True,
    package_data = {
        'hata.discord.bin': [
            'libopus-0.x64.dll',
            'libopus-0.x86.dll',
        ],
    },
    python_requires = '>=3.6',
    install_requires = [
        'scarletio>=1.0.47',
        'chardet>=2.0',
    ],
    extras_require = {
        'voice': [
            'PyNaCl>=1.3.0',
        ],
        'relativedelta': [
            'python-dateutil>=2.0',
        ],
        'cpythonspeedups': [
            'cchardet>=2.0',
        ],
    },
    entry_points = {
        'console_scripts': [
            'hata = hata.__main__:__main__'
        ]
    },
)
