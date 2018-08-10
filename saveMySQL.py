#-*- coding: utf8 -*-

import pymysql
import codecs
import json
import time
import re

def create_db(dbname):
    db = pymysql.connect(host='localhost', user='root', password='', port=3306, charset='utf8')
    cursor = db.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS ' + dbname)
    cursor.execute('alter database ' + dbname + ' character set utf8')
    db.close()

def save_pw_simple():
    db = pymysql.connect(host='localhost', user='root', password='', db='pw_simple', port=3306, charset='utf8')
    cursor = db.cursor()

    # Creating categories table...
    print("Creating categories table...")
    cursor.execute('DROP TABLE IF EXISTS categories')
    cursor.execute(
        """CREATE TABLE categories (
            category_id INT(11),
            category_name VARCHAR(200),
            category_pw_url VARCHAR(255))"""
    )
    with codecs.open('categories.json', 'r', 'utf8') as f:
        categories = json.load(f)
        count = 1
        for category in categories:
            # Combine to sql and execute it.
            keys = ','.join(category.keys())
            values = ','.join(['%s'] * len(category))
            sql = 'INSERT INTO categories({keys}) VALUES({values})'.format(keys=keys, values=values)
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
            api['api_desc'] = re.compile(r'<[^>]+>|\n|\r', re.S).sub('', api['api_desc']) # [^>]+ 不是^的任意字符
            api['api_desc'] = re.compile(r'\[[^\]]+\]', re.S).sub('', api['api_desc']) # 匹配[This API is no longer available.]
            if 'api_secondary_category' in api:
                api['api_secondary_category'] = ",".join(list(set(api['api_secondary_category']))) # 将二级标签去重
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
    with codecs.open('categories.json', 'r', 'utf8') as f:
        categories = json.load(f)
        count = 1
        for category in categories:
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
            api['api_desc'] = re.compile(r'<[^>]+>|\n|\r', re.S).sub('', api['api_desc']) # [^>]+ 不是^的任意字符
            api['api_desc'] = re.compile(r'\[[^\]]+\]', re.S).sub('', api['api_desc']) # 匹配[This API is no longer available.]
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
    
def save_programmableweb_new():
    db = pymysql.connect(host='localhost', user='root', password='', db='programmableweb_new', port=3306, charset='utf8')
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
            PwURL VARCHAR(255),
            Amount INT(11))"""
    )
    with codecs.open('categories.json', 'r', 'utf8') as f:
        categories = json.load(f)
        count = 1
        for category in categories:
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
            Provider VARCHAR(100),
            ProviderURL VARCHAR(255),
            PorHomePage VARCHAR(300),
            Endpoint VARCHAR(255),
            Version VARCHAR(100),
            Type INT(11),
            ArchStyle INT(11),
            IsDeviceSpec INT(11),
            Scope INT(11),
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
            api['api_desc'] = re.compile(r'<[^>]+>|\n|\r', re.S).sub('', api['api_desc']) # [^>]+ 不是^的任意字符
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
            Company VARCHAR(100),
            URL VARCHAR(300),
            Description TEXT,
            Type INT(11))"""
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
    cursor.execute('DROP TABLE IF EXISTS mashupsketch')
    cursor.execute(
        """CREATE TABLE mashupsketch (
            Name VARCHAR(100),
            PwURL VARCHAR(255),
            Description VARCHAR(255),
            CategoryName VARCHAR(100),
            CategoryURL VARCHAR(255),
            SubmitDate DATE)"""
    )
    cursor.execute('DROP TABLE IF EXISTS apisketch')
    cursor.execute(
        """CREATE TABLE apisketch (
            Name VARCHAR(100),
            PwURL VARCHAR(255),
            Description VARCHAR(255),
            CategoryName VARCHAR(100),
            CategoryURL VARCHAR(255),
            SubmitDate DATE)"""
    )
    cursor.execute('DROP TABLE IF EXISTS apiaddition')
    cursor.execute(
        """CREATE TABLE apiaddition (
            ID	int(11),
            DocsHomePage	varchar(255),
            TwitterURL	varchar(255),
            SupEmail	varchar(100),
            Forum	varchar(255),
            ConsoleURL	varchar(255),
            TermURL	varchar(255),
            DescFileURL	varchar(255),
            DescFileType	int(11),
            IsNonPrptry	int(11),
            LiceType	varchar(100),
            IsSslSup	int(11),
            AuthModel	varchar(100),
            ReqFmt	varchar(100),
            IsHyperApi	int(11),
            IsRstctAces	int(11),
            IsUnoffical	int(11))"""
    )
    

