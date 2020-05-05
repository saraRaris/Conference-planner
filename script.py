import csv, argparse
from talks import Talk, TalksList
from conference import Conference
import pdb

def main():
	ap = argparse.ArgumentParser()
	ap.add_argument("-p", "--path", required=True, help="path csv file containing talks")
	args = vars(ap.parse_args())

	# Load arguments
	file_name = args['path']

	# Global variables
	n_days = 3 # (days)
	starting_time = 9 # (hours)
	closing_time = 17 # (hours)
	cleaning_break = 15 # (minutes)
	lunch_break = [12,13] # (hours)

	# Create talk list object
	tList = TalksList()

	# Load list of talks into the TalkList object
	with open(file_name, newline='') as csvfile:
		talksreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for idx, row in enumerate(talksreader):
			if idx == 0:
				pass
			else:
				tList.add_talk(Talk(row[0], row[1], row[2]))

	# Create Conference object
	conf = Conference(n_days, starting_time, closing_time, cleaning_break, lunch_break)

	# Fit list of talks into the conference
	conf.fit_talks(tList)

	# Load Agenda and print it
	agenda = conf.get_agenda()
	for row in agenda:
		print(row)

if __name__ == '__main__':
	main()
