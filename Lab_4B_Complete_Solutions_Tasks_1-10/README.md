# Lab 4B — Complete Python solutions (Tasks 1–10)

## Contents
- `task01.py` … `task10.py`: one file per main task.
- Each file contains the short design answers in its opening comments, a complete
  implementation, and pytest tests.

## Requirements
Python 3.10 or newer.

```bash
python -m pip install pytest mypy pyflakes
```

## Run all tests
Run this command from the extracted folder:

```bash
python -m pytest -v
```

Or run one task at a time:

```bash
python -m pytest -v task01.py
python -m pytest -v task02.py
```

## Static checks
Task 6 demonstrates a structural `Protocol`:

```bash
mypy task06.py
```

Task 8 asks you to run pyflakes on the original duplicate-method example.
The solution file contains the corrected implementation, so to see the
redefinition warning, run pyflakes against the original code from the handout.
The relevant warning is normally `redefinition of unused 'search' from line ...`
(F811).

## Important concepts to understand

1. **Abstract class:** defines required behaviour; it cannot be instantiated
   while abstract methods remain unimplemented.
2. **Polymorphism:** callers use a shared interface and do not need to know the
   concrete class.
3. **Inheritance:** use it for a genuine, stable “is-a” relationship.
4. **Composition:** use it when one object owns or contains another object,
   such as an audit log containing entries or an employee having a role.
5. **Duck typing:** an object is suitable when it provides the operations the
   caller needs, regardless of its parent class.
6. **Protocol:** documents duck-typed requirements for static type checking.
7. **Value object:** immutable object whose value defines its identity, such
   as Money.
8. **MRO:** Python's method resolution order determines which implementation
   is called in multiple inheritance. Cooperative mixins must call `super()`.
9. **Factory/registry:** converts external identifiers into the correct
   implementation at the boundary of the application.

## Notes
- Amounts in Task 1 and Task 7 are integer minor units as specified by the lab.
- Task 3 uses integer arithmetic and applies VAT once to the final net amount.
- Task 5 uses dates to select the role applicable to a payroll date.
- Task 9's `ReorderedInvoice` is deliberately included to demonstrate why
  concrete `Model` should come after cooperative mixins.
