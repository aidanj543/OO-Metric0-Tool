
# OO Metrics Analyzer

A Python-based software testing tool that analyzes
Object-Oriented class definitions and calculates
four OO software metrics.

## Project Overview

This project was developed for Assignment 2:
OO Metric Tool.

The application uses Python's Abstract Syntax Tree
(AST) module to analyze Python class definitions
without executing the uploaded code.

The frontend is developed using Streamlit.

## Features

- Upload Python (.py) files
- Paste Python class definitions
- Analyze multiple classes
- Calculate four OO metrics
- Display results in an interactive table
- Visualize metric comparisons
- Handle invalid Python syntax
- Validate the analyzer using pytest

## Implemented Metrics

### 1. Weighted Methods per Class (WMC)

Counts methods explicitly defined in each class.

Formula:

WMC = Sum of method weights

Each method is assigned weight 1.

### 2. Cohesion of Methods (COM)

Measures the proportion of method pairs that
share at least one instance attribute.

Formula:

COM = Shared method pairs / Total method pairs

For zero-method classes, COM = 0.0.
For one-method classes, COM = 1.0.

### 3. Coupling Between Objects (CBO)

Counts distinct other classes referenced by a
class within the analyzed source file.

Each unique referenced class counts once.

### 4. Response for a Class (RFC)

Counts distinct method names explicitly declared
in a class and attribute-style method names
directly called by those methods.

## Technologies

- Python 3
- Python AST
- Streamlit
- pytest
- Git and GitHub

## Project Structure

    OO-Metric-Tool/
    ├── app.py
    ├── analyzer.py
    ├── metrics/
    │   ├── wmc.py
    │   ├── com.py
    │   ├── cbo.py
    │   └── rfc.py
    ├── samples/
    │   └── hospital_management.py
    ├── tests/
    ├── screenshots/
    ├── requirements.txt
    └── README.md

## Installation

1. Clone the GitHub repository.

    git clone https://github.com/YOUR_USERNAME/OO-Metric-Tool.git

2. Enter the project folder.

    cd OO-Metric-Tool

3. Create a virtual environment.

    python3 -m venv .venv

4. Activate the environment.

    source .venv/bin/activate

5. Install project dependencies.

    python -m pip install -r requirements.txt

## Running the Application

Start the Streamlit application:

    python -m streamlit run app.py

Then open the local URL displayed in the terminal.

## How to Use

1. Select Upload Python File or Paste Python Code.
2. Provide valid Python class definitions.
3. Click Analyze OO Metrics.
4. Review the WMC, COM, CBO, and RFC results.
5. Inspect the summary metrics and chart.

## Testing

Run all automated tests using:

    python -m pytest tests/ -v

Tests cover:
- Individual metric calculations
- Multiple classes
- Empty classes
- Invalid syntax
- The hospital management example
- Integrated analysis
- Streamlit interface behavior

## Example Results

| Class | WMC | COM | CBO | RFC |
|---|---:|---:|---:|---:|
| Prescription | 0 | 0.00 | 0 | 0 |
| Patient | 3 | 0.00 | 1 | 5 |
| Doctor | 2 | 1.00 | 2 | 5 |
| Nurse | 1 | 1.00 | 1 | 2 |
| Pharmacist | 2 | 1.00 | 2 | 5 |

These are expected results under the implemented
metric definitions.

## Limitations

This tool uses simplified static analysis.

- Only top-level class definitions are analyzed.
- Generated dataclass methods are not counted.
- WMC uses unit weights instead of control-flow
  complexity.
- COM does not fully resolve aliases or indirect
  attribute usage.
- CBO counts outgoing references to other classes
  defined within the analyzed file.
- RFC counts distinct method names rather than
  fully resolved method identities.
- Dynamic dispatch and runtime behavior are not
  analyzed.

The uploaded source is parsed, not executed.

## Version Control

Git was used throughout development.

Each metric was implemented and tested separately
before integration into the Streamlit application.

## AI Usage

ChatGPT was used as a development and learning
assistant for explanations of Python AST,
implementation guidance, testing examples,
debugging assistance, and documentation.

The project was developed and validated using
Python, pytest, Git, and GitHub.

## Assignment

Assignment 2 - OO Metric Tool
