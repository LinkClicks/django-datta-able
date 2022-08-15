# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
import requests
import os
from .models import Tokens


@login_required(login_url="/login/")
def oauth(request):
    print("oauth!!!")
    print("Test")
    # Fetching code value from the URL
    code = request.GET.get("code")
    code = str(code)
    print(code)
    # Generating Access and refresh tokens
    clientid = os.environ.get("CLIENT_ID")
    clientsecret = os.environ.get("CLIENT_SECRET")
    payload = {"client_id" : (clientid), "client_secret" : (clientsecret), "code" : (code), "grant_type" : "authorization_code", "redirect_uri" : "https://django.linkclicks.com/oauth"}
    r = requests.post("https://accounts.snapchat.com/login/oauth2/access_token", data=payload)
    # Using python dict to print access token
    r_dict = r.json()
    a_tkn = r_dict["access_token"]
    r_tkn = r_dict["refresh_token"]
    print("access token is:")
    print(a_tkn)
    print("refresh token is:")
    print(r_tkn)
    url = "https://adsapi.snapchat.com/v1/me/organizations"
    querystring = {"with_ad_accounts":"true"}
    headers = {"Authorization": "Bearer "+ (a_tkn)}
    response = requests.request("GET", url, headers=headers, params=querystring)
    # print(response.json())
    response_dict = response.json()
    organizations = response_dict["organizations"]
    print("a")
    i = 0
    print("b")
    while i < len(organizations):
        print("c")
        organization = organizations[i]["organization"]
        print("d")
        i = i + 1
        print(i)
        print(organization)
        print("e")
        # ad_accounts = organization["ad_accounts"]
        # print("f")
        # print(ad_accounts)
    tokenn = Tokens(access_token=r_dict['access_token'], refresh_token=r_dict['refresh_token']) # create new model instance
    tokenn.save() #save to db
    return render(request, "home/oauth.html")


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
