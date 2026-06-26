# Architecture

The application uses a small layered architecture to keep command parsing, business rules, storage, and relationship calculations separate.

## Model Layer

`Person` is the core domain model. It stores a person's name, gender, parents, spouse, and ordered children. Child insertion order is preserved by the `children` list and is used by relationship output.

## Repository Layer

`FamilyRepository` stores people in `dict[str, Person]`, giving O(1) lookup by name. It owns person registration and marriage lookup/linking. It does not contain relationship traversal rules.

## Service Layer

`FamilyTreeService` coordinates use cases:

- Validate and add children through a mother.
- Reject duplicate child names.
- Resolve relationships through the `RelationshipFactory`.
- Convert outcomes to the exact challenge output messages.

## Relationship Strategy Layer

Every relationship is implemented as a `RelationshipResolver`. This keeps each traversal rule focused and independently testable. The service asks the factory for a resolver rather than branching on every relationship.

## Command Processor

`CommandProcessor` parses input lines, handles blank lines and malformed command shapes, and dispatches valid command shapes to the service layer.

## Flask API And UI

`family_tree.api` exposes the challenge behavior over HTTP. It reuses `FamilyTreeService` and `CommandProcessor`, so API and CLI behavior stay aligned. The Flask layer owns request parsing and JSON responses only.

The browser pages are kept separate from both the API entry point and the terminal entry point:

- `src/family_tree/templates/ui.html` contains the form-based validator.
- `src/family_tree/templates/terminal.html` contains the command-file validator.
- `src/family_tree/main.py` remains the terminal CLI.

## Extensibility

The design is maintainable because new relationships can be added by creating a resolver and registering it in the factory. Existing services, commands, and model classes do not need to be rewritten for each new family traversal rule.
