# Installation

First, create a virtual enviroment this avoid the crash of your projects if u are working on diferent project

> python -m venv venv

Now we need to activate the virtualenv, i asume you are using a mac so it should be:

> source venv/bin/activate

we going to install all the dependencies.

> pip install -r requirements.txt

We going to initialize the database.

>python manage.py makemigrations

> python manage.py migrate

Now that the database is initialized you can replace with the one in original_records.zip

In case you want to enter new input:

use the comment funcions on main.py 

Tip: you can rename the databases and modify the file on min_max_database_config with the new name so you don't have to substitute the file every time you want 
to modify the data.

Tip: You can install db browser for sqlite so you can see and delete data easily, even insert from a csv.