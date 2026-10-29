
from pathlib import Path
from metrics.com import calculate_com


# Read the hospital management code
file = Path("samples/hospital_management.py")

source_code = file.read_text(encoding="utf-8")

# Calculate cohesion
results = calculate_com(source_code)

print("------- Cohesion of Methods (COM) -------")

for class_name, com in results.items():
    print(f"{class_name}: COM = {com:.2f}")
