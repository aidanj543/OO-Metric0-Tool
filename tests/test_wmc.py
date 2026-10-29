
import pytest
from pathlib import Path
from metrics.wmc import calculate_wmc


def test_single_class():
    code = """
class Student:
    def study(self):
        pass

    def sleep(self):
        pass
"""
    assert calculate_wmc(code) == {"Student": 2}


def test_multiple_classes():
    code = """
class Doctor:
    def diagnose(self):
        pass

    def prescribe(self):
        pass

class Nurse:
    def check_vitals(self):
        pass
"""
    assert calculate_wmc(code) == {
        "Doctor": 2,
        "Nurse": 1
    }


def test_empty_class():
    code = """
class Empty:
    pass
"""
    assert calculate_wmc(code) == {"Empty": 0}


def test_async_method():
    code = """
class Service:
    async def fetch_data(self):
        pass
"""
    assert calculate_wmc(code) == {"Service": 1}


def test_hospital_management():
    source = Path(
        "samples/hospital_management.py"
    ).read_text(encoding="utf-8")

    expected = {
        "Prescription": 0,
        "Patient": 3,
        "Doctor": 2,
        "Nurse": 1,
        "Pharmacist": 2
    }

    assert calculate_wmc(source) == expected


def test_invalid_python():
    code = "class Broken("

    with pytest.raises(SyntaxError):
        calculate_wmc(code)
