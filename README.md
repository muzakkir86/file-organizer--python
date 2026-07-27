# File Organizer (Python)

A small, practical Python toolset to organize project files by type and produce a documented sales report.

## Project overview

This repository contains a lightweight file-organizer automation script and a helper script that generates a documented Excel report from CSV sales data. The main automation (`program5.py`) scans a folder and groups files into category folders (e.g., `code`, `data`, `documents`) in a safe preview mode and an optional apply mode to perform the changes.

## Features

- Preview file organization without changing anything
- Apply changes to move files into categorized folders
- Produce a JSON report of planned or performed actions (`automation_report.json`)
- Generate a documented Excel production report from `sales_summary.csv` (`program12.py`)

## Technologies used

- Python 3 (tested on 3.13)
- Standard library: `pathlib`, `shutil`, `argparse`, `json`
- Optional for report generation: `pandas`, `openpyxl` (used by `program12.py`)

## Installation

1. Clone the repo:

```bash
git clone https://github.com/muzakkir86/file-organizer--python.git
cd file-organizer--python
```

2. (Optional) Create and activate a virtual environment:

Windows PowerShell
```powershell
python -m venv .venv
. .venv\Scripts\Activate.ps1
```

3. Install optional dependencies for the report script only:

```bash
pip install pandas openpyxl
```

## Usage

Preview mode (safe): shows what would be moved and writes `automation_report.json`.

```bash
python program5.py
```

Apply mode: actually moves files into categorized folders.

```bash
python program5.py --apply
```

Other options:
- Use `--source <path>` to run on a different folder (defaults to current directory).

Generate the documented Excel production report (reads `sales_summary.csv` and writes `production_report.xlsx`):

```bash
python program12.py
```

## Project structure

- `program5.py` — main file-organizer automation (preview and apply)
- `program12.py` — generates `production_report.xlsx` from `sales_summary.csv`
- `sales_summary.csv` — example sales data used by `program12.py`
- `production_report.xlsx` — generated Excel file (gitignored)
- `automation_report.json` — report produced by `program5.py` (gitignored)
- `code/`, `data/`, `documents/` — example folders after organization

## Author

M. Muzakkir — GitHub: [muzakkir86](https://github.com/muzakkir86)

---

If you want, I can also:
- commit this README to the repository (I can run the git commands),
- add a `requirements.txt`, or
- open the repo page in your browser.
