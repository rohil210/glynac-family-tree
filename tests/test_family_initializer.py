from __future__ import annotations

from family_tree.repository.family_repository import FamilyRepository


EXPECTED_PEOPLE = {
    "King Arthur",
    "Queen Margaret",
    "Bill",
    "Charlie",
    "Percy",
    "Ronald",
    "Ginerva",
    "Flora",
    "Victoire",
    "Dominique",
    "Louis",
    "Ted",
    "Remus",
    "Audrey",
    "Molly",
    "Lucy",
    "Helen",
    "Rose",
    "Hugo",
    "Malfoy",
    "Draco",
    "Aster",
    "Harry",
    "James",
    "Albus",
    "Lily",
    "Darcy",
    "William",
    "Alice",
    "Ron",
    "Ginny",
}


def test_initial_tree_contains_all_expected_people(repository: FamilyRepository) -> None:
    assert {person.name for person in repository.all_people()} == EXPECTED_PEOPLE


def test_spouses_are_linked_correctly(repository: FamilyRepository) -> None:
    bill = repository.get_person("Bill")
    flora = repository.get_person("Flora")
    james = repository.get_person("James")
    darcy = repository.get_person("Darcy")

    assert bill is not None and flora is not None
    assert james is not None and darcy is not None
    assert bill.spouse is flora
    assert flora.spouse is bill
    assert james.spouse is darcy
    assert darcy.spouse is james


def test_children_are_linked_correctly(repository: FamilyRepository) -> None:
    flora = repository.get_person("Flora")
    bill = repository.get_person("Bill")
    victoire = repository.get_person("Victoire")

    assert flora is not None and bill is not None and victoire is not None
    assert [child.name for child in flora.children] == ["Victoire", "Dominique", "Louis"]
    assert [child.name for child in bill.children] == ["Victoire", "Dominique", "Louis"]
    assert victoire.mother is flora
    assert victoire.father is bill
