import vampytest

from ....bases import Icon, IconType

from ..user_base import UserBase


def test__UserBase__repr():
    """
    Tests whether ``UserBase.__repr__`` works as intended.
    """
    user_id = 202302030003
    avatar = Icon(IconType.static, 14)
    name = 'orin'
    
    user = UserBase._create_empty(user_id)
    vampytest.assert_instance(repr(user), str)

    user = UserBase(
        avatar = avatar,
        name = name,
    )
    vampytest.assert_instance(repr(user), str)


def test__UserBase__hash():
    """
    Tests whether ``UserBase.__hash__`` works as intended.
    """
    user_id = 202302030004
    avatar = Icon(IconType.static, 14)
    name = 'orin'
    
    user = UserBase._create_empty(user_id)
    vampytest.assert_instance(repr(user), str)

    user = UserBase(
        avatar = avatar,
        name = name,
    )
    vampytest.assert_instance(repr(user), str)


def test__UserBase__eq():
    """
    Tests whether ``UserBase.__eq__`` works as intended.
    """
    user_id = 202302030005
    
    avatar = Icon(IconType.static, 14)
    name = 'orin'
    
    keyword_parameters = {
        'avatar': avatar,
        'name': name,
    }
    
    user = UserBase(**keyword_parameters)
    vampytest.assert_eq(user, user)
    vampytest.assert_ne(user, object())

    test_user = UserBase._create_empty(user_id)
    vampytest.assert_eq(test_user, test_user)
    vampytest.assert_ne(user, test_user)
    
    for field_name, field_value in (
        ('avatar', None),
        ('name', 'okuu'),
    ):
        test_user = UserBase(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(user, test_user)


def test__UserBase__format():
    """
    Tests whether ``UserBase.__format__`` works as intended.
    
    Case: Shallow.
    """
    avatar = Icon(IconType.static, 14)
    name = 'orin'
    
    user = UserBase(
        avatar = avatar,
        name = name,
    )
    
    vampytest.assert_instance(format(user, ''), str)


def test__UserBase__sort():
    """
    Tests whether sorting ``UserBase` works as intended.
    """
    user_id_0 = 202302030006
    user_id_1 = 202302030007
    user_id_2 = 202302030008
    
    user_0 = UserBase._create_empty(user_id_0)
    user_1 = UserBase._create_empty(user_id_1)
    user_2 = UserBase._create_empty(user_id_2)
    
    to_sort = [
        user_1,
        user_2,
        user_0,
    ]
    
    expected_output = [
        user_0,
        user_1,
        user_2,
    ]
    
    vampytest.assert_eq(sorted(to_sort), expected_output)
