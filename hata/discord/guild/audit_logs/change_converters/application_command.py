__all__ = ()


from .shared import convert_snowflake


def convert_application_command_id(name, data):
    return convert_snowflake('application_command_id', data)


APPLICATION_COMMAND_CONVERTERS = {
    'command_id': convert_application_command_id,
}
