#Object wrapper for interacting with mongo
from pymongo import MongoClient
import connectioninfo

class DatabaseConnection:
    def __init__(self) :
        self.m=MongoClient(connectioninfo.ip,connectioninfo.port)
        self.g=self.m.unisq
        self.cs=self.g.Courses
        self.sess=self.g.Session
        self.users=self.g.Users
        self.choice=self.g.Choices
    def checkcookie(cookid):
        #m=MongoClient()
        #t=m.unisq
        if self.sess.find_one({"_id":int(cookid)}):
            return True
        else:
            return False
    def find_one_course(param):
        return self.cs.find_one(param)
    def find_course(params):
        return self.cs.find(params)
    def insert_course(params):
        return self.cs.insert(params)

    def find_session(param):
        return self.sess.find_one(param)
    def remove_session(param):
        self.sess.remove(param)
    def insert_session(param):
        self.sess.insert(param)

    def find_user(param):
        return self.users.find_one(param)
    def update_user(param,repl):
        self.users.update(param,repl)
    def insert_user(param):
        self.user.insert(param)
        
    
    def find_one_choice(param):
        self.choice.find_one(param)
    
    def close(self):
        self.M.close()
