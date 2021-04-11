

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
