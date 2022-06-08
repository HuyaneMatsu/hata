# Introduction

As your bot grows you will probably want to split the code into multiple files to improve readability and extendability.

Hata offers you a solution called plugin loading.

As it comes from the name, plugins can be plugged in and out, allowing your application to be more modular.
Any added, removed event handler or interaction is tracked while loading a plugin defining what changes should be
reversed if required.

The main aim of hata's plugin loader is to preserve traditional code flow inside of plugins without introducing weird
top level classes.
When designing it an important factor was to not limit it's support for a single client instance producing a pretty
unique solution for the problem. The concept is based on presetting variables before the module is executing, but more
about this later.

# Getting started

To get started we need a few plugins. These can be either files or directories.
To use them first we will register, then load them.

```py
from hata.ext.plugin_loader import register_plugin, load_plugin

register_plugin('directory')
load_plugin('directory')
```

Or there is a shortcut function to do all this:

```py
from hata.ext.plugin_loader import register_and_load_plugin

register_and_load_plugin('plugins')
```

## Presetting variables

As mentioned in the introduction, the plugin loader is based on setting variables before the module is executed.
You can set these variables by using the `add_default_plugin_variables` function.

```py
from hata import Client
from hata.ext.plugin_loader import add_default_plugin_variables, register_and_load_plugin


my_beloved_bot = Client(...)

add_default_plugin_variables(my_beloved_bot=my_beloved_bot)

register_and_load_plugin('plugin')
```

**plugin.py**
```py
@my_beloved_bot.events
async def launch(client):
    print(f'{client} launched!')

@my_beloved_bot.events
async def ready(client):
    print(f'{client} is ready!')
```

Added *default* variables will show up in all files. (There is option to turn this off / file)

You can also define file specific variables. To do this, pass additional keyword variables when
registering the plugin.

```py
register_and_load_plugin('plugin', add_launch_event_handler=False)
```

An important to note, that these plugin-specific variables wont show up in sub-modules imported from that file.

### Linter confusion

These variables might confuse linters. To help them out, you can annotate them.

```py
from hata import Client

my_beloved_bot: Client
```

After this the linter will see that `my_beloved_bot` is indeed a `Client`, but "it might not be defined" still.

Hata ignores these annotations, they are completely up to you.

## Setup & Teardown

Not every change can be tracked inside of a plugin, sometimes you might want to access resources,
which are actively used while the bot is running. An other case is when you want to make other changes to the
application outside of the tracked scope.

At these cases you might want to use the `setup` and the `teardown` functions.

```py
def setup(module):
    # allocate resources
    ...

def teardown(module):
    # unallocate resources
    ...
```

The plugin's body runs inside of an executor, allowing blocking tasks to be executed, but the setup & teardown
functions always **run on the event loop**, meaning they can be *async* as well, but they should
**not contains blocking** operations.

## Registering rules

When registering a plugin, multiple preferences are applied:

1. If the plugin name refers to a file, load that.
    
    ```
    /plugins.py
    ```
    
2. If the plugin is a directory, load all files from it.
    
    ```
    /plugins/file_1.py
    /plugins/file_2.py
    ```

3. If a directory has an `__init__.py` file, will load only that file from the directory.
    
    ```
    /plugins/__init__.py
    /plugins/file_1.py                          <- this wont be registered.
    /plugins/file_2.py                          <- this wont be registered.
    ```

4. Apply recursive loading on directories without `__init__.py` file.

    ```
    /plugins/file_1.py
    /plugins/file_2.py
    
    /plugins/directory_1/__init__.py
    /plugins/diretcory_1/file_3.py              <- `__init__.py` rule: this wont be registered.
    /plugins/diretcory_1/directory_n/file_n.py  <- `__init__.py` rule: this wont be registered.
    
    /plugins/directory_2/file_4.py
    /plugins/diretcory_2/file_5.py
    ```


## Directory based plugins

