
import pytest
from pathlib import Path
from metrics.com import calculate_com


def test_high_cohesion():
    code = """
class BankAccount:
    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount

    def get_balance(self):
        return self.balance
"""
    assert calculate_com(code) == {"BankAccount": 1.0}


def test_low_cohesion():
    code = """
class Student:
    def update_name(self):
        self.name = "Alex"

    def update_age(self):
        self.age = 20
"""
    assert calculate_com(code) == {"Student": 0.0}


def test_partial_cohesion():
    code = """
class Example:
    def method_a(self):
        return self.name

    def method_b(self):
        return self.name

    def method_c(self):
        return self.age
"""
    assert calculate_com(code) == {"Example": 0.33}


def test_empty_class():
    assert calculate_com("class Empty: pass") == {
        "Empty": 0.0
    }


def test_single_method():
    code = """
class Nurse:
    def record_vitals(self):
        return self.temperature
"""
    assert calculate_com(code) == {"Nurse": 1.0}


def test_method_call_not_attribute():
    code = """
class Example:
    def method_a(self):
        self.save()

    def method_b(self):
        self.save()
"""
    assert calculate_com(code) == {"Example": 0.0}


def test_hospital_management():
    source = Path(
        "samples/hospital_management.py"
    ).read_text(encoding="utf-8")

    expected = {
        "Prescription": 0.0,
        "Patient": 0.0,
        "Doctor": 1.0,
        "Nurse": 1.0,
        "Pharmacist": 1.0
    }

    assert calculate_com(source) == expected


def test_invalid_python():
    with pytest.raises(SyntaxError):
        calculate_com("class Broken(")
