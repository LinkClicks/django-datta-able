# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
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
    print("asas")
    print(a_tkn)
    print("refresh token is:")
    print(r_tkn)
    url = "https://adsapi.snapchat.com/v1/me/organizations"
    querystring = {"with_ad_accounts":"true"}
    headers = {"Authorization": "Bearer "+ (a_tkn)}
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.json())
    response_dict = response.json()
    print(response.json())
    organizations = response_dict["organizations"]
    i = 0
    while i < len(organizations):
        organization = organizations[i]["organization"]
        i = i + 1
        print(i)
        print(organization)
        # ad_accounts = organization["ad_accounts"]
        # print(ad_accounts)

    # CREATING CAMPAIGN
    url = "https://adsapi.snapchat.com/v1/adaccounts/184d5ad6-86ea-48dc-b35e-e7153f95fcc8/campaigns"
    querystring = {"ad_account_id":"184d5ad6-86ea-48dc-b35e-e7153f95fcc8"}
    payload = {"campaigns": [
        {
            "name": "Cool Campaign",
            "ad_account_id": "184d5ad6-86ea-48dc-b35e-e7153f95fcc8",
            "status": "PAUSED",
            "start_time": "2022-09-11T22:03:58.869Z"
        }
        ]}
    headers = {
    "Authorization": "Bearer "+ (a_tkn),
    "Content-Type": "application/json"
    }
    response = requests.request("POST", url, json=payload, headers=headers, params=querystring)
    print("CAMPAIGN CREATED!!!")
    print(response.text)

    #CREATING AD_SQUAD
    url = "https://adsapi.snapchat.com/v1/campaigns/c4562a36-7973-4523-a5f1-a0db7e2feb43/adsquads"
    querystring = {"campaign_id":"c4562a36-7973-4523-a5f1-a0db7e2feb43"}
    payload = {"adsquads": [
        {
            "campaign_id": "c4562a36-7973-4523-a5f1-a0db7e2feb43",
            "name": "Ad Squad Uno",
            "type": "SNAP_ADS",
            "placement_v2": {"config": "AUTOMATIC"},
            "optimization_goal": "IMPRESSIONS",
            "bid_micro": 1000000,
            "daily_budget_micro": 1000000000,
            "bid_strategy": "LOWEST_COST_WITH_MAX_BID",
            "billing_event": "IMPRESSION",
            "targeting": {"geos": [{"country_code": "can"}]},
            "start_time": "2022-09-11T22:03:58.869Z"
        }
    ]}
    headers = {
    "Authorization": "Bearer "+ (a_tkn),
    "Content-Type": "application/json"
    }
    response = requests.request("POST", url, json=payload, headers=headers, params=querystring)
    print("AD SQUAD CREATED!!")
    print(response.text)
    
    tokenn = Tokens(access_token=r_dict['access_token'], refresh_token=r_dict['refresh_token']) # create new model instance
    tokenn.save() #save to db
    return redirect("adaccounts.html")


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