As mentioned above if a directory has an `__init__.py`, only that file will be loaded.
Altho when a plugin's **sub-module is imported** the file will be automatically registered as a plugin as well.
This becomes really handy when dealing with bigger (multi-file) commands.

### Plugin trees

By importing a plugin from an other one, a plugin tree is built internally. These trees can be used to decide which
files should be grouped together when unloading / reloading plugins.

As an example:

```
/file_1.py
/file_2.py
```

If `file_1.py` imports from `file_2.py`, the two file will be linked together and by default when any of them is
reloaded, both will be.

### Sub module trees

Sub-module trees are applied to directories which have an `__init__.py` files in them.
They can be either weak or strong sub module trees.

### Strong sub-module trees

Strong sub-module trees can be handy when dealing with a command with sub-commands.

Imagine that each sub-command has it's own file.

```
/__init__.py
sub_command_1.py
sub_command_2.py
sub_command_3.py
```

To build a command, you might do something like:

**\_\_init\_\_.py**
```
from . import sub_command_1
from . import sub_command_2
from . import sub_command_3

main_command = ...

for module in (sub_command_1, sub_command_2, sub_command_3):
    sub_command = getattr(sub_command_1, sub_command_1.__all__[0])
    main_command.add_sub_command(sub_command)

```

**sub_command_1.py**
```
__all__ = ('add', )

async def add(...):
    """Adds a new plum to the basket."""
    ...
```

> This is just an example you can do it completely differently.


### Weak sub-module trees

This case occurs when inside of a directory not every module relies on each other. To build a weak sub-module tree,
you need import only the module itself and no value from it.

- Correct example:

    **\_\_init\_\_.py**
    ```py
    from . import file_1
    ```
    
    You can also use `import *`, if the file has empty `__all__` defined.
    
    **\_\_init\_\_.py**
    ```py
    from file_1 import *
  
    __all__ = ()
    ```
    
    **file_1.py**
    ```py
    __all__ = ()
    ```
    
    > I recommend adding `__all__ = ()` to every file which should be weakly bound. It makes it more stupid-proof.

- Bad example

    **\_\_init\_\_.py**
    ```
    from file_1 import command
    ```
    
    A weird case might be when you just want to access a sub-module value, but  accessing an attribute like this is
    same as directly importing it!
    
    **\_\_init\_\_.py**
    ```
    from . import file_1
    command = file_1.command
    ```

# API

The plugin loader offers a function and a more object oriented api. They do the same mostly... the functional api
offers a few extra utility functions too as an extra.

Here is a full list of the offered functionalities:

| Functional                        | Object oriented                           | Description                                                                   |
|-----------------------------------|-------------------------------------------|-------------------------------------------------------------------------------|
| `add_default_plugin_variables`    | `PLUGIN_LOADER.add_default_variables`     | Add variables to present to all plugins.                                      |
| `clear_default_plugin_variables`  | `PLUGIN_LOADER.clear_default_variables`   | Clears all variables to preset.                                               |
| `get_plugin`                      | `PLUGIN_LOADER.get_plugin`                | Get a plugin with that exact name.                                            |
| `get_plugin_like`                 | N / A                                     | Gets a plugin which name contains the given value.                            |
| `get_plugins_like`                | N / A                                     | Gets all the plugins which name contains the given value.                     |
| `import_plugin`                   | N / A                                     | Registers & imports the defined module. Familiar to *register and load*.      |
| `load_all_plugin`                 | `PLUGIN_LOADER.load_all`                  | Loads all plugins excluding the *locked* ones.                                |
| `load_plugin`                     | `PLUGIN_LOADER.load`                      | Loads one or an iterable of plugins.                                          |
| `register_and_load_plugin`        | `PLUGIN_LOADER.register_and_load`         | Registers one or an iterable of plugins, then directly after loads them.      |
| `register_plugin`                 | `PLUGIN_LOADER.register`                  | Registers one or an iterable of plugins.                                      |
| `reload_all_plugin`               | `PLUGIN_LOADER.reload_all`                | Reloads all plugins except the *locked* ones.                                 |
| `reload_plugin`                   | `PLUGIN_LOADER.reload`                    | Reloads one or an iterable of plugins.                                        |
| `remove_default_plugin_variables` | `PLUGIN_LOADER.remove_default_variables`  | Removes a variable from the preset ones.                                      |
| `require`                         | N / A                                     | Stops a plugin from loading by requiring specific variables to be present.    |
| `unload_all_plugin`               | `PLUGIN_LOADER.unload_all`                | Unloads all plugins except the *locked* ones.                                 |
| `unload_plugin`                   | `PLUGIN_LOADER.unload`                    | Unloads one or an iterable of plugins.                                        |


