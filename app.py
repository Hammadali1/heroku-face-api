from flask_pymongo import PyMongo
from wtforms import Form, StringField, SubmitField
from flask import Flask, jsonify,json,request,render_template
import os

app = Flask(__name__)


app.config['MONGO_DBNAME']=''
app.config['MONGO_URI']='mongodb://hammad:hammad123@ds351455.mlab.com:51455/data'
mongo = PyMongo(app)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/suspect", methods=['POST'])
def upload():
    if request.method=='POST':
        Uname=request.form['name']
        Id=request.form['id']
        Message=request.form['message']#s='img/'+Id
        target = os.path.join(APP_ROOT, 'img/')
        if not os.path.isdir(target):
            os.mkdir(target)
                
        for file in request.files.getlist("img"):
            print(file)
            filename=Id+'.jpg'
            destination = "/".join([target, filename])
            print(destination)
            file.save(destination)
        
        mongo.db.suspect.insert({"_id": Id,"name":Uname,"message": Message,"Path":destination})
        return jsonify({'msg':"successfull Add"})   
      

@app.route("/suspect", methods=['GET'])
def retrieve():
    if request.method=='GET':
        data = mongo.db.suspect.find({}).count()
        if (data == 0):
            return "data not found"
        else:
            d = []
            data=mongo.db.suspect.find({})
            for i in data:
                #image="/".join([target, i['_id']])
                d.append({"id":i["_id"] ,"name": i["name"],"message":i["message"],'image':i["Path"]})
        
            return jsonify(d)
            

@app.route("/suspect/<string:param>", methods=['DELETE'])
def delete(param):
    if request.method=='DELETE':
        
        data=mongo.db.suspect.find({'_id': param})
        ddd={}
        data=mongo.db.suspect.find({'_id': param})
        for i in data:
          ddd={"id":i["_id"] ,"name": i["name"],"message":i["message"],'Path':i["Path"]}  
        addrr=ddd['Path']
        mongo.db.suspect.delete_one({'_id': param})
        os.remove(addrr)
        return "deleted"
        
@app.route("/suspect/<string:param>", methods=['POST','GET'])
def Update(param):
    if request.method=='GET':
        if (mongo.db.suspect.find({'_id': param})):
             d = []
             data=mongo.db.suspect.find({'_id':param})
             for i in data:
                 d.append({"id":param ,"name": i["name"],"message":i["message"],'Path':i['Path']})
             return jsonify(d)
        return ('not find')                
    if request.method=='POST':
        Uname=request.form['name']
        Id=param
        Message=request.form['message']
        
        d={}
        data=mongo.db.suspect.find({'_id': param})
        for i in data:
          dd={"id":i["_id"] ,"name": i["name"],"message":i["message"],'Path':i["Path"]}  
        addrr=dd['Path']
        target = os.path.join(APP_ROOT, 'img/')

        if not os.path.isdir(target):
            os.mkdir(target)
                
        for file in request.files.getlist("img"):
            os.remove(addrr)
            filename=Id+'.jpg'
            destination = "/".join([target, filename])
            file.save(destination)
        if (mongo.db.suspect.find({'_id': param})):
        
           update_query=mongo.db.suspect.update_one({"_id": Id},{'$set':{"name":Uname,"message": Message,"Path":destination}})
        return jsonify({'msg':"successfull Add"})   


# ADMIN PART

@app.route("/Admin",methods=['POST'])
def AddAdmin():
    if request.method=='POST':
       Uname=request.form['Uname']
       Email=request.form['Email']
       Password=request.form['Password']
       NIC=request.form['NIC']
       mongo.db.admin.insert({'_id':NIC,'uname':Uname,'email':Email,'password':Password})
       return "Successfully add"
                  

@app.route("/Admin",methods=['GET'])
def ShowAdmin():
    if request.method=='GET':
       data=mongo.db.admin.find({}).count()
       if(data==0):
           return "data not found"
       else:
            d = []
            data=mongo.db.admin.find({})
            for i in data:
                d.append({"id":i["_id"] ,"name": i["uname"],"email":i["email"]})
            return (jsonify(d))
                  

@app.route("/Admin/<string:param>",methods=['GET','POST'])
def UpdateAdmin(param):
        
      if request.method=='GET':
        print("enter")
        if (mongo.db.admin.find({'_id': param})):
             d = []
             data=mongo.db.admin.find({'_id':param})
             for i in data:
                 d.append({"id":i["_id"] ,"name": i["uname"],"email":i["email"]})
             return jsonify(d)
        return ('not find')           

      
      if request.method=='POST':
        Uname=request.form['name']
        Id=param
        Message=request.form['email']
        Oldpassword=request.form['oldPassword']
        Newpassword=request.form['newPassword']
        d={}
        data=mongo.db.admin.find({'_id': param})
        for i in data:
          dd={"id":i["_id"] ,"name": i["uname"],"email":i["email"],'password':i["password"]}  
        password=dd['password']
        if (Oldpassword==password):
            if (mongo.db.admin.find({'_id': param})):
              update_query=mongo.db.admin.update_one({"_id": Id},{'$set':{"name":Uname,"email": Message,"password":Newpassword}})
            return jsonify({'msg':"successfull Add"})   
        else:
           return ("wrong password")           
    

# USER PART





@app.route("/User",methods=['POST'])
def AddUser():
    if request.method=='POST':
       Uname=request.form['Uname']
       Email=request.form['Email']
       Password=request.form['Password']
       NIC=request.form['NIC']

       mongo.db.user.insert({'_id':NIC,'uname':Uname,'email':Email,'password':Password})
       return "Successfully add"
                  
    return render_template('signupUser.html')


@app.route("/User",methods=['GET'])
def ShowUser():
    if request.method=='GET':
       data=mongo.db.user.find({}).count()
       if(data==0):
           return "data not found"
       else:
            d = []
            data=mongo.db.user.find({})
            for i in data:
                d.append({"id":i["_id"] ,"name": i["uname"],"email":i["email"],"password":i["password"]})
            return (jsonify(d))
              
@app.route("/User/<string:param>",methods=['GET','POST'])
def UpdateUser(param):
        
      if request.method=='GET':
        if (mongo.db.user.find({'_id': param})):
             d = []
             data=mongo.db.user.find({'_id':param})
             for i in data:
                 d.append({"id":i["_id"] ,"name": i["uname"],"email":i["email"],"password":i["password"]})
             return jsonify(d)
        return ('not find')           

      
      if request.method=='POST':
        Uname=request.form['name']
        Id=param
        Message=request.form['email']
        password=request.form['password']
        
        if (mongo.db.user.find({'_id': param})):
        
              update_query=mongo.db.user.update_one({"_id": Id},{'$set':{"name":Uname,"email": Message,"password":password}})
              return jsonify({'msg':"successfull Add"})   
                   


@app.route("/User/<string:param>", methods=['DELETE'])
def DeleteUser(param):
    if request.method=='DELETE':
        
        data=mongo.db.user.find({'_id': param})
        ddd={}
        mongo.db.user.delete_one({'_id': param})
        return "deleted"







if __name__ == "__main__":
    app.run(debug=True)