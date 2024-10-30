# Slackpoint 2.0

<img src = "./assets/Logo.png" width="370" height="200"/> 

![This is an image](https://img.shields.io/badge/purpose-Software_Engineering-blue)
[![DOI](https://zenodo.org/badge/865016138.svg)](https://doi.org/10.5281/zenodo.13926072)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Language: Python](https://img.shields.io/badge/language-python-red.svg)](https://docs.python.org/3/)
[![GitHub top language](https://img.shields.io/github/languages/top/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint)](https://docs.python.org/3/)
[![GitHub last commit](https://img.shields.io/github/last-commit/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint)](https://github.com/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint/commits/main)

[![GitHub issues](https://img.shields.io/github/issues/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint)](https://github.com/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint)](https://github.com/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint/pulls)
[![GitHub closed issues](https://img.shields.io/github/issues-closed-raw/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint)](https://github.com/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint/issues?q=is%3Aissue+is%3Aclosed)
[![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed-raw/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint)](https://github.com/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint/pulls?q=is%3Apr+is%3Aclosed)
![GitHub forks](https://img.shields.io/github/forks/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint?style=social)
[![GitHub contributors](https://img.shields.io/github/contributors/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint)](https://github.com/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint/graphs/contributors)

Code coverage (develop): [![codecov](https://codecov.io/gh/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint/branch/develop/graph/badge.svg?token=A82OVFZBYL)](https://codecov.io/gh/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint)
Code coverage (main): [![codecov](https://codecov.io/gh/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint/graph/badge.svg?token=A82OVFZBYL)](https://codecov.io/gh/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint)
Syntax checker and code formatter: [![code checker](https://github.com/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint/actions/workflows/code_formatter.yml/badge.svg)](https://github.com/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint/blob/main/.github/workflows/code_formatter.yml)
Style checker: [![Python Style Checker](https://github.com/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint/actions/workflows/style-checker.yml/badge.svg)](https://github.com/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint/blob/main/.github/workflows/style-checker.yml)
Run unit tests: [![Run Tests](https://github.com/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint/actions/workflows/run-tests.yml/badge.svg)](https://github.com/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint/tree/main/tests)

Click on the image below to view the demo video of the project

[![Demo Vidoe of the project](hxxps://img.youtube.com/vi/AG6aSE3xFzE/0.jpg)](https://www.youtube.com/watch?v=AG6aSE3xFzE)

Gamify your slack tasks! 💻

A lot of teams use Slack to get things done. However when you have ton of things to do with no short term rewards in sight, it gets difficult to check off those tasks. That's where Slackpoint comes to the rescue! Slackpoint aims to make work more fun and get people motivated to finish their tasks by gamifying Slack!

## Built with

<img src = "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original.svg" width="40" height="40"/> Flask
<br/>
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="40" height="40" /> Python
<br/>
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" width="40" height="40" /> PostgreSQL


## Scalability

- Deployment of the server from ngrok to the cloud ☁️ - via Heroku. 

- Deployment of the database from local to the cloud ☁️ - on Heroku Postgres which uses AWS EC2 instances at the backend to scale up and down depending on the amount of data.

  <br/>
  <img src = './assets/HerokuDB.png' width='650' height='450'/>
  <br/>


### Chat Channel

<code>https://discord.com</code>


## Features

Here is a list of features added during phase 3 of this project:

- Request help: Users can request help from any number of other users for a specific task.
- Set reminders for upcoming tasks: Get reminded for upcoming tasks!
- Daily standup notifications: See quickly who is doing what work as well as recently completed work and upcoming deadlines for each member of the team.

## Project documentation

The `docs` folder incorporates all necessary documents and documentation in our project.

Visit `docs/_build/html/autoapi/index.html` for the html version of our documentation

## Tools used

Code formatter: black and flake8

## 📖 Getting started:

See [INSTALL.md](INSTALL.md)

## List of miracles that Slackpoint can perform✨:

- Create a new task
- Mark task as done
- View pending tasks
- View completed tasks
- Ask for help

Let's go over these one by one...

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


#### **7. Request Help:**

Request for help from teammates on your task

Command: `/requesthelp {id} {teammate} [other teammates...]`


#### **8. Daily Standup:**

Get information about each teammates' upcoming, previous, and current tasks assigned to them

Command: `[none]`

Automatically sent to a specific channel at a configurable time.


#### **7. Set reminders:**

Set reminders for your upcoming tasks so you don't forget about them

Command: `/reminder`