# Something is going way wrong a.k.a. how can things derp out on the most unexpected ways!

## Deadlock

Yupp, there can be deadlock, but when and why is more interesting!

We will go from from top to bottom to find out what is happening and how to solve it.

- **The issue**
  
    When importing a plugin from an other, the native `import` hooks might lock code execution when the control is
    given back to the source file.
    
    **/plugins/file_1.py**
    ```py
    # Before import everything is fine
    
    from .file_2 import something
        # file_2 runs, no problem. Executor opened and then left.
        # Everything is fine, importlibs returns the control.
    
    # random, probably C code runs
    # our code is frozen
    ```
    
    To solve this, you can use the `import_plugin` function, where this wont happen, because we never leave python
    lands.
    
    **/plugins/file_1.py**
    ```py
    from hata.ext.plugin_loader import import_plugin
    
    something = import_plugin('.file_2', 'something')
    ```

- **The black magic**
    
    This can only happen when calling `load_plugin` from **not the main file**, as an example:
    
    **/main.py**
    ```py
    ...
    
    import bots
    
    ...  
    ```
    
    **/bots.py**
    ```py
    from hata.ext.plugin_loader import load_all_plugin
    
    ...
    
    load_all_plugin()
    ```
    
    To solve this move the function call to the main file :WHAT:
    
    **/main.py**
    ```py
    ...
    
    import hata
    
    import bots
    
    hata.ext.plugin_loader.load_all_plugin()
    
    ...
    ```
    
    **/bots.py**
    ```py
    ...
    ```

- **Welcome to HELL**
    
    This is not a python issue, but as weird as it might sound, an implementation one.
    
    ```sh
    $ python3 main.py
    ```
    
    This bug only occurs on Cpython. **Use pypy.**
    
    ```sh
    $ pypy3 main.py
    ```
      
    Problem solved.


## Random import error when using relative imports

When using relative imports to an other plugin, something might derp out and you can end up with a random import error.

- **The issue**
    
    Lets say our directory looks like:
    ```
    /plugins/file_1.py
    /plugins/file_2.py
    /plugins/file_3.py
    ```
    
    We try to import `file_2.py` from `file_1.py` and the file cannot be resolved.
    
    **/plugins/file_1.py**
    ```py
    from . import file_2
    ```
    
    The plugin loader is smart enough to resolve this tho. Kinda weird.
    
    **/plugins/file_1.py**
    ```py
    from hata.ext.plugin_loader import import_plugin
    
    import_plugin('.file_2')
    ```

- **The reason**
    
    When doing relative imports, it is required to have an `__init__.py` in the directory. *The more you know*
    
    ```
    /plugins/__init__.py
    /plugins/file_1.py
    /plugins/file_2.py
    /plugins/file_3.py
    ```
    
    This produces a weird case when the plugin lookup is catched by the `__init__.py` file.
    To resolve this issue we can build a weak sub-module tree, like:
    
    **/plugins/\_\_init\_\_.py**
    ```py
    from . import file_1
    from . import file_2
    from . import file_3
    ```

- **Welcome to HELL**
    
    The *random* import error is again not a python error.
    
    To solve this, we will switch pypy, which will raise a `SystemError` instead with the details of what is happening
    telling you, you indeed need an `__init__.py` file.
