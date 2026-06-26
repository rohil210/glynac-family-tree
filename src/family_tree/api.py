from __future__ import annotations

from threading import Lock
from typing import Any

from flask import Flask, jsonify, redirect, render_template, request, url_for

from family_tree.bootstrap.family_initializer import FamilyInitializer
from family_tree.services.command_processor import CommandProcessor
from family_tree.services.family_tree_service import FamilyTreeService


SUPPORTED_RELATIONSHIPS = [
    "Siblings",
    "Son",
    "Daughter",
    "Paternal-Uncle",
    "Maternal-Uncle",
    "Paternal-Aunt",
    "Maternal-Aunt",
    "Sister-In-Law",
    "Brother-In-Law",
]


class FamilyTreeApplication:
    def __init__(self) -> None:
        self._lock = Lock()
        self.reset()

    def reset(self) -> None:
        with self._lock:
            repository = FamilyInitializer().initialize()
            self.service = FamilyTreeService(repository)
            self.processor = CommandProcessor(self.service)

    def add_child(self, mother_name: str, child_name: str, gender: str) -> str:
        with self._lock:
            return self.service.add_child(mother_name, child_name, gender)

    def get_relationship(self, name: str, relationship: str) -> str:
        with self._lock:
            return self.service.get_relationship(name, relationship)

    def process_commands(self, commands: list[str]) -> list[str]:
        with self._lock:
            return self.processor.process_lines(commands)


def create_app() -> Flask:
    app = Flask(__name__)
    family_tree_app = FamilyTreeApplication()

    @app.get("/")
    def index() -> Any:
        return redirect(url_for("ui_page"))

    @app.get("/ui")
    def ui_page() -> str:
        return render_template(
            "ui.html",
            relationships=SUPPORTED_RELATIONSHIPS,
        )

    @app.get("/terminal")
    def terminal_page() -> str:
        return render_template("terminal.html")

    @app.get("/api/health")
    def health() -> Any:
        return jsonify({"status": "ok"})

    @app.post("/api/add-child")
    def add_child() -> Any:
        payload = request.get_json(silent=True) or {}
        output = family_tree_app.add_child(
            str(payload.get("mother_name", "")).strip(),
            str(payload.get("child_name", "")).strip(),
            str(payload.get("gender", "")).strip(),
        )
        return jsonify({"output": output})

    @app.post("/api/relationship")
    def relationship() -> Any:
        payload = request.get_json(silent=True) or {}
        output = family_tree_app.get_relationship(
            str(payload.get("name", "")).strip(),
            str(payload.get("relationship", "")).strip(),
        )
        return jsonify({"output": output})

    @app.post("/api/commands")
    def commands() -> Any:
        payload = request.get_json(silent=True) or {}
        if bool(payload.get("reset_before", False)):
            family_tree_app.reset()

        raw_commands = payload.get("commands", [])
        if isinstance(raw_commands, str):
            command_lines = raw_commands.splitlines()
        elif isinstance(raw_commands, list):
            command_lines = [str(command) for command in raw_commands]
        else:
            command_lines = []
        outputs = family_tree_app.process_commands(command_lines)
        return jsonify({"outputs": outputs})

    @app.post("/api/reset")
    def reset() -> Any:
        family_tree_app.reset()
        return jsonify({"output": "RESET_DONE"})

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
