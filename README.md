<t style="font-size:30">Recipe Finder and Glucose Peak Calculator</t></br>
<t style="font-size:24">Final Project</t>

# Table of contents
- [Table of contents](#table-of-contents)
- [1. Developing guidelines](#1-developing-guidelines)
  - [1.1. Openning project in VS code](#11-openning-project-in-vs-code)
  - [1.2. Debugging with flask](#12-debugging-with-flask)
  - [1.3. Notes on development](#13-notes-on-development)
  - [1.4 Handling secret variables](#14-handling-secret-variables)
- [2. The project and its structure](#2-the-project-and-its-structure)

# 1. Developing guidelines

| Concept | Requirement        |
| ------- | ------------------ |
| Python  | version>=3.12      |
| IDE     | Visual Studio Code |

## 1.1. Openning project in VS code

1) Press `F1` to open command palette
2) Have Python 3.12.X installed
3) Search for "*Tasks: Run Build Task*" and click on it
4) Run the "*Environment Setup Task*", which will install all necessary dependencies and get the virtual environment ready
5) Press `F1` again and select interpreter as

## 1.2. Debugging with flask

1) Go to the debug pane (left bar in visual studio)
2) Find "*RUN AND DEBUG*" on the top of that pane (you will see a Play button and a *drop down* selector)
3) In that *drop-down* selector, chose `Python Debugger: Flask ({Project Name})`
4) Run it. It will launch flask in *debug mode* with *hot reload*.

## 1.3. Notes on development
- All necessary pip installs must be added to the requirements.txt, since will be used for the container setup aswell
- Changes in settings for this project must be done at "workspace" level so they are updated to all users

## 1.4 Handling secret variables

Secret variables like API keys, database credentials, and other sensitive information should be handled as follows:

- Create a `.env.local` file in the root directory of the project
- The `.env.local` file is already added to the `.gitignore` file so these secret variables don't get tracked.

><t style="font-size:16">***Warning!***</t></br>
>All sensitive information such as "API" keys, passwords or any login information which use is intended for testing or development should be stored inside this `env.local` file.

><t style="font-size:16">***Pending...***</t></br>
>Definition of where and how to store login information. For the purposes of this project, we will simply add them to the env file and handle them from there

# 2. The project and its structure

```bash
root/
│
├──.scripts/    # Scripts for helping task automations
│   └──env-setup.bash
│
├── requirements.txt    # Python dependencies
│
├──.vscode/     # VS Code specific settings
│   ├── launch.json         # Debug configurations
│   ├── settings.json       # Editor settings
│   ├── extensions.json     # Recommended VSCode extensions
│   └── tasks.json          # Build tasks
│
├──config/     #  Source code regarding different implementations, and
│   ├──".json" files        # Storing serialized information for the app
│   └──settings.yaml        # settings for the app deployment
│
├──src/        #  Source code regarding different implementations, and
│   │           # contains the libraries app.python will call,regarding   
│   │           # other API calls, models for information, helpers and 
│   │           # handlers, etc. 
│   │           
│   ├── API_interfaces/     # Classes in charge of handling external API communications
│   ├── commons/            # Helpers for different tasks
│   ├── db/                 # Classes in charge of handling the DataBase
│   └── models/             # Models for structuring information
│               
├──templates/  #  Directory holding the frontend part of the project,
│   │           # namely the code and resources for the web
│   │           
│   ├── css/            # Styles
│   ├── js/             # Frontent Javascript Code
│   ├── html/           # HTML pages
│   ├── resources/      # Resources for the site (such as logos, fonts, etc)
│   └── index.html      # Main directory, the one the app will launch
│
│
├── data.db     # Database storing historic data (recipes, glucose reports...)
├── app.py      # Main Flask application
│
├──tests/      # UnitTesting files (mainly for helping with a more TDD)
│
├──.logs/       # Generated logging files
│
├── .env                # Public environment variables (not sensitive)
├── .env.local          # Secret variables and credentials (sensitive)
│
└── .gitignore          # Git ignore rules

```
