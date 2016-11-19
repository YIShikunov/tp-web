from django.shortcuts import render
from django.template import RequestContext, loader
from django import forms
from django.http import HttpResponseRedirect
from django.core.files import File
from ask.models import User, Question, Answer, Tag, UserAccount
import random, os

def index(request):
	return page(request, 1)

def page(request, page_num):
	page_num = int(page_num)
	context = {
		"questions":Question.objects.all().order_by('-author__rating', 'creationDate')[(int(page_num)-1)*20:int(page_num)*20],
		"current_page": page_num,
		"page_nums": range(max(1, page_num-2),page_num+5)[:5],
	}
	return render(request, "page.html", context)

def hot(request):
	return page(request, 1)

def hot_page(request, page_num):
	return page(request, page_num)

def tag_page(request, tagName, page_num):
	page_num = int(page_num)
        context = {
                "questions":Question.objects.all().filter(tags__tagName=tagName).order_by('-author__rating', 'creationDate')[(int(page_num)-1)*20:int(page_num)*20],
                "current_page": page_num,
                "page_nums": range(max(1, page_num-2),page_num+5)[:5],
        }
        return render(request, "page.html", context)

def tag(request, tagName):
	return tag_page(request,tagName,1)

def show_question(request, question_id):
	q = Question.objects.get(id=question_id)
	context = {
		"question": q,
		"answers": Answer.objects.filter(question=q),
	}
	return render(request, 'quest_page.html', context)

class SignupForm(forms.Form):
	username = forms.CharField(label="Username:", max_length=50)
	email = forms.EmailField(label="Email:")
	password = forms.CharField(widget=forms.PasswordInput)
	first_name = forms.CharField(required=False, max_length=100)
	last_name = forms.CharField(required=False, max_length=100)
		  
def signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			#f = form.cleaned_data
			#raise form.cleaned_data
			#kw = {
			#  "username": form.fields['username'],
			#  "password": form.fields['password'],
			#  "first_name": form.fields['first_name'],
			#  "last_name": form.fields['last_name'],
			#  "email": form.fields['email'],			  
			#}
			try: 
			      u = User.objects.create_user(**(form.cleaned_data))
			      u.save()
			except:
			      raise #forms.ValidationError('Username or email already taken')
			avatar_dir = "/var/www/askproject/uploads/avatars/"
			av = avatar_dir + random.choice(os.listdir(avatar_dir))
			av = File(open(av, 'rw'))
			user_data(avatar=av, rating=0, user=u).save()
			return HttpResponseRedirect('/')
	else:
		form = SignupForm()
		
	return render(request, 'signup.html', {'form': form})
      
      
class AskQuestionForm(forms.Form):
	title = forms.CharField(label="Title:", max_length=300)
	content = forms.CharField(label="Text:", widget=forms.Textarea)
	tags = forms.CharField(label="Tags (comma-separate):", max_length=100)
	

def ask(request):
	if request.method == 'POST':
		form = AskQuestionForm(request.POST)
		if form.is_valid() and request.user.is_authenticated():
			kw = {
			      "name": form.cleaned_data["title"],
			      "content": form.cleaned_data["content"],
			      "author": request.user,
			}
			q = question(**kw)
			q.save()
			for tg in form.cleaned_data["tags"].split(","):
				tg_c = tg.replace(" ", "")
				t = Tag.objects.all().filter(tagName=tg_c)
				if t:
					q.tags.add(t[0])
				else:
					t = Tag(tagName=tg_c)
					t.save()
					q.tags.add(t)
			return HttpResponseRedirect('/question/' + str(q.id))
	else:
		form = AskQuestionForm()
		
	return render(request, 'ask.html', {'form': form})

class AnswerQuestionForm(forms.Form):
	content = forms.CharField(label="Answer:", widget=forms.Textarea)
	

def give_answer(request, question_id):
	q = None
	try:
	      q = Question.objects.all().get(id=question_id)
	except:
	      return HttpResponseRedirect('/')
	      
	if request.method == 'POST':
		form = AnswerQuestionForm(request.POST)
		if form.is_valid() and request.user.is_authenticated():
			kw = {
				"content": form.cleaned_data["content"],
				"author": request.user,
				"question": q,
			}
			a = answer(**kw)
			a.save()
			return HttpResponseRedirect('/question/' + str(question_id))
	else:
		form = AnswerQuestionForm()
		
	return render(request, 'answer.html', {'form': form, 'question': q})
