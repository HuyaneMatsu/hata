
#### 1.1.64  *\[Soon TM\]*

##### Public API:

`CLIENTS` now uses `dict` type` instead of `ClientDictionary`.

##### Internal:

- `Client._delete` could construct not a fully built `User` object. Add `User._from_cleint` to fix this.
- Remove `ClientDictionary`.
- Speed up `dict.get` by passing default value.
- Fix some bad assignments in `Client._delete`.
- `Icon.__repr__` did not upper case `IconType.name`. (Pichu#0357)
- `Icon.__repr__` displayed incorrect names. (Zeref Draganeel#3524)
- Dupe client check was not working. (Zeref Draganeel#3524)

#### 1.1.63  *\[2021-04-11\]*

##### Public API:

- Rework `Slasher.do_main_sync` and rename to `.sync`,
- Slash commands now instant sync meanwhile added runtime. (Zeref Draganeel#3524)
- Add `ExtensionLoader.is_processing_extension`.

##### Internal:

- Speed up multi client dispatch event parsers.
- Add some new embed methods.
- Add sync-time slash command addition and removal detection and handling.
- Move slash extension's parts into different files to improve readability.
