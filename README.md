# spacex-de-challenge

## Task
Create a script to call on SpaceX's open-source [launch API](https://github.com/r-spacex/SpaceX-API). 
Use it to pull data about SpaceX launches to answer the queries below (documentation on responses 
here: https://docs.spacexdata.com)

a. Which drone ships has received the most successful successive landings by falcon 9 booster? List landing drone ships in order from most successful successive landings to least. 

b. Which payload nationality has been on the most launches? List nationalities and the count of launches that the nationality has been up on from most to least launches. 


## Plan
1. Database: Postgres
    - docker-compose for postgres 13
1. Extract: Pull data using Spacex api
    - using python 3.9
    - using requests package
    - store on file system in jsonl files
1. Load: Insert data into Postgres
    - using pandas package
    - little to no transformations
    - into "raw" tables
1. Query: Answer task questions
    - query only, using CTEs
    - unnest arrays and JSON when needed
    - no tables or stored procedures
1. Package: Documentation and instructions for running
    - readme
        - running the database
        - options for etl:
            - docker image
            - run local
        - reporting
        - cleanup
    - publish to github

## Structure
* /source/py: Python files for extracting and loading data are found in 
* /source/sql: Sql queries are stored in 
* docker-compose: File is for the postgres database
* Dockerfile: File for building the etl environment

## Run

1. Have docker desktop (Windows) or docker-compose (Linux/OSX) installed
1. Clone this repo to a local machine
    ```bash
    git clone https://github.com/robby-rob/spacex-de-challenge
    ```
1. Navigate to the repo root directory and run the following to start a postgres server:
    ```bash
    docker-compose up -d
    ```
1. Load data into the database:
    1. The easiest way is to build and run an image which executes the scripts in source/py in a predictable environment:
        ```bash
        docker build -t spacex-loader --no-cache .  
        docker run --name spacex-loader spacex-loader
        ```
        >Messages will display the status of each file extracted and loaded

    1. Alternatively, to run on local machine
        1. Install python 3.9.12
        1. Create and activate a virtual environment
        1. Install the packages in /source/requirements.txt using pip
        1. Alter /source/py/main.py `db_host` to *'localhost'*
        1. Run the script
1. Run the queries in the /source/sql queries against the database
    - The easiest way to run is to use a query tool of choice to connect to and query the database. The connection info is:
        - server: localhost
        - port: 5432
        - user: postgres
        - password: mysecretpassword
        - database: spacex 
    - Alternatively, use psql in the database:
        1. connect to database container
            ```bash
            docker exec -it spacex-db /bin/bash
            ```
        1. change user
            ```bash
            su postgres
            ```
        1. enter psql
            ```bash
            psql
            ```
        1. connect to database
            ```bash
            \c spacex
            ```
        1. paste and execute each query in /source/sql

## Cleanup
1. Database:
    ```bash
    docker-compose down -v
    docker image rm postgres:13
    ```
1. Data loader:
    ```bash
    docker container stop spacex-loader
    docker container rm spacex-loader
    docker image rm spacex-loader
    ```