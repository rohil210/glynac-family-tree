from __future__ import annotations

from family_tree.models.person import Person


def unique_in_order(people: list[Person]) -> list[Person]:
    seen: set[str] = set()
    unique_people: list[Person] = []
    for person in people:
        if person.name not in seen:
            unique_people.append(person)
            seen.add(person.name)
    return unique_people


def siblings_of(person: Person) -> list[Person]:
    source_parent = person.mother or person.father
    if source_parent is None:
        return []
    return [child for child in source_parent.children if child is not person]
