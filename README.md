# Offer Readiness QA Tool

A Streamlit MVP for comparing Offer Readiness source data with observations
from Dell product detail pages.

## Requirements

- Python 3.11 or newer
- Dependencies from `requirements.txt`

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## Manual comparison

Enter matching source and live specifications using one item per line:

```text
Processor: Intel Core Ultra 7
Memory: 16GB DDR5
```

The comparison ignores letter case and repeated whitespace.

## CSV/XLSX audit

The source file must contain these columns:

- `Offer ID`
- `Country`
- `Checkpoint`
- `Expected Format / Rule`

After selecting an Offer ID and market, copy the visible content from the
live Dell PDP and paste it into the app:

```text
Dell Pro 7 Series 14 Laptop
AMD Ryzen AI 5 PRO 435, 6 Cores
Windows 11 Pro
16 GB DDR5
512 GB SSD
14" Non Touch FHD (1920x1200)
Estimated delivery: October 20, 2026
```

The app automatically evaluates supported checkpoints and records the text
that supports each result. Checkpoints that cannot be determined reliably
from copied text are marked `REVIEW`. The result table can be downloaded as
a CSV compatible with Excel.

Rules without complete definitions remain visible as references and are not
evaluated automatically.

## Tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Current scope

This phase analyzes text manually copied from PDP pages. It does not scrape
Dell pages. Checks that require images, interaction, pricing calculations,
configuration dependencies, or page layout remain manual reviews.
