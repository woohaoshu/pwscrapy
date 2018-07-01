#-*- coding: utf8 -*-

import pymysql
import codecs
import json
import time

def create_db(dbname):
    db = pymysql.connect(host='localhost', user='root', password='', port=3306, charset='utf8')
    cursor = db.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS ' + dbname)
    cursor.execute('alter database ' + dbname + ' character set utf8')
    db.close()

def save_pw_simple():
    db = pymysql.connect(host='localhost', user='root', password='', db='pw_simple', port=3306, charset='utf8')
    cursor = db.cursor()

    # Creating categorys table...
    print("Creating categorys table...")
    cursor.execute('DROP TABLE IF EXISTS categorys')
    cursor.execute(
        """CREATE TABLE categorys (
            category_id INT(11),
            category_name VARCHAR(200),
            category_pw_url VARCHAR(255))"""
    )
    with codecs.open('categorys.json', 'r', 'utf8') as f:
        categorys = json.load(f)
        count = 1
        for category in categorys:
            # Combine to sql and execute it.
            keys = ','.join(category.keys())
            values = ','.join(['%s'] * len(category))
            sql = 'INSERT INTO categorys({keys}) VALUES({values})'.format(keys=keys, values=values)
            try:
                if cursor.execute(sql, tuple(category.values())):
                    # print('insert successful')
                    db.commit()
            except Exception as e:
                print(category['category_id'] + "insert failed!", e)
                db.rollback()
            count += 1
            if count % 1000 == 0:
                print(count)

    # Creating APIs table...
    print("Creating APIs table...")
    cursor.execute('DROP TABLE IF EXISTS APIS')
    cursor.execute(
        """CREATE TABLE APIS (
            api_id INT(11),
            api_name VARCHAR(200),
            api_pw_url VARCHAR(255),
            api_url VARCHAR(300),
            api_primary_category VARCHAR(100),
            api_secondary_category TEXT,
            api_desc TEXT)"""
    )
    with codecs.open('apis.json', 'r', 'utf8') as f:
        apis = json.load(f)
        count = 1
        for api in apis:
            if 'api_secondary_category' in api:
                api['api_secondary_category'] = ",".join(api['api_secondary_category'])
            keys = ','.join(api.keys())
            values = ','.join(['%s'] * len(api))
            sql = 'INSERT INTO APIS({keys}) VALUES({values})'.format(keys=keys, values=values)
            try:
                if cursor.execute(sql, tuple(api.values())):
                    # print('insert successful')
                    db.commit()
            except Exception as e:
                print(api['api_id'] + "insert failed!", e)
                db.rollback()
            count += 1
            if count % 1000 == 0:
                print(count)

    # Creating MASHUPs table...
    print("Creating MASHUPs table...")
    cursor.execute('DROP TABLE IF EXISTS MASHUPS')
    cursor.execute(
        """CREATE TABLE MASHUPS (
            mashup_id INT(11),
            mashup_name VARCHAR(200),
            mashup_pw_url VARCHAR(255),
            mashup_url VARCHAR(300),
            mashup_category TEXT,
            mashup_related_apis TEXT,
            mashup_desc TEXT)"""
    )
    with codecs.open('mashups.json', 'r', 'utf8') as f:
        mashups = json.load(f)
        count = 1
        for mashup in mashups:
            if 'mashup_category' in mashup:
                mashup['mashup_category'] = ",".join(mashup['mashup_category'])
            if 'mashup_related_apis' in mashup:
                mashup['mashup_related_apis'] = ",".join(mashup['mashup_related_apis'])
            keys = ','.join(mashup.keys())
            values = ','.join(['%s'] * len(mashup))
            sql = 'INSERT INTO MASHUPS({keys}) VALUES({values})'.format(keys=keys, values=values)
            try:
                if cursor.execute(sql, tuple(mashup.values())):
                    # print('insert successful')
                    db.commit()
            except Exception as e:
                print(mashup['mashup_id'] + "insert failed!", e)
                db.rollback()
            count += 1
            if count % 1000 == 0:
                print(count)

    # Creating NEWs table...
    print("Creating NEWs table...")
    cursor.execute('DROP TABLE IF EXISTS NEWS')
    cursor.execute(
        """CREATE TABLE NEWS (
            news_page_count INT(11),
            news_count INT(11),
            news_name VARCHAR(200),
            news_pw_url VARCHAR(400),
            news_article_type VARCHAR(100),
            news_category TEXT,
            news_author VARCHAR(100),
            news_date VARCHAR(100),
            news_abstract TEXT,
            news_content TEXT)"""
    )
    with codecs.open('news.json', 'r', 'utf8') as f:
        news = json.load(f)
        count = 1
        for new in news:
            if 'news_date' in new:
                new['news_date'] = "-".join(new['news_date'])
            if 'news_category' in new:
                new['news_category'] = ",".join(new['news_category'])
            keys = ','.join(new.keys())
            values = ','.join(['%s'] * len(new))
            sql = 'INSERT INTO NEWS({keys}) VALUES({values})'.format(keys=keys, values=values)
            try:
                if cursor.execute(sql, tuple(new.values())):
                    # print('insert successful')
                    db.commit()
            except Exception as e:
                print(new['news_pw_url'] + "insert failed!", e)
                db.rollback()
            count += 1
            if count % 1000 == 0:
                print(count)
    db.close()

