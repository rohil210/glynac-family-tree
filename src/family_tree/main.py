from __future__ import annotations

import sys

from family_tree.bootstrap.family_initializer import FamilyInitializer
from family_tree.constants import INVALID_COMMAND
from family_tree.services.command_processor import CommandProcessor
from family_tree.services.family_tree_service import FamilyTreeService
from family_tree.utils.file_reader import FileReader


def run(input_file_path: str) -> list[str]:
    repository = FamilyInitializer().initialize()
    service = FamilyTreeService(repository)
    processor = CommandProcessor(service)
    lines = FileReader().read_lines(input_file_path)
    return processor.process_lines(lines)


def main() -> None:
    if len(sys.argv) != 2:
        print(INVALID_COMMAND)
        return

    try:
        outputs = run(sys.argv[1])
    except (FileNotFoundError, IsADirectoryError, OSError):
        print(INVALID_COMMAND)
        return

    for output in outputs:
        print(output)


if __name__ == "__main__":
    main()
