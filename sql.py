import uuid
import psycopg2

db = psycopg2.connect(
    host='ec2-54-160-120-28.compute-1.amazonaws.com',
    database='d5r3vf6s48dgvv',
    port='5432',
    user='aymgvugjhvnutc',
    password='a60532153347a5db87b1a3ad4191e2990164b9bcf2fa95deb4b7461fcfe8f9a8')
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
    sqlquery = f"""select * from users where "username"  = '{username}' and "password" = '{password}';"""
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
    
