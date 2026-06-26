from __future__ import annotations

import pytest

from family_tree.bootstrap.family_initializer import FamilyInitializer
from family_tree.repository.family_repository import FamilyRepository
from family_tree.services.command_processor import CommandProcessor
from family_tree.services.family_tree_service import FamilyTreeService


@pytest.fixture
def repository() -> FamilyRepository:
    return FamilyInitializer().initialize()


@pytest.fixture
def service(repository: FamilyRepository) -> FamilyTreeService:
    return FamilyTreeService(repository)


@pytest.fixture
def processor(service: FamilyTreeService) -> CommandProcessor:
    return CommandProcessor(service)
