from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
import csv
from textblob import TextBlob
import matplotlib.pyplot as plt


def index(request):
	return redirect('login')


@login_required(login_url='login')
def home(request):
    return render(request,'home.html')


@login_required(login_url='login')
def Scrape(request):
    return render(request,'Scrape.html')


@login_required(login_url='login')
def contact(request):

    return render(request,'contact.html')


@login_required(login_url='login')
def about(request):
    return render(request,'about.html')


def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'login.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login')


def register(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)

				return redirect('login')
			

		context = {'form':form}
		return render(request, 'register.html', context)


@login_required(login_url='login')
def dataform(request):
	return render(request,'dataform.html')


@login_required(login_url='login')
def dataform2(request):
	return render(request,'dataform2.html')


@login_required(login_url='login')
def dataform3(request):
	return render(request,'dataform3.html')


@login_required(login_url='login')
def cleaning(request):
	return render(request,'cleaning.html')


@login_required(login_url='login')
def form(request):
	return render(request,'form.html')


@login_required(login_url='login')
def cleaningform(request):
	return render(request,'cleaningform.html')


@login_required(login_url='login')
def sentimentform(request):
	return render(request,'sentimentform.html')


@login_required(login_url='login')
def course(request):
	return render(request,'course.html')


@login_required(login_url='login')
def ebooks(request):
	return render(request,'ebooks.html')


@login_required(login_url='login')
def amazon(request):
	return render(request,'amazon.html')


@login_required(login_url='login')
def table(request):
	return render(request,'table.html')


@login_required(login_url='login')
def sentiment(request):
	return render(request,'sentiment.html')


@login_required(login_url='login')	
def courses(request):


	from selenium import webdriver
	from selenium.webdriver.chrome.options import Options
	from selenium.webdriver.common.by import By
	from bs4 import BeautifulSoup

	chrome_options = Options()
	chrome_options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--window-size=1420,1080')
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument("--disable-extensions")
	driver = webdriver.Chrome(executable_path=r'C:\\Users\\aali5\\scrapper\\myapp\\chromedriver.exe', options=chrome_options)
	urls={'https://www.coursera.org/search?query=data%20science&':["Data Science"],'https://www.coursera.org/search?query=artificial%20intelligence':["AI"],
			'https://www.coursera.org/search?query=machine%20learning':["Machine Learning"],'https://www.coursera.org/search?query=digital%20marketing&index=prod_all_launched_products_term_optimization':["Digital Marketing"]}
	choice=[]
	if request.POST:
		user = request.POST.items()
		for u in user:
			choice.append(u)

	user_inp=choice[1][1]

	if user_inp =='Data Science':
		val = list(urls.keys())
		url=(val[0])
	elif user_inp =='AI':
		val = list(urls.keys())
		url=(val[1])
	elif user_inp =='Machine Learning':
		val = list(urls.keys())
		url=(val[2])
	elif user_inp =='Digital Marketing':
		val = list(urls.keys())
		url=(val[3])
	driver.get(url)

	result = {'Title':[],'Skills':[],'Ratings':[]}
	page=1

	for i in range(5):
		while True:
			html = driver.page_source
			soup = BeautifulSoup(html, 'html.parser')
			
			for el in soup.find_all("div", attrs={"class": "css-1j8ushu"}):
				for ptag in el.find_all('h2', attrs={"class": "cds-1 css-cru2ji cds-3"}):
					result['Title'].append(ptag.get_text())
				flag = True
				for ptag in el.find_all('p', attrs={"class": "cds-1 css-z4vnns cds-3"}):
					flag = False
					result['Skills'].append(ptag.get_text())
				if flag:
					result['Skills'].append('null')
				
				for ptag in el.find_all('p', attrs={"class": "cds-1 css-1hb1zhk cds-3"}):
					flag = False
					result['Ratings'].append(ptag.get_text())
				if flag:
					result['Ratings'].append('0')
			
			if len(driver.find_elements(by=By.CSS_SELECTOR, value="button.label-text.box.arrow")) > 0:
				page += 1
				if user_inp =='Data Science':
					url = "https://www.coursera.org/search?query=data%20science&page={}&index=prod_all_launched_products_term_optimization".format(page)
				elif user_inp =='AI':
					url ="https://www.coursera.org/search?query=artificial%20intelligence&page={}&index=prod_all_launched_products_term_optimization".format(page)
				elif user_inp =='Machine Learning':
					url ="https://www.coursera.org/search?query=machine%20learning&page={}&index=prod_all_launched_products_term_optimization".format(page)
				elif user_inp =='Digital Marketing':
					url="https://www.coursera.org/search?query=digital%20marketing&page={}&index=prod_all_launched_products_term_optimization".format(page)
				driver.get(url)
				if int(page)>7:
					break

	if len(list(result['Title'])) != len(list(result['Ratings'])):
		d= len(list(result['Title'])) - len(list(result['Ratings']))
		for i in range(d):
			result['Ratings'].append('0')
	dict_ = {'Titles':list(result['Title']),
			'Skills':list(result['Skills']),
			'Ratings':list(result['Ratings'])}
	
	response = HttpResponse()
	if user_inp =='Data Science':
		response['Content-Disposition'] = 'attachment; filename=data_science.csv'
	elif user_inp =='AI':
		response['Content-Disposition'] = 'attachment; filename=artificial_intelligence.csv'
	elif user_inp =='Machine Learning':
		response['Content-Disposition'] = 'attachment; filename=machine_learning.csv'
	elif user_inp =='Digital Marketing':
		response['Content-Disposition'] = 'attachment; filename=digital_marketing.csv'
		
	writer = csv.writer(response)
	writer.writerow(['Title', 'Skills','Ratings'])
	for (title,skills,ratings ) in zip(result['Title'], result['Skills'],result['Ratings']):
		writer.writerow([title,skills,ratings])
	return response


