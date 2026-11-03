"""
Task 5 — Employee roles

Design answers:
1. A person's employment identity continues through promotion; the role changes.
   Replacing the Employee breaks references held by payroll, timesheets and ACLs.
2. Employee delegates pay calculation to its current role object.
3. change_role() changes the role without replacing the Employee instance/id.
4. Employee owns a role-history collection (composition). Each history entry
   stores the role and its start date, allowing past payroll to use the old role.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date


class Role(ABC):
    @abstractmethod
    def monthly_pay(self) -> int:
        pass


@dataclass(frozen=True)
class LecturerRole(Role):
    hours: int

    def monthly_pay(self) -> int:
        return self.hours * 120_000


@dataclass(frozen=True)
class HeadRole(Role):
    salary: int

    def monthly_pay(self) -> int:
        return self.salary + 3_000_000


@dataclass(frozen=True)
class RolePeriod:
    role: Role
    start_date: date


class Employee:
    def __init__(self, emp_id: int, name: str, role: Role,
                 start_date: date):
        self.emp_id = emp_id
        self.name = name
        self.role = role
        self.role_history = [RolePeriod(role, start_date)]

    def monthly_pay(self) -> int:
        return self.role.monthly_pay()

    def change_role(self, new_role: Role, start_date: date) -> None:
        if start_date < self.role_history[-1].start_date:
            raise ValueError("new role cannot start before the current role")
        self.role = new_role
        self.role_history.append(RolePeriod(new_role, start_date))

    def monthly_pay_on(self, when: date) -> int:
        applicable = [
            period for period in self.role_history
            if period.start_date <= when
        ]
        if not applicable:
            raise ValueError("employee did not yet have a role on this date")
        return applicable[-1].role.monthly_pay()


def test_promotion_keeps_employee_identity():
    employee = Employee(7, "Ali", LecturerRole(100), date(2026, 1, 1))
    reference_held_by_payroll = employee
    employee.change_role(HeadRole(14_000_000), date(2026, 7, 1))
    assert reference_held_by_payroll is employee
    assert employee.emp_id == 7
    assert employee.monthly_pay() == 17_000_000


def test_role_history_preserves_previous_pay():
    employee = Employee(7, "Ali", LecturerRole(100), date(2026, 1, 1))
    employee.change_role(HeadRole(14_000_000), date(2026, 7, 1))
    assert employee.monthly_pay_on(date(2026, 5, 1)) == 12_000_000
    assert employee.monthly_pay_on(date(2026, 8, 1)) == 17_000_000


def test_date_before_employment_has_no_role():
    import pytest
    employee = Employee(7, "Ali", LecturerRole(100), date(2026, 1, 1))
    with pytest.raises(ValueError):
        employee.monthly_pay_on(date(2025, 12, 31))