def save_pw_old():
    db = pymysql.connect(host='localhost', user='root', password='', db='pw_old', port=3306, charset='utf8')
    cursor = db.cursor()
    
    # Set up Category, API Map
    category_dict = {}
    api_dict = {}

    # Creating category table...
    print("Creating category table...")
    cursor.execute('DROP TABLE IF EXISTS category')
    cursor.execute(
        """CREATE TABLE category (
            ID INT(11),
            Name VARCHAR(200),
            PwURL VARCHAR(255))"""
    )
    with codecs.open('categorys.json', 'r', 'utf8') as f:
        categorys = json.load(f)
        count = 1
        for category in categorys:
            category_dict[category['category_name']] = category['category_id']
            # Map new fields to old fields.
            category['ID'] = category.pop('category_id')
            category['Name'] = category.pop('category_name')
            category['PwURL'] = category.pop('category_pw_url')
            # Combine to sql and execute it.
            keys = ','.join(category.keys())
            values = ','.join(['%s'] * len(category))
            sql = 'INSERT INTO category({keys}) VALUES({values})'.format(keys=keys, values=values)
            try:
                if cursor.execute(sql, tuple(category.values())):
                    # print('insert successful')
                    db.commit()
            except Exception as e:
                print(category['ID'] + "insert failed!", e)
                db.rollback()
            count += 1
            if count % 1000 == 0:
                print(count)
    
    # Creating apibasic, apicate table...
    print("Creating apibasic, apicate table...")
    cursor.execute('DROP TABLE IF EXISTS apibasic')
    cursor.execute(
        """CREATE TABLE apibasic (
            ID INT(11),
            Name VARCHAR(200),
            PwURL VARCHAR(255),
            PorHomePage VARCHAR(300),
            Description TEXT)"""
    )
    cursor.execute('DROP TABLE IF EXISTS apicate')
    cursor.execute(
        """CREATE TABLE apicate (
            ApiID INT(11),
            CateID INT(11),
            IsPri INT(11))"""
    )
    with codecs.open('apis.json', 'r', 'utf8') as f:
        apis = json.load(f)
        count = 1
        for api in apis:
            api_dict[api['api_name']] = api['api_id']
            # Map APIs to category
            if 'api_primary_category' in api:
                apicate = {}
                apicate['ApiID'] = api['api_id']
                apicate['CateID'] = category_dict[api['api_primary_category']]
                apicate['IsPri'] = 1
                keys = ','.join(apicate.keys())
                values = ','.join(['%s'] * len(apicate))
                sql = 'INSERT INTO apicate({keys}) VALUES({values})'.format(keys=keys, values=values)
                try:
                    if cursor.execute(sql, tuple(apicate.values())):
                        db.commit()
                except Exception as e:
                    print(api['api_id'] + "insert failed!", e)
                    db.rollback()
                del api['api_primary_category']
            if 'api_secondary_category' in api:
                for c in api['api_secondary_category']:
                    apicate = {}
                    apicate['ApiID'] = api['api_id']
                    apicate['CateID'] = category_dict[c]
                    apicate['IsPri'] = 0
                    keys = ','.join(apicate.keys())
                    values = ','.join(['%s'] * len(apicate))
                    sql = 'INSERT INTO apicate({keys}) VALUES({values})'.format(keys=keys, values=values)
                    try:
                        if cursor.execute(sql, tuple(apicate.values())):
                            db.commit()
                    except Exception as e:
                        print(api['api_id'] + "insert failed!", e)
                        db.rollback()
                del api['api_secondary_category']
            # Map new fields to old fields.
            api['ID'] = api.pop('api_id')
            api['Name'] = api.pop('api_name')
            api['PwURL'] = api.pop('api_pw_url')
            api['PorHomePage'] = api.pop('api_url')
            api['Description'] = api.pop('api_desc')
            # Combine to sql and execute it.
            keys = ','.join(api.keys())
            values = ','.join(['%s'] * len(api))
            sql = 'INSERT INTO apibasic({keys}) VALUES({values})'.format(keys=keys, values=values)
            try:
                if cursor.execute(sql, tuple(api.values())):
                    # print('insert successful')
                    db.commit()
            except Exception as e:
                print(api['ID'] + "insert failed!", e)
                db.rollback()
            
            count += 1
            if count % 1000 == 0:
                print(count)

    # Creating mashup, mashupapi, mashupcate table...
    print("Creating mashup, mashupapi, mashupcate table...")
    cursor.execute('DROP TABLE IF EXISTS mashup')
    cursor.execute(
        """CREATE TABLE mashup (
            ID INT(11),
            Name VARCHAR(200),
            PwURL VARCHAR(255),
            URL VARCHAR(300),
            Description TEXT)"""
    )
    cursor.execute('DROP TABLE IF EXISTS mashupapi')
    cursor.execute(
        """CREATE TABLE mashupapi (
            MashupID INT(11),
            ApiID INT(11))"""
    )
    cursor.execute('DROP TABLE IF EXISTS mashupcate')
    cursor.execute(
        """CREATE TABLE mashupcate (
            MashupID INT(11),
            CateID INT(11),
            IsPri INT(11))"""
    )
    with codecs.open('mashups.json', 'r', 'utf8') as f:
        mashups = json.load(f)
        count = 1
        for mashup in mashups:
            # Map MASHUPs to category, the first cate is primary cate
            if 'mashup_category' in mashup:
                # The first cate is primary cate
                mashupcate = {}
                mashupcate['MashupID'] = mashup['mashup_id']
                mashupcate['CateID'] = category_dict[mashup['mashup_category'][0]]
                mashupcate['IsPri'] = 1
                keys = ','.join(mashupcate.keys())
                values = ','.join(['%s'] * len(mashupcate))
                sql = 'INSERT INTO mashupcate({keys}) VALUES({values})'.format(keys=keys, values=values)
                try:
                    if cursor.execute(sql, tuple(mashupcate.values())):
                        db.commit()
                except Exception as e:
                    print(mashup['mashup_id'] + "insert failed!", e)
                    db.rollback()
                # The others are not primary cate
                for m in mashup['mashup_category'][1:]:
                    mashupcate = {}
                    mashupcate['MashupID'] = mashup['mashup_id']
                    mashupcate['CateID'] = category_dict[m]
                    mashupcate['IsPri'] = 0
                    keys = ','.join(mashupcate.keys())
                    values = ','.join(['%s'] * len(mashupcate))
                    sql = 'INSERT INTO mashupcate({keys}) VALUES({values})'.format(keys=keys, values=values)
                    try:
                        if cursor.execute(sql, tuple(mashupcate.values())):
                            db.commit()
                    except Exception as e:
                        print(mashup['mashup_id'] + "insert failed!", e)
                        db.rollback()
                del mashup['mashup_category']
            if 'mashup_related_apis' in mashup:
                for r in mashup['mashup_related_apis']:
                    mashupapi = {}
                    mashupapi['MashupID'] = mashup['mashup_id']
                    if r in api_dict:
                        mashupapi['ApiID'] = api_dict[r]
                    else:
                        mashupapi['ApiID'] = -1
                    keys = ','.join(mashupapi.keys())
                    values = ','.join(['%s'] * len(mashupapi))
                    sql = 'INSERT INTO mashupapi({keys}) VALUES({values})'.format(keys=keys, values=values)
                    try:
                        if cursor.execute(sql, tuple(mashupapi.values())):
                            db.commit()
                    except Exception as e:
                        print(mashup['mashup_id'] + "insert failed!", e)
                        db.rollback()
                del mashup['mashup_related_apis']
            # Map new fields to old fields.
            mashup['ID'] = mashup.pop('mashup_id')
            mashup['Name'] = mashup.pop('mashup_name')
            mashup['PwURL'] = mashup.pop('mashup_pw_url')
            mashup['URL'] = mashup.pop('mashup_url')
            mashup['Description'] = mashup.pop('mashup_desc')
            # Combine to sql and execute it.
            keys = ','.join(mashup.keys())
            values = ','.join(['%s'] * len(mashup))
            sql = 'INSERT INTO mashup({keys}) VALUES({values})'.format(keys=keys, values=values)
            try:
                if cursor.execute(sql, tuple(mashup.values())):
                    db.commit()
            except Exception as e:
                print(mashup['ID'] + "insert failed!", e)
                db.rollback()
            count += 1
            if count % 1000 == 0:
                print(count)
    

if __name__ == '__main__':
    create_db("pw_simple")
    save_pw_simple()
    create_db("pw_old")
    save_pw_old()