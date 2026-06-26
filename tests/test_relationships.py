from __future__ import annotations

from family_tree.constants import INVALID_RELATIONSHIP, NONE, PERSON_NOT_FOUND
from family_tree.services.family_tree_service import FamilyTreeService


def test_siblings(service: FamilyTreeService) -> None:
    assert service.get_relationship("Lily", "Siblings") == "James Albus"


def test_son(service: FamilyTreeService) -> None:
    assert service.get_relationship("Ginerva", "Son") == "James Albus"


def test_daughter(service: FamilyTreeService) -> None:
    assert service.get_relationship("Ginerva", "Daughter") == "Lily"


def test_paternal_uncle(service: FamilyTreeService) -> None:
    assert service.get_relationship("William", "Paternal-Uncle") == "Albus"


def test_maternal_uncle(service: FamilyTreeService) -> None:
    assert service.get_relationship("Remus", "Maternal-Uncle") == "Louis"


def test_paternal_aunt(service: FamilyTreeService) -> None:
    assert service.get_relationship("William", "Paternal-Aunt") == "Lily"


def test_maternal_aunt(service: FamilyTreeService) -> None:
    service.add_child("Flora", "Minerva", "Female")

    assert service.get_relationship("Remus", "Maternal-Aunt") == "Dominique Minerva"


def test_sister_in_law(service: FamilyTreeService) -> None:
    assert service.get_relationship("Lily", "Sister-In-Law") == "Darcy Alice"


def test_brother_in_law(service: FamilyTreeService) -> None:
    assert service.get_relationship("Darcy", "Brother-In-Law") == "Albus"


def test_person_not_found(service: FamilyTreeService) -> None:
    assert service.get_relationship("Unknown", "Siblings") == PERSON_NOT_FOUND


def test_relationship_returns_none(service: FamilyTreeService) -> None:
    assert service.get_relationship("Remus", "Siblings") == NONE


def test_invalid_relationship(service: FamilyTreeService) -> None:
    assert service.get_relationship("Remus", "Cousin") == INVALID_RELATIONSHIP
