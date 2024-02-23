from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.hashers import make_password,check_password
from .models import stock
# print(make_password('123'))
# print(check_password('123','pbkdf2_sha256$600000$MCAMO1eACf9Y6U7E4LKCxR$574s7gUQKMxiC9ONamuERHZ6U7bc4XxqIvJ2u/+7N9Q='))
import nltk
nltk.download('vader_lexicon')

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from newsapi import NewsApiClient
from datetime import date, timedelta, datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

sia = SentimentIntensityAnalyzer()

pd.set_option('display.max_colwidth',1000)

NEWS_API_KEY = "f49400abecf94e12887066996c925a07"

newsapi = NewsApiClient(api_key = NEWS_API_KEY)

from functools import wraps

def session_login_required(function=None):
    def decorator(view_func):
        @wraps(view_func)
        def f(request, *args, **kwargs):
            token = request.session.get('token', False)

            if token:
                access_token = AccessToken(token)
                print(access_token)
                user = access_token.payload.get('user_id')
                print(user)
                return view_func(request, *args, **kwargs)
            
            return redirect('/')
        
        return f
    if function is not None:
        return decorator(function)
    return decorator

# def session_login_required(func):
#     @wraps(func)
#     def wrapper(request, *args, **kwargs):

#         print(request.session.items())
#         email = request.session.get('email', False)
#         print(email)

#         if email in request.session:
#             return func(request,*args, **kwargs)
#         else:
#             return redirect('/')
#     return wrapper

def index(request):
    if request.method=="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')


        # data = stock.objects.filter(email= email).first()
        try:
            # check user already logged in or not
            if 'token' in request.session:  
                return render(request, "homepage.html")
            user= stock.objects.get(email=email)
            print(user)

            if user is not None:
                if(check_password(password,user.password)):
                # request.session['id']=user.id
                #generating JWT token
                # print(user)
                    refresh = RefreshToken.for_user(user)
                
                    token = str(refresh.access_token)
                    request.session['token'] = token
                # obj =stock.objects.get(id=user.id)
                # obj.status =True
                # obj.save()
                    return render(request,"homepage.html")
                else:
                    return render(request,"login.html",{"error_message": "password not found"})
                
            else:
                return render(request,"login.html",{"error_message": "user not found"})
            
        
        except stock.DoesNotExist:
            return render(request, "login.html", {"error_message": "User not found"})


        # if data:
        #     # if check_password(password,data.password):
        #     if (password == data.password):    
        #         return render(request,"homepage.html")
                
        #     else:
        #         return render(request, "login.html",{"error_message": "password is incorrect"})
        # else:
        #     return render(request, "login.html",{"error_message": "user not found"})
    return render(request,"login.html")
# Create your views here.

@session_login_required
def get_news(request):
    if request.method == "POST":
        company = request.POST.get('company')
        keywrd= company+" stock"
        s1 = datetime.now().date()
        startd = s1 - timedelta(days=2)
        newsapi = NewsApiClient(api_key = NEWS_API_KEY)
        
        if type(startd) == str:
            my_date = datetime.strptime(startd, '%d-%b-%Y')

        else:
            my_date = startd

        articles = newsapi.get_everything(q = keywrd,
                                        from_param = my_date.isoformat(),
                                        to = (my_date + timedelta(days = 2)).isoformat(),
                                        language = "en",
                                        sort_by = "relevancy",
                                        page_size = 100)
    
        articles_list = articles['articles']
        if not articles_list:
            error_message = "No Stock news found for {}".format(company)
            return render(request,"homepage.html", {"error_message": error_message})
        articles_list = sorted(articles_list, key=lambda x: datetime.strptime(x['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'), reverse=True)
        date_sentiments = {}
        date_sentiments_list = []
        seen = set()

        for article in articles_list:
            if str(article['title']) in seen:
                continue
            else:
                seen.add(str(article['title']))
                article_content = str(article['title']) + '. ' + str(article['description'])
                sentiment = sia.polarity_scores(article_content)['compound']
                date_sentiments.setdefault(my_date, []).append(sentiment)
                published_at = datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d')
                date_sentiments_list.append((article['title'],sentiment,published_at))
        date_sentiments_l = sorted(date_sentiments_list, key=lambda tup: tup[0],reverse = True)
        sent_list = list(date_sentiments.values())[0]
        stock_data = pd.DataFrame(date_sentiments_list, columns=['Headline', 'Sentiment', 'PublishedAt'])
        def replace_sentiment(sentiment):
            if sentiment < 0:
                return 'Negative'
            elif sentiment >0:
                return 'Positive'
            else:
                return sentiment
        stock_data=stock_data[stock_data['Sentiment']!=0]
        stock_data=stock_data.reset_index(drop=True)
        stock_data['Sentiment'] = stock_data['Sentiment'].apply(replace_sentiment)
        stock_data_html=stock_data.to_html(index = False)
        stock_data_html = stock_data_html.replace('<th>', '<th style="text-align: center;">')
        return render(request,"homepage.html",{"stock_data_html":stock_data_html})
    return render(request,"homepage.html")

# @login_required()
def logout_user(request):
    # obj=stock.objects.get(id=request.session.get('id',None))
    # obj.status= False
    # obj.save()
    # del request.session['id']
    del request.session['token']
    print(request.session.items())

    print('\nLOGGING OUT...')
    return redirect('/')


# def homePage(request):
#         # if request.method =="GET":
#         #     return render(request, "home.html")
        
#         # if request.method =="POST":
#         #     return render(request, "home.html")
        
        
#         if request.method == "POST":
#             search = request.POST.get('search')
#             if search:
#                 return render(request, "home.html")
        
