from __future__ import annotations

from family_tree.enums import Gender
from family_tree.models.person import Person
from family_tree.repository.family_repository import FamilyRepository


class FamilyInitializer:
    def initialize(self) -> FamilyRepository:
        repository = FamilyRepository()

        self._add_people(
            repository,
            [
                ("King Arthur", Gender.MALE),
                ("Queen Margaret", Gender.FEMALE),
                ("Flora", Gender.FEMALE),
                ("Ted", Gender.MALE),
                ("Audrey", Gender.FEMALE),
                ("Helen", Gender.FEMALE),
                ("Malfoy", Gender.MALE),
                ("Harry", Gender.MALE),
                ("Darcy", Gender.FEMALE),
                ("Alice", Gender.FEMALE),
            ],
        )

        self._marry(repository, "King Arthur", "Queen Margaret")
        self._add_children(
            repository,
            "Queen Margaret",
            [
                ("Bill", Gender.MALE),
                ("Charlie", Gender.MALE),
                ("Percy", Gender.MALE),
                ("Ronald", Gender.MALE),
                ("Ginerva", Gender.FEMALE),
            ],
        )

        self._marry(repository, "Bill", "Flora")
        self._add_children(
            repository,
            "Flora",
            [
                ("Victoire", Gender.FEMALE),
                ("Dominique", Gender.FEMALE),
                ("Louis", Gender.MALE),
            ],
        )

        self._marry(repository, "Victoire", "Ted")
        self._add_child(repository, "Victoire", "Remus", Gender.MALE)

        self._marry(repository, "Percy", "Audrey")
        self._add_children(
            repository,
            "Audrey",
            [("Molly", Gender.FEMALE), ("Lucy", Gender.FEMALE)],
        )

        self._marry(repository, "Ronald", "Helen")
        self._add_children(
            repository,
            "Helen",
            [("Rose", Gender.FEMALE), ("Hugo", Gender.MALE)],
        )

        self._marry(repository, "Rose", "Malfoy")
        self._add_children(
            repository,
            "Rose",
            [("Draco", Gender.MALE), ("Aster", Gender.FEMALE)],
        )

        self._marry(repository, "Ginerva", "Harry")
        self._add_children(
            repository,
            "Ginerva",
            [
                ("James", Gender.MALE),
                ("Albus", Gender.MALE),
                ("Lily", Gender.FEMALE),
            ],
        )

        self._marry(repository, "James", "Darcy")
        self._add_child(repository, "Darcy", "William", Gender.MALE)

        self._marry(repository, "Albus", "Alice")
        self._add_children(
            repository,
            "Alice",
            [("Ron", Gender.MALE), ("Ginny", Gender.FEMALE)],
        )

        return repository

    def _add_people(
        self, repository: FamilyRepository, people: list[tuple[str, Gender]]
    ) -> None:
        for name, gender in people:
            repository.add_person(Person(name=name, gender=gender))

    def _marry(self, repository: FamilyRepository, person1_name: str, person2_name: str) -> None:
        repository.add_marriage(person1_name, person2_name)

    def _add_children(
        self,
        repository: FamilyRepository,
        mother_name: str,
        children: list[tuple[str, Gender]],
    ) -> None:
        for child_name, gender in children:
            self._add_child(repository, mother_name, child_name, gender)

    def _add_child(
        self,
        repository: FamilyRepository,
        mother_name: str,
        child_name: str,
        gender: Gender,
    ) -> None:
        mother = repository.get_person(mother_name)
        if mother is None:
            raise ValueError(f"Mother not found: {mother_name}")
        child = Person(name=child_name, gender=gender, mother=mother, father=mother.spouse)
        repository.add_person(child)
        mother.add_child(child)
        if mother.spouse is not None:
            mother.spouse.add_child(child)
