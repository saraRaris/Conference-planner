class TalksList():
	'''
	Talk list to store talks for the conference.
	'''
	def __init__(self):
		self.talk_30 = []
		self.talk_50 = []
		self.l_30 = len(self.talk_30)
		self.l_50 = len(self.talk_50)

	def add_talk(self, talk):
		if int(talk.length) == 30:
			self.talk_30.append(talk)
			self.l_30 += 1

		elif int(talk.length) == 50:
			self.talk_50.append(talk)
			self.l_50 += 1

		else:
			print('There is no talk allowed with that talking length.')

	def n_talks(self):
		return len(self.talk_30 + self.talk_50)

	def get_talk_by_name(self, name):
		for talks in (talk_30 + talk_50):
			if talk.name == name.strip():
				return talk
		return 'Not found'

	def pop_50(self):
		self.l_50 -= 1
		return self.talk_50.pop()

	def pop_30(self):
		self.l_30 -= 1
		return self.talk_30.pop()

class Talk():
	'''
	Object to handle individual Talks
	'''
	def __init__(self, title, length, speaker):
		self.title = title
		self.length = length
		self.speaker = speaker