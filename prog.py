import numpy as np
import string
import re
from nltk.corpus import stopwords
import pandas as pd
from flask import Flask,request,jsonify,render_template, redirect, url_for
from flask_bootstrap import Bootstrap
import pickle
from titletest import *
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

app=Flask(__name__)
Bootstrap(app)

newstitle_object = checkTitle("")
processes = [newstitle_object.spelling_mistakes, newstitle_object.classify_clickbait, newstitle_object.subjective_test, newstitle_object.is_newstitle, newstitle_object.present_on_google]
names = ['Checkingforspellingmistakes', 'Checkingforclickbaittitle', 'Checkingforsubjectivetitles', 'Checkingforvalidnewstitle', 'Checkingforwebavailability']
index = -1
pages = ['spellfail.html', 'clickfail.html', 'subjecfail.html', 'newtitilefail.html', 'availweb.html']
headline = ''
last_executed = True

def present_on_google_news_2(self, domain):
    print(domain)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    ggl_news_link = f"https://www.google.com/search?q={domain}&tbm=nws"
    req = requests.get(ggl_news_link, headers=headers)
    sup = BeautifulSoup(req.content, 'html.parser')
    link = sup.find('a', class_='WlydOe')
    if link:
        nd_domain = urlparse(link['href'])
        domain_name = nd_domain.netloc
        domain_name = domain_name.replace('www.', '')
        if domain == domain_name:
            return True
    return False


def is_url(text):
    pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(pattern, text) is not None

def checkbox_activate1():
    global processes
    global names
    global pages
    processes = [newstitle_object.classify_clickbait, newstitle_object.subjective_test, newstitle_object.is_newstitle, newstitle_object.present_on_google]
    names = ['Checkingforclickbaittitle', 'Checkingforsubjectivetitles', 'Checkingforvalidnewstitle', 'Checkingforwebavailability']
    pages = ['clickfail.html', 'subjecfail.html', 'newtitilefail.html', 'availweb.html']

def checkbox_activate2():
    global processes
    global names
    global pages
    processes = [newstitle_object.subjective_test, newstitle_object.present_on_google]
    names = ['Checkingforsubjectivetitles', 'Checkingforwebavailability']
    pages = ['subjecfail.html', 'availweb.html']

def checkbox_activate3():
    global processes
    global names
    global pages
    processes = [newstitle_object.present_on_google]
    names = ['Checkingforwebavailability']
    pages = ['availweb.html']


def set_all():
    global processes
    global names
    global index
    global pages
    global headline
    headline = ''
    processes = [newstitle_object.spelling_mistakes, newstitle_object.classify_clickbait, newstitle_object.subjective_test, newstitle_object.is_newstitle, newstitle_object.present_on_google]
    names = ['Checkingforspellingmistakes', 'Checkingforclickbaittitle', 'Checkingforsubjectivetitles', 'Checkingforvalidnewstitle', 'Checkingforwebavailability']
    index = -1
    pages = ['spellfail.html', 'clickfail.html', 'subjecfail.html', 'newtitilefail.html', 'availweb.html']


@app.route('/')
def home():
    global index
    global headline
    headline = ''
    index = -1
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/detect',methods=['POST','GET'])
def detect():
    global headline
    set_all()
    if request.method=='POST':
        input_text = request.form.get('text')
        input_image = request.form.get('image')
        input_url = request.form.get('url')

        if input_text != None:
            print(input_text)
            headline = input_text
            checkbox1 = request.form.get('check1')
            checkbox2 = request.form.get('check2')
            if checkbox1:
                checkbox_activate1()
            if checkbox2:
                checkbox_activate2()

            return redirect(url_for('given_is_text', text=input_text, progress_name=names[0], num = 1))
        elif input_url != None:
            if is_url(input_url) == False:
                print("Please enter valid url")
            try:
                req = requests.get(input_url)
            except:
                print("The Website is not accessible")
            soup = BeautifulSoup(req.content, 'html.parser')
            text = soup.find('h1')
            if text == None:
                print("the given website has no Headline text, please avoid using social media website urls")
            nd_domain = urlparse(input_url)
            domain_name = nd_domain.netloc
            if present_on_google_news_2(domain_name) == False:
                print("the given domain is not present on google news, Please give only news websites url, if a news website is not present on google news there is a high possibility that the news pubished by that specific news website if fake")
            checkbox_activate3()
            return redirect(url_for('given_is_text', text=text, progress_name=names[0], num = 1))
        elif input_image != None:
            pass
    return render_template('detect.html')

@app.route('/listen')
def listen():
    global index
    global headline
    index+=1
    newstitle_object.headline = headline
    val = processes[index]()
    print(val)
    if val == True:
        return jsonify({'value': True})
    else:
        return jsonify({'value': False})

@app.route('/progress/<string:text>/<string:progress_name>/<int:num>', methods=['GET', 'POST'])
def given_is_text(text, progress_name, num):
    global last_executed
    global headline
    global names
    global pages
    print(num)
    if num == 0:
        page = pages[names.index(progress_name)]
        return render_template(page)
    else:
        ind = names.index(progress_name)
        return render_template('new.html', input_data=[progress_name], my_list=names)

@app.route('/predict',methods=['POST'])
def predict():
    if request.method=='POST':
        input_text=request.form.get('text')
        if input_text:
            print("hello"+input_text)
    test=request.form.values()
    test_ser=pd.Series(test)
    return render_template('detect.html',prediction_text='Given News is {}!'.format('true'),result="RESULT:")

@app.route('/names')
def names():
    global names
    num = 1
    if len(names) == 5:
        num = 1
    if len(names) == 4:
        num = 2
    if len(names) == 2:
        num = 3
    if len(names) == 1:
        num = 4
    return jsonify({'number':num})


if __name__=='__main__':
    app.run(debug=True)