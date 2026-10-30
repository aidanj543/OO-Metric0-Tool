
from pathlib import Path

import pytest

from metrics.rfc import calculate_rfc


def test_no_methods():
    code = """
class Empty:
    pass
"""
    assert calculate_rfc(code) == {"Empty": 0}


def test_one_method():
    code = """
class Student:
    def study(self):
        pass
"""
    assert calculate_rfc(code) == {"Student": 1}


def test_internal_method_call():
    code = """
class Calculator:
    def add(self, a, b):
        return a + b

    def calculate(self):
        return self.add(5, 10)
"""
    assert calculate_rfc(code) == {"Calculator": 2}


def test_external_method_call():
    code = """
class Doctor:
    def schedule(self, patient):
        patient.add_appointment()
"""
    assert calculate_rfc(code) == {"Doctor": 2}


def test_duplicate_method_calls():
    code = """
class Doctor:
    def treat(self, patient):
        patient.save()
        patient.save()
        patient.save()
"""
    assert calculate_rfc(code) == {"Doctor": 2}


def test_multiple_called_methods():
    code = """
class Doctor:
    def treat(self, patient):
        patient.validate()
        patient.save()
        patient.notify()
"""
    assert calculate_rfc(code) == {"Doctor": 4}


def test_async_method():
    code = """
class Service:
    async def fetch(self):
        client.connect()
"""
    assert calculate_rfc(code) == {"Service": 2}


def test_hospital_management():
    source = Path(
        "samples/hospital_management.py"
    ).read_text(encoding="utf-8")

    expected = {
        "Prescription": 0,
        "Patient": 5,
        "Doctor": 5,
        "Nurse": 2,
        "Pharmacist": 5
    }

    assert calculate_rfc(source) == expected


def test_invalid_python():
    with pytest.raises(SyntaxError):
        calculate_rfc("class Broken(")