@login_required(login_url='login')		
def products(request):
	
	
	from selenium import webdriver
	from selenium.webdriver.chrome.options import Options
	from bs4 import BeautifulSoup
	
	chrome_options = Options()
	chrome_options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--window-size=1420,1080')
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument("--disable-extensions")
	
	driver = webdriver.Chrome(executable_path=r'C:\\Users\\aali5\\scrapper\\myapp\\chromedriver.exe', options=chrome_options)
	urls={'https://www.amazon.in/s?k=Clothing%2C+Shoes%2C+and+Jewelry&crid=1BSOEJ0EBW14F&sprefix=clothing%2C+shoes%2C+and+jewelry%2Caps%2C469&ref=nb_sb_noss_2':["Clothing, Shoes, and Jewelry Items"],'https://www.amazon.in/s?k=electronics&crid=32CBNWXHT8BMQ&sprefix=electronics%2Caps%2C1254&ref=nb_sb_noss_1':["Electronics"],
          'https://www.amazon.in/s?k=Camera+and+Photography&crid=1FWJ48KHNROVE&sprefix=camera+and+photography%2Caps%2C1173&ref=nb_sb_noss_1':["Camera and Photography"],'https://www.amazon.in/s?k=Beauty+and+Personal+Care+Products&crid=3QHZD3CU5MSTY&sprefix=beauty+and+personal+care+products%2Caps%2C465&ref=nb_sb_noss_1':["Beauty and Personal Care Products"],'https://www.amazon.in/s?k=home+and+kitchen+products&crid=2UPE44234K1LB&sprefix=Home+and+Kitchen%2Caps%2C741&ref=nb_sb_ss_ts-doa-p_1_16':["Home and Kitchen Products"]}
	
	choice=[]
	if request.POST:
		user = request.POST.items()
		for u in user:
			choice.append(u)
	user_inp=choice[1][1]
	if user_inp =='Clothing, Shoes, and Jewelry Items':
		val = list(urls.keys())
		url=(val[0])
	elif user_inp =='Electronics':
		val = list(urls.keys())
		url=(val[1])
	elif user_inp =='Camera and Photography':
		val = list(urls.keys())
		url=(val[2])
	elif user_inp =='Beauty and Personal Care Products':
		val = list(urls.keys())
		url=(val[3])
	elif user_inp =='Home and Kitchen Products':
		val = list(urls.keys())
		url=(val[4])

	driver.get(url)
	page=1
	result = {'Title':[],'Price':[],'Ratings':[]}

	for i in range(3):
		while True:
			doc=driver.page_source
			soup = BeautifulSoup(doc, 'html.parser')
			for el in soup.find_all("a", attrs={"class": "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"}):
				flag = False
				result['Title'].append(el.get_text())
			if flag:
				result['Title'].append('null')
			flag = True 
			for el in soup.find_all("span", attrs={"class": "a-price-whole"}):
				flag = False
				result['Price'].append(el.get_text())
			if flag:
				result['Price'].append('0')
			
			for el in soup.find_all("a", attrs={"class": "a-popover-trigger a-declarative"}):
				flag = False
				result['Ratings'].append(el.get_text())
			if flag:
				result['Ratings'].append('0')
			page += 1
			if user_inp =='Clothing, Shoes, and Jewelry Items':
				url="https://www.amazon.in/s?k=Clothing%2C+Shoes%2C+and+Jewelry&page={0}&crid=1BSOEJ0EBW14F&qid=1653147071&sprefix=clothing%2C+shoes%2C+and+jewelry%2Caps%2C469&ref=sr_pg_{0}".format(page)
			elif user_inp =='Electronics':
				url ="https://www.amazon.in/s?k=electronics&page={0}&crid=32CBNWXHT8BMQ&qid=1653145249&sprefix=electronics%2Caps%2C1254&ref=sr_pg_{0}".format(page)
			elif user_inp =='Camera and Photography':
				url ="https://www.amazon.in/s?k=Camera+and+Photography&page=(0)&crid=1FWJ48KHNROVE&qid=1653147535&sprefix=camera+and+photography%2Caps%2C1173&ref=sr_pg_{0}".format(page)
			elif user_inp == 'Beauty and Personal Care Products':
				url="https://www.amazon.in/s?k=Beauty+and+Personal+Care+Products&page={0}&crid=3QHZD3CU5MSTY&qid=1653147710&sprefix=beauty+and+personal+care+products%2Caps%2C465&ref=sr_pg_{0}".format(page)
			elif user_inp =='Home and Kitchen Products':
				url="https://www.amazon.in/s?k=home+and+kitchen+products&page={0}&crid=2UPE44234K1LB&qid=1653148179&sprefix=Home+and+Kitchen%2Caps%2C741&ref=sr_pg_{0}".format(page)
		
			driver.get(url)
			if int(page)>8:
				break
	if len(list(result['Title'])) != len(list(result['Price'])):
		d= len(list(result['Title'])) - len(list(result['Price']))
		for i in range(d):
			result['Price'].append('0')
	
	if len(list(result['Title'])) != len(list(result['Ratings'])):
		d= len(list(result['Title'])) - len(list(result['Ratings']))
		for i in range(d):
			result['Ratings'].append('0')

	response = HttpResponse()
	if user_inp =='Clothing, Shoes, and Jewelry Items':
		response['Content-Disposition'] = 'attachment; filename=amazon_products_category1.csv'
	elif user_inp =='Electronics':
		response['Content-Disposition'] = 'attachment; filename=amazon_products_category2.csv'
	elif user_inp =='Camera and Photography':
		response['Content-Disposition'] = 'attachment; filename=amazon_products_category3.csv'
	elif user_inp =='Beauty and Personal Care Products':
		response['Content-Disposition'] = 'attachment; filename=amazon_products_category4.csv'
	elif user_inp =='Home and Kitchen Products':
		response['Content-Disposition'] = 'attachment; filename=amazon_products_category5.csv'
		
	writer = csv.writer(response)
	writer.writerow(['Title', 'Price','Ratings'])
	for (title,price,ratings ) in zip(result['Title'], result['Price'],result['Ratings']):
		writer.writerow([title,price,ratings])
	return response


