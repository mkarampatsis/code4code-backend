from flask import Blueprint, request, Response, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from src.models.exercise import Exercise
from bson.json_util import dumps, loads 
import json

exercises = Blueprint("exercises", __name__)

@exercises.route("/one/<string:code>", methods=["GET"])
@jwt_required()
def get_exercise(code):
    try:
        exercise = Exercise.objects.get(exercise=code)
        return Response(exercise.to_json(), mimetype="application/json", status=200)
    except Exercise.DoesNotExist:
        return Response(
            json.dumps({"error": f"Exercise with code {code} does not exist"}),
            mimetype="application/json",
            status=404,
        )


@exercises.route("/all/<string:type>", methods=["GET"])
@jwt_required()
def get_all_exercises_by_type(type):
    try:
        print("Get all exercises")
        exercises = Exercise.objects(type=type)
        return Response(exercises.to_json(), mimetype="application/json", status=200)
    except Exercise.DoesNotExist:
        return Response(
            json.dumps({"error": f"Failed to load {type} exercises"}),
            mimetype="application/json",
            status=404,
        )
    
@exercises.route("/learner/<string:course>", methods=["GET"])
# @jwt_required()
def get_learner_exercises_by_course(course):
    try:
        print("Get learner exercises")
        pipeline = [
            {"$match" : {"type" : course}},
            {"$sample": {"size": 1}}
        ]
        exercises = Exercise.objects.aggregate(pipeline)
        return Response(dumps(list(exercises)), mimetype="application/json", status=200)
    except Exercise.DoesNotExist:
        return Response(
            json.dumps({"error": f"Failed to load learner's {course} exercises"}),
            mimetype="application/json",
            status=404,
        )