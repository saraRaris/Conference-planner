# Read Me

## Excerisce description
We create a new startuo for conference planning. Now we need an automated way for creating the conference schedule.

**Preconditions:**

* Talks should be imported from a CSV
* Talks are either 30 or 50 min long
* There is a lunch break between 12 and 13 o'clock each day

**Solution:**

The solution should generate a conference plan that minimizes empty slots and breaks between talks. Each day should feature a talk starting at 9 o'clock and another talk ending at 17 o'clock.
The output should be a table that lists all talks for all days.

## Instrucions

In this repository the following files can be found:

* A .py file : ```script.py```.
* A .py file: ```talks.py ``` defining the classes related to the talks.
* A .py file: ``conference.py`` defining conference class.
* A .csv file: ``conferences.csv`` with a sample list of talks.


To run this program please enter the following command on the terminal:
	
	python script.py --path [PATH_TO_CSV_FILE]

Two assumptions have been considered to develop the solution:

1. A talk ending just before the lunch break or before of the end of the conference day does not have a reserved cleaning slot, hence those were not applied.

2. Break time was considered only the time where it was not possible to fit a new talk. Cleaning slots or lunch break were not considered as such.
