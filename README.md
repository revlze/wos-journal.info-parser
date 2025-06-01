# Parser for wos-journal.info

Short description
-----------------

This program collects a database of all submitted journals on the wos-journal.info.

Raw data is saved to `<data_path>/raw/page_{page_number}.html`

Processed csv is saved to `<data_path>/processed/journals.csv`

An example of working code is in `main.py`


## Setup

python>=3.9

### In order for the selenium library to simulate a browser, you need to have the [Firefox]((https://www.mozilla.org/en-US/firefox/new/)) browser pre-installed and the [gekodriver.exe]((https://github.com/mozilla/geckodriver/releases)) file, then specify the `path` to gekodriver on your computer in the `config.py` file.
----

Example:
- Archlinux
- Python 3.13.3
- Shell: fish
```bash
git clone https://github.com/revlze/wos-journal.info-parser.git
cd wos-journal.info-parser
python -m venv .
source bin/activate.fish
pip install -r requirements.txt
python main.py
```