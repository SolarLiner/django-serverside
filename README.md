# Serverside for Django

A mind-bending, highly experimental Django project to render JS applications from the server-side.

## How this works

Each request received by Django spawns a short-lived Node.js process, called with a path to a JS file, and the
 requested URL. Passed to standard input is the serialized context (QuerySet and Model instances included), as well
  as the length of the stdin data as `NODE_CTX_LEN` in the environment.
  
The Node.js script is expected to return the HTML contents to stdout, which is then echoed with the response.
 
## Test the prototype

In order to test the included test application, you need Python 3.7 (including `pipenv`, as well as Node.js 10 (or
 higher).

Run `yarn install` to install the Node.js dependencies, then `pipenv install --dev` to install the Python dependencies.
Migrate the SQLite database with `pipenv run python manage.py migrate`, and then launch the Django server with
 `pipenv run python runserver`. Enjoy!
