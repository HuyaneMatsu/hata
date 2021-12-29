try:
    import dotenv
except ModuleNotFoundError as err:
    raise ImportError(
        'The extension requires `dotenv` package.'
    ) from err
