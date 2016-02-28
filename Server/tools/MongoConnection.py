#Object wrapper for interacting with mongo
from pymongo import MongoClient
import connectioninfo

class DatabaseConnection:
    
    def __init__(self,ip=connectioninfo.ip,port=connectioninfo.port) :
        self.m=MongoClient(connectioninfo.ip,connectioninfo.port)
        self.g=self.m.unisq
        self.cs=self.g.Courses
        self.sess=self.g.Session
        self.users=self.g.Users
        self.choice=self.g.Choices
    def checkcookie(self,cookid):
        #m=MongoClient()
        #t=m.unisq
        if self.sess.find_one({"_id":int(cookid)}):
            return True
        else:
            return False
    def find_one_course(self,param):
        return self.cs.find_one(param)
    def find_course(self,params):
        return self.cs.find(params)
    def insert_course(self,params):
        return self.cs.insert(params)
    def update_course(self,a,params):
        self.cs.update(a,params)
    def distinct_course(self,params):
        return self.cs.distinct(params)
    

    def find_session(self,param):
        return self.sess.find_one(param)
    def remove_session(self,param):
        self.sess.remove(param)
    def insert_session(self,param):
        self.sess.insert(param)

    def find_user(self,param):
        return self.users.find_one(param)
    def user_len(self):
        return self.users.count()
    def update_user(self,param,repl):
        self.users.update(param,repl)
    def insert_user(self,param):
        self.users.insert(param)
        
    
    def find_one_choice(self,param):
        return self.choice.find_one(param)
    def update_choice(self,a,param):
        self.choice.update(a,param)
    def insert_choice(self,param):
        self.choice.insert(param)
    
    def close(self):
        self.M.close()
