# Glynac Family Tree Coding Challenge

Production-quality Python solution for the King Arthur family tree challenge. The application keeps the family tree in memory, accepts commands from a text file, and prints command results to the console.

## Tech Stack

- Python 3.11+
- pytest
- Object-oriented design with a repository, service layer, and Strategy Pattern relationship resolvers

## Project Structure

```text
.
├── README.md
├── docs
│   ├── architecture.md
│   ├── flow_diagram.md
│   └── relationship_rules.md
├── input
│   └── sample_input.txt
├── pyproject.toml
├── requirements.txt
├── src
│   └── family_tree
│       ├── api.py
│       ├── bootstrap
│       ├── main.py
│       ├── models
│       ├── relationships
│       ├── repository
│       ├── services
│       ├── templates
│       └── utils
└── tests
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run Application

Terminal command processor:

```bash
PYTHONPATH=src python -m family_tree.main input/sample_input.txt
```

## Run Flask API And UI

Install dependencies first, then start the Flask app:

```bash
pip install -r requirements.txt
PYTHONPATH=src flask --app family_tree.api run
```

Open `http://127.0.0.1:5000/ui` to validate `ADD_CHILD` and `GET_RELATIONSHIP` with form controls.

Open `http://127.0.0.1:5000/terminal` to validate the same command-file flow as the terminal program.

The terminal entry point is `src/family_tree/main.py`. The Flask API entry point is `src/family_tree/api.py`. The form UI is `src/family_tree/templates/ui.html`, and the command-style UI is `src/family_tree/templates/terminal.html`.

API endpoints:

- `GET /api/health`
- `POST /api/add-child` with `mother_name`, `child_name`, and `gender`
- `POST /api/relationship` with `name` and `relationship`
- `POST /api/commands` with `commands` as text or a list of command strings
- `POST /api/reset`

## Run Tests

```bash
pytest
```

## Sample Input

```text
ADD_CHILD Flora Minerva Female
GET_RELATIONSHIP Remus Maternal-Aunt
GET_RELATIONSHIP Minerva Siblings
ADD_CHILD Luna Lola Female
GET_RELATIONSHIP Luna Maternal-Aunt
ADD_CHILD Ted Bella Female
GET_RELATIONSHIP Remus Siblings
GET_RELATIONSHIP Lily Sister-In-Law
```

## Sample Output

```text
CHILD_ADDED
Dominique Minerva
Victoire Dominique Louis
PERSON_NOT_FOUND
PERSON_NOT_FOUND
CHILD_ADDITION_FAILED
NONE
Darcy Alice
```

## Assumptions

- Person names are unique across the tree.
- Gender values are `Male` and `Female`, case-insensitive for input convenience.
- Blank input lines are ignored.
- Invalid command shape, unknown command names, and unsupported argument counts return `INVALID_COMMAND`.
- Relationship names must match the supported challenge relationship names.
- Relationship results preserve the order in which people were added to the family tree.

## Error Handling

| Scenario | Output |
| --- | --- |
| Child added successfully | `CHILD_ADDED` |
| Mother does not exist | `PERSON_NOT_FOUND` |
| Parent is male | `CHILD_ADDITION_FAILED` |
| Duplicate child name | `CHILD_ADDITION_FAILED` |
| Invalid gender | `INVALID_GENDER` |
| Person does not exist | `PERSON_NOT_FOUND` |
| Unsupported relationship | `INVALID_RELATIONSHIP` |
| Relationship has no results | `NONE` |
| Invalid command | `INVALID_COMMAND` |

## Design Decisions

- `Person` owns relationship links such as spouse, parents, and ordered children.
- `FamilyRepository` provides O(1) person lookup by name.
- `FamilyTreeService` coordinates validations and delegates relationship calculations to strategies.
- Each relationship lives in its own resolver class, keeping relationship logic isolated and easy to test.
- The Flask API is a thin adapter over the same service layer used by the CLI.
- No database is used; the entire family tree is stored in memory.

## Adding A New Relationship

1. Create a new resolver in `src/family_tree/relationships/`.
2. Implement `RelationshipResolver.resolve`.
3. Register the resolver in `RelationshipFactory`.
4. Add tests for success and empty-result behavior.

## Why Strategy Pattern

Each relationship has different traversal rules. Strategy Pattern keeps those rules independent, avoids a large conditional block in the service layer, and makes the application open to new relationships without changing existing resolver code.
