from __future__ import annotations

from family_tree.constants import (
    CHILD_ADDED,
    CHILD_ADDITION_FAILED,
    INVALID_GENDER,
    INVALID_RELATIONSHIP,
    NONE,
    PERSON_NOT_FOUND,
)
from family_tree.enums import Gender
from family_tree.models.person import Person
from family_tree.relationships.relationship_factory import RelationshipFactory
from family_tree.repository.family_repository import FamilyRepository


class FamilyTreeService:
    def __init__(
        self,
        repository: FamilyRepository,
        relationship_factory: RelationshipFactory | None = None,
    ) -> None:
        self._repository = repository
        self._relationship_factory = relationship_factory or RelationshipFactory()

    def add_child(self, mother_name: str, child_name: str, gender_value: str) -> str:
        mother = self._repository.get_person(mother_name)
        if mother is None:
            return PERSON_NOT_FOUND

        if not mother.is_female() or self._repository.exists(child_name):
            return CHILD_ADDITION_FAILED

        gender = Gender.from_string(gender_value)
        if gender is None:
            return INVALID_GENDER

        child = Person(name=child_name, gender=gender, mother=mother, father=mother.spouse)
        if not self._repository.add_person(child):
            return CHILD_ADDITION_FAILED

        mother.add_child(child)
        if mother.spouse is not None:
            mother.spouse.add_child(child)
        return CHILD_ADDED

    def get_relationship(self, name: str, relationship: str) -> str:
        person = self._repository.get_person(name)
        if person is None:
            return PERSON_NOT_FOUND

        resolver = self._relationship_factory.get_resolver(relationship)
        if resolver is None:
            return INVALID_RELATIONSHIP

        relatives = resolver.resolve(person)
        if not relatives:
            return NONE
        return " ".join(relative.name for relative in relatives)
