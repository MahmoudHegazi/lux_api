#!/usr/bin/python
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, BakeryLinks, Bakery, EggsLinks, Eggs, SeafoodLinks, Seafood, FruitsLinks, Fruits
from database_setup import FreshmeatLinks, FreshMeat, FreshVegetablesLinks, FreshVegetables, NoodlesSupplementsLinks
from database_setup import NoodlesSupplements, OtherFreshFoodLinks, OtherFreshFood
from flask import session as login_session
import string
import httplib2
import json
from flask import make_response
import requests
import pandas as pd
from tablib import Dataset
import numpy as np
import excel
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from PyPDF2 import PdfFileReader
import io
from collections import Counter
import base64
# IMPORTS FOR THIS STEP
import pprint
import httplib2
import json
import sqlite3
from flask import make_response
import time
from datetime import date
from datetime import datetime

app = Flask(__name__)

APPLICATION_NAME = "api_scaner"

# Connect to Database and create database session
engine = create_engine('sqlite:///api_scaner.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# You need install :
# pip install PyPDF2 - > Read and parse your content pdf
# pip install requests - > request for get the pdf
# pip install BeautifulSoup - > for parse the html and find all url hrf with ".pdf" final



@app.route('/bakery')
def bakery_links():
    bakeries = session.query(BakeryLinks).all()
    return jsonify(bakeries=[r.serialize for r in bakeries])

@app.route('/bakery_data')
def bakery_data():
    bakeries_data = session.query(Bakery).all()
    return jsonify(bakeries=[r.serialize for r in bakeries_data])

@app.route('/eggs')
def eggs_links():
    eggs_links = session.query(EggsLinks).all()
    return jsonify(eggs_links=[r.serialize for r in eggs_links])

@app.route('/eggs_data')
def eggs_data():
    eggs_data = session.query(Eggs).all()
    return jsonify(eggs=[r.serialize for r in eggs_data])


@app.route('/seafood')
def seafood_links():
    seafood_links = session.query(SeafoodLinks).all()
    return jsonify(seafood_links=[r.serialize for r in seafood_links])

@app.route('/seafood_data')
def seafood_data():
    seafood_data = session.query(Seafood).all()
    return jsonify(seafood=[r.serialize for r in seafood_data])


@app.route('/fruits')
def fruits_links():
    fruits_links = session.query(FruitsLinks).all()
    return jsonify(fruits_links=[r.serialize for r in fruits_links])

@app.route('/fruits_data')
def fruits_data():
    fruits_data = session.query(Fruits).all()
    return jsonify(fruits=[r.serialize for r in fruits_data])


@app.route('/meat')
def meat_links():
    meat_links = session.query(FreshmeatLinks).all()
    return jsonify(meat_links=[r.serialize for r in meat_links])

@app.route('/meat_data')
def meat_data():
    meat_data = session.query(FreshMeat).all()
    return jsonify(meat=[r.serialize for r in meat_data])


@app.route('/vegetables')
def vegetables_links():
    vegetables_links = session.query(FreshVegetablesLinks).all()
    return jsonify(vegetables_links=[r.serialize for r in vegetables_links])

@app.route('/vegetables_data')
def vegetables_data():
    vegetables_data = session.query(FreshVegetables).all()
    return jsonify(vegetables=[r.serialize for r in vegetables_data])

@app.route('/noodles_supplements')
def noodles_supplements():
    noodles_supplements_links = session.query(NoodlesSupplementsLinks).all()
    return jsonify(noodels_supplements_links=[r.serialize for r in noodles_supplements_links])

@app.route('/noodles_supplements_data')
def noodles_supplements_data():
    noodles_supplements_data = session.query(NoodlesSupplements).all()
    return jsonify(noodels_and_supplements=[r.serialize for r in noodles_supplements_data])

@app.route('/other_feshfood_links')
def other_feshfood_links():
    other_feshfood_links = session.query(OtherFreshFoodLinks).all()
    return jsonify(other_fresh_food=[r.serialize for r in other_feshfood_links])

@app.route('/other_fresh_food')
def other_fresh_food():
    other_fresh_food = session.query(OtherFreshFood).all()
    return jsonify(other_fresh_food=[r.serialize for r in other_fresh_food])

#this function generate list of all pagination link for given url or category OtherFreshFoodLinks, OtherFreshFood

def get_pagination(url):
    #url = 'https://eshop.tesco.com.my/groceries/en-GB/shop/fresh-food/bakery/all'
    filters = []
    mylinks = []
    while url not in filters:
        print(url)
        if url not in mylinks:
            mylinks.append(url)
        r = requests.get(url,headers={"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"})
        soup = BeautifulSoup(r.text ,"lxml")
        url = soup.findAll('a', {'class': 'pagination--button prev-next'})
        if url in filters:
            filters.append(url)
            print(filters)
            print('scaner API got The all pagination Links for The URL')
            return mylinks
        filters.append(url)
        for x in url:
            if x:
                url = 'https://eshop.tesco.com.my' + x.get('href')
            else:
                break
    return mylinks



# this function collect the proudcts for each link
def proudcts_collecter(pagination_list):
    projectData = []
    for link in pagination_list:
        # error handle partners
        try:
            print('Scaner API Fetch that URl ' + str(link))
            response = requests.get(link, headers={"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"})
            content = response.content
            soup = BeautifulSoup(response.content, 'html.parser')
            top_domain = 'https://eshop.tesco.com.my'
            proudcts = soup.find_all('a' , class_="product-image-wrapper")
            for proudct in proudcts:
                proudct_link = top_domain + proudct.get('href')
                if proudct_link not in projectData:
                    projectData.append(proudct_link)
                else:
                    continue
        # if no error print error and add exception for that error
        except Exception as e:
            print(e.message, e.args)
            print('we are going to wait 5 minutes until the app solve the error.')
            time.sleep(300)

            # this way app will be imune to stop
            try:
                print('We Solved Error Scaner API Fetch that URl ' + str(link))
                response = requests.get(link, headers={"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"})
                content = response.content
                soup = BeautifulSoup(response.content, 'html.parser')
                top_domain = 'https://eshop.tesco.com.my'
                proudcts = soup.find_all('a' , class_="product-image-wrapper")
                for proudct in proudcts:
                    proudct_link = top_domain + proudct.get('href')
                    if proudct_link not in projectData:
                        projectData.append(proudct_link)
                    else:
                        continue
            # if no error print error and add exception for that error
            except Exception as e:
                print(e.message, e.args)
                time.sleep(300)
                pirnt('We now Have wait 10 minutes now fetching: ' + str(link))
                response = requests.get(link, headers={"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"})
                content = response.content
                soup = BeautifulSoup(response.content, 'html.parser')
                top_domain = 'https://eshop.tesco.com.my'
                proudcts = soup.find_all('a' , class_="product-image-wrapper")
                for proudct in proudcts:
                    proudct_link = top_domain + proudct.get('href')
                    if proudct_link not in projectData:
                        projectData.append(proudct_link)
                    else:
                        continue


    return projectData




# this function accept one paramter which is list of prudcts links
def get_proudct_data(prudcts_links):
    projectData = []
    # start from Carbs and end with Protein

    for link in prudcts_links:
        url_part1 = link
        #url_part1 = 'https://eshop.tesco.com.my/groceries/en-GB/products/7000010766'
        try:
            response = requests.get(url_part1,headers={"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"})
            content = response.content
            soup = BeautifulSoup(response.content, 'html.parser')
            proudct_image = soup.find('img' , class_="product-image").get('src')
            proudct_name = soup.find('h1' , class_="product-details-tile__title").getText()
            proudct_price = soup.find('span' , class_="value").getText()
            proudct = {"image": proudct_image,"name": proudct_name,"price": proudct_price}
            if proudct not in projectData:
                projectData.append(proudct)
            else:
                continue
        except Exception as e:
            print(e.message, e.args)
            print('API Scanner Blocked For A while Do not Worry We Will override that error Wait 5 minutes...')
            time.sleep(300)
            print('Continue from The Last point..')
            try:
                response = requests.get(url_part1,headers={"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"})
                content = response.content
                soup = BeautifulSoup(response.content, 'html.parser')
                proudct_image = soup.find('img' , class_="product-image").get('src')
                proudct_name = soup.find('h1' , class_="product-details-tile__title").getText()
                proudct_price = soup.find('span' , class_="value").getText()
                proudct = {"image": proudct_image,"name": proudct_name,"price": proudct_price}
                if proudct not in projectData:
                    projectData.append(proudct)
                else:
                    continue
            except Exception as e:
                print(e.message, e.args)
                print('Again API Scanner Blocked For A while Do not Worry We Will override that error Wait 5 minutes...')
                print('Do not worry Nothing Can stop this API')
                time.sleep(400)
                print('Continue from The Last point..')
                response = requests.get(url_part1,headers={"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"})
                content = response.content
                soup = BeautifulSoup(response.content, 'html.parser')
                proudct_image = soup.find('img' , class_="product-image").get('src')
                proudct_name = soup.find('h1' , class_="product-details-tile__title").getText()
                proudct_price = soup.find('span' , class_="value").getText()
                proudct = {"image": proudct_image,"name": proudct_name,"price": proudct_price}
                if proudct not in projectData:
                    projectData.append(proudct)
                else:
                    continue


    return projectData



@app.route('/update')
def targeter():
    # this step will make the data base empty in order to update the new values good for preformance
    def clear_db():
        print('start deleting process...')
        def the_remover(col_to_delete):
                #clear links table
                for col in col_to_delete:
                    try:
                        session.delete(col)
                        session.commit()
                    except Exception as e:
                        return e.message
                # clear main table
                for col in col_to_delete:
                    try:
                        session.delete(col)
                        session.commit()
                    except Exception as e:
                        return e.message
        # clear category
        ColumnToDelete = session.query(BakeryLinks).all()
        ColumnToDelete1 = session.query(Bakery).all()
        the_remover(ColumnToDelete)
        the_remover(ColumnToDelete1)

        # clear category
        ColumnToDelete = session.query(EggsLinks).all()
        ColumnToDelete1 = session.query(Eggs).all()
        the_remover(ColumnToDelete)
        the_remover(ColumnToDelete1)

        # clear category
        ColumnToDelete = session.query(SeafoodLinks).all()
        ColumnToDelete1 = session.query(Seafood).all()
        the_remover(ColumnToDelete)
        the_remover(ColumnToDelete1)

        # clear category
        ColumnToDelete = session.query(FruitsLinks).all()
        ColumnToDelete1 = session.query(Fruits).all()
        the_remover(ColumnToDelete)
        the_remover(ColumnToDelete1)

        # clear category
        ColumnToDelete = session.query(FreshmeatLinks).all()
        ColumnToDelete1 = session.query(FreshMeat).all()
        the_remover(ColumnToDelete)
        the_remover(ColumnToDelete1)

        # clear category
        ColumnToDelete = session.query(FreshVegetablesLinks).all()
        ColumnToDelete1 = session.query(FreshVegetables).all()
        the_remover(ColumnToDelete)
        the_remover(ColumnToDelete1)

        # clear category
        ColumnToDelete = session.query(NoodlesSupplementsLinks).all()
        ColumnToDelete1 = session.query(NoodlesSupplements).all()
        the_remover(ColumnToDelete)
        the_remover(ColumnToDelete1)

        # clear category
        ColumnToDelete = session.query(OtherFreshFoodLinks).all()
        ColumnToDelete1 = session.query(OtherFreshFood).all()
        the_remover(ColumnToDelete)
        the_remover(ColumnToDelete1)
        print('Database Clear...')
        return True
    # call the function
    clear_db()

    # this function return list contains real time optio
    def printTime():
        time_results = []
        today = date.today()
        # dd/mm/YY
        d1 = today.strftime("%d/%m/%Y")
        # Textual month, day and year
        d2 = today.strftime("%B %d, %Y")
        time_results = []
        time_results.append(str(d1))
        time_results.append(str(d2))
        return time_results
    # we call proudcts_collecter to get proudct links which accept list of pagination and give it category url
    # ---------------- Steps for scrap and get the data ----------
    #-----------------------------------------------------------
    #this list for baker
    the_bakery_list = []
    the_egs_list = []
    the_seafood_list = []
    the_fruits_list = []
    the_fresh_meet_list = []
    the_fresh_vegetables_list = []
    the_noodles_supplements_list = []
    the_other_fresh_list = []
    print('Welcome To API scaner We going to Start soon...')
    time.sleep(1)
    print('1')
    time.sleep(1)
    print('2')
    time.sleep(1)
    print('3 Go..')
    # bakery category
    ju_bakery_links = proudcts_collecter(get_pagination('https://eshop.tesco.com.my/groceries/en-GB/shop/fresh-food/bakery/all'))
    #next step for category_link in category links call proudcts_collecter(get_pagination(category_link))
    time_list = printTime()
    last_update = time_list[0]
    last_update_text = time_list[1]
    for proudct_link in ju_bakery_links:
        print('API scaner saving : ' + str(proudct_link))
        newproudct_link = BakeryLinks(url=proudct_link,market_place='tesco',last_update=last_update,last_update_text=last_update_text)
        session.add(newproudct_link)
        session.commit()
    print('successfully Saved All Bakeries link..')
    print('Next Step Starting soon Get Proudct data ..')
    bakeries_list = session.query(BakeryLinks).all()
    for proudct_url in bakeries_list:
        if proudct_url not in the_bakery_list:
            the_bakery_list.append(proudct_url.url)
        else:
            continue
    print('scaner API ready To get proudcts Data...')
    print('This will take time max 5 minutes Please wait Until we fetch all project data...')
    all_proudcts = get_proudct_data(the_bakery_list)
    print('We successfully got all proudcts and saved internal..')
    print('API scaner now will save the proudcts data in the Database..')
    print('Please Wait until we Fetch all proudcts data and save it in the Database..')
    time_list = printTime()
    last_update = time_list[0]
    last_update_text = time_list[1]
    for proudct_object in all_proudcts:
        ju_proudct_image = proudct_object['image']
        ju_proudct_name = proudct_object['name']
        ju_proudct_price = proudct_object['price']
        newproudct_data = Bakery(name=ju_proudct_name,price=ju_proudct_price,image=ju_proudct_image,market_place='tesco',last_update=last_update,last_update_text=last_update_text)
        session.add(newproudct_data)
        session.commit()


    # Egs category
    ju_eggs_links = proudcts_collecter(get_pagination('https://eshop.tesco.com.my/groceries/en-GB/shop/fresh-food/eggs/all'))
    #next step for category_link in category links call proudcts_collecter(get_pagination(category_link))
    time_list = printTime()
    last_update = time_list[0]
    last_update_text = time_list[1]
    for proudct_link in ju_eggs_links:
        print('API scaner saving : ' + str(proudct_link))
        newproudct_link = EggsLinks(url=proudct_link,market_place='tesco',last_update=last_update,last_update_text=last_update_text)
        session.add(newproudct_link)
        session.commit()
    print('successfully Saved All Bakeries link..')
    print('Next Step Starting soon Get Proudct data ..')
    bakeries_list = session.query(EggsLinks).all()
    for proudct_url in bakeries_list:
        if proudct_url not in the_egs_list:
            the_egs_list.append(proudct_url.url)
        else:
            continue
    print('scaner API ready To get proudcts Data...')
    print('This will take time max 5 minutes Please wait Until we fetch all project data...')
    all_proudcts = get_proudct_data(the_egs_list)
    print('We successfully got all proudcts and saved internal..')
    print('API scaner now will save the proudcts data in the Database..')
    print('Please Wait until we Fetch all proudcts data and save it in the Database..')
    time_list = printTime()
    last_update = time_list[0]
    last_update_text = time_list[1]
    for proudct_object in all_proudcts:
        ju_proudct_image = proudct_object['image']
        ju_proudct_name = proudct_object['name']
        ju_proudct_price = proudct_object['price']
        newproudct_data = Eggs(name=ju_proudct_name,price=ju_proudct_price,image=ju_proudct_image,last_update=last_update,last_update_text=last_update_text)
        session.add(newproudct_data)
        session.commit()




    # Fish & Seafood category
    ju_seafood_links = proudcts_collecter(get_pagination('https://eshop.tesco.com.my/groceries/en-GB/shop/fresh-food/fish-and-seafood/all'))
    #next step for category_link in category links call proudcts_collecter(get_pagination(category_link))
    time_list = printTime()
    last_update = time_list[0]
    last_update_text = time_list[1]
    for proudct_link in ju_seafood_links:
        print('API scaner saving : ' + str(proudct_link))
        newproudct_link = SeafoodLinks(url=proudct_link,market_place='tesco',last_update=last_update,last_update_text=last_update_text)
        session.add(newproudct_link)
        session.commit()
    print('successfully Saved All Bakeries link..')
    print('Next Step Starting soon Get Proudct data ..')
    bakeries_list = session.query(SeafoodLinks).all()
    for proudct_url in bakeries_list:
        if proudct_url not in the_seafood_list:
            the_seafood_list.append(proudct_url.url)
        else:
            continue
    print('scaner API ready To get proudcts Data...')
    print('This will take time max 5 minutes Please wait Until we fetch all project data...')
    all_proudcts = get_proudct_data(the_seafood_list)
    print('We successfully got all proudcts and saved internal..')
    print('API scaner now will save the proudcts data in the Database..')
    print('Please Wait until we Fetch all proudcts data and save it in the Database..')
    time_list = printTime()
    last_update = time_list[0]
    last_update_text = time_list[1]
    for proudct_object in all_proudcts:
        ju_proudct_image = proudct_object['image']
        ju_proudct_name = proudct_object['name']
        ju_proudct_price = proudct_object['price']
        newproudct_data = Seafood(name=ju_proudct_name,price=ju_proudct_price,image=ju_proudct_image,market_place='tesco',last_update=last_update,last_update_text=last_update_text)
        session.add(newproudct_data)
        session.commit()



    # Fruits category
    ju_fruits_links = proudcts_collecter(get_pagination('https://eshop.tesco.com.my/groceries/en-GB/shop/fresh-food/fresh-fruits/all'))
    #next step for category_link in category links call proudcts_collecter(get_pagination(category_link))
    time_list = printTime()
    last_update = time_list[0]
    last_update_text = time_list[1]
    for proudct_link in ju_fruits_links:
        print('API scaner saving : ' + str(proudct_link))
        newproudct_link = FruitsLinks(url=proudct_link, market_place='tesco',last_update=last_update,last_update_text=last_update_text)
        session.add(newproudct_link)
        session.commit()
    print('successfully Saved All Bakeries link..')
    print('Next Step Starting soon Get Proudct data ..')
    bakeries_list = session.query(FruitsLinks).all()
    for proudct_url in bakeries_list:
        if proudct_url not in the_fruits_list:
            the_fruits_list.append(proudct_url.url)
        else:
            continue
    print('scaner API ready To get proudcts Data...')
    print('This will take time max 5 minutes Please wait Until we fetch all project data...')
    all_proudcts = get_proudct_data(the_fruits_list)
    print('We successfully got all proudcts and saved internal..')
    print('API scaner now will save the proudcts data in the Database..')
    print('Please Wait until we Fetch all proudcts data and save it in the Database..')
    time_list = printTime()
    last_update = time_list[0]
    last_update_text = time_list[1]
    for proudct_object in all_proudcts:
        ju_proudct_image = proudct_object['image']
        ju_proudct_name = proudct_object['name']
        ju_proudct_price = proudct_object['price']
        newproudct_data = Fruits(name=ju_proudct_name,price=ju_proudct_price,image=ju_proudct_image,market_place='tesco',last_update=last_update,last_update_text=last_update_text)
        session.add(newproudct_data)
        session.commit()




    # Fresh Meat & Poultry
    ju_fresh_meat_links = proudcts_collecter(get_pagination('https://eshop.tesco.com.my/groceries/en-GB/shop/fresh-food/fresh-meat-and-poultry/all'))
    #next step for category_link in category links call proudcts_collecter(get_pagination(category_link))
    time_list = printTime()
    last_update = time_list[0]
    last_update_text = time_list[1]
    for proudct_link in ju_fresh_meat_links:
        print('API scaner saving : ' + str(proudct_link))
        newproudct_link = FreshmeatLinks(url=proudct_link,market_place='tesco',last_update=last_update,last_update_text=last_update_text)
        session.add(newproudct_link)
        session.commit()
    print('successfully Saved All Bakeries link..')
    print('Next Step Starting soon Get Proudct data ..')
    bakeries_list = session.query(FreshmeatLinks).all()
    for proudct_url in bakeries_list:
        if proudct_url not in the_fresh_meet_list:
            the_fresh_meet_list.append(proudct_url.url)
        else:
            continue
    print('scaner API ready To get proudcts Data...')
    print('This will take time max 5 minutes Please wait Until we fetch all project data...')
    all_proudcts = get_proudct_data(the_fresh_meet_list)
    print('We successfully got all proudcts and saved internal..')
    print('API scaner now will save the proudcts data in the Database..')
    print('Please Wait until we Fetch all proudcts data and save it in the Database..')
    for proudct_object in all_proudcts:
        ju_proudct_image = proudct_object['image']
        ju_proudct_name = proudct_object['name']
        ju_proudct_price = proudct_object['price']
        newproudct_data = FreshMeat(name=ju_proudct_name,price=ju_proudct_price,image=ju_proudct_image,market_place='tesco',last_update=last_update,last_update_text=last_update_text)
        session.add(newproudct_data)
        session.commit()


    # Fresh Vegetables
    ju_fresh_vegetables_links = proudcts_collecter(get_pagination('https://eshop.tesco.com.my/groceries/en-GB/shop/fresh-food/fresh-vegetables/all'))
    #next step for category_link in category links call proudcts_collecter(get_pagination(category_link))
    time_list = printTime()
    last_update = time_list[0]
    last_update_text = time_list[1]
    for proudct_link in ju_fresh_vegetables_links:
        print('API scaner saving : ' + str(proudct_link))
        newproudct_link = FreshVegetablesLinks(url=proudct_link,market_place='tesco',last_update=last_update,last_update_text=last_update_text)
        session.add(newproudct_link)
        session.commit()
    print('successfully Saved All Bakeries link..')
    print('Next Step Starting soon Get Proudct data ..')
    bakeries_list = session.query(FreshVegetablesLinks).all()
    for proudct_url in bakeries_list:
        if proudct_url not in the_fresh_vegetables_list:
            the_fresh_vegetables_list.append(proudct_url.url)
        else:
            continue
    print('scaner API ready To get proudcts Data...')
    print('This will take time max 5 minutes Please wait Until we fetch all project data...')
    all_proudcts = get_proudct_data(the_fresh_vegetables_list)
    print('We successfully got all proudcts and saved internal..')
    print('API scaner now will save the proudcts data in the Database..')
    print('Please Wait until we Fetch all proudcts data and save it in the Database..')
    time_list = printTime()
    last_update = time_list[0]
    last_update_text = time_list[1]
    for proudct_object in all_proudcts:
        ju_proudct_image = proudct_object['image']
        ju_proudct_name = proudct_object['name']
        ju_proudct_price = proudct_object['price']
        newproudct_data = FreshVegetables(name=ju_proudct_name,price=ju_proudct_price,image=ju_proudct_image,market_place='tesco',last_update=last_update,last_update_text=last_update_text)
        session.add(newproudct_data)
        session.commit()


    # Noodles, Beancurd & Cooking Supplements
    ju_noodles_supplements_links = proudcts_collecter(get_pagination('https://eshop.tesco.com.my/groceries/en-GB/shop/fresh-food/noodles-beancurd-and-cooking-supplements/all'))
    #next step for category_link in category links call proudcts_collecter(get_pagination(category_link))
    time_list = printTime()
    last_update = time_list[0]
    last_update_text = time_list[1]
    for proudct_link in ju_noodles_supplements_links:
        print('API scaner saving : ' + str(proudct_link))
        newproudct_link = NoodlesSupplementsLinks(url=proudct_link,market_place='tesco',last_update=last_update,last_update_text=last_update_text)
        session.add(newproudct_link)
        session.commit()
    print('successfully Saved All Bakeries link..')
    print('Next Step Starting soon Get Proudct data ..')
    bakeries_list = session.query(NoodlesSupplementsLinks).all()
    for proudct_url in bakeries_list:
        if proudct_url not in the_noodles_supplements_list:
            the_noodles_supplements_list.append(proudct_url.url)
        else:
            continue
    print('scaner API ready To get proudcts Data...')
    print('This will take time max 5 minutes Please wait Until we fetch all project data...')
    all_proudcts = get_proudct_data(the_noodles_supplements_list)
    print('We successfully got all proudcts and saved internal..')
    print('API scaner now will save the proudcts data in the Database..')
    print('Please Wait until we Fetch all proudcts data and save it in the Database..')
    for proudct_object in all_proudcts:
        ju_proudct_image = proudct_object['image']
        ju_proudct_name = proudct_object['name']
        ju_proudct_price = proudct_object['price']
        newproudct_data = NoodlesSupplements(name=ju_proudct_name,price=ju_proudct_price,image=ju_proudct_image,market_place='tesco',last_update=last_update,last_update_text=last_update_text)
        session.add(newproudct_data)
        session.commit()


    # Other Fresh Food
    ju_other_fresh_links = proudcts_collecter(get_pagination('https://eshop.tesco.com.my/groceries/en-GB/shop/fresh-food/other-fresh-food/all'))
    #next step for category_link in category links call proudcts_collecter(get_pagination(category_link))
    time_list = printTime()
    last_update = time_list[0]
    last_update_text = time_list[1]
    for proudct_link in ju_other_fresh_links:
        print('API scaner saving : ' + str(proudct_link))
        newproudct_link = OtherFreshFoodLinks(url=proudct_link, market_place='tesco',last_update=last_update,last_update_text=last_update_text)
        session.add(newproudct_link)
        session.commit()
    print('successfully Saved All Bakeries link..')
    print('Next Step Starting soon Get Proudct data ..')
    bakeries_list = session.query(OtherFreshFoodLinks).all()
    for proudct_url in bakeries_list:
        if proudct_url not in the_other_fresh_list:
            the_other_fresh_list.append(proudct_url.url)
        else:
            continue
    print('scaner API ready To get proudcts Data...')
    print('This will take time max 5 minutes Please wait Until we fetch all project data...')
    all_proudcts = get_proudct_data(the_other_fresh_list)
    print('We successfully got all proudcts and saved internal..')
    print('API scaner now will save the proudcts data in the Database..')
    print('Please Wait until we Fetch all proudcts data and save it in the Database..')
    time_list = printTime()
    last_update = time_list[0]
    last_update_text = time_list[1]
    for proudct_object in all_proudcts:
        ju_proudct_image = proudct_object['image']
        ju_proudct_name = proudct_object['name']
        ju_proudct_price = proudct_object['price']
        newproudct_data = OtherFreshFood(name=ju_proudct_name,price=ju_proudct_price,image=ju_proudct_image,market_place='tesco',last_update=last_update,last_update_text=last_update_text)
        session.add(newproudct_data)
        session.commit()

        #for single_data in proudct_object:
    return str('successfully Got All The Bakery Data Please Visit Link localhost:5000/bakery_data to get the all data..')


#Noodles, Beancurd & Cooking Supplements OtherFreshFoodLinks, OtherFreshFood
# this is the main file


if __name__ == '__main__':
    app.secret_key = 'AS&S^1234Aoshsheo152h23h5j7ks9-1---3*-s,#k>s'
    app.debug = True
    app.run(host='0.0.0.0', port=5000, threaded=False)
