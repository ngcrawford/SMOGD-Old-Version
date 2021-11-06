## How to run locally

First clone this repo, navigate the root directory, then run this command.

1. Install the conda *smog-old* environment. Note that it's crucial that django be version 1.1.3.

		conda create -n smogd-old --file smogd-old-packages.txt

2. Activate the environment

		conda activate smogd-old

3. Execute the *runserver* command

		python django/myproject/manage.py runserver

4. Go to: http://127.0.0.1:8000/jost/