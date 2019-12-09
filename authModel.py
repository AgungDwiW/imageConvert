#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 22:32:55 2019

@author: temperantia
"""
import pymysql
import uuid
import os
import json
from flask import jsonify
class Auth :
    def __init__(self):
        """
        connect to database
        """
        dbCon = {
        "server" : "127.0.0.1",
        "id" : "root",
        "pass" : "",
        "db" : "imageconverter"
        }        
        self.maxFree = 30000000
        try:
            self.db=pymysql.connect(dbCon['server'],dbCon["id"],dbCon['pass'],dbCon['db'])
            self.cursor = self.db.cursor()
        except:
            return jsonify(status = "error", message = "couldnt connect to db")
    
    def login(self, user, password):
        """
        login function; input user, password; output {"token" : "generatedToken"}
        """
        try:
            self.cursor.execute("select id from users where username='"+user+"' and password ='"+ password+"'" )
            result = self.cursor.fetchall()
        except:
            return jsonify(status = "error", message = "username or password incorrect")
        if (len(result)==0):
            return False
        else:
            return jsonify(status = "success", message = "login success", token = self.generateToken(result[0][0]))
    
    def getIdByUsername(self, user):
        try:
            self.cursor.execute("select id from users where username = '"+ user+"'")
            a = self.cursor.fetchall()
            return a[0][0]
        except:
            return False
    
    def generateToken(self, idUser):
        """
        to generate token, auxilary function to login function
        """
        try:
            token = uuid.uuid4().hex
            self.cursor.execute("insert into token(token, id_user) values('"+
                                token+"', '" +str(idUser)+"')")
            self.db.commit()
            return token
        except:
            return False
    
    
    def register(self, user, password, type_user):
        """
        to register
        """
        try:
            self.cursor.execute("insert into users(username, password, type, data_usage)"+" values('"+ str(user) + "', '"+str(password)+ "', "+ str(type_user) + ", 0)")
            self.db.commit()
            return jsonify(status = "success", message = "user successfully registered")
        
        except:
            return jsonify(status = "error", message = "username already taken")
        
    def checkToken(self, token):
        """
        check token; return user id if success, false if fail
        """
        try:
            self.cursor.execute("select id_user from token where token = '"+ token+"'")
            result = self.cursor.fetchall()
            return result[0][0]
        except:
            return False
    
    def checkUserType(self, id_user):
        """
        check user type; 0 for free, 1 for premium
        """
        try:
            self.cursor.execute("select type from users where id = " + str(id_user))
            result = self.cursor.fetchall()
            return result[0][0]
        except:
            return False
    
    def checkUsage(self, id_user):
        """
        check data usage for user
        """
        try:
            self.cursor.execute("select data_usage from users where id = " + str(id_user))
            return self.cursor.fetchall()[0][0]
        except:
            return False
    
    def updateUsage(self, id_user, filepath):
        """
        update datausage for user
        """
        try:
            size = os.stat(filepath).st_size
            currentUsage = int(self.checkUsage(id_user))
            self.cursor.execute("Update users set data_usage = '"+ str(currentUsage+size) +"'")
            self.db.commit()
        except:
            return False
        
    def checkLimit(self, id_user):
        """
        check wether an user hit its limit; 
        """
        tipe =  self.checkUserType(id_user)
        if (tipe == 1):
            return False
        usage = self.checkUsage(id_user)
        if (usage>self.maxFree):
            return True
    
    def putFile(self, id_user, filepath, root):
        """
        check wether an user hit its limit; 
        """
        try:
            self.cursor.execute("insert into storage (filepath, id_user) values('"+
                                str(filepath)+"', '"+ str(id_user)+"')")
            self.db.commit()
            idFile = self.cursor.lastrowid
            link = os.path.join(str(root),"api/download", str(id_user),  str(idFile))
            return link
        except:
            return False
    
    def getFile(self, id_user, id_file):
        try:
            self.cursor.execute("select filepath from storage where id_user = '" 
                                +str(id_user) + "' and id = '"+ str(id_file)+"'")
            result = self.cursor.fetchall()
            return result[0][0]
        except:
            return False

if __name__ == "__main__":
    auth = Auth()
    auth.register("admin2", "adminadmin", "1")
    token = json.load(auth.login("admin5", "adminadmin"))
    print(token)
    idUser = auth.checkToken(token)
    print(idUser)
    print(auth.checkLimit(idUser))
    auth.updateUsage(idUser, "size")
    
    
