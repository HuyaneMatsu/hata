from datetime import datetime as DateTime

import vampytest

from ....utils import id_to_datetime

from ..entity_base import DiscordEntity


class TestEntityType(DiscordEntity):
    def __new__(cls, entity_id):
        self = object.__new__(cls)
        self.id = entity_id
        return self


def test__DiscordEntity__id():
    """
    Tests whether ``DiscordEntity.id`` works as intended.
    """
    entity = DiscordEntity()
    
    entity_id = entity.id
    
    vampytest.assert_instance(entity_id, int)
    vampytest.assert_eq(entity_id, 0)


def test__DiscordEntity__created_at():
    """
    Tests whether ``DiscordEntity.created_at`` works as intended.
    """
    entity_id = 202502280000_000000
    entity = TestEntityType(entity_id)
    
    output = entity.created_at
    
    vampytest.assert_instance(output, DateTime)
    vampytest.assert_eq(output, id_to_datetime(entity_id))


def test__DiscordEntity__hash():
    """
    Tests whether ``DiscordEntity.__hash__`` works as intended.
    """
    entity_id = 202502280001
    entity = TestEntityType(entity_id)
    
    output = hash(entity)
    
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, entity_id)


def test__DiscordEntity__ordering():
    """
    Tests whether ``DiscordEntity`` ordering works as intended.
    """
    entity_id_0 = 202502280002
    entity_id_1 = 202502280003
    entity_id_2 = 202502280004
    
    entity_0 = TestEntityType(entity_id_0)
    entity_1 = TestEntityType(entity_id_1)
    entity_2 = TestEntityType(entity_id_2)
    
    to_sort = [
        entity_0,
        entity_1,
        entity_2,
        entity_2,
        entity_1,
        entity_0,
    ]
    
    to_sort.sort()
    
    vampytest.assert_eq(
        to_sort,
        [
            entity_0,
            entity_0,
            entity_1,
            entity_1,
            entity_2,
            entity_2,
        ],
    )
