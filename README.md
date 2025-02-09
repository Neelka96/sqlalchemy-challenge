# SQL Alchemy Challenge - SurfsUp  
`Module 10`  
`EdX(2U) & UT Data Analytics and Visualization Bootcamp`  
`Cohort UTA-VIRT-DATA-PT-11-2024-U-LOLC`  
`By Neel Kumar Agarwal`  

## Table of Contents  
1. [Introduction](#introduction)  
2. [Setup & Usage](#setup--usage)  
    - [Prerequisites](#prerequisites)
    - [Instructions](#instructions)  
    - [Directory Structure](#directory-structure)  
3. [Challenge Overview](#challenge-overview)  
    - [Part 1](#part-1-analyzeexplore-data)  
    - [Part 2](#part-2-design-climate-app)  
4. [Summary Breakdowns](#summary-breakdowns)  
5. [Expected Results](#expected-results)  
    - [Queries](#queries)  

> [!NOTE]  
> All roleplaying instructions, rubric requirements, and Starter Code (with  
> database and csv's) are provided by 2U/edX as part of their educational  
> package provided with paid entry into the class.  


## Introduction  
Congratulations to me! I've decided to treat myself to a long holiday vacation in Honolulu, Hawaii. To help with my trip planning, I'm going to do a climate analysis about the area.  
In order to do so, I'll first use Jupyter Notebooks to write/run code in isolated code blocks so that I can experiment with my `SQL Alchemy` abstraction layer and ensure that I perform my queries correctly. I'll also do some basic analysis by using `Pandas` and `Matplotlib` to get a better grasp on my data and and provide a visual aid. Jupyter Notebook is excellent for testing purposes as it allows for easy running and printing of code blocks. This also means that after I ensure it's veracity, I can copy and paste desired queries inside of a regular python (.py) file to run as an executable!  
That serves the purposes of this project very well, as after I finish exploring and doing my analysis of Hawaii's climate data I can create an application in a python file using `Flask` and `SQL Alchemy` to create APIs! `Flask` will allow for the exportation of python functions into specific webpage softlink routes, which can be filled with `SQL` queries performed with `SQL Alchemy`, as well as `HTML` and `CSS` code for any explanation or styling. Now I'm prepared for my vacation!  



## Setup & Usage  


### Prerequisites  
1. Python 3.x  
- Standard libraries: `datetime` (included with Python)  
- Non-standard library: `pandas`, `numpy`, `matplotlib`, `sqlalchemy`, and `Flask`  
- IDE that supports Jupyter Notebooks with Python  
- DBMS: **SQLite 3.49.0**  by way of --> **SQL Alchemy**  

[:arrow_up: Return to TOC](#table-of-contents)  


### Instructions  

1. Clone this repository and open it on your local device.  
2. For `climate_analysis.ipynb` (Part 1):  
    - Open `climate_analysis.ipynb` in your IDE and run all cells.  
    - (Better viewing experience by using the 'Outline' tab in VSCode)  
    - If the necessary dependencies aren't found, please install using one of the following methods (however pip is preferred):  
        - `pip install <missing_library>`  
        - `conda install <missing_library>` (use the channel of your choice if multiple are found)  
3. For `app.py` (Part 2):  
    - Open `app.py` using an integrated terminal and run using your python compiler (Version 3.x)  
    - By use of `Flask` a local only webpage will be instantiated on a server on your computer  
    - Perform any of the listed API calls using the webpage directly or by using a `requests.get()` method in python (as well in other languages that offer API extensions).  
4. Enjoy!  

[:arrow_up: Return to TOC](#table-of-contents)  



### Directory Structure  
```  
sqlalchemy-challenge/  
|  
|—- SurfsUp/  
|   |—- Resources/  
|   |   —- hawaii_measurements.csv  
|   |   -- hawaii_stations.csv  
|   |   -- hawaii.sqlite  
|   |  
|   |—- app.py  
|   |-- climate_analysis.ipynb  
```  
This structure ensures all inputs are organized within their respective folders.  

[:arrow_up: Return to TOC](#table-of-contents)  



## Challenge Overview  
The real purpose of this assignment is to explore using these technologies and methods in conjunction with each other, but within the scope of the project the purpose is the creation of multiple APIs that allow for calling to retrieve live JSON representation of queried data.  


### Part 1: Analyze/Explore Data  
First off, I'll need to use Python and SQLAlchemy to do a basic climate analysis and data exploration of my climate database. Specifically, I'll use SQLAlchemy's ORM to perform queries, Pandas for easy manipulation, and Matplotlib for visualization.  
The following list outlines steps taken to perform exploration and analysis:  

1. Use SQLAlchemy method create_engine() to connect to the SQLite database.  
2. Use SQLAlchemy method automap_base() to reflect tables into classes and save references to the classes.  
3. Link Python to the database by creating SQLAlchemy sessions.  
4. Perform a precipitation analysis and station analysis...  

[:arrow_up: Return to TOC](#table-of-contents)  


### Part 2: Design Climate App  
The second part of this project is to create a functioning webpage based API that can be called  
like a normal API. This part actually combines the use of general use Python, SQL Alchemy, HTML, and CSS  
to create retrievable JSON objects. The following are the Flask App routes that will be created.  

1. **Route: /**  
    - Create a Homepage at the base route.  
2. **Route: /api/v1.0/precipitation**  
    - Convert the query results from the precipitation analysis to a dictionary using the date and precipitation as key: value pairs and returns the JSON.  
3. **Route: /api/v1.0/stations**  
    - Returns JSON of stations from the dataset.  
4. **Route: /api/v1.0/tobs**  
    - Queries dates/temperatures for the most active station of the prior year and returns the JSON.  
5. **Route: /api/v1.0/&lt;start&gt;**  
    - Returns JSON of temperature minimum, average, and maximum for a given starting date, which will end at the end of the database.  
6. **Route: /api/v1.0/&lt;start&gt;/&lt;end&gt;**  
    - Returns JSON of temperature minimum, average, and maximum for a given starting and ending date.  

[:arrow_up: Return to TOC](#table-of-contents)  