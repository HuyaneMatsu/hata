from .embedded_activity_configuration import *
from .fields import *
from .preinstanced import *


__all__ = (
    *embedded_activity_configuration.__all__,
    *fields.__all__,
    *preinstanced.__all__,
)


# Structure as in 2023-11-28:
#
#
# tp EmbeddedActivityConfiguration : Object
#     activity_preview_video_asset_id : null | String # 0-9 # rename to preview_video_asset_id
#     supported_platforms : list<PlatformType> # we can ignore this, we already got client_platform_config
#     default_orientation_lock_state : OrientationLockState
#     tablet_default_orientation_lock_state : OrientationLockState # rename to default_tablet_orientation_lock_state
#     requires_age_gate : bool # rename to age_gated
#     premium_tier_requirement : null # probably not used anymore
#     free_period_starts_at : null | DateTime # probably not used anymore
#     free_period_ends_at : null | DateTime # probably not used anymore
#     client_platform_config : null | Dictionary<PlatformType, ClientPlatformConfiguration> # rename to client_platform_configurations
#     shelf_rank : Integer # rename to position
#     has_csp_exception : Boolean # always false | csp = Content Security Policy | if true -> developers may see your ip # rename to content_security_policy_exceptions_exists
#     instance_mode : Enum<Integer<0>> # no results -> not yet used perhaps?
#
#
# tp ClientPlatformConfiguration : Object
#     label_type : LabelType
#     label_until : null | DateTime # rename to labelled_until
#     release_phase : ReleasePhase # Not used
#
#
# tp ReleasePhase : Enum<String>
#     GLOBAL_LAUNCH = "global_launch"
#
#     fn __default__(type) -> type.GLOBAL_LAUNCH
#
#
# tp LabelType : Enum<Integer>
#     NONE = 0
#     NEW = 1
#     UPDATED = 2
#
#
# tp OrientationLockState : Enum<Integer>
#     NONE = 0
#     UNLOCKED = 1
#     PORTRAIT = 2
#     LANDSCAPE = 3
#
#
# tp PlatformType : Enum<String>
#     ANDROID = "android"
#     IOS = "ios"
#     WEB = "web"
#
#     fn __default__(type) -> type.WEB
