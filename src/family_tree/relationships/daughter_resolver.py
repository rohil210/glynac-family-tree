from __future__ import annotations

from family_tree.models.person import Person
from family_tree.relationships.base import RelationshipResolver


class DaughterResolver(RelationshipResolver):
    def resolve(self, person: Person) -> list[Person]:
        return [child for child in person.children if child.is_female()]
