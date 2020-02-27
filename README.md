# CS/INFO 4300 Django Starter Template

This is an alternative to the Flask template which provides a simple website framework using Django. *We will provide minimal support for this template*; it is intended for groups with prior Django experience or with more complicated use cases that don't fit well with Flask. 

You should follow the quickstart instructions below which will provide you with a functional web app which you can push to Heroku. Instructions on how to push to Heroku are also provided below. Google Cloud support an instructions are still to come.

If you have any questions dont hesistate to ask the TAs or come to office hours!

## Quickstart Guide
### 1. Cloning the repository from Git
```bash
git clone https://github.com/CornellNLP/CS4300-Django-template.git
cd CS4300-Django-template
```

### 2. Setting up your virtual environment
We assume by now all of you have seen and used virtualenv, but if not, go [here](https://virtualenv.pypa.io/en/stable/installation/) to install and for dead-simple usage go [here](https://virtualenv.pypa.io/en/stable/installation/)

```bash
# Create a new python3 virtualenv named venv.
virtualenv -p python3 venv
# Activate the environment
source venv/bin/activate

# Install all requirements
pip install -r requirements.txt
```
An aside note: In the above example, we created a virtualenv for a python3 environment. You will have python3.7.6 installed by default as we have used that version for assignments. This is what we will use for the application as well.

**NOTE: While you should be able to install these requirements in the virtualenv you used for the assignments, we advise using a fresh virtualenv so you can be sure that your virtualenv's installed packages and your repository's `requirements.txt` match exactly. 
This will be important when you add new dependencies.**

If you wish to add any dependencies for future development just do this:

```bash
pip install <MODULE_NAME>
pip freeze > requirements.txt
```

### 3. Run Django
You should now be able to run the Django template. Run it as follows:
```bash
python manage.py runserver
```

If your server, it should see output in your terminal which looks something like this:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

February 27, 2020 - 03:35:20
Django version 3.0.3, using settings 'app.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

## Useful Commands
### Setting up the database
The template does not come packaged with any models - however, when you add new models to your app or modify existing ones, you will need to update your database accordingly. You can do this as follows.
```bash
python manage.py makemigrations
python manage.py migrate --run-syncdb
```

## Deployment to Heroku
Heroku is a platform as a service (PaaS) that enables developers to build and run applications entirely in the cloud. We can easily deploy our Django app in minutes on Heroku. You can do this almost exclusively from the terminal:

- First, install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
- Create a Heroku account
- Login to your account locally, using
    ```sh
    heroku login
    ```
- Revise the `requirements.txt` file if you added any new packages (use the `pip freeze` command described in the setup instructions)
- Create an app on Heroku
    ```sh
    heroku create <your_project_name>
    ```
- Disable `collectstatic` running during project deployment
    ```sh
    heroku config:set DISABLE_COLLECTSTATIC=1
    ```
- Push your project to Heroku
    ```sh
    git push heroku master
    ```
- Run migrations on the server
    ```sh
    heroku run python manage.py migrate
    ```
- Check that at least one instance of the app is running
    ```sh
    heroku ps:scale web=1
    ```
- Now you should be able to visit your web app! Go to `https://<your_project_name>.herokuapp.com`. Be patient, it sometimes takes a while for Heroku to spin up your server.