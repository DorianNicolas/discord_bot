import random

import discord

from module import *
import utils.utils
import utils.constants as const
import utils.aws_utils as s3

import os
import asyncio

class Quiz:

	def __init__(self, client, default=10):

		self.__running = False #Is the quiz active or not
		self.current = None
		self._client = client
		self.default = default
		self.filepath = []
		self.lenqst = None
		self.question = []
		self.answer = []

		Quiz.loadquestions(self)

	def loadquestions(self):
		with open("./quizdatabase/quiz_database.csv", "r") as self.filepath:
			lines = self.filepath.readlines()

		print("Questions successfully loaded.")
		position = 0
		question = None
		answer = None
		data = None
		
		while position < len(lines):
			data = lines[position].split('\\')
			if len(data) != 2:
				position += 1
			else:
				question = data[0]
				answer = data[1]
			if lines[position].strip() == '':
				if question is not None and answer is not None:
					q = Question(question=question, answer=answer)
					self.question.append(q)
			question = None
			answer = None
			position += 1
			continue
		position += 1
	def started(self):
		print(self.__running)
		return self.__running

	async def start(self, bot, number):
		if number <= 0:
			await bot.say('Le nombre de question doit être supérieur ou égal à 1.')
		else:
			if Quiz.started(self):
				await bot.say('Un quiz est déjà en cours, veuillez attendre la fin de celui-ci pour lancer un quiz.')
			else:
				#await bot.say('@here\n:loudspeaker:\n**Début du quiz dans 1 minute.**')
				self.__running = True
				self.current = None
				#await asyncio.sleep(45)
				#await bot.say('@here\n:loudspeaker:\n**Début du quiz dans 15 secondes.**')
				#await asyncio.sleep(15)
				await bot.say('Début du quiz ici')
				#await bot.say(number)
				#await Quiz.askqst(self, bot)

	async def stop(self, bot):
		if Quiz.started(self):
			await bot.say('Arrêt du quiz en cours. Pour en relancer un !startquiz')
			self.__running = False
		else:
			await bot.say('Aucun quiz en cours. !startquiz pour en lancer un.')

	#async def askqst(self, bot):
	#	if self.__running:
			
class Question:

	def __init__(self, question, answer):
		self.question = question
		self.answer = answer