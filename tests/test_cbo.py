
import pytest
from pathlib import Path

from metrics.cbo import calculate_cbo


def test_no_coupling():
    code = """
class Student:
    def study(self):
        print("Studying")
"""
    assert calculate_cbo(code) == {"Student": 0}


def test_one_dependency():
    code = """
class Patient:
    pass

class Doctor:
    def treat(self, patient: Patient):
        pass
"""
    assert calculate_cbo(code) == {
        "Patient": 0,
        "Doctor": 1
    }


def test_multiple_dependencies():
    code = """
class Patient:
    pass

class Prescription:
    pass

class Doctor:
    def prescribe(self, patient: Patient):
        return Prescription()
"""
    assert calculate_cbo(code) == {
        "Patient": 0,
        "Prescription": 0,
        "Doctor": 2
    }


def test_duplicate_dependency():
    code = """
class Patient:
    pass

class Doctor:
    def first(self, patient: Patient):
        pass

    def second(self, patient: Patient):
        pass
"""
    assert calculate_cbo(code)["Doctor"] == 1


def test_inheritance():
    code = """
class Person:
    pass

class Doctor(Person):
    pass
"""
    assert calculate_cbo(code) == {
        "Person": 0,
        "Doctor": 1
    }


def test_self_reference():
    code = """
class Node:
    def connect(self, other: Node):
        pass
"""
    assert calculate_cbo(code) == {"Node": 0}


def test_hospital_management():
    source = Path(
        "samples/hospital_management.py"
    ).read_text(encoding="utf-8")

    expected = {
        "Prescription": 0,
        "Patient": 1,
        "Doctor": 2,
        "Nurse": 1,
        "Pharmacist": 2
    }

    assert calculate_cbo(source) == expected


def test_invalid_python():
    with pytest.raises(SyntaxError):
        calculate_cbo("class Broken(")
