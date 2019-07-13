
import os
from wtforms import Form, StringField, SubmitField
from flask_pymongo import PyMongo
from flask import Flask, jsonify,json,request,render_template
from wtforms import Form, StringField, SubmitField
import glob
import numpy as np
import face_recognition
from cv2 import cv2
import pickle

app = Flask(__name__)

"""
@app.route("/image",methods=['POST'])

def Recognition():  
  if request.method=='POST':
     # Grab a single frame of video
    with open("test1.txt", "rb") as fp:   # Unpickling
      known_face_encodings = pickle.load(fp)


    with open("test2.txt", "rb") as fp:   # Unpickling
       known_face_names = pickle.load(fp)

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    frame=request.files['img']
    #data=frame.base64.b64decode(frame)
    #img=request.files['img']
    #frame = cv2.imread(data)
    #im=base64.b64decode(img)
    #nparr=np.fromstring(im,np.uint8)
    #frame=cv2.imdecode(nparr,cv2.IMREAD_UNCHANGED)  
    image = cv2.imdecode(np.fromstring(frame.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    #frame = cv2.imread(request.files['img'])
    # Resize frame of video to 1/4 size for faster face recognition processing
    #                           small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    #frame = face_cascade.detectMultiScale(frame, 1.3, 5)
    
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    #                            rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    faces = face_cascade.detectMultiScale(image, 1.3, 5,minSize=(100, 100))


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
              



            

        # Find all the faces and face encodings in the current frame of video
    #face_locations = face_recognition.face_locations(lastimg)
    face_encodings = face_recognition.face_encodings(lastimg)[0]

            # See if the face is a match for the known face(s)
    matches = face_recognition.compare_faces(known_face_encodings, face_encodings)
    name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
    if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
            
               #return jsonify(name)
                # face_names.append({'id':name})
                #cv2.imshow("input",data)
                
                return jsonify([{'response':name}])
            
    else:
                 return ("ID does not exist")

  else:
    return render_template("api.html")
"""


@app.route("/")
def index():
    return ("OKKKK")

if __name__ == "__main__":
    app.run(debug=True)
