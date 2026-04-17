from .application import *
from .application_command import *
from .application_role_connection import *
from .auto_moderation import *
from .channel import *
from .client import *
from .client_gateway import *
from .discovery import *
from .emoji_application import *
from .emoji_guild import *
from .guild import *
from .guild_ban import *
from .interaction import *
from .integration import *
from .invite import *
from .locked import *
from .message import *
from .oauth2 import *
from .miscellaneous import *
from .poll import *
from .reaction import *
from .role import *
from .scheduled_event import *
from .soundboard import *
from .stage import *
from .sticker import *
from .thread import *
from .user import *
from .webhook import *


__all__ = (
    *application.__all__,
    *application_command.__all__,
    *application_role_connection.__all__,
    *auto_moderation.__all__,
    *channel.__all__,
    *client.__all__,
    *client_gateway.__all__,
    *discovery.__all__,
    *emoji_application.__all__,
    *emoji_guild.__all__,
    *guild.__all__,
    *guild_ban.__all__,
    *interaction.__all__,
    *integration.__all__,
    *invite.__all__,
    *locked.__all__,
    *message.__all__,
    *miscellaneous.__all__,
    *oauth2.__all__,
    *poll.__all__,
    *reaction.__all__,
    *role.__all__,
    *scheduled_event.__all__,
    *soundboard.__all__,
    *stage.__all__,
    *sticker.__all__,
    *thread.__all__,
    *user.__all__,
    *webhook.__all__,
)


from .application import ClientCompoundApplicationEndpoints
from .application_command import ClientCompoundApplicationCommandEndpoints
from .application_role_connection import ClientCompoundApplicationRoleConnectionEndpoints
from .auto_moderation import ClientCompoundAutoModerationEndpoints
from .channel import ClientCompoundChannelEndpoints
from .client import ClientCompoundClientEndpoints
from .client_gateway import ClientCompoundClientGateway
from .discovery import ClientCompoundDiscoveryEndpoints
from .emoji_application import ClientCompoundEmojiApplicationEndpoints
from .emoji_guild import ClientCompoundEmojiGuildEndpoints
from .guild import ClientCompoundGuildEndpoints
from .guild_ban import ClientCompoundGuildBanEndpoints
from .interaction import ClientCompoundInteractionEndpoints
from .integration import ClientCompoundIntegrationEndpoints
from .invite import ClientCompoundInviteEndpoints
from .locked import ClientCompoundLockedEndpoints
from .message import ClientCompoundMessageEndpoints
from .miscellaneous import ClientCompoundMiscellaneousEndpoints
from .oauth2 import ClientCompoundOauth2Endpoints
from .poll import ClientCompoundPollEndpoints
from .reaction import ClientCompoundReactionEndpoints
from .role import ClientCompoundRoleEndpoints
from .scheduled_event import ClientCompoundScheduledEventEndpoints
from .soundboard import ClientCompoundSoundBoardEndpoints
from .stage import ClientCompoundStageEndpoints
from .sticker import ClientCompoundStickerEndpoints
from .thread import ClientCompoundThreadEndpoints
from .user import ClientCompoundUserEndpoints
from .webhook import ClientCompoundWebhookEndpoints


CLIENT_COMPOUNDS = (
    ClientCompoundApplicationEndpoints,
    ClientCompoundApplicationCommandEndpoints,
    ClientCompoundApplicationRoleConnectionEndpoints,
    ClientCompoundAutoModerationEndpoints,
    ClientCompoundChannelEndpoints,
    ClientCompoundClientEndpoints,
    ClientCompoundClientGateway,
    ClientCompoundDiscoveryEndpoints,
    ClientCompoundEmojiApplicationEndpoints,
    ClientCompoundEmojiGuildEndpoints,
    ClientCompoundGuildEndpoints,
    ClientCompoundGuildBanEndpoints,
    ClientCompoundInteractionEndpoints,
    ClientCompoundIntegrationEndpoints,
    ClientCompoundInviteEndpoints,
    ClientCompoundLockedEndpoints,
    ClientCompoundMessageEndpoints,
    ClientCompoundMiscellaneousEndpoints,
    ClientCompoundOauth2Endpoints,
    ClientCompoundPollEndpoints,
    ClientCompoundReactionEndpoints,
    ClientCompoundRoleEndpoints,
    ClientCompoundScheduledEventEndpoints,
    ClientCompoundSoundBoardEndpoints,
    ClientCompoundStageEndpoints,
    ClientCompoundStickerEndpoints,
    ClientCompoundThreadEndpoints,
    ClientCompoundUserEndpoints,
    ClientCompoundWebhookEndpoints,
)
