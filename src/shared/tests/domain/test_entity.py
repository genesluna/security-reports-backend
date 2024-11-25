import uuid

from src.shared.domain.entity import Entity
from src.shared.domain.notification import Notification


class ConcreteEntity(Entity):
    def validate(self):
        pass


class TestConcreteEntity:
    def test_entity_creation(self):
        entity = ConcreteEntity()
        assert isinstance(entity.id, uuid.UUID)
        assert isinstance(entity.notification, Notification)

    def test_entity_equality(self):
        entity1 = ConcreteEntity()
        entity2 = ConcreteEntity()
        entity2.id = entity1.id
        assert entity1 == entity2

    def test_entity_inequality(self):
        entity1 = ConcreteEntity()
        entity2 = ConcreteEntity()
        assert entity1 != entity2

    def test_entity_validate(self):
        entity = ConcreteEntity()
        entity.validate()  # Should not raise NotImplementedError
