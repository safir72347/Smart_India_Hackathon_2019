from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import HOME, HEAD, ABOUTUS, FOOTER, ARTICLE, REGISTER,  QUESTIONS, ANSWERS, slider, cards, AGGREGATED_DATA
# from nltk import word_tokenize
# from nltk.corpus import stopwords
# from nltk.stem import PorterStemmer
from .models import NewPage
import time
import requests as ay_rq
from bs4 import BeautifulSoup


flag = 0
# Create your views here.
# def tag_gen(tmp):
# 	ps=PorterStemmer()
# 	question=[]
# 	answer=[]
#
# 	qid=tmp
# 	question.append(tmp.Heading)
# 	answer.append(tmp.Description)
# 	answer1=" ".join(answer)
# 	question1=" ".join(question)
# 	question1=question1.lower()
# 	answer1=answer1.lower()
# 	answer=word_tokenize(answer1)
#
# 	stop=set(stopwords.words('english'))
# 	faltu=[',','.','hello','hi']
# 	for w in faltu:
# 		stop.add(w)
# 	question=word_tokenize(question1)
# 	tags=[]
# 	for word in question:
# 		m=ps.stem(word)
# 		tags.append(m)
# 	words=''
# 	partial_token=[]
# 	for words in tags:
# 		if words not in stopf:
# 			partial_token.append(words)
# 	tags=[]
# 	for words in partial_token:
# 		if words not in tags:
# 			tags.append(words)
#
# 	taga=[]
# 	for word in answer:
# 		taga.append(ps.stem(word))
# 	partial_token=[]
# 	for words in taga:
# 		if words not in stop:
# 			partial_token.append(words)
# 	words=''
# 	for words in partial_token:
# 		if words not in tags:
# 			tags.append(words)
# 	return tags

def login(request):

	global flag
	if request.method == "POST":
		data = request.POST
		if data['login_popup']:
			em = data['email']
			pa = data['password']
			r = REGISTER.objects.filter(Email=em, Password=pa)
			if(len(r)>0):
				flag=1
				request.session["login"] = True
				request.session["account_name"] = str(r[0].First_name + " " + r[0].Last_name)
				request.session["phone"] = str(r[0].Phone)
				request.session["email"] = str(r[0].Email)
				request.session['username'] = str(r[0].Email)
				request.session['account_name'] = str(r[0].First_name + " " + r[0].Last_name)
				request.session["institution"] = str(r[0].Institution)
				print(request.session)


		return redirect("/home/")

def home(request):

	if request.method =="POST":
		print("in here")
		data = request.POST
		try:
			if data['sub_popup']:
				print("in sub popup")
				article = ARTICLE(Heading = data['head1'], Description = data['des1'], User = request.session["account_name"])
				article.save()
				tmp=ARTICLE.objects.all().last()
				l=tag_gen(tmp)
				l1 = " ".join(l)
				tmp = ARTICLE.objects.all().last()
				tmp.tags = l1
				a=time.ctime()
				a=a[0:10]+a[19:]
				tmp.Time_date=a
				tmp.save()

		except Exception as e:
			print("exception",e)
	length=0
	context = {}

	try:
		print("TRY: ", request.session["account_name"])
	except Exception as e:
		print("Catch")
		request.session["account_name"] = ""

	home = HOME.objects.all()
	l = len(home)
	tmp=ARTICLE.objects.all()
	context = {'company_name':home[l-1].Company_name, 'caption':home[l-1].Caption,
	 'back_img': home[l-1].Back_img, 'curosal1': home[l-1].Curosal1,
	  'curosal2': home[l-1].Curosal2, 'news_title': home[l-1].News_title,
	   'news_img': home[l-1].News_img, 'News_des': home[l-1].News_des, 'account_name':request.session["account_name"]}
	tmp=(ARTICLE.objects.all()).reverse()
	if len(tmp)!=length:
		context["tmp"]=tmp
		length=len(tmp)
	print("request.session: ", request.session)
	return render(request,'home.html',context)

def about(request):

	context = {}
	aboutus = ABOUTUS.objects.all()
	l = len(aboutus)
	context = {'about_us': aboutus[l-1].About_us, 'aim': aboutus[l-1].Aim, 'content': aboutus[l-1].Content, 'image': aboutus[l-1].Image, 'developer': aboutus[l-1].Developer }
	return render(request,'aboutus.html',context)

