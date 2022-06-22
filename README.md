# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

For Trello api integration, set up a trello account, and add values to the file for the following: TRELLO_API_KEY, TRELLO_TOKEN, TRELLO_BOARD_ID

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Running the tests

Tests can be run by using:
```bash
$ poetry run pytest
```

## Running on a VM

* Copy the inventory, todoapp.service and ansible-playbook.yml files over to your control node (or clone the entire repo)
* [Set up SSH](https://www.ssh.com/academy/ssh/copy-id) from the control node to the managed node 
* Edit the inventory file to contain all IP addresses of your managed nodes you want to set up
* Ensure ansible is installed on the control node: 
    * Install:  `sudo pip install ansible`
    * Check installation:  `ansible --version`
* Run the playbook: `ansible-playbook ansible-playbook.yml -i inventory`
* Check the service is running on the managed nodes

## Running inside a docker container:
### Development:
Build the image:
```bash
$ docker build --target development --tag todo-app:dev .
```
Run the image:
```bash
$ docker run --env-file ./.env -p 5000:5000 --mount type=bind,source="$(pwd)"todo_app,target=/app/todo_app todo-app:dev
```

### Production:
Build the image:
```bash
$ docker build --target production --tag todo-app:prod .
```
Run the image:
```bash
$ docker run --env-file ./.env -p 80:80 --mount type=bind,source="$(pwd)"todo_app,target=/app/todo_app todo-app:prod
```

### CD pipeline:
If the build completes and the tests pass, the app will be automatically deployed to Heroku. 
The url for the app is: https://peter4137-todo-app.herokuapp.com/