import vampytest

from .. import AutoModerationAction, AutoModerationActionType, SendAlertMessageActionMetadata, TimeoutActionMetadata


def test__AutoModerationAction__from_data__block_message():
    """
    Tests whether the auto moderation action's `from_data` method works.
    """
    action = AutoModerationAction.from_data({
        'type': AutoModerationActionType.block_message.value,
        'metadata': {},
    })
    
    vampytest.assert_instance(action, AutoModerationAction)
    vampytest.assert_is(action.type, AutoModerationActionType.block_message)
    vampytest.assert_is(action.metadata, None)


def test__AutoModerationAction__from_data__send_alert_message():
    """
    Tests whether the auto moderation action's `from_data` method works.
    """
    action = AutoModerationAction.from_data({
        'type': AutoModerationActionType.send_alert_message.value,
        'metadata': {
            'channel_id': '0',
        },
    })
    
    vampytest.assert_instance(action, AutoModerationAction)
    vampytest.assert_is(action.type, AutoModerationActionType.send_alert_message)
    vampytest.assert_instance(action.metadata, SendAlertMessageActionMetadata)


def test__AutoModerationAction__from_data__timeout():
    """
    Tests whether the auto moderation action's `from_data` method works.
    """
    action = AutoModerationAction.from_data({
        'type': AutoModerationActionType.timeout.value,
        'metadata': {
            'duration_seconds': 0,
        },
    })
    
    vampytest.assert_instance(action, AutoModerationAction)
    vampytest.assert_is(action.type, AutoModerationActionType.timeout)
    vampytest.assert_instance(action.metadata, TimeoutActionMetadata)


def test__AutoModerationAction__to_data__block_message():
    """
    Tests whether the auto moderation action's `to_data` method works.
    """
    action = AutoModerationAction(AutoModerationActionType.block_message)
    
    vampytest.assert_eq(
        action.to_data(),
        {
            'type': AutoModerationActionType.block_message.value,
            'metadata': {},
        }
    )


def test__AutoModerationAction__to_data__send_alert_message():
    """
    Tests whether the auto moderation action's `to_data` method works.
    """
    action = AutoModerationAction(channel=0)
    
    vampytest.assert_eq(
        action.to_data(),
        {
            'type': AutoModerationActionType.send_alert_message.value,
            'metadata': {
                'channel_id': 0,
            },
        }
    )


def test__AutoModerationAction__to_data__timeout():
    """
    Tests whether the auto moderation action's `to_data` method works.
    """
    action = AutoModerationAction(duration=0)
    
    vampytest.assert_eq(
        action.to_data(),
        {
            'type': AutoModerationActionType.timeout.value,
            'metadata': {
                'duration_seconds': 0,
            },
        }
    )