def forum(request):

	print("request.session: ", request.session['email'])

	if request.method == "POST":
		print("In here")
		print(request.POST.get('question'))
		print(request.POST.get('description'))
		question_entry = QUESTIONS(user_email=request.session["email"], question=request.POST.get('question'), description=request.POST.get('description'), likes=0, dislikes=0, reports=0)
		print(question_entry)
		question_entry.save()
		return redirect("/forum/")

	print("Questions", QUESTIONS.objects.all())

	return render(request, 'forum.html',{})

# def edit(request):
# 	context={}
# 	foot1=FOOTER.objects.all()
# 	l=len(foot1)
# 	context['disclaimer'] = foot1[len(foot1)-1].Disclaimer
# 	print(foot1[len(foot1)-1].Disclaimer)
# 	context['email']=foot1[len(foot1)-1].Email
# 	context['phone']=foot1[len(foot1)-1].Phone
# 	context['facebook']=foot1[len(foot1)-1].Facebook
# 	context['twitter']=foot1[len(foot1)-1].Twitter
# 	context['google']=foot1[len(foot1)-1].Google
# 	context['instagram']=foot1[len(foot1)-1].Instagram
# 	context['terms']= foot1[len(foot1)-1].Terms
#
# 	return render(request,"admin_footer.html",context)


def news(request):
	print("****************")
	if request.POST.get('Signup1')=="Add slider":
		print("**********")
		data=request.POST
		recent=slider(slider_heading=data["slider_heading"], slider_caption=data["slider_caption"], image_link=data["image_link"])
		recent.save()

	if request.POST.get('Signup2') == "Submit":
		data=request.POST
		recent=cards(heading=data["heading"], image1_link=data["image1_link"], contents=data["contents"] )
		recent.save()

	context={}
	new1=AGGREGATED_DATA.objects.all()
	context['obj_list']=new1


	'''context={'slider_heading':recent.slider_heading}
	context={'slider_caption':recent.slider_caption}
	context={'image_link':recent.image_link}
	print(recent.slider_heading)'''

	new=slider.objects.all()
	id = len(new)

	'''print(new[id-1].id)
	context['slider_heading']=new[id-1].slider_heading
	context['slider_caption']=new[id-1].slider_caption
	context['image_link']=new[id-1].image_link
	print(new)
	print(new[id-1].image_link)'''
	list = []

	for x in range(len(new)):
		list.append(x+1)
		print(new[x].id)
		print(new[x].image_link)
		context["central_image_link"] = new[x].image_link

	print(list)
	print(new1)

	context['sliders'] = new
	context['list_of_numbers'] = list
	context['id'] = id

	print("agd_id:", new1[0].agd_id)

	return render(request, "latest_news.html",  context)

def user_profile(request):
	return render(request, 'profile.html',{})

def admin_home(request):
	if request.method == "POST":
		data = request.POST
		home = HOME(Company_name = data['company_name'], Caption = data['caption'], Back_img = data['back_img'], Curosal1 = data['curosal1'], Curosal2 = data['curosal2'], News_title = data['news_title'], News_img = data['news_img'], News_des = data['news_des'])
		home.save()
	return render(request, 'admin_home.html',{})

def admin_header(request):
	if request.method =='POST':
		data = request.POST
		head = HEAD(App_link = data['app_link'], Login_link = data['login_link'])
		head.save()
		head1=HEAD.objects.all()
		l = len(head1)
		context = {'applink':head1[l-1].App_link, 'loginlink': head1[l-1].Login_link}
		return render(request, 'header.html', context)
	return render(request, 'admin_header.html',{})

def admin_navbar(request):
	return render(request, 'admin_navbar.html',{})

def admin_footer(request):
	context={}
	foot1=FOOTER.objects.all()
	l=len(foot1)
	context['disclaimer'] = foot1[len(foot1)-1].Disclaimer
	print(foot1[len(foot1)-1].Disclaimer)
	context['email']=foot1[len(foot1)-1].Email
	context['phone']=foot1[len(foot1)-1].Phone
	context['facebook']=foot1[len(foot1)-1].Facebook
	context['twitter']=foot1[len(foot1)-1].Twitter
	context['google']=foot1[len(foot1)-1].Google
	context['instagram']=foot1[len(foot1)-1].Instagram
	context['terms']= foot1[len(foot1)-1].Terms

	if request.method=="POST":
		data = request.POST
		foot = FOOTER(Disclaimer=data['disclaimer'], Email=data['email'], Phone=data['phone'], Facebook=data['facebook'], Twitter=data['twitter'], Google=data['google'], Instagram=data['instagram'], Terms=data['terms'])
		foot.save()
		foot1 = FOOTER.objects.all()
		l = len(foot1)
		context = {'disclaimer':foot1[l-1].Disclaimer, 'email':foot1[l-1].Email, 'phone':foot1[l-1].Phone, 'facebook':foot1[l-1].Facebook, 'twitter':foot1[l-1].Twitter, 'google':foot1[l-1].Google, 'instagram':foot1[l-1].Instagram, 'terms': foot1[l-1].Terms}
		return render(request, 'footer.html', context)

	return render(request, 'admin_footer.html',{})