def books(request):


	from selenium import webdriver
	from selenium.webdriver.chrome.options import Options
	from bs4 import BeautifulSoup

	chrome_options = Options()
	chrome_options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--window-size=1420,1080')
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument("--disable-extensions")
	b = webdriver.Chrome(executable_path=r'C:\\Users\\aali5\\scrapper\\myapp\\chromedriver.exe', options=chrome_options)
	urls={'https://www.amazon.in/s?i=digital-text&bbn=1637083031&rh=n%3A1637083031%2Cp_n_feature_three_browse-bin%3A11301931031&dc&fs=true&qid=1653208369&rnid=10837938031&ref=sr_nr_p_n_feature_three_browse-bin_1':["Crime Mystery Thriller"],'https://www.amazon.in/s?i=digital-text&bbn=1637085031&rh=n%3A1637085031%2Cp_n_feature_three_browse-bin%3A11301931031&dc&fs=true&qid=1653210880&rnid=10837938031&ref=sr_nr_p_n_feature_three_browse-bin_1':["Fantasy Horror Science Fiction"],
			'https://www.amazon.in/s?i=digital-text&bbn=1637171031&rh=n%3A1637171031%2Cp_n_feature_three_browse-bin%3A11301931031&dc&fs=true&qid=1653211114&rnid=10837938031&ref=sr_nr_p_n_feature_three_browse-bin_1':["Social Sciences"],'https://www.amazon.in/s?i=digital-text&bbn=1637142031&rh=n%3A1571277031%2Cn%3A1634753031%2Cn%3A1637142031%2Cn%3A1637150031%2Cp_n_feature_three_browse-bin%3A11301931031&dc&fs=true&qid=1653211359&rnid=1637142031&ref=sr_nr_n_7':["Religion and Spirituality"],
		'https://www.amazon.in/s?i=digital-text&bbn=1634753031&rh=n%3A1571277031%2Cn%3A1634753031%2Cn%3A1637059031%2Cp_n_feature_three_browse-bin%3A11301931031&dc&fs=true&qid=1653212686&rnid=1634753031&ref=sr_nr_n_8':["Computing Internet and Digital Media"]}

	choice=[]
	if request.POST:
		user = request.POST.items()
		for u in user:
			choice.append(u)
		user_inp=choice[1][1]
		url=""
		if user_inp =='Crime Mystery Thriller':
			val = list(urls.keys())
			url=(val[0])
			
		elif user_inp =='Fantasy Horror Science Fiction':
			val = list(urls.keys())
			url=(val[1])
		elif user_inp =='Social Sciences':
			val = list(urls.keys())
			url=(val[2])
		elif user_inp =='Religion and Spirituality':
			val = list(urls.keys())
			url=(val[3])
		elif user_inp =='Computing Internet and Digital Media':
			val = list(urls.keys())
			url=(val[4])
		
		b.get(url)
		page=1
		result = {'Title':[],'Author':[],'Price':[]}

		for i in range(3):
			while True:
				doc=b.page_source
				soup = BeautifulSoup(doc, 'html.parser')
				for el in soup.find_all("a", attrs={"class": "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"}):
					result['Title'].append(el.get_text())
				flag = True 
				for el in soup.find_all("a", attrs={"class": "a-size-base a-link-normal s-light-weight-text s-underline-text s-underline-link-text s-link-style s-link-centralized-style"}):
					flag = False
					result['Author'].append(el.get_text())
				if flag:
					result['Author'].append('null')
				
				for el in soup.find_all("span", attrs={"class": "a-price"}):
					result['Price'].append(el.get_text())
				
				page += 1
				if user_inp =='Crime Mystery Thriller':
					url="https://www.amazon.in/s?i=digital-text&bbn=1637083031&rh=n%3A1637083031%2Cp_n_feature_three_browse-bin%3A11301931031&dc&fs=true&page={0}&qid=1653208375&rnid=10837938031&ref=sr_pg_{0}".format(page)
				elif user_inp =='Fantasy Horror Science Fiction':
					url ="https://www.amazon.in/s?i=digital-text&bbn=1637085031&rh=n%3A1637085031%2Cp_n_feature_three_browse-bin%3A11301931031&dc&fs=true&page={0}&qid=1653210889&rnid=10837938031&ref=sr_pg_{0}".format(page)
				elif user_inp =='Social Sciences':
					url ="https://www.amazon.in/s?i=digital-text&bbn=1637171031&rh=n%3A1637171031%2Cp_n_feature_three_browse-bin%3A11301931031&dc&fs=true&page={0}&qid=1653211125&rnid=10837938031&ref=sr_pg_{0}".format(page)
				elif user_inp == 'Religion and Spirituality':
					url="https://www.amazon.in/s?i=digital-text&bbn=1637142031&rh=n%3A1571277031%2Cn%3A1634753031%2Cn%3A1637142031%2Cn%3A1637150031%2Cp_n_feature_three_browse-bin%3A11301931031&dc&fs=true&page={0}&qid=1653211387&rnid=1637142031&ref=sr_pg_{0}".format(page)
				elif  user_inp =='Computing Internet and Digital Media':
					url="https://www.amazon.in/s?i=digital-text&bbn=1634753031&rh=n%3A1571277031%2Cn%3A1634753031%2Cn%3A1637059031%2Cp_n_feature_three_browse-bin%3A11301931031&dc&fs=true&page={0}&qid=1653211701&rnid=1634753031&ref=sr_pg_{0}".format(page)
			
				b.get(url)
				if int(page)>6:
					break

		if len(list(result['Title'])) != len(list(result['Author'])):
			d= len(list(result['Title'])) - len(list(result['Author']))
			for i in range(d):
				result['Author'].append('null')
		if len(list(result['Title'])) != len(list(result['Price'])):
			d= len(list(result['Title'])) - len(list(result['Price']))
			for i in range(d):
				result['Price'].append('0')
		
		response = HttpResponse()
		if user_inp =='Crime Mystery Thriller':
			response['Content-Disposition'] = 'attachment; filename=Crime Ebooks.csv'
		elif user_inp =='Fantasy Horror Science Fiction':
			response['Content-Disposition'] = 'attachment; filename=Fantasy Ebooks.csv'
		elif user_inp =='Social Sciences':
			response['Content-Disposition'] = 'attachment; filename=Social Sciences Ebooks.csv'
		elif user_inp =='Religion and Spirituality':
			response['Content-Disposition'] = 'attachment; filename=Religion Ebooks.csv'
		elif  user_inp =='Computing Internet and Digital Media':
			response['Content-Disposition'] = 'attachment; filename=Digital Media Ebooks.csv'
		
		writer = csv.writer(response)
		writer.writerow(['Title', 'Author','Price'])
		for (title,author,price ) in zip(result['Title'], result['Author'],result['Price']):
			writer.writerow([title, author,price])
		
		# dict_ = {'Titles':list(result['Title']),
		# 		'Author':list(result['Author']),
		# 		'Price':list(result['Price'])}
		#dict_=dict_.to_html("templates\\table.html")
		#return render(request, 'table.html')
		#return render(request, 'ebooks.html',{'data':dict_})
		return response


