
from pathlib import Path

import pytest

from analyzer import analyze_code


def test_complete_analysis():
    code = """
class Student:
    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name
"""

    expected = [{
        "Class": "Student",
        "WMC": 2,
        "COM": 1.0,
        "CBO": 0,
        "RFC": 2
    }]

    assert analyze_code(code) == expected


def test_multiple_classes():
    code = """
class Patient:
    def get_name(self):
        return self.name

class Doctor:
    def treat(self, patient: Patient):
        patient.get_name()
"""

    results = analyze_code(code)

    assert len(results) == 2

    patient = results[0]
    doctor = results[1]

    assert patient["Class"] == "Patient"
    assert patient["WMC"] == 1
    assert patient["CBO"] == 0

    assert doctor["Class"] == "Doctor"
    assert doctor["WMC"] == 1
    assert doctor["CBO"] == 1
    assert doctor["RFC"] == 2


def test_hospital_management():
    source = Path(
        "samples/hospital_management.py"
    ).read_text(encoding="utf-8")

    results = analyze_code(source)

    assert len(results) == 5

    doctor = next(
        row for row in results
        if row["Class"] == "Doctor"
    )

    assert doctor == {
        "Class": "Doctor",
        "WMC": 2,
        "COM": 1.0,
        "CBO": 2,
        "RFC": 5
    }


def test_empty_code():
    with pytest.raises(ValueError):
        analyze_code("")


def test_no_classes():
    code = """
def hello():
    print("Hello")
"""

    with pytest.raises(ValueError):
        analyze_code(code)


def test_invalid_syntax():
    with pytest.raises(SyntaxError):
        analyze_code("class Broken(")


def test_invalid_input_type():
    with pytest.raises(ValueError):
        analyze_code(None)
