from ....http import DiscordApiClient


class TestDiscordApiClient(DiscordApiClient):
    __slots__ = ('__dict__',)
    
    async def discord_request(self, handler, method, url, data = None, params = None, headers = None, reason = None):
        raise RuntimeError('Real request during testing.')
