<---------------------------------------------------------------------------------------------------------------------------------------------------------->
▀║==========================================================================================================================================================║
............................«« ABOUT »».....................................................................................................................
▀║==========================================================================================================================================================║
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤

The app is a running model for a rudimentary Ticket Booking Show that implements RBAC and allows admins to manage Theaters, Movies and map Shows (Theater and Movie). The app also allows Users to search for movies and get shows for the same, get available slots for a show and book seats to view it.

A "SHOW" is considered an instance of a Theater and a Movie at a given time. For Example: Given a Movie: "Movie" and a Theater: "Theater", a "SHOW" is defined as:

SHOW : Movie hosted at Theater between 24th to 28th of July, everyday at 8pm.

Each day of the show is considered as an object of show itself and used for keeping track of availability of seats for upcoming show instance objects.

├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
║==========================================================================================================================================================║
...........................«« REQUIREMENTS »»...............................................................................................................
▀║==========================================================================================================================================================║
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤

1. Python 3.10 or higher
2. Python Packages like Flask as mentioned in the requirements.txt
3. Redis 6.0.16 or higher
4. celery 5.3.1 (emerald-rush)

To quickly install all required dependencies given that pip is installed, run the following code in termminal:

	pip install -r requirements.txt


Note: For the line to work, pip must be installed

Refer to the HELP section for any further help regarding installations.

├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
║==========================================================================================================================================================║
...........................«« STEPS TO RUN »»...............................................................................................................
▀║==========================================================================================================================================================║
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤

1. Open the local/online IDE and load the files and folder to it. DO NOT disturb the folder structure.
2. Simply run the main.py file.
3. In the terminal click on the host address or go to a preferred browser and paste: ("http://127.0.0.1:5000/") to run the web app.


- To run the file using a terminal:
	1. Change the current directory to the one containing the folders and main.py
	2. Type the following command:
     		python main.py
 	or
     		python3 main.py

- To run redis:
	1. Install the resources (or run requirements.txt)
	2. simply run the following code in a terminal
		redis-server

- To run celery:
	1. Install the resources and dependencies
	2. Navigate to the root folder using the terminal
	3. Run the following code to run the Workers:
		celery -A main.cel worker

	4. Run the following code to run celery beat:
		celery -A main.cel beat

├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
║==========================================================================================================================================================║
...........................«« HELP »»...............................................................................................................
▀║==========================================================================================================================================================║
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤

1. To install all required dependencies follow the following steps:
	
	- pip : A package installer
		Installation Steps: https://pip.pypa.io/en/stable/installation/

	- python: Installation Steps: https://realpython.com/installing-python/

	NOTE: All other required dependencies are listed in requirements.txt and can be directly installed after installing pip using the following command
	- pip install -r requirements.txt

2. To setup python virtual enviornment to run the same:
	- Windows/linux: https://www.geeksforgeeks.org/creating-python-virtual-environment-windows-linux/
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
<---------------------------------------------------------------------------------------------------------------------------------------------------------->
NOTE:
Use Insomnia to open YAML file

Hope the following Resources help. ENJOY!

To report bugs, contact me:
21f2000602@gmail.com