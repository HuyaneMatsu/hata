from setuptools import setup

setup(
    name        = 'hata',
    version     = '20191218.1',
    packages    = [
        'hata',
        'hata.bin',
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
        'hata': [
            'emojis.dnd',
                ],
        'hata.bin' : [
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
