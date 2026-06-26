from __future__ import annotations

from family_tree.constants import (
    CHILD_ADDED,
    CHILD_ADDITION_FAILED,
    INVALID_COMMAND,
    PERSON_NOT_FOUND,
)
from family_tree.services.command_processor import CommandProcessor


def test_parses_add_child(processor: CommandProcessor) -> None:
    assert processor.process_line("ADD_CHILD Flora Minerva Female") == CHILD_ADDED


def test_parses_get_relationship(processor: CommandProcessor) -> None:
    assert processor.process_line("GET_RELATIONSHIP Lily Sister-In-Law") == "Darcy Alice"


def test_handles_blank_lines(processor: CommandProcessor) -> None:
    assert processor.process_line("   ") is None


def test_handles_invalid_commands(processor: CommandProcessor) -> None:
    assert processor.process_line("REMOVE_CHILD Flora Minerva") == INVALID_COMMAND
    assert processor.process_line("ADD_CHILD Flora Minerva") == INVALID_COMMAND


def test_handles_extra_spaces(processor: CommandProcessor) -> None:
    assert processor.process_line("  ADD_CHILD   Flora   Minerva   Female  ") == CHILD_ADDED


def test_process_lines_skips_blank_lines(processor: CommandProcessor) -> None:
    assert processor.process_lines(
        [
            "",
            "ADD_CHILD Ted Bella Female",
            "ADD_CHILD Luna Lola Female",
        ]
    ) == [CHILD_ADDITION_FAILED, PERSON_NOT_FOUND]
