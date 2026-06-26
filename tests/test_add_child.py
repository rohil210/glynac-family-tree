from __future__ import annotations

from family_tree.constants import (
    CHILD_ADDED,
    CHILD_ADDITION_FAILED,
    INVALID_GENDER,
    PERSON_NOT_FOUND,
)
from family_tree.repository.family_repository import FamilyRepository
from family_tree.services.family_tree_service import FamilyTreeService


def test_adds_child_successfully_through_valid_mother(
    service: FamilyTreeService, repository: FamilyRepository
) -> None:
    assert service.add_child("Flora", "Minerva", "Female") == CHILD_ADDED
    minerva = repository.get_person("Minerva")
    flora = repository.get_person("Flora")

    assert minerva is not None
    assert minerva.mother is flora
    assert minerva in flora.children  # type: ignore[union-attr]


def test_fails_when_mother_not_found(service: FamilyTreeService) -> None:
    assert service.add_child("Luna", "Lola", "Female") == PERSON_NOT_FOUND


def test_fails_when_parent_is_male(service: FamilyTreeService) -> None:
    assert service.add_child("Ted", "Bella", "Female") == CHILD_ADDITION_FAILED


def test_fails_for_duplicate_child_name(service: FamilyTreeService) -> None:
    assert service.add_child("Flora", "Victoire", "Female") == CHILD_ADDITION_FAILED


def test_adds_child_in_correct_order(
    service: FamilyTreeService, repository: FamilyRepository
) -> None:
    assert service.add_child("Flora", "Minerva", "Female") == CHILD_ADDED
    flora = repository.get_person("Flora")

    assert [child.name for child in flora.children] == [  # type: ignore[union-attr]
        "Victoire",
        "Dominique",
        "Louis",
        "Minerva",
    ]


def test_adds_father_reference_if_mother_has_spouse(
    service: FamilyTreeService, repository: FamilyRepository
) -> None:
    assert service.add_child("Flora", "Minerva", "Female") == CHILD_ADDED
    minerva = repository.get_person("Minerva")
    bill = repository.get_person("Bill")

    assert minerva is not None
    assert minerva.father is bill
    assert minerva in bill.children  # type: ignore[union-attr]


def test_invalid_gender(service: FamilyTreeService) -> None:
    assert service.add_child("Flora", "Minerva", "Unknown") == INVALID_GENDER
