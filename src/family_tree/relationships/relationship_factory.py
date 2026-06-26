from __future__ import annotations

from family_tree.relationships.base import RelationshipResolver
from family_tree.relationships.brother_in_law_resolver import BrotherInLawResolver
from family_tree.relationships.daughter_resolver import DaughterResolver
from family_tree.relationships.maternal_aunt_resolver import MaternalAuntResolver
from family_tree.relationships.maternal_uncle_resolver import MaternalUncleResolver
from family_tree.relationships.paternal_aunt_resolver import PaternalAuntResolver
from family_tree.relationships.paternal_uncle_resolver import PaternalUncleResolver
from family_tree.relationships.sibling_resolver import SiblingResolver
from family_tree.relationships.sister_in_law_resolver import SisterInLawResolver
from family_tree.relationships.son_resolver import SonResolver


class RelationshipFactory:
    def __init__(self) -> None:
        self._resolvers: dict[str, RelationshipResolver] = {
            "Siblings": SiblingResolver(),
            "Son": SonResolver(),
            "Daughter": DaughterResolver(),
            "Paternal-Uncle": PaternalUncleResolver(),
            "Maternal-Uncle": MaternalUncleResolver(),
            "Paternal-Aunt": PaternalAuntResolver(),
            "Maternal-Aunt": MaternalAuntResolver(),
            "Sister-In-Law": SisterInLawResolver(),
            "Brother-In-Law": BrotherInLawResolver(),
        }

    def get_resolver(self, relationship: str) -> RelationshipResolver | None:
        return self._resolvers.get(relationship)
