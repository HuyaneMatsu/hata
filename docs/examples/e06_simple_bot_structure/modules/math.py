from hata import Client

# Annotating `Sakuya` might helps your IDE to not derp out completely.
Sakuya: Client

@Sakuya.commands(aliases='*')
async def multiply(first:int, second:int):
    """Multiplies the two numbers."""
    return first*second
