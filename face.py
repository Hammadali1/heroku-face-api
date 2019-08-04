import base64
import os
from wtforms import Form, StringField, SubmitField
from flask_pymongo import PyMongo
from flask import Flask, jsonify,json,request,render_template
from wtforms import Form, StringField, SubmitField
import glob
import numpy as np
import face_recognition
import cv2
import pickle
from flask_cors import CORS
import urllib

app = Flask(__name__)
CORS(app)

app.config['MONGO_DBNAME']=''
app.config['MONGO_URI']='mongodb://hammad:hammad123@ds351455.mlab.com:51455/data'
mongo = PyMongo(app)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

@app.route("/cam")

def cam():
        known_face_encoding=[]
        known_face_name=[]
        known_id=[]
        data = mongo.db.suspect.find({})
        for i in data:
            for image in i["image"]:
                print(image)
                print(i["name"])
                
                resp = urllib.request.urlopen(image)
                image= np.asarray(bytearray(resp.read()),dtype="uint8")
                image=cv2.imdecode(image,cv2.IMREAD_COLOR)               

                
                faces = face_cascade.detectMultiScale(image, 1.3, 5,minSize=(100, 100))
                if type(faces) is not tuple:
                        facecnt = len(faces)
                        height, width = image.shape[:2]



                        for (x, y, w, h) in faces:
                           r = max(w, h) / 2
                           centerx = x + w / 2
                           centery = y + h / 2
                           nx = int(centerx - r)
                           ny = int(centery - r)
                           nr = int(r * 2)

                           faceimg = image[ny:ny+nr, nx:nx+nr]
                           lastimg = cv2.resize(faceimg, (300, 300))

                        mubi = face_recognition.face_encodings(lastimg)[0]
                        known_face_encoding.append(mubi)
                        known_face_name.append(i["name"])
                        known_id.append(i["_id"])    

        with open("test1.txt", "wb") as fp:   #Pickling
             pickle.dump(known_face_encoding, fp)

        with open("test2.txt", "wb") as fp:   #Pickling
             pickle.dump(known_face_name, fp)

        with open("test3.txt", "wb") as fp:   #Pickling
             pickle.dump(known_id, fp)

        
        return  jsonify('Model Updated')
        
              



@app.route("/image",methods=['POST','GET'])

def Recognition():  
  if request.method=='POST':
     # Grab a single frame of video
    with open("test1.txt", "rb") as fp:   # Unpickling
      known_face_encodings = pickle.load(fp)


    with open("test2.txt", "rb") as fp:   # Unpickling
       known_face_names = pickle.load(fp)
     
    with open("test3.txt", "rb") as fp:   # Unpickling
       known_id = pickle.load(fp)
 
    
    frame=request.files['img']

    image = cv2.imdecode(np.fromstring(frame.read(), np.uint8), cv2.IMREAD_UNCHANGED)

    faces = face_cascade.detectMultiScale(image, 1.3, 5)
    



    if type(faces) is not tuple:
        
        facecnt = len(faces)
        height, width = image.shape[:2]



        for (x, y, w, h) in faces:
              r = max(w, h) / 2
              centerx = x + w / 2
              centery = y + h / 2
              nx = int(centerx - r)
              ny = int(centery - r)
              nr = int(r * 2)

              faceimg = image[ny:ny+nr, nx:nx+nr]
              lastimg = cv2.resize(faceimg, (300, 300))
              


        face_encodings = face_recognition.face_encodings(lastimg)[0]

                # See if the face is a match for the known face(s)
        match=face_recognition.face_distance(known_face_encodings,face_encodings)
        matches=list(match<=0.4)
        #matches = face_recognition.compare_faces(known_face_encodings, face_encodings)
        name = "Unknown"

        if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                ID= known_id[first_match_index]
                
                data = mongo.db.suspect.find({"_id":ID})
                for i in data:
                  images=i["image"]
                print(name)

                return jsonify([{'response':name,'images':images}])
            
        else:
                 return ('Unknown')
    else:
       return ('Face Not Detected')   

    
  else:
    return render_template("api.html")
    


if __name__ == "__main__":
    app.run(debug=True)
