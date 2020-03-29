# class `Extension`

- Source : [extension_loader.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/extension_loader.py)

## Properties

### `entry_point` (get)

- returns : `Any`
- default : `None`

Returns the entry point of the extension.

### `entry_point` (set)

- raises : `ValueError` / `TypeError`

Sets the entry point of the extension. Can be passed as `None`, `str`
instance or as `callable` what accepts 1 argument, the loaded module.
Async callables are supported as well.

> If set as `None`, the [extension loader's](ExtensionLoader.md)'s
> [default entry point](ExtensionLoader.md#default_entry_point-get)
> will be used instead.

### `entry_point` (del)

Removes the entry point of the extension by setting it as `None`.

### `exit_point` (get)

- returns : `Any`
- default : `None`

Returns the exit point of the extension.

### `exit_point` (set)

- raises : `ValueError` / `TypeError`

Sets the exit point of the extension. Can be passed as `None`, `str`
instance or as `callable` what accepts 1 argument, the loaded module
Async callables are supported as well.

> If set as `None`, the [extension loader's](ExtensionLoader.md)'s
> [default exit point](ExtensionLoader.md#default_exit_point-get)
> will be used instead.

### `exit_point` (del)

Removes the exit point of the extension by setting it as `None`.

### `extend_default_variables` (get)

- returns : `bool`

Returns whether the extension uses the loader's default variables or
just it's own's.

### `extend_default_variables` (set)

- raises : `TypeError`

Sets whether the extension should use the loader's default variables or
just it's own's.

### `locked` (get)

- returns : `bool`

Returns whether the extension uses the loader's default variables or
just it's own's.

### `locked` (set)

- raises : `TypeError`

Sets whether the extension should be picked up by the `.{}_all` methods of the
[extension loader](ExtensionLoader.md).

### `name`

- returns : `str`

Returns the extension's name.

## Methods

### `add_default_variables(self, **variables)`

Adds default variables to the extension. These variables are asigned to the
module before it is loaded.

> Raises `ValueError` if a variable name is used, what is `module` attribute.

### `remove_default_variables(self, *names)`

- returns : `None`

Removes the default variables of the extension, which's names are mentioned.
If a variable with a specific name is not found, no error is raised.

### `clear_default_variables(self)`

- returns : `None`

Removes all the default variables of the extension.

## Magic methods

### `__hash__(self)`

- returns : `int`

Returns the extension's [`._spec`](#_spec-instance-attribute)'s
[`.origin`](https://docs.python.org/3/library/importlib.html#importlib.machinery.ModuleSpec.origin)'s
hash.

### `__repr__(self)`

- returns : `str`

Returns the extension's representation.

## Internal

### `__new__((cls, name, entry_point, exit_point, extend_default_variables, default_variables)` (magic method)

- returns : [`Extension`](Extension.md)
- raises : `ModuleNotFoundError`

Creates an extension with the given arguments. If an extension already exists
with the given name, returns that.

> If no module is found with the given name, raises `ModuleNotFoundError`.

### `_state` (instance attibute)

The state of the extension. Can be:

| name                      | value |
|---------------------------|-------|
| EXTENSION_STATE_UNDEFINED | 0     |
| EXTENSION_STATE_LOADED    | 1     |
| EXTENSION_STATE_UNLOADED  | 2     |

### `_spec` (instance attribute)

- type : [`ModuleSpec`](https://docs.python.org/3/library/importlib.html#importlib.machinery.ModuleSpec)
The module specification for the extension's module's import system related
state.

### `_lib` (instance attribute)

- type : `module` / `NoneType`
- default : `None`

The extension's module. Set as `module` object only if it the extension was
already loaded.

### `_locked` (instance attribute)

- type : `bool`

The internal slot used for the [locked](#locked-get) property.

### `_entry_point` (instance attribute)

- type : `Any`
- default : `None`

The internal slot used by the [entry_point](#entry_point-get) property.

### `_exit_point` (instance attribute)

- type : `Any`
- default : `None`

The internal slot used by the [exit_point](#exit_point-get) property.

### `_extend_default_variables` (instance attribute)

The internal slot used by the
[extend_default_variables](#extend_default_variables-get) property.

### `_default_variables` (instance attribute)

- type: `HybridValueDictionary` / `NoneType`
- items: (`str`, `Any`)
- default : `None`

An optionally weak value dictionary to store objects for asigning them to
modules before lodaing them. If it is empty, then it is set as `None` instead.

### `_added_variable_names` (instance attribute)

- type : `list`

A list of the added variables' names to the module.

### `_load(self)` (method)

- returns : `module` / `NoneType`

Loads the module and returns it. If it is already loaded returns `None`.

### `_unload(self)` (method)

- returns : `module` / `NoneType`

Unloads the module and returns it. If it is already unloaded returns `None`.

### `_unasign_variables(self)` (method)

- returns : `None`

Unasigns the asigned variables to the module and clears
[`._added_variable_names`](#_added_variable_names-instance-attribute).

### `_unlink(self)` (method)

Removes the extension's module from the loaded ones. Should not be called on
loaded extensions.