def admin_latestnews(request):
	return render(request, 'admin_latestnews.html',{})

def admin_profilepage(request):
	return render(request, 'admin_profilepage.html',{})

def admin_aboutus(request):
	if request.method == 'POST':
		data = request.POST
		aboutus = ABOUTUS(About_us = data['about_us'], Aim = data['aim'], Content = data['content'], Image = data['image'], Developer = data['developer'])
		aboutus.save()
	return render(request, 'admin_aboutus.html',{})

def admin_registerpage(request):
	return render(request, 'admin_registerpage.html',{})

def admin_category(request):
	return render(request, 'admin_category.html',{})

def register(request):
	if request.method=="POST":
		data = request.POST
		pass1 = data['password']
		pass2 = data['password1']
		if pass1==pass2:
			reg = REGISTER(First_name = data['first_name'], Last_name = data['last_name'], Gender = data['gender'],
			Email = data['email'], Password = data['password'], Institution = data['institution'], Phone = data['phone'],
			Date = data['date'], OTP = data['otp'])
			reg.save()
			return render(request,'home.html',{})
		else:
			context = {'print_status': "Passwords don't match. Enter again!!!" }
			return render(request, 'register.html', context )
	return render(request,'register.html',{})

def header(request):
	return render(request, 'header.html', {})

def logout(request):

	request.session["account_name"] = False
	request.session["login"] = False
	return redirect('/home/')

# def news(request):
#
# 	print("****************")
# 	if request.POST.get('Signup') == "Submit":
# 		data=request.POST
# 		recent=SLIDER(slider_heading=data["slider_heading"], slider_caption=data["slider_caption"], image_link=data["image_link"], heading=data["heading"], image1_link=data["image1_link"],contents=data["contents"])
# 		recent.save()
# 	'''context={'slider_heading':recent.slider_heading}
# 	context={'slider_caption':recent.slider_caption}
# 	context={'image_link':recent.image_link}
# 	print(recent.slider_heading)'''
#
# 	new=SLIDER.objects.all()
# 	id = len(new)
# 	print(new[id-1])
# 	data1=new[id-1].slider_heading
# 	data2=new[id-1].slider_caption
# 	data3=new[id-1].image_link
# 	print(data3)
# 	print(new[id-1].image1_link)
# 	context={'slider_heading': data1, 'slider_caption': data2, 'image_link': data3, 'obj_list':new, 'account_name':request.session["account_name"]}
# 	print(data1)
# 	return render(request, "latest_news.html",  context)

def question_page(request):

	context = {}
	context["account_name"] = request.session["account_name"]
	context["institution"] = request.session["institution"]

	if request.method == "POST":
		print("#### IN  ####")
		answer = request.POST.get("answer")
		likes = 0
		question_id = request.POST.get("question_id")
		dislikes = 0
		reports = 0
		user_email = request.session["email"]
		print("question_id:", question_id)

		ans = ANSWERS(answer=answer, question_id=question_id, user_email=user_email, likes=likes, dislikes=dislikes, reports=reports)
		ans.save()
		return redirect("/question_page/")

	answers = ANSWERS.objects.all()
	questions = QUESTIONS.objects.all()

	for x in questions:
		print("#", x, " QUESTION: ", x.question_id)
		for y in answers:
			if y.question_id == x.question_id:
				print("#", x, " Answer: ", y.answer, ", Question ID: ", x.question_id)



	context["QUESTIONS"] = questions
	context["ANSWERS"] = answers




	return render(request,"answer.html", context	)

def read_more(request):
	return render(request,"article.html",{})

def laws(request):
	return render(request,"laws.html",{})

def survey_q(request):
	data = survey_question(questions="Specify your Gender : ")
	data.save()
	return HttpResponse("Done")

def survey_a(request):
	data = survey_answer(Gender = 'Male', Time = '8', Years = '5', age = '30', place = 'Pune',salary = '8000')
	data.save()
	return HttpResponse("Done")

