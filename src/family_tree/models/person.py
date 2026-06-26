from __future__ import annotations

from dataclasses import dataclass, field

from family_tree.enums import Gender


@dataclass(eq=False)
class Person:
    name: str
    gender: Gender
    mother: Person | None = None
    father: Person | None = None
    spouse: Person | None = None
    children: list[Person] = field(default_factory=list)

    def add_child(self, child: Person) -> None:
        if child not in self.children:
            self.children.append(child)

    def set_spouse(self, spouse: Person) -> None:
        self.spouse = spouse
        if spouse.spouse is not self:
            spouse.set_spouse(self)

    def is_male(self) -> bool:
        return self.gender is Gender.MALE

    def is_female(self) -> bool:
        return self.gender is Gender.FEMALE
