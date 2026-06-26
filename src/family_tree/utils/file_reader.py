from __future__ import annotations

from pathlib import Path


class FileReader:
    def read_lines(self, file_path: str) -> list[str]:
        path = Path(file_path)
        return path.read_text(encoding="utf-8").splitlines()
