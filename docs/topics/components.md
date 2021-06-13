# Components

### Introduction

Components, mainly known as buttons are interactive gui elements, which might be included with messages.

Hata supports components on native ways as well, but this topic is a continuation of the [slash](slash.md) one.

## Component Structures

Components can be passed to `InteractionResponse` and to many client methods as well:

- `.message_create`
- `.message_edit`
- `.interaction_response_message_create`
- `.interaction_response_message_edit`
- `.interaction_followup_message_create`
- `.interaction_followup_message_edit`
- `.interaction_component_message_edit`

3 component types are supported, `Row`, `Button` and `Select`. However select is not yet released (not really useful
either), so we will ignore it for now.

`components` parameters can be either as the component itself, list of components, or as a nested list of components.
Some examples might clarify it more.

First start with the 1 row, 3 buttons next to each other cases.

```py
# The component itself
components = Row(Button(...), Button(...), Button(...))

# List of components.
components = [
    Row(Button(...), Button(...), Button(...)),
]

# Nexted list of components.
components = [
    [Button(...), Button(...), Button(...)],
]
```

Then, 3 row, 1 button in each example:

```py

# List of components
components = [
    Row(Button(...)),
    Row(Button(...)),
    Row(Button(...)),
]

# List of components with skipping rows.
components = [
    Button(...),
    Button(...),
    Button(...),
]

# Nested list of  components
components = [
    [Button(...)],
    [Button(...)],
    [Button(...)],
]
```

## Limitations

- Row limit is `5`.
- Up to `5` buttons can be in a row.
- Component `label` can be `80` characters long.
- `custom_id` can be `100` character long.

###### Select limitations

- Up to `1` select can be in a row.
- A select can have `25` choices.
- A select can have choices in range `[1:25]`.
- Select `min_values` can be in range `[1:15]`.
- Select `max_values` can be in range `[1:25]`.

> TODO
