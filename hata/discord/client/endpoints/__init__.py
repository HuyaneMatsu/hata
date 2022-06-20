from .achievement import *
from .application_command import *
from .channel import *
from .client import *
from .discovery import *
from .emoji import *
from .guild import *
from .interaction import *
from .integration import *
from .invite import *
from .locked import *
from .message import *
from .oauth2 import *
from .miscellaneous import *
from .reaction import *
from .role import *
from .scheduled_event import *
from .stage import *
from .sticker import *
from .thread import *
from .user import *
from .webhook import *

__all__ = (
    *achievement.__all__,
    *application_command.__all__,
    *channel.__all__,
    *client.__all__,
    *discovery.__all__,
    *emoji.__all__,
    *guild.__all__,
    *interaction.__all__,
    *integration.__all__,
    *invite.__all__,
    *locked.__all__,
    *message.__all__,
    *miscellaneous.__all__,
    *oauth2.__all__,
    *reaction.__all__,
    *role.__all__,
    *scheduled_event.__all__,
    *stage.__all__,
    *sticker.__all__,
    *thread.__all__,
    *user.__all__,
    *webhook.__all__,
)


from .achievement import AchievementEndpoints
from .application_command import ApplicationCommandEndpoints
from .channel import ChannelEndpoints
from .client import ClientEndpoints
from .discovery import DiscoveryEndpoints
from .emoji import EmojiEndpoints
from .guild import GuildEndpoints
from .interaction import InteractionEndpoints
from .integration import IntegrationEndpoints
from .invite import InviteEndpoints
from .locked import LockedEndpoints
from .message import MessageEndpoints
from .miscellaneous import MiscellaneousEndpoints
from .oauth2 import Oauth2Endpoints
from .reaction import ReactionEndpoints
from .role import RoleEndpoints
from .scheduled_event import ScheduledEventEndpoints
from .stage import StageEndpoints
from .sticker import StickerEndpoints
from .thread import ThreadEndpoints
from .user import UserEndpoints
from .webhook import WebhookEndpoints


ENDPOINT_COMPONENTS = (
    AchievementEndpoints,
    ApplicationCommandEndpoints,
    ChannelEndpoints,
    ClientEndpoints,
    DiscoveryEndpoints,
    EmojiEndpoints,
    GuildEndpoints,
    InteractionEndpoints,
    IntegrationEndpoints,
    InviteEndpoints,
    LockedEndpoints,
    MessageEndpoints,
    MiscellaneousEndpoints,
    Oauth2Endpoints,
    ReactionEndpoints,
    RoleEndpoints,
    ScheduledEventEndpoints,
    StageEndpoints,
    StickerEndpoints,
    ThreadEndpoints,
    UserEndpoints,
    WebhookEndpoints,
)
