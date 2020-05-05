from datetime import time, timedelta

class Conference():
	'''
	Conference object with its properties and its functions.
	'''
	def __init__(self, n_days, start_time, end_time, cleaning_time, lunch_break):
		self.n_days = n_days
		self.n_talks = 0
		self.silence_time = timedelta(minutes=10000)
		self.order_talks = None
		self.start_time = timedelta(hours=start_time)
		self.end_time = timedelta(hours=end_time)
		self.start_break = timedelta(hours=lunch_break[0])
		self.end_break = timedelta(hours=lunch_break[1])
		self.cleaning_break = timedelta(minutes=cleaning_time)
		self.agenda = []

	def fit_talks(self, talklist):
		'''
		Function to fit talks into the agenda. 
		'''
		self.n_talks = talklist.n_talks()
		self.min_break_time(len(talklist.talk_50), len(talklist.talk_30), self.start_time, '', timedelta(minutes=0), self.n_days)
		self.create_agenda(self.order_talks, talklist)
		print(str(self.silence_time))

	def get_agenda(self):
		return self.agenda
	
	def is_in_break(self, start_time, duration):
		'''
		Check if 'start_time + duration' is in the lunch break
		'''
		return self.start_break < start_time+duration < self.end_break
	
	def is_final_talk(self, start_time, duration):
		'''
		Checks if the talk fits before the day ends.
		'''
		return start_time+duration >= self.end_time

	def is_last_talk_of_the_day(self, current_time, minutes, n_talk_duration):
		'''
		Check if the next talk in the pipelins fits after the current one.
		'''
		return current_time + minutes + self.cleaning_break + timedelta(minutes=int(n_talk_duration)*10) > self.end_time

	def add_cleaning_break(self, end_talk):
		'''
		Function to add cleaning breaks if needed.
		'''
		if self.is_in_break(end_talk, self.cleaning_break):
			return self.start_break - end_talk, self.end_break

		elif self.is_final_talk(end_talk, self.cleaning_break):
			return timedelta(minutes=0), end_talk

		return timedelta(minutes=0), end_talk + self.cleaning_break

	def get_silence(self, minutes, start_talk, day):
		'''
		Function to compute the minutes of silence and update with the start talk time for the next talk.
		Also, keeps tracks of the counting days.
		'''
		minutes = timedelta(minutes=minutes)

		if self.is_in_break(start_talk, minutes):
			return self.start_break - start_talk, self.end_break + minutes + self.cleaning_break, day

		elif self.is_final_talk(start_talk, minutes):
			return self.end_time - start_talk, self.start_time + minutes + self.cleaning_break, day - 1

		else:
			silence, start_talk = self.add_cleaning_break(start_talk + minutes)
			return silence, start_talk, day

	def min_break_time(self, n_50, n_30, start_talk, talk_order, minutes_silence, day):
		'''
		Function that fits talks minimizing the empty slots between talks. Saves the order as a string, 
		indicating '5' or '3' as the order of talks. Also, it saves the minutes of break for the optimal case.
		@params:
			n_50 and n_30: number of talks availble of 50 and 30 minutes respectively.
			start_talk: current time when the talk should start.
			minutes_silence: break minutes stored so far.
			day: days that are left to be filled. When it gets to 0, the program stops.
		'''
		if n_50 and day > 0:
			silence, start_next_talk, day = self.get_silence(50, start_talk, day)
			self.min_break_time(n_50 - 1, n_30, start_next_talk, talk_order + '5', minutes_silence + silence, day)

		if n_30 and day > 0:
			silence, start_next_talk, day = self.get_silence(30, start_talk, day)
			self.min_break_time(n_50, n_30 - 1, start_next_talk, talk_order + '3', minutes_silence + silence, day)

		elif len(talk_order) == self.n_talks:

			if self.silence_time > minutes_silence:
				self.order_talks = talk_order
				self.silence_time = minutes_silence

	def add_talk(self, tlist, duration, current_time):
		'''
		Function that adds talk to the correspondant time slot.
		'''
		if duration == timedelta(minutes=30):
			talk = tlist.pop_30()
		else:
			talk = tlist.pop_50()

		schedule = str(current_time) + ' -> ' + str(current_time + timedelta(minutes=int(talk.length)))
		self.agenda.append((schedule, talk.title, talk.speaker))
		current_time += duration 

		if not self.is_in_break(current_time, self.cleaning_break) and not self.is_final_talk(current_time, self.cleaning_break):

			schedule = schedule = str(current_time) + ' -> ' + str(current_time + self.cleaning_break)
			self.agenda.append((schedule, '-- Cleaning break --', '-- Cleaning break --'))
			current_time += self.cleaning_break

		return current_time

	def create_agenda(self, order, tlist):
		'''
		Function that creates the agenda loading each of the talks in the order as computed by order.
		'''
		current_time = self.start_time
		self.agenda.append(('----------','Day '+str(1),'----------'))
		n_day = 2

		for idx, element in enumerate(order):

			minutes = timedelta(minutes=int(element)*10)

			if self.is_in_break(current_time, minutes):
				schedule = str(self.start_break) + ' -> ' + str(self.end_break)
				self.agenda.append((schedule, '-- Lunch break--', '-- Lunch break--'))
				current_time = self.end_break

			elif self.is_final_talk(current_time, minutes):

				if n_day == self.n_days + 1:
					print('There were '+str(tlist.n_talks())+' talks that could not fit into the agenda.')
					break

				self.agenda.append(('----------','Day '+str(n_day),'----------'))
				n_day += 1
				current_time = self.start_time

			if idx < len(order) - 1:

				if self.is_last_talk_of_the_day(current_time, minutes, order[idx+1]):
					current_time = self.end_time - minutes

			elif idx == len(order) - 1:
				current_time = self.end_time - minutes

			current_time = self.add_talk(tlist, minutes, current_time)








