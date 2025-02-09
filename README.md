# SQL Alchemy Challenge - SurfsUp  
`Module 10`  
`EdX(2U) & UT Data Analytics and Visualization Bootcamp`  
`Cohort UTA-VIRT-DATA-PT-11-2024-U-LOLC`  
`By Neel Kumar Agarwal`  

## Table of Contents  
1. [Introduction](#introduction)  
2. [Setup and Usage](#setup-and-usage)  
    - [Prerequisites](#prerequisites)  
    - [Instructions](#instructions)  
    - [Prerequisites & Instructions](#prerequisites--instructions)  
    - [Directory Structure](#directory-structure)  
    - [Schema](#schema)  
3. [Challenge Overview](#challenge-overview)  
    - [Part 1](#part-1-analyzeexplore-data)  
    - [Part 2](#part-2-design-climate-app)  
4. [Summary Breakdowns](#summary-breakdowns)  
5. [Entity Relationship Diagram](#entity-relationship-diagram-erd)  
6. [Files and Directory Structure](#files-and-directory-structure)  
7. [Expected Results](#expected-results)  
    - [Queries](#queries)  

## Introduction  
Congratulations to me! I've decided to treat myself to a long holiday vacation in Honolulu, Hawaii. To help with my trip planning, I'm going to do a climate analysis about the area.  
The following sections outline the steps that I'll need to take to accomplish this task.  


## Challenge Overview  
The real purpose of this assignment is to explore using these technologies and methods in conjunction with each other, but within the scope of the project the purpose is the creation of multiple APIs that allow for calling to retrieve live JSON representation of queried data.  

### Part 1: Analyze/Explore Data  
First off, I'll need to use Python and SQLAlchemy to do a basic climate analysis and data exploration of my climate database. Specifically, I'll use SQLAlchemy's ORM to perform queries, Pandas for easy manipulation, and Matplotlib for visualization. The following list outlines steps taken to perform exploration and analysis:  

1. Use SQLAlchemy method create_engine() to connect to the SQLite database.  
2. Use SQLAlchemy method automap_base() to reflect tables into classes and save references to the classes.  
3. Link Python to the database by creating SQLAlchemy sessions.  
4. Perform a precipitation analysis and station analysis...  

### Part 2: Design Climate App  
The second part of this project is to create a functioning webpage based API that can be called  
like a normal API. This part actually combines the use of general use Python, SQL Alchemy, HTML, and CSS  
to create retrievable JSON objects. The following are the stepped routes that will be created.  
1. (Route: /) Create a Homepage at the base route.  
2. (Route: /api/v1.0/precipitation) Convert the query results from the precipitation analysis to a dictionary using the date and precipitation as key: value pairs and returns the JSON.  
3. (Route: /api/v1.0/stations) Returns JSON of stations from the dataset.  
4. (Route: /api/v1.0/tobs) Queries dates/temperatures for the most active station of the prior year and returns the JSON.  
5. (Route: /api/v1.0/&lt;start&gt;) Returns JSON of temperature minimum, average, and maximum for a given starting date, which will end at the end of the database.  
6. (Route: /api/v1.0/<start>/<end>) Returns JSON of temperature minimum, average, and maximum for a given starting and ending date.  