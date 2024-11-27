# Slackpoint 4.0

<img width="338" alt="Screenshot 2024-11-24 at 8 07 18 PM" src="https://github.com/user-attachments/assets/8be955ed-dc77-4384-9012-6e70410cb319">

  
![This is an image](https://img.shields.io/badge/purpose-Software_Engineering-blue)
[![DOI](https://zenodo.org/badge/890675627.svg)](https://doi.org/10.5281/zenodo.14210449)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Github](https://img.shields.io/badge/language-python-red.svg)](https://docs.python.org/3/)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/NCSU-SE-ABK/slackpoint/Running%20Code%20Coverage)](https://github.com/NCSU-SE-ABK/Slackpoint/actions)
[![npm_build](https://github.com/NCSU-SE-ABK/Slackpoint/actions/workflows/code_formatter.yml/badge.svg)](https://github.com/NCSU-SE-ABK/Slackpoint/actions/workflows/code_formatter.yml)
[![npm_build](https://github.com/NCSU-SE-ABK/Slackpoint/actions/workflows/style-checker.yml/badge.svg)](https://github.com/NCSU-SE-ABK/Slackpoint/actions/workflows/style-checker.yml)
[![npm_build](https://github.com/NCSU-SE-ABK/Slackpoint/actions/workflows/ci-cd-pipeline.yml/badge.svg)](https://github.com/NCSU-SE-ABK/Slackpoint/actions/workflows/ci-cd-pipeline.yml)
[![GitHub top language](https://img.shields.io/github/languages/top/NCSU-SE-ABK/slackpoint)](https://docs.python.org/3/)
[![GitHub last commit](https://img.shields.io/github/last-commit/NCSU-SE-ABK/Slackpoint)](https://github.com/NCSU-SE-ABK/Slackpoint/commits/main/)
[![codecov](https://codecov.io/gh/NCSU-SE-ABK/Slackpoint/graph/badge.svg?token=9OKXD0QUTP)](https://codecov.io/gh/NCSU-SE-ABK/Slackpoint)
[![GitHub issues](https://img.shields.io/github/issues/NCSU-SE-ABK/slackpoint)](https://github.com/NCSU-SE-ABK/slackpoint/issues)
![Forks](https://img.shields.io/github/forks/NCSU-SE-ABK/Slackpoint?style=social)
[![GitHub contributors](https://img.shields.io/github/contributors/NCSU-SE-ABK/slackpoint)](https://github.com/NCSU-SE-ABK/slackpoint/graphs/contributors)
![Lines of code](https://tokei.rs/b1/github/NCSU-SE-ABK/Slackpoint)
![repo-size](https://img.shields.io/github/repo-size/NCSU-SE-ABK/Slackpoint)
![file count](https://img.shields.io/github/directory-file-count/NCSU-SE-ABK/Slackpoint)
![language_count](https://img.shields.io/github/languages/count/NCSU-SE-ABK/Slackpoint)

Click on the image below to view the demo video of the project

[![Demo Vidoe of the project](https://img.youtube.com/vi/AG6aSE3xFzE/0.jpg)](https://www.youtube.com/watch?v=AG6aSE3xFzE)

Gamify your slack tasks! 💻

A lot of teams use Slack to get things done. However when you have ton of things to do with no short term rewards in sight, it gets difficult to check off those tasks. That's where SlackPoint comes to the rescue! SlackPoint aims to make work more fun and get people motivated to finish their tasks by gamifying Slack!

## Built with

<img src = "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original.svg" width="40" height="40"/> Flask
<br/>
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="40" height="40" /> Python
<br/>
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" width="40" height="40" /> PostgreSQL


## Scalability

- Deployment of the server from ngrok to the cloud ☁️ - via Heroku. We no longer need re-routing of localhost to ngrok since our server has been deployed on the cloud (https://slackpoint-server.herokuapp.com/).

- Deployment of the database from local to the cloud ☁️ - on Heroku Postgres which uses AWS EC2 instances at the backend to scale up and down dewpending on the amount of data.

  <br/>
  <img src = './assets/HerokuDB.png' width='650' height='450'/>
  <br/>


### Chat Channel

<code><a href="https://app.slack.com/client/T04D1KLCU2Y/C04CZ600AHY" target="_blank"><img height="30" width="100" src="https://user-images.githubusercontent.com/111834635/194175304-834d5663-b6bb-4e38-981d-98bc1bf028b8.png"></a></code>


## Features

Here is a list of features added during phase 4 of this project:

1) ## Dockerize the Flask Application:
Create a Dockerfile to containerize the Flask application. Ensure the Docker image includes
all necessary dependencies and configurations.

2) ## Set Up Kubernetes Configuration:
Create Kubernetes deployment and service YAML files to define how the application should
be deployed and exposed in the GCP Kubernetes Engine (GKE).

3) ## Integrate with CI/CD Tools:
Use a CI/CD tool to automate the build, test, and deployment process. Configure the pipeline
to: Build the Docker image. Push the Docker image to a container registry (e.g., Google
Container Registry). Deploy the application to GKE using the Kubernetes configuration files.

4) ## Deploy to GCP:
Set up a GKE cluster on GCP. Ensure the CI/CD pipeline has the necessary permissions to
interact with GCP services.

## Project documentation

The `docs` folder incorporates all necessary documents and documentation in our project.

## Tools used

Code formatter: black and flake8

Tech stack: Flask, PostgreSQL, Python

## 📖 Getting started:

- ### Prerequisite:
  - Download [Python3.x](https://www.python.org/downloads/).
  - Download [Flask](https://flask.palletsprojects.com/en/2.2.x/installation/).
  - Download [PostgreSQL](https://www.postgresql.org/download/)
  - Download [Pgadmin](https://www.pgadmin.org/download/)

## Run Locally

Clone the project

```bash
  git clone https://github.com/NCSU-SE-ABK/Slackpoint.git
```

Go to the project directory

```bash
  cd Slackpoint
```

Create a virtual environment:

```bash
  python3 -m venv test_env
```

Activate the virtual environment:
Linux/MacOS:

```bash
  source test_env/bin/activate
```

Windows:

```bash
  ./test_env/Scripts/activate
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Log on to api.slack.com and create your own slack bot.

On ngrok shell run 'ngrok http 5000' to get the public IP address in your local machine.

Add all the /commands in the bot configuration and paste the url from ngrok shell to requesting url section in the bot configuration.

Finally, change the URL in interactivity and shortcuts, URL: <BaseURL>/slack/interactive-endpoint.

Start the server

```bash
  flask run
```

     - Site will be hosted at:
       `http://127.0.0.1:5000/`

Before creating the database,

(1) Create a database in PgAdmin with any name convention.

(2) Change the local path of PostgreSQL in .env file (DATABASE_URL= 'postgresql://postgres:(password)@localhost/(database name from PgAdmin')

(3) Provide the Slack sigining secret and Slack bot token from the bot you created.

To create tables in the database,

```bash
First run the command 'flask shell'
Next command to create the database - 'db.create_all()'
```

### Project Dependencies

- flask
- slackclient
- python-dotenv
- slackeventsapi
- flask-sqlalchemy
- psycopg2
- pytest
- pytest-mock
- black
- pylint
- coverage
- pytest-cov


# Slackpoint 4.0

- Create a new task
- Mark task as done
- View pending tasks
- View completed tasks
- Ask for help

lets go over these one by one...

#### **1. Create new task:**

You can create a new task by simple using the `/create-task` command. We ask for just a few more parameters in addition to that:

Command: `/create`

![Create Task GIF](https://i.imgur.com/lUtX23a.gif)

This particular command will create a new task with the description as `Hey! This is my new task` having `100` points and a deadline of `15th October 2022`

#### **2. Mark task as done:**

Here you can mark a task as completed. You just need to give the task ID as a parameter

Command: `/task-done [task ID]`

Example:
`/task-done 10214`

![Task Done GIF](https://i.imgur.com/gOB6dVs.gif)

This will mark the task having task ID `10214` as completed. Further, updates records to show that this task is completed by user who posted this command

#### **3. View pending tasks:**

This command will return the list of incomplete tasks. Relax! no parameters required here

Command: `/viewpending [no parameters]`

![View pending GIF](https://i.imgur.com/TAnNoSO.gif)

Above command will display a list of pending tasks

#### **4. View completed tasks:**

Like the above command this will return a list of completed tasks. No parameters here as well!

Command: `/viewcompleted [no parameter]`

![View completed GIF](https://i.imgur.com/3SFQU2N.gif)

Above command will display a list of completed tasks

#### **5. Leaderboard:**

Want to get competitive? Take a peek at the leaderboard and try to beat the winner!

Command: `/leaderboard [no parameters]`

![Leaderboard GIF](https://i.imgur.com/LNfVFHX.gif)

It displays the list of the top performers on the channel along with their points.

#### **6. Help:**

Newbie at using slackpoint? You could use some help...

Command: `/help [no parameters]`

![Help GIF](https://i.imgur.com/RNykp6p.gif)
