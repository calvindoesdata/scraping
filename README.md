# Scraping Understat Data

*Note: this was last working as of 2024. Issues have been identified since with grabbing data from Understat for beyond 
the 24/25 season. This is due to a change in the HTML response from the EPL landing page.*

Basic code for scraping match data from Understat and compiling charts for:
- Shot locations for home and away teams on separate half pitch plots
- xG flow graphs for home and away teams

### Install requirements
It is recommended to create a Python 3.11 virtual environment and install the dependencies listed in the requirements 
file. This can be done in the command line by:
```
python3 -m venv my_venv
source my_venv/bin/activate
pip3 install -r requirements.txt
```

### Accessing the code base
The code base accessed locally by cloning the repository. After navigating to your local directory of choice, run the following in the command line:
```
git clone https://github.com/calvindoesdata/scraping.git
```
Alternatively the project can be downloaded as a .zip from the repository home page by selecting 'Code' > 'Download ZIP'.

### Running the project
This project can be run from the command line using the following commands:
```
cd .../scraping/
python3 main.py
```
