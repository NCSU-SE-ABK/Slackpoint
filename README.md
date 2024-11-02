# Slackpoint 3.0

<img src = "./assets/Logo.png" width="370" height="200"/> 

![This is an image](https://img.shields.io/badge/purpose-Software_Engineering-blue)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14027325.svg)](https://doi.org/10.5281/zenodo.14027325)


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Language: Python](https://img.shields.io/badge/language-python-red.svg)](https://docs.python.org/3/)
[![GitHub top language](https://img.shields.io/github/languages/top/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint)](https://docs.python.org/3/)
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint/develop)

[![GitHub issues](https://img.shields.io/github/issues/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint)](https://github.com/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint)](https://github.com/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint/pulls)
[![GitHub closed issues](https://img.shields.io/github/issues-closed-raw/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint)](https://github.com/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint/issues?q=is%3Aissue+is%3Aclosed)
[![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed-raw/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint)](https://github.com/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint/pulls?q=is%3Apr+is%3Aclosed)
![GitHub forks](https://img.shields.io/github/forks/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint?style=social)
[![GitHub contributors](https://img.shields.io/github/contributors/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint)](https://github.com/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint/graphs/contributors)

Code coverage (develop): [![codecov](https://codecov.io/gh/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint/branch/develop/graph/badge.svg?token=A82OVFZBYL)](https://codecov.io/gh/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint)
Syntax checker and code formatter: [![code checker](https://github.com/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint/actions/workflows/code_formatter.yml/badge.svg)](https://github.com/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint/blob/main/.github/workflows/code_formatter.yml)
Style checker: [![Python Style Checker](https://github.com/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint/actions/workflows/style-checker.yml/badge.svg)](https://github.com/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint/blob/main/.github/workflows/style-checker.yml)
Run unit tests: [![Run Tests](https://github.com/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint/actions/workflows/run-tests.yml/badge.svg)](https://github.com/CSC510-Team-Wise-Vilkomir-Sykes/Slackpoint/tree/main/tests)

Click on the link below to view the video of why you should contribute to the project

https://drive.google.com/file/d/1MPdmfJAbb_nGqiKyJrDB99I1aMbLmwxN/view?usp=sharing

https://github.com/user-attachments/assets/e49ba2e0-a8d1-4c1f-841e-982c40984e04


Click on the link below to view the video of our new features for Slackpoint 3.0

https://drive.google.com/file/d/1OU31ga5OA5_lIIkBelZQHMiCF4yW_JXB/view?usp=sharing

https://github.com/user-attachments/assets/5d816b4f-0f25-4b83-920b-55b98ff5ed98



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

### View the features in action:
https://drive.google.com/file/d/1bXHxav2GSvVzRXukVvgQunq2usONtrj1/view?usp=sharing

https://github.com/user-attachments/assets/0fa9a46d-cfbd-4c73-8a20-72bf704f742d

## NEW Features

Here is a list of features added during phase 3 of this project:

- **Request help:** Users can request help from other users for a specific task.
- **Daily standup notifications:** Quickly see who is working on what, recently completed work, and upcoming deadlines for each team member.
- **Set reminders for upcoming tasks:** Users can set reminders for upcoming tasks to stay on track.

## Features Description

| Num | Name                | Command                    | Description                                                                                       |
|-----|----------------------|----------------------------|---------------------------------------------------------------------------------------------------|
| 1   | Create new task     | `/create`                  | Creates a new task with a description, points, and deadline.                                      |
| 2   | Mark task as done   | `/task-done [task ID]`     | Marks a task as completed by the user who posted this command.                                    |
| 3   | View pending tasks  | `/viewpending`             | Displays a list of incomplete tasks; no parameters required.                                      |
| 4   | View completed tasks| `/viewcompleted`           | Displays a list of completed tasks; no parameters required.                                       |
| 5   | Leaderboard         | `/leaderboard`             | Displays the top performers on the channel along with their points; no parameters required.       |
| 6   | Help                | `/help`                    | Provides help for using SlackPoint commands; no parameters required.                              |
| 7   | Request Help        | `/requesthelp {id} {teammate} [other teammates...]` | Requests help from specified teammates on a particular task.   |
| 8   | Daily Standup       | [automated]                | Automatically sent to a specific channel at a configurable time, showing tasks per teammate.      |
| 9   | Set reminders       | `/create-reminder`         | Sets reminders for upcoming tasks.                                                                |


## Project documentation

The `docs` folder incorporates all necessary documents and documentation in our project.

Visit https://csc510-team-wise-vilkomir-sykes.github.io/Slackpoint-Docs/ for the html version of our documentation

## Tools used

Code formatter: black and flake8

## 📖 Getting started:

See [INSTALL.md](INSTALL.md)


Citation for [Slackpoint 2.0](https://github.com/kartikson1/slackpoint/blob/main/CITATION.md):
<br>Rathod, P., Soni, K., Mundra, N., Maheshwari, S., & Sinha, T. (2022, August 28). slackpoint Version (1.0.0). Retrieved November 1, 2024, from https://doi.org/10.5281/zenodo.7402494
