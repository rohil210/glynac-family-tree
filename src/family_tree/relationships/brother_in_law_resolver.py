from __future__ import annotations

from family_tree.models.person import Person
from family_tree.relationships.base import RelationshipResolver
from family_tree.relationships.common import siblings_of, unique_in_order


class BrotherInLawResolver(RelationshipResolver):
    def resolve(self, person: Person) -> list[Person]:
        relatives: list[Person] = []
        if person.spouse is not None:
            relatives.extend(
                sibling for sibling in siblings_of(person.spouse) if sibling.is_male()
            )

        for sibling in siblings_of(person):
            if sibling.spouse is not None and sibling.spouse.is_male():
                relatives.append(sibling.spouse)

        return unique_in_order(relatives)
