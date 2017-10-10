# Quick Start

1. Download the project and navigate to the project folder
2. Install packages `pip install tabulate psycopg2`
3. Set the analysis script as an executable `chmod a+x logAnalysis.py`
4. Run the program `./logAnalysis.py`

# Design

* The analysis script will ask which report you would like to see 1-3
* After entering an option the script will query the database using psycopg2 and a predefined sql query
  * The script assumes the DB is `news` change if needed
* The script will return a formated table using the tabulate package
* Rerun as needed (probaly should improve this)