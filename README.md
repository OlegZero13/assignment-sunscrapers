# assignment-sunscrapers

## Task Description
Data Warehouse Prototype Project
Download Data

We will be exploring Lending Club’s loan origination data from 2007-2015. Please download the dataset in CSV format (loan.csv) and associated dictionary (LCDataDictionary.xlsx) from https://www.kaggle.com/wendykan/lending-club-loan-data.

### Part 1: Data Exploration and Evaluation
>Create an exploratory data analysis project. Load the data and perform any necessary cleaning and aggregations to explore and better understand the dataset

### Part 2: Data Pipeline Engineering
> Please build a prototype of a production data pipeline that will feed an analysis system (data warehouse) based on this dataset. This system will allow data scientists and data analysts to interactively query and explore the data, and will also be used for machine learning model training and evaluation. Assume that the system will receive periodic updates of this dataset over time, and that these updates will need to be processed in a robust, efficient way.

> For this section, please:

> Create a data model / schema in a database or storage engine of your choice. Develop code that will persist the dataset into this storage system. Include any data validation routines that you think may be necessary. Use your choice of geospatial python package and create spatial analysis Loan.csv file has addr_state. Please aggregate loan data for states and visualize it.

> Prioritize simplicity in your data model and processing code. Explain your thought process.

### Mechanics
> Use the tools, programming languages and frameworks that you are most comfortable with. We primarily use Jupyter, Python and SQL, but this is not a requirement.

> Submit all code and documentation via GitHub. Please include all code files, outputs, and visualizations in the repository. Do not include any passwords or secrets in your code. Include a documentation file with your project. Please assume that your work will be shared with data engineers as well as data scientists and software engineers in a collaborative environment. 

## Solution
### Part 1: Exploratory Data Analysis
#### Runing using Google Colab
The Exploratory Data Analysis (EDA) part is achieved using of Google-hosted instance of Jupyter notebook. The notebook is available as a file:  `./Exploratory-Data-Analysis.ipynb`, which needs to be uploaded to [Google Colab](https://colab.research.google.com).
For convinence, the datasets are hosted using Google Drive, but it is also possible to upload them directly without synching them with the Drive. In this case one has to edit a few lines in the notebook iself, and it is explained therein.

#### Viewing using Github
It is possible to view the EDA notebook directly using Github.
However, sometimes the notebook does not render correctly when viewing it directly on Github, we are we are presenting a snapshot of the geospatial analysis here for confirmation:

![](./uszipmap.png).

#### Running locally
To run the notebook locally, you need it activate a virtual environment and running an instance of the Jupyter noteook. Use the following commands:
```
$ git clone <this-repo-url>
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
$ jupyter notebook
```
This will start an instance of the notebook on `localhost:8888`. 
Use your browser to open the notebook and view it.
Again, please make sure that the datasets paths are correct.

### Part 2: Simple Warehouse
For the warehouse part, we decided to create a simple web application featuring PostgreSQL and Django.
The reasons behind choosing Django are developer's comfort and easiness in data modeling (ORM).
The reasons behind setting up Postgres are the fact that this is a better, more production oriented database comparing to sqlite (Django's defualt) and it is also easy to set up.

### Setting it up.
To set it up, we need to have a linux OS with sudo rights.
To install and configure Postres, use the following commands:
```
$ sudo su - postgres
$ psql
```
Then "inside" of the database, we need to create the default user and define it's access rights"
```
CREATE DATABASE myproject;
CREATE USER myuser WITH PASSWORD mypassord;
ALTER ROLE myuser SET client_encoding TO 'utf-8';
ALTER ROLE myuser SET default_transaction_isolation TO 'read_committed';
ALTER ROLE myuser SET timezone TO 'utc';
GRANT ALL PRIVILEGES ON DATABASE myproject TO myuser;
```

If you have Postres set up locally, you will need to perform initial database migrations (assuming you use virtual environment).
```
$ ./manage.py makemigrations
$ ./manage.py migrate
$ ./manage.py runserver
```
The last command will also start a local development server for you.

In case you have an instance of Postgres somewhere else, please redefine the values in `warehouse/settings.py` file.

The Django project resides in `warehouse` directory, with `pipeline` being the main application code.

### Files in the project
The following list explains the purpose of the project files and directories:
* `data/` - storage space for data tables (see Exploratory-Data-Analysis.ipynb notebook for more information).
* `environ` - envrionmental varialbles are stored here. Note that this file is expempted from revisioning.
* `persist_borrowers.py` - python script that uses the application to initially populate of the database with records (table: `Borrowers`).
* `persist_loans.py` - similar to above, but populates the `Loans` table.
* `requirements.txt` - this file contains all python packages and dependencies.
* `schema-todo.md` - an auxiliary summary note on the relational database idea.
* `warehouse/` - main django project
* `pipeline/` - main django application (logic).
* `pipeline/post_borrower.sh` - script used for testing of the upload
* `pipeline/post_loans.sh` - similar to above
* `pipeline/states_lookup.csv` - table containing states - abbreviations link (e.g. 'CA' - California).
* `pipeline/validations.py`- all validation logic on all columns
* `pipeline/models.py` - the database model
* `pipeline/views.py` - the logic behind http requests
* `pipeline/urls.py` - url definitions

The remaining files are Django specific.

### Endpoints
To solve the warehousing tasks the following URLs have been defined:
1. `/` (index) - used just for testing
2. `/borrowers/<pk>/` - used for populating the Borrowers table (if used as POST) or getting the objects (if used as GET).
3. `/loans/<pk>/` - similar to above, but with the Loans table
4. `/batch/<from>/<to>` - (GET), used for querying of the data for machine learning and analytics purposes. The use case is that when a model is trained, the system will request the database content in batches, making subsequent http calls.
5. `/count/` - used for requesting of the total number of records.

### Final remarks
This project does not take security into considerations at all.
Apart from exempting secrets from hard-coding or revisioning, it does not take any steps to make this applicaiton safe, since:
1. This is a prototype project, aka homework assignment.
2. The project can just as well be deployed behind firewalls (aka "demilitarized zone"), where security checks will be performed elsewhere.

This is just to implify things, such as exempting CSRF tokens from being passed when using of a POST request.

Thank you.


