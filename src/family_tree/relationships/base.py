from __future__ import annotations

from abc import ABC, abstractmethod

from family_tree.models.person import Person


class RelationshipResolver(ABC):
    @abstractmethod
    def resolve(self, person: Person) -> list[Person]:
        raise NotImplementedError
