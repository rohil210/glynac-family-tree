from __future__ import annotations

from family_tree.models.person import Person
from family_tree.relationships.base import RelationshipResolver
from family_tree.relationships.common import siblings_of


class MaternalAuntResolver(RelationshipResolver):
    def resolve(self, person: Person) -> list[Person]:
        if person.mother is None:
            return []
        return [sibling for sibling in siblings_of(person.mother) if sibling.is_female()]
