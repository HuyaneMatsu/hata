#### 1.1.66  *\[2021-04-??\]*

#### 1.1.65  *\[2021-04-14\]*

##### Internal:

- Fix some spacing. (sleep-cult#3040)
- `ActivityFlag` now use lower case flag names.
- Create `urls.py` from `http.URLS` module.
- Fix type `MAX_RERP_ELEMENT_LIMIT` -> `MAX_REPR_ELEMENT_LIMIT`.
- Move json conversion to backend.
- `CommandState._try_purge_from_changes` returned values in bad order. (Zeref Draganeel#3524)
- `CommandState._try_purge` returned values in bad order. (Zeref Draganeel#3524)
- Fix an `AttributeError` in `User._from_client`. (Zeref Draganeel#3524)
- Add lazy interaction choice definition. (Zeref Draganeel#3524)

#### 1.1.64  *\[2021-04-12\]*

##### Public API:

`CLIENTS` now uses `dict` type instead of `ClientDictionary`.

##### Internal:

- `Client._delete` could construct not a fully built `User` object. Add `User._from_client` to fix this.
- Remove `ClientDictionary`.
- Speed up `dict.get` by passing default value.
- Fix some bad assignments in `Client._delete`.
- `Icon.__repr__` did not upper case `IconType.name`. (Pichu#0357)
- `Icon.__repr__` displayed incorrect names. (Zeref Draganeel#3524)
- Dupe client check was not working. (Zeref Draganeel#3524)
- Fix reading readme issue on windows. (Zeref Draganeel#3524)
- Fix a `TypeError` in `User._update_presence`. (from 1.1.63)
- `EventWaitforMeta._call_channel_edit` passed bad args to guild waiters.
- Fix a `NameError` in `EventLoop.create_datagram_endpoint`. (Charlotte|💻⭐#5644)
- Fix a `NameError` in `cr_pg_channel_object`. (Charlotte|💻⭐#5644)
- Fix a `NameError` in `Client.request_members`. (Charlotte|💻⭐#5644)
- Fix a `NameError` in `Client.message_create`. (Charlotte|💻⭐#5644)
- Fix a `NameError` in `Client.interaction_followup_message_edit`. (Charlotte|💻⭐#5644)
- Fix a `NameError` in `Client.interaction_followup_message_create`. (Charlotte|💻⭐#5644)
- Fix a `NameError` in `Client.interaction_response_message_edit`. (Charlotte|💻⭐#5644)
- Fix a `NameError` in `Client.interaction_response_message_create`. (Charlotte|💻⭐#5644)
- Fix a `NameError` in `Client.webhook_message_edit`. (Charlotte|💻⭐#5644)
- Fix a `NameError` in `Client.webhook_message_create`. (Charlotte|💻⭐#5644)
- Fix a `NameError` in `Client.message_edit`. (Charlotte|💻⭐#5644)
- Fix a `NameError` in `Client.permission_overwrite_edit`. (Charlotte|💻⭐#5644)
- Fix a `NameError` in `ApplicationCommandOption.add_option`. (Charlotte|💻⭐#5644)
- Fix a `TypeError` in `Client.interaction_response_message_edit`. (Charlotte|💻⭐#5644)
- Fix a `NameError` in `Client.guild_edit`. (Charlotte|💻⭐#5644)
- Fix a `NameError` in `Client.channel_edit`. (Charlotte|💻⭐#5644)
- Fix a `NameError` in `Client.guild_user_add`. (Charlotte|💻⭐#5644)

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
