from __future__ import annotations

from family_tree.models.person import Person
from family_tree.relationships.base import RelationshipResolver
from family_tree.relationships.common import siblings_of


class SiblingResolver(RelationshipResolver):
    def resolve(self, person: Person) -> list[Person]:
        return siblings_of(person)
