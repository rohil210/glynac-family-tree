from __future__ import annotations

from family_tree.models.person import Person


class FamilyRepository:
    def __init__(self) -> None:
        self._people: dict[str, Person] = {}

    def add_person(self, person: Person) -> bool:
        if self.exists(person.name):
            return False
        self._people[person.name] = person
        return True

    def get_person(self, name: str) -> Person | None:
        return self._people.get(name)

    def exists(self, name: str) -> bool:
        return name in self._people

    def add_marriage(self, person1_name: str, person2_name: str) -> bool:
        person1 = self.get_person(person1_name)
        person2 = self.get_person(person2_name)
        if person1 is None or person2 is None:
            return False
        person1.set_spouse(person2)
        return True

    def all_people(self) -> list[Person]:
        return list(self._people.values())