# This method is used to count and save the primary and secondary category number in table category
def count_cate(dbname):
    db = pymysql.connect(host='localhost', user='root', password='', db=dbname, port=3306, charset='utf8')
    cursor = db.cursor()

    # Add two new field
    try:
        cursor.execute("ALTER TABLE category DROP primary_num, DROP secondary_num")
        print("Field primary_num and secondary_num have droped.")
    except:
        pass
    sql = "ALTER TABLE category ADD primary_num int(11) Default 0, ADD secondary_num int(11) Default 0"
    cursor.execute(sql)

    sql = "SELECT ID FROM category"
    cursor.execute(sql)
    categories_id = cursor.fetchall()
    for cate_id in categories_id:
        sql = "SELECT COUNT(*) FROM apicate WHERE CateID={cate_id} AND IsPri=1".format(cate_id=cate_id[0])
        cursor.execute(sql)
        primary_num = cursor.fetchone()
        sql = "SELECT COUNT(*) FROM apicate WHERE CateID={cate_id} AND IsPri=0".format(cate_id=cate_id[0])
        cursor.execute(sql)
        secondary_num = cursor.fetchone()
        sql = "UPDATE category SET primary_num={primary_num}, secondary_num={secondary_num} WHERE ID={cate_id}".format(primary_num=primary_num[0], secondary_num=secondary_num[0], cate_id=cate_id[0])
        cursor.execute(sql)

    db.commit()
    print("The number of category has successfully statistics completed.")

def count_cate2(dbname):
    db = pymysql.connect(host='localhost', user='root', password='', db=dbname, port=3306, charset='utf8')
    cursor = db.cursor()
    db2 = pymysql.connect(host='localhost', user='root', password='', db='pw_old', port=3306, charset='utf8')
    cursor2 = db2.cursor()

    # Add two new field
    try:
        cursor.execute("ALTER TABLE categories DROP primary_num, DROP secondary_num")
        print("Field primary_num and secondary_num have droped.")
    except:
        pass
    sql = "ALTER TABLE categories ADD primary_num int(11) Default 0, ADD secondary_num int(11) Default 0"
    cursor.execute(sql)

    sql = "SELECT category_id FROM categories"
    cursor.execute(sql)
    categories_id = cursor.fetchall()
    for cate_id in categories_id:
        sql = "SELECT COUNT(*) FROM apicate WHERE CateID={cate_id} AND IsPri=1".format(cate_id=cate_id[0])
        cursor2.execute(sql)
        primary_num = cursor2.fetchone()
        sql = "SELECT COUNT(*) FROM apicate WHERE CateID={cate_id} AND IsPri=0".format(cate_id=cate_id[0])
        cursor2.execute(sql)
        secondary_num = cursor2.fetchone()
        sql = "UPDATE categories SET primary_num={primary_num}, secondary_num={secondary_num} WHERE category_id={cate_id}".format(primary_num=primary_num[0], secondary_num=secondary_num[0], cate_id=cate_id[0])
        cursor.execute(sql)

    db.commit()
    print("The number of category has successfully statistics completed.")

if __name__ == '__main__':
    create_db("pw_simple")
    save_pw_simple()
    create_db("pw_old")
    save_pw_old()
    count_cate("pw_old")
    count_cate2("pw_simple")
    create_db("programmableweb_new")
    save_programmableweb_new()