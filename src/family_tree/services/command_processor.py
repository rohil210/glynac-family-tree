from __future__ import annotations

from family_tree.constants import ADD_CHILD_COMMAND, GET_RELATIONSHIP_COMMAND, INVALID_COMMAND
from family_tree.services.family_tree_service import FamilyTreeService


class CommandProcessor:
    def __init__(self, family_tree_service: FamilyTreeService) -> None:
        self._family_tree_service = family_tree_service

    def process_line(self, line: str) -> str | None:
        tokens = line.strip().split()
        if not tokens:
            return None

        command = tokens[0]
        if command == ADD_CHILD_COMMAND and len(tokens) == 4:
            return self._family_tree_service.add_child(tokens[1], tokens[2], tokens[3])
        if command == GET_RELATIONSHIP_COMMAND and len(tokens) == 3:
            return self._family_tree_service.get_relationship(tokens[1], tokens[2])
        return INVALID_COMMAND

    def process_lines(self, lines: list[str]) -> list[str]:
        outputs: list[str] = []
        for line in lines:
            output = self.process_line(line)
            if output is not None:
                outputs.append(output)
        return outputs
