import pymongo
import certifi
from flask import Flask, request, jsonify, json

client = pymongo.MongoClient("mongodb+srv://sharmin-02:HqK39MyaCeWjNuD1@cluster0.alwppg4.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = client["mydb"]


app =  Flask(__name__)
@app.route("/jokes", methods=["GET"])
def mymethod():
    rows = db.mycollection.find({})
    jokes = []
    for x in rows:
        jokes.append(x.get("joke"))
    return jsonify({"all jokes": jokes})

@app.route("/post/env", methods=["POST"])
def setEnv():
    data = json.loads(request.data)
    db.environmental_data.insert_one(data)
    return jsonify({"message" : "data insertion was successful"})

@app.route("/post/pose", methods=["POST"])
def setPose():
    data = json.loads(request.data)
    db.pose_data.insert_one(data)
    return jsonify({"message" : "data insertion was successful"})

@app.route("/sensors/env", methods=["GET"])
def getEnv():
    row = db.environmental_data.find().sort("_id", -1).limit(1)
    item = row[0]
    return jsonify({"temp": item.get("temp"), 
    "humidity": item.get("humidity"), 
    "timestamp": item.get("timestamp")})

@app.route("/sensors/pose", methods=["GET"])
def getPose():
    row = db.pose_data.find().sort("_id", -1).limit(1)
    item = row[0]
    return jsonify({"presence": item.get("presence"), 
    "pose": item.get("pose"), 
    "timestamp": item.get("timestamp")})    

if __name__ == "__main__":
    app.run(debug=True)