@login_required(login_url='login')
def cleaning_csv(req):
	import pandas as pd
	import re
	import string
	from nltk.stem import WordNetLemmatizer
	from nltk.corpus import stopwords
	
	if req.POST:
		uploaded_file=req.FILES["file"]
		file_name=uploaded_file.name
		file_name="cleaned_"+file_name
		missing_values = ["n/a", "na", "--", " ", ""]
		df = pd.read_csv(uploaded_file, na_values=missing_values)
		file_header=df.columns.to_list()
		headers=len(file_header)

		dict_={}
		df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)
		all_columns = df.columns.to_list()
		new_df = pd.DataFrame()

		all_columns_data = {}
		stemmer = WordNetLemmatizer()

		for column in all_columns:
			all_columns_data[column] = []
			if df[column].dtypes == 'float64' or df[column].dtypes == 'int64':
				for data in df[column]:
					all_columns_data[column].append(data)
				continue
			for data in df[column]:
				if '$' in data or 'PKR' in data:
					all_columns_data[column].append(data)
					continue
				document = re.sub(r'\W', ' ', str(data))
				documents = re.sub(re.escape(string.punctuation), ' ', document)
				document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)
				document = re.sub(r'\^[a-zA-Z]\s+', ' ', document)
				document = re.sub(r'\s+', ' ', document, flags=re.I)
				document = re.sub(r'^b\s+', ' ', document)
				document = document.lower()

				document = document.split()
				document = [stemmer.lemmatize(word) for word in document]
				document = ' '.join(document)
				document = [word for word in document.split(
				) if word not in stopwords.words("english")]
				document = ' '.join(document)
				all_columns_data[column].append(document)
		
		for index, column_name in enumerate(all_columns_data.keys()):
			new_df.insert(index, column_name, all_columns_data[column_name])
			
		for i in file_header:
			dict_[i]=new_df[i]
		
		dict_=new_df.to_html("templates\\table.html")
		return render(req, 'table.html')


@login_required(login_url='login')
def sentiment_csv(request):	
	lines=[]
	val=[]
	list = []
	iterP = 0
	iterN = 0
	iterNN = 0
	if request.POST:
		uploaded_file=request.FILES["csv_file"]
		for row in uploaded_file:
			lines.append(row)		
		
		for line in lines:
			line = line.rstrip()
			val.append(str(line))
	
		for line in val:
			list.append(TextBlob(line).sentiment.polarity)
		for i in list:
			if(i > 0):
				iterP = iterP + 1
			elif(i < 0):
				iterN = iterN + 1
			elif(i == 0):
				iterNN = iterNN + 1

		
		left = [1, 2, 3]
		height = [iterP, iterN, iterNN]
		tick_label = ['Positive Reviews : ' + str(iterP), 'Negative Reviews : ' + str(iterN), 'Neutral Reviews : ' + str(iterNN)]

		plt.bar(left, height, tick_label = tick_label,
						width = 0.8, color = ['green', 'red', 'blue'])

		plt.xlabel('x - axis')
		plt.ylabel('y - axis')
		plt.title('Sentiments of users in graphical form!')

		out=plt.show()
		return render(request,'home.html')
	
