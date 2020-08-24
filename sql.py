import uuid
import psycopg2

db = psycopg2.connect(
    host='ec2-3-213-102-175.compute-1.amazonaws.com',
    database='db5d6qngk856a5',
    port='5432',
    user='vyqyaeriinmhhj',
    password='c8fcb209e20cb2fab624757d29123ded4816f94502f67ea6e1d1c304f1054477')
cursor = db.cursor()


def signUpUser(username, password):
    key = uuid.uuid1()
    sqlquery = f"""insert into users(username,key,password) values('{username}','{key}','{password}')"""
    cursor.execute(sqlquery)
    db.commit()


def presenceOfUser(username):
    sqlquery = f"""select * from users where username = '{username}' """
    cursor.execute(sqlquery)
    data = cursor.fetchone()
    return True if data else False

def authenticateUser(username,password):
    sqlquery = f"""select * from users where "username"  = '{username}' and "pasword" = '{password}';"""
    cursor.execute(sqlquery)
    data = cursor.fetchone()
    return True if data else False

def getApiKey(uname):
    sqlquery = f"""select "key" from users where "username" = '{uname}';"""
    cursor.execute(sqlquery)
    return cursor.fetchone()


def get_value(apikey,id):
    sqlquery = f"""select "value" from data where apikey = '{apikey}' and id = '{id}';"""
    cursor.execute(sqlquery)
    data = cursor.fetchone()
    return data[0] if data else False

def apikeyPresenceCheck(apikey):
    sqlquery = f"""select * from users where "key" = '{apikey}'"""
    cursor.execute(sqlquery)
    data = cursor.fetchone()
    return True if data else False

def idPresenceCheck(id):
    sqlquery = f"""select * from data where "id" = '{id}'"""
    cursor.execute(sqlquery)
    data = cursor.fetchone()
    return True if data else False


def getUsernameAndPasswordFromApiKey(apikey):
    sqlquery = f"""select "username","password" from users where "key" = '{apikey}';"""
    cursor.execute(sqlquery)
    data = cursor.fetchone()
    return data if data else False

def alterValue(apikey,id,value):
    if apikeyPresenceCheck(apikey) and idPresenceCheck(id):
        sqlquery = f"""update data set value = '{value}' where "apikey" = '{apikey}' and "id" = '{id}';"""
        cursor.execute(sqlquery)
        db.commit()
        return True
    else:
        return False    
    
