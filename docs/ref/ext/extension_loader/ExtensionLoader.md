# Extension Loader

There are some cases when you propably want to change some functional part of
your client in runtime. Load, unload or reload code. Hata provides an easy to
use (that's what she said) solution to solve this issue.

It is called extension loader is an extension of hata. It is separated from
`events` extension, but it does not mean they do not go well together. But
what more, extension loader was made to complement it.

- Source : [extension_loader.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/ext/extension_loader/extension_loader.py)

## Usage

The `ExtensionLoader` class is instanced already as `EXTENSION_LOADER` and that
can be imported as well from `extension_loader.py`. Instancing the class again
will yield the same object.

Because hata can have more clients, we needed a special extension loader what
can handle using more clients at any file, so the choice ended up on a 
really interesting idea: asign variables to a module before it is (re)loaded.

To show this is not blackmagic, here is an example,
[*or just skip it*](#Adding-extensions):

###### main.py
```py
from hata.extension_loader import EXTENSION_LOADER
from datetime import datetime

cake = 'cake'
now = datetime.now()

EXTENSION_LOADER.add_default_variables(cake=cake, now=now)
EXTENSION_LOADER.load_extension('extension')
```

###### extension.py

```py
print(cake, now)
```

Make sure you start `main.py` with interactive mode. If you never did it, just use
the `-i` option like:

```sh
$ python3 -i main.py
```

Or on windows:

```sh
$ python -i main.py
```

After you ran `main.py` you should see the following (excecpt the date):

```
cake 2020-03-14 09:40:41.587673
``` 

Because now we have the interpreter, you can change the variables.

```py
>>> EXTENSION_LOADER.add_default_variables(cake='cakes taste good, and now is:')
>>> EXTENSION_LOADER.reload_all()
```

And a different text is printed out:

```
cakes taste good, and now is: 2020-03-14 09:40:41.587673
```

Now lets edit `extension.py`.
```py
cake = cake.split()
print(*cake, now, sep='\n')
```

And reload the extension:
```py
>>> EXTENSION_LOADER.reload_all()
```

The printed text really changed again:

```
cakes
taste
good,
and
now
is:
2020-03-14 09:40:41.587673
```

If you remove default variables and the extension file still uses them,
you get an [`ExtensionError`](ExtensionError.md):
```py
>>> EXTENSION_LOADER.remove_default_variables('cake')
>>> EXTENSION_LOADER.reload_all()
```

```
Traceback (most recent call last):
  File "<pyshell#13>", line 1, in <module>
    EXTENSION_LOADER.reload_all()
  File ".../hata/extension_loader.py", line 652, in reload_all
    task.syncwrap().wait()
  File ".../hata/futures.py", line 823, in wait
    return self.result()
  File ".../hata/futures.py", line 723, in result
    raise exception
  File ".../hata/futures.py", line 1602, in __step
    result=coro.throw(exception)
  File ".../hata/extension_loader.py", line 670, in _reload_all
    raise ExtensionError(error_messages) from None
hata.extension_loader.ExtensionError: ExtensionError (1):
Exception occured meanwhile loading an extension: `extension`.

Traceback (most recent call last):
  File ".../hata/extension_loader.py", line 675, in _load_extension
    lib = await KOKORO.run_in_executor(extension.load)
  File ".../hata/extension_loader.py", line 270, in load
    reload_module(lib)
  File ".../importlib/__init__.py", line 169, in reload
    _bootstrap._exec(spec, module)
  File "<frozen importlib._bootstrap>", line 630, in _exec
  File "<frozen importlib._bootstrap_external>", line 728, in exec_module
  File "<frozen importlib._bootstrap>", line 219, in _call_with_frames_removed
  File ".../extension.py", line 1, in <module>
    cake = cake.split()
NameError("name 'cake' is not defined")
```

##### Adding extensions

Extensions can be added with the `.add` method.

```py
EXTENSION_LOADER.add('cute_commands')
```

Or more extension can be added as well by passing an iterable:

```py
EXTENSION_LOADER.add(['cute_commands', 'nice_commands'])
```

> If an extension's file is not found, then `.add` will raise 
> `ModuleNotFoundError`. If the passed argument is not `str` instance or
> `iterable of str`, `TypeError` is raised.

##### Entry point

By default the extension loader searches a function at the file called
`setup`, what should accept 1 argument, the library itself. We call this point
`entry_point`. An other `entry_point` can be defined as default, or an unique
can be specified for each different extension as well.

Modifying the default `entry_point`:

```py
EXTENSION_LOADER.default_entry_point = 'entry'
```

Adding an extension with a different entry point:

```py
EXTENSION_LOADER.add('cute_commands', entry_point='entry')
```

These entry points can be passed as a `callable` (can be async) or as `str`
instances as well.

##### Loading

Extensions can be loaded by their name:

```py
EXTENSION_LOADER.load('cute_commands')
```

All extension can be loaded by using:

```py
EXTENSION_LOADER.load_all()
```

Or extension can be added and loaded at the same time as well:

```py
EXTENSION_LOADER.load_extension('cute_commands')
```

> `.load_extension` method supports all the keyword argumnts as `.add`.

##### Passing variables to extensions

You can pass variables to extensions with the `.add_default_variables` method:
```py
EXTENSION_LOADER.add_default_variables(cake=cake, now=now)
```

> Adding or removing variables wont change the already loaded extensions'
> state, those needs to be reloaded to see them.

Or pass variables to just specific extensions:

```py
EXTENSION_LOADER.add('cute_commands', cake=cake, now=now)
```

You can specify if the extension should use just it's own variables and ignore
the default ones too:

```
EXTENSION_LOADER.add('cute_commands', extend_default_variables=False, cake=cake, now=now)
```

Every variable added is stored in an optionally weak value dictionary.
But you can remove the added variables as well:

```py
EXTENSION_LOADER.remove_default_variables('cake', 'now')
```

The extensions can be accessed by their name as well, then you can use their
properties to modify them.

```py
EXTENSION_LOADER.extensions['cute_commands'].remove_default_variables('cake')
```

##### Unloading and Exit point

You can unload extension on the same way as loading them.

```py
EXTENSION_LOADER.unload('cute_commands')
```

Or unload all:

```py
EXTENSION_LOADER.unload_all()
```

When unloading an extension, the extension loader will search a function at the
extension, what we call `exit_point` and will run it. By default it looks for
a variable named `teardown`. `exit_point` acts on the same way as the
`entry_point`, so it can be modified for looking for other name to defining
and passing a callable (can be async again).

Can be set almost on the same way as well:

```py
EXTENSION_LOADER.default_exit_point = 'exit'
```

Or

```py
EXTENSION_LOADER.add('cute_commands', exit_point='exit')
```

> There are also methods for reloaing: `.reload(name)` and `.reload_all()`

##### Removing extensions.

Unloaded extensions can be removed from the extension loader by using the
`.remove` method:

```py
EXTENSION_LOADER.remove('cute_commands')
```

Or more extension with an iterable:

```py
EXTENSION_LOADER.remove(['cute_commands', 'nice_commands'])
```

> Removing loaded extension will yield `RuntimeError`.

##### Threading model

When you call the different methods of the extension loader, they ll run on the
[clients'](../../discord/Client.md) thread, what is named `KOKORO` internally.

These methods are:
- `.load_extension`
- `.load`
- `.load_all`
- `.unload`
- `.unload_all`
- `.reload`
- `.reload_all`

Meanwhile loading and executing the extension's code the thread is switched
to an executor, so blocking tasks can be executed easily. The exception under
this rule are the `entry_point`-s and the `exit_point`-s, which always run on
the same thread as the clients, that is why they can be async as well.

These methods also act differently depending from which thread they were called
from. Whenever they are called from the client's thread, a `Task` is returned
what can be `awaited`. If called from other `EventThread`, then the task is
asyncwrapped and that is returned. When calling from any other thread (like the
main thread for example), the task is syncwrapped and the thread is blocked till
the extension's loading is finished.

# Structure

Other references:
- [`ExtensionError`](ExtensionError.md)
- [`Extension`](Extension.md)

## Instance attributes

### `extensions`

- type : `dict`
- items : (`str`, `Extension`)

A dict of the added extensions to the extension loader, where the keys are the
extensions' name and the values are the extensions.

## Properties

### `default_entry_point` (get)

- returns : `Any`
- default : `'setup'`

Returns the default entry point of the extension loader.

### `default_entry_point` (set)

- raises : `ValueError` / `TypeError`

Sets the default entry point of the extension loader. Can be passed as
`None`, `str` instance or as `callable` what accepts 1 argument, the loaded
module. Async callables are supported as well.

### `default_entry_point` (del)

Removes the default entry point of the extension loader by setting it as
`None`.

### `default_exit_point` (get)

- returns : `Any`
- default : `'setup'`

Returns the default exit point of the extension loader.

### `default_exit_point` (set)

- raises : `ValueError` / `TypeError`

Sets the default exit point of the extension loader. Can be passed as
`None`, `str` instance or as `callable` what accepts 1 argument, the loaded
module. Async callables are supported as well.

### `default_exit_point` (del)

Removes the default exit point of the extension loader by setting it as
`None`.

## Methods

### `add_default_variables(self, **variables)`

- returns : `None`
- raises : `ValueError`

Adds default variables to the extension loader. These variables are asigned
to the module before it is loaded.

> Raises `ValueError` if a variable name is used, what is `module` attribute.

### `remove_default_variables(self, *names)`

- returns : `None`

Removes the default variables of the extension loader, which's names are
mentioned. If a variable with a specific name is not found, no error is raised.

### `clear_default_variables(self)`

- returns : `None`

Removes all the default variables of the extension loader.

### `add(self, name, entry_point=None, exit_point=None, extend_default_variables=True, locked=False, **variables)`

- returns : `None`
- raises : `TypeError` / `ModuleNotFoundError` / `ValuError`

The method to add extensions to the extension loader.

`name` should be `str`, or an `iterable` of `str`-s, which contains
extension (module) names. `entry_point` and `exit_point` can be `None`, 
`str`, or a `callable`.

The `entry_point`, `exit_point`, `extend_default_variables`, `locked` and the
`variables` are going to be extension specific. If `entry_point` and
`exit_point` is specified, then the extension loader will use those instead of
it's own defaults. If `extend_default_variables` is passed as `False` the
extension will not pick up the extension loader's default variables, instead
just use it's own. If `locked` is passed as `True` means that the extension
wont be picked up by the `.{}_all` methods.

> If the extension is not found, a `ModuleNotFoundError` will be raised.

### `remove(self, name)`

- returns : `None`
- raises : `TypeError` / `RuntimeError`

Removes one or more extensions from the extension loader. If any of the 
extensions is not found, no errors will be raised.

`name` should be `str`, or an `iterable` of `str`-s, which contains
extension (module) names.

> If a loaded extension is requested for remove, `RuntimeError` will
> be raised.

### `load_extension(self, name, *args, **kwargs)`

- returns : `None` / `Task` -> `None` / `FutureAsyncWrapper` -> `None`
- raises : [`ExtensionError`](ExtensionError.md) / `TypeError` / `ModuleNotFoundError` / `ValuError`

[Adds](#addself-name-entry_pointnone-exit_pointnone-extend_default_variablestrue-lockedfalse-variables)
the extension first with the passed `args` and `kwargs`, then [loads](#loadself-name) it.

> If the extension is not found, an [`ExtensionError`](ExtensionError.md) will
> be raised.

> If the method is called from an `AsyncThread`, then an `awaitable` is
> returned, if not then the function returns when the extension finished
> loading.

### `load(self, name)`

- returns : `None` / `Task` -> `None` / `FutureAsyncWrapper` -> `None`
- raises : [`ExtensionError`](ExtensionError.md) / `RuntimeError`

Loads an extension with the given name. If anything goes wrong, raises
[`ExtensionError`](ExtensionError.md), which contains the traceback of the
exception(s).

> If the extension is not found, an [`ExtensionError`](ExtensionError.md) will
> be raised.

> If the method is called from an `AsyncThread`, then an `awaitable` is
> returned, if not then the function returns when the extension finished
> loading.

### `unload(self, name)`

- returns : `None` / `Task` -> `None` / `FutureAsyncWrapper` -> `None`
- raises : [`ExtensionError`](ExtensionError.md) / `RuntimeError`

Unloads an extension with the given name. If anything goes wrong, raises
[`ExtensionError`](ExtensionError.md), which contains the traceback of the
exception(s).

If the extension is not loaded yet, will do nothing.

> If the extension is not found, an [`ExtensionError`](ExtensionError.md) will
> be raised.

> If the method is called from an `AsyncThread`, then an `awaitable` is
> returned, if not then the function returns when the extension finished
> unloading.

### `reload(self, name)`

- returns : `None` / `Task` -> `None` / `FutureAsyncWrapper` -> `None`
- raises : [`ExtensionError`](ExtensionError.md) / `RuntimeError`

Reloads an extension with the given name. If anything goes wrong, raises
[`ExtensionError`](ExtensionError.md), which contains the traceback of the
exception(s).

If the extension is not loaded yet, will load it. if the extension is loaded,
will unload it first, then load it.

> If the extension is not found, an [`ExtensionError`](ExtensionError.md) will
> be raised.

> If the method is called from an `AsyncThread`, then an `awaitable` is
> returned, if not then the function returns when the extension finished
> reloading.

### `load_all(self)`

- returns : `None` / `Task` -> `None` / `FutureAsyncWrapper` -> `None`
- raises : [`ExtensionError`](ExtensionError.md) / `RuntimeError`

Loads all the extension of the extension loader. If anything goes wrong,
raises an [`ExtensionError`](ExtensionError.md) only at the end, with the
exception(s).

> If the method is called from an `AsyncThread`, then an `awaitable` is
> returned, if not then the function returns when the extensions are
> finished loading.

### `unload_all(self)`

- returns : `None` / `Task` -> `None` / `FutureAsyncWrapper` -> `None`
- raises : [`ExtensionError`](ExtensionError.md) / `RuntimeError`

Unloads all the extension of the extension loader. If anything goes wrong,
raises an [`ExtensionError`](ExtensionError.md) only at the end, with the
exception(s).

> If the method is called from an `AsyncThread`, then an `awaitable` is
> returned, if not then the function returns when the extensions are
> finished unloading.

### `reload_all(self)`

- returns : `None` / `Task` -> `None` / `FutureAsyncWrapper` -> `None`
- raises : [`ExtensionError`](ExtensionError.md) / `RuntimeError`

Reloads all the extension of the extension loader. If anything goes wrong,
raises an [`ExtensionError`](ExtensionError.md) only at the end, with the
exception(s).

> If the method is called from an `AsyncThread`, then an `awaitable` is
> returned, if not then the function returns when the extensions are
> finished resloading.

## Magic methods

### `__new__(cls)`

- returns : [`ExtensionLoader`](ExtensionLoader.md)

Creates an `ExtensionLoader` instance. If the `ExtensionLoader` was instanced
already, then returns that instead.

### `__repr__(self)`

- returns : `str`

Returns the representation of the extension loader.

## Internal

### `_instance` (class attribute)

- type : `NoneType` / `ExtensionLoader`
- default : `None`

An internal attribute for storing the already created extension loader.

### `_default_entry_point` (instance attribute)

- type : `Any`
- default : `None`

Internal slot for the [`default_entry_point`](#default_entry_point-get)
property.

### `_default_exit_point` (instance attribute)

- type : `Any`
- default : `None`

Internal slot for the [`default_exit_point`](#default_exit_point-get)
property.

### `_default_variables` (instance attributes)

- type: `HybridValueDictionary`
- items: (`str`, `Any`)

An optionally weak value dictionary to store object for asigning them to
modules before lodaing them.

### `_load(self, name)` (method)

- returns : `None`
- raises : [`ExtensionError`](ExtensionError.md) / `RuntimeError`
- `awaitable`

[Loads](#_load_extensionself-client-extension-method) the given extension.
If the loading raises, the exception will contain every time only one message.

> If the extension is not found, an [`ExtensionError`](ExtensionError.md) will
> be raised.

### `_unload(self, name)` (method)

- returns : `None`
- raises : [`ExtensionError`](ExtensionError.md) / `RuntimeError`
- `awaitable`

[Unloads](#_unload_extensionself-client-extension-method) the given extension.
If the unloading raises, the exception will contain every time only one message.

> If the extension is not found, an [`ExtensionError`](ExtensionError.md) will
> be raised.

### `_reload(self, name)` (method)

- returns : `None`
- raises : [`ExtensionError`](ExtensionError.md) / `RuntimeError`
- `awaitable`

Reloads the given extension. First
[unloads](#_unload_extensionself-client-extension-method),
then [loads](#_load_extensionself-client-extension-method) it.
If unloading raises, wont try to load. The raised exception will contain every
time only one message.

> If the extension is not found, an [`ExtensionError`](ExtensionError.md) will
> be raised.

### `_load_all(self)` (method)

- returns : `None`
- raises : [`ExtensionError`](ExtensionError.md) / `RuntimeError`
- `awaitiable`

Loads all the extensions of the extension loader. Will not load already loaded
extension. Loads each extension one after the other. If any of the extensions 
raises, will still try to load the leftover ones. The raised exceptions'
messages are collected into one exception, what will be raised at the end.

### `_unload_all(self)` (method)

- returns : `None`
- raises : [`ExtensionError`](ExtensionError.md) / `RuntimeError`
- `awaitable`

Unloads all the extensions of the extension loader. Will not unload not loaded,
or unloaded extensions. Unloads each extension one after the other. The raised
exceptions' messages are collected into one exception, what will be raised at
the end.  If any of the extensions raises, will still try to unload the
leftover ones.

### `_reload_all(self)` (method)

- returns : `None`
- raises : [`ExtensionError`](ExtensionError.md) / `RuntimeError`
- `awaitiable`

Reloads all the extensions of the extension loader. If an extension is not
loaded, will load it, if the extension is loaded, will unload, then load it,
or if the extension is unload, will load it. Reloads each extension one after
the other. The raised exceptions' messages are collected into one exception,
what will be raised at the end.  If any of the extensions raises, will still
try to unload the leftover ones.

### `_load_extension(self, client, extension)` (method)

- returns : `None`
- raises : [`ExtensionError`](ExtensionError.md)
- `awaitable`

Loads an extension to the client. If the extension is already loaded, will do 
nothing. The loading can be separated into 3 parts:

1. Asign the default variables.
2. Load the module.
3. Find the entry point (if needed).
4. Ensure the entry point (if found).

If any of these fails, an [`ExtensionError`](ExtensionError.md) will be
raised. If step 2 or 4 raises, then a traceback will be included.

### `_unload_extension(self, client, extension)` (method)

- returns : `None`
- raises : [`ExtensionError`](ExtensionError.md)
- `awaitable`

Unloads an extension from the client. If the extension is not loaded, will do
nothing. The unloading can be separated into 2 parts:

1. Find the exit point (if needed).
2. Ensure the exit point (if found).
3. Remove the default variables.

If any of these fails, an [`ExtensionError`](ExtensionError.md) will be
raised. If step 2 raises, then a traceback will be included.

### `_render_exc(exception, header)` (staticmethod)

- returns : `str`

A function used to render exceptions' tracebacks. This function runs
in executor.
