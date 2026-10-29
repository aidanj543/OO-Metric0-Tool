from pathlib import Path

from metrics.wmc import calculate_wmc

#Reads the python file
file = Path("samples/hospital_management.py")

source_code = file.read_text(encoding="utf-8")

#calculates the WMC
results = calculate_wmc(source_code)

#Displays the results
print("--------Weighted Methods Per Class--------")
for class_name, wmc in results.items():
    print(f"{class_name}: WMC = {wmc}")

