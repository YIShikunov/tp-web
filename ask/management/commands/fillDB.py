from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from ask.models import Question, Answer, Tag, UserAccount, User
import random

def generateTags(n):
	import urllib2
	url = "http://randomword.setgetgo.com/get.php"
	for i in range(n):
		urldata = urllib2.urlopen(url)
		word = urldata.readlines()[0][:-2] #removed \r\n
		tag = Tag(tagName=word)
		#print word, tag
		tag.save()
		if i % 5 == 0:
			print i

def generateUsers(n):
	import urllib2, hashlib
	nickWords = ["Void", "Facelessness", "OMG", "_xxxMLGxxx_", "lox", "zeus", "warlock", "murlock", "YoLo", "YoYo", 
		"rwl_lll_rl", "Flash", "Batman", "Bat", "mobile", "rang", "l33t", "h@xx0r", "Orange", "Annoying", "Apple", "Hey",
		"dummy", "stuff", "annoy", "word", "Shadow", "Ivan", "Vladimir", "ROFL", "Enigma", "Rubick", "cube", "Cube",
		"Horadirc", "Deckard", "Kain", "user", "version", "test", "hello", "world", "master", "HealBot", "Loatheb", "jinxed"] + [""]*5
	nameWords = ["Ivan", "Leah", "Deckard", "Tyrael", "Nova", "Sarah", "Jim", "Tassadar", "Zeratul", "Azmodan"] + [""]*10
	surnameWords = ["Chrono", "Kain", "ArchangelOfJustice", "Terra", "Kerrigan", "Raynor", "SaviorOfTemplar", "LordOfSin"] + [""]*9
	for i in range(n):
		username = random.choice(nickWords) + random.choice(nickWords) + str(random.randint(i, i*10+10))
		password = ''.join([random.choice("qwertyuiopasdfghjklzxcvbnm!@1234567890") for t in range(16)])
		email = random.choice(nickWords) + random.choice(username) + '@' + random.choice(["mail.ru"] + ["mailinator.com"]*10) 
		firstName = random.choice(nameWords)
		lastName = random.choice(surnameWords)
		avatarSize = 100
		gravatarUrl = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
		gravatarUrl += "d=identicon&s=100"
		av = urllib2.urlopen(gravatarUrl)
		tmpFile = open("tmp", "w")
		tmpFile.write(av.read())
		tmpFile.close()
		av = open("tmp", "r")
		av = File(av)
		usr = User(username=username, password=password, email=email, first_name=firstName, last_name=lastName)
		usr.save()
		usrAccount = UserAccount(user=usr, avatar = av, rating = random.randint(1, 10))
		usrAccount.save()
		av.close()
		if i % 5 == 0:
			print i

def generateQuestions(n):
		questionStarts = ["Who", "How", "Why", "When", "Please"]
		questionAction = ["can", "should", "to", "may", "do"]
		questionActor = ["I", "my mom", "django", "python", "diablo", "god", "protoss", "terran", "zerg"]
		questionStuff = ["kill", "compile", "clear", "solve", "install", "banish", "love", "hug", "complete", "do", 
				"make", "enjoy", "start", "delete"]
		questionActee = ["zerg infestation", "django", "c++ code", "a barell roll", "my mom", "my friend", "server",
				"president", "iPhone", "iPad", "windows", "file in linux", "legolas", "world domination",
				"illuminati", "forum", "summit", "eSports", "DOTA2", "idiotism", "protoss arrogance"]
		questionEnd = ["?", "don't tell my mom!!1?", "111", "!!!", "!", "??", "???", "!!", "??!!?", ""]
		questionText = ["I really need help", "HELP ME PLEASE", "It's gonna eat me", "I can't live without this", "I am heartbroken"]
		questionTextEnd = ["i wanna help ASAP!", "tell me or i'm calling cops!", "i hope someone will answer me.", "Anyone?"]
		tags = Tag
		for i in range(n):
			title = random.choice(questionStarts)+" "+random.choice(questionAction)+" "+random.choice(questionActor)+\
			" "+random.choice(questionStuff)+" "+random.choice(questionActee)+" "+random.choice(questionEnd)
			text = random.choice(questionText)+" "+random.choice(questionTextEnd)
			author = UserAccount.objects.all().order_by('?')[0]
			q = Question(name = title, content = text, author = author)
			q.save()
			j = random.randint(1, 10)
			for t in Tag.objects.all().order_by('?')[:j]:
				q.tags.add(t)
			q.save()
			if i % 50 == 0:
				print i

def generateAnswers(n):
	for i in range(n):
		start = ["Do ", "Get ", "Leave ", "Remove ", "Press ", "Don't ", "Use ", "EXTERMINATE!!!! ", "Kill ","Banish ", "Love ", "Hug ",
			 "Complete ", "Do ", "Make ", "Enjoy ", "Start ", "Delete ", "Keep Calm "]
		mid = ["a barrel roll", "your mom", "the configs", "the Force", "the attack", "that RED button", "your wits", "WD-40", "duct tape", 
			"card", "EXTERMINATE!!! ", "some noise", "the show", "and go on"]
		end = [", Luke.", ", noob!", ", man!", " or you're screwed.", "!", "br@h!", "EXTERMINATE?!"] + [".", "?", "!"]*2
		ansText = random.choice(start) + random.choice(mid) + random.choice(end) + '(' + str(random.randint(1,1000000)) + ')'
		author =  UserAccount.objects.all().order_by('?')[0]
		approved = random.choice([True] + 5 * [False])
		question = Question.objects.all().order_by('?')[0]
		ans = Answer(content = ansText, author = author, approved = approved, question = question)
		ans.save()
		if i % 500 == 0:
			print i

class Command(BaseCommand):
	args = '<type> <count>'
	help = 'Fills the database with some data'
	
	def add_arguments(self,parser):
		parser.add_argument('type')
		parser.add_argument('count')

	def handle(self, *args, **options):
		type = options['type']
		count = int(options['count'])
		if type == "tags":
			generateTags(count)
		elif type == "users":
			generateUsers(count)
		elif type == "questions":
			generateQuestions(count)
		elif type == "answers":
			generateAnswers(count)