def survey(request):
	if request.method=="POST":
		data = request.POST
		temp = int(data['time'])
		if temp>8:
			print_result="Law is being Violated"
			law = "As per the Factories Act 1948, every adult (a person who has completed 18 years of age) cannot work for more than 48 hours in a week and not more than 9 hours in a day. According to Section 51 of the Act, the spread over should not exceed 10-1/2 hours.\nTo report the violations; Click here"
			context={'result':print_result, 'law':law}
			return render(request,'survey.html',context)
	return render(request, 'survey.html', {})

def admin_aggregate(request):

	context = {}

	context["labour_gov_in"] = "Publish"
	context["vvngli"] = "Publish"

	if request.method == "POST":
		try:
			if request.POST["labour_gov_in"] == "Publish":
				print("IN LABOUR GOV IN PUBLISH")
				context["labour_gov_in"] = "Unpublish"
				lists = extract_website_data()
				latest_href, latest_text = zip(*lists)

				for x in range(len(latest_text)):
					object = AGGREGATED_DATA(website="https://labour.gov.in", institute_name="Central Ministry", article_heading=latest_text[x], pdf_links=latest_href[x])
					print(object)
					object.save()
		except Exception as e:
			print("Exception: req.post[labour_gov_in] = Publish", e)

		try:
			if request.POST["labour_gov_in"] == "Unpublish":
				print("IN LABOUR GOV IN UNPUBLISH")
				context["labour_gov_in"] = "Publish"
				objects = AGGREGATED_DATA.objects.filter(website="https://labour.gov.in").delete()
		except Exception as e:
			print("Exception: req.post[labour_gov_in] = unPublish", e)

		if request.POST["vvngli"] == "Publish":
			print("IN VVNGLI IN PUBLISH")
			context["vvngli"] = "Unpublish"
			lists = extract_website_data2()
			list_headings, list_content = zip(*lists)
			print("\n######################################\n")
			print("List Headings: ", len(list_headings))
			print("\n######################################\n")
			print("List Content: ", len(list_content))
			print("\n######################################\n")
			for x in range(len(list_headings)):
				object = AGGREGATED_DATA(website="https://vvgnli.gov.in", institute_name="VV Giri National Labour Institute", article_heading=list_headings[x], html_content=str(list_content[x]))
				print("Object:", object)
				object.save()

		try:
			if request.POST["vvngli"] == "Unpublish":
				print("IN VVNGLI IN UNPUBLISH")
				context["vvngli"] = "Publish"
				objects = AGGREGATED_DATA.objects.filter(website="https://vvgnli.gov.in").delete()

		except Exception as e:
			print("Exception: req.post[vvngli] = unPublish", e)


	return render(request, "aggregate.html", context)

def extract_website_data():

	labour_gov_in = ay_rq.get("https://labour.gov.in/whats-new")
	soup = BeautifulSoup(labour_gov_in.text, "html.parser")

	table = soup.find(class_='views-table cols-4')

	table_items_text = table.find_all('td')
	table_items_href = table.find_all('a')
	count0 = 0
	count1 = 0

	latest_text = []
	latest_href = []

	for item in table_items_text:
		if (len(item.contents[0]) > 50):
			#print("Prettify: ", item.prettify())
			print("Content: ", item.contents[0])
			#print("HREF: ", item.get("href"))
			count0 += 1
			latest_text.append(str(item.contents[0]))

	for item in table_items_href:
		#print("Prettify: ", item.prettify())
		#print("Content: ", item.contents[0])
		print("HREF: ", item.get("href"))
		latest_href.append(item.get("href"))
		count1 += 1

	final_text = []

	for text in latest_text:
		new_char = ""
		count = 0
		for a in text:
			if a.isalpha() and count == 0:
				count = 1
				new_char += a
			elif count == 1:
				new_char += a
		final_text.append(new_char)

	return zip(latest_href, final_text)
	# print("TEXT:", count0)
	# print("HREF:", count1)
	# print(latest_href)
	# print(latest_text)
	# print(final_text)

def extract_website_data2():

	website = "https://vvgnli.gov.in"
	vvngli = ay_rq.get(website)
	soup = BeautifulSoup(vvngli.text, "html.parser")

	links_of_content = soup.find(class_= "training_list")
	list_of_ahref = links_of_content.find_all("a")

	list_of_trainings = []
	content_headings = []
	for x in list_of_ahref:
		content_headings.append(x.contents[0])
		list_of_trainings.append(website + x.get("href"))

	content_list = []

	for training in range(len(list_of_trainings)):
		temp_data_get = ay_rq.get(list_of_trainings[training])
		soup = BeautifulSoup(temp_data_get.text, "html.parser")
		list_of_data = soup.find(class_="content")
		print(list_of_data)
		content_list.append(list_of_data)

	return zip(content_headings, content_list)
