from hata import Client

# Annotating client will help your IDE with linting/inspection (it won't not derp out).
Sakuya: Client


@Sakuya.commands(aliases='*')
async def multiply(first:int, second:int):
    """Multiplies the two numbers."""
    return first * second
