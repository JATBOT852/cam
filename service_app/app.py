from flask import flask ,  request, jsonify
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from Video import FaceDetectionApp
app=Flask(__name__)
CORS(app)

@app.route("/video", methods=["POST", "GET"])
def face_detection():
    if request.method == "POST":
        video = FaceDetectionApp.genarate_video()
        mimetype = 'multipart/x-mixed-replace; boundary=frame'
        return Response(video, mimetype=mimetype)
    elif request.method == "GET":
        return jsonify({"message": "Video is being generated"})

        