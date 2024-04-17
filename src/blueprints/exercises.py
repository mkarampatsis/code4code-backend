from flask import Blueprint, request, Response, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from src.models.exercise import Exercise, TrainingExercises
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

#########################
### EXERCISES QUERIES ###
#########################
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
    pyQuery = {
        "type":"python", 
        "difficulty":{ "$in": [ "1", "2" ]},
        "category.chapter": {"$in": [ "python dates", "python strings","built in functions","python string formatting","python operators","python numbers","python booleans"]}
    }

    jsQuery = {
         "type":"javascript", 
        "difficulty":{ "$in": [ "1", "2" ]},
        "category.chapter": {"$in": ["numbers","syntax variables scope", "strings", "control structures", "expressions and operators", "data types"]}
    }
    try:
        print("Get learner exercises")
        pipeline = [
            {"$match" : pyQuery if course=="python" else jsQuery},
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
    
########################
### TRAINING QUERIES ###
########################

@exercises.route("/training/learner/<string:email>", methods=["GET"])
@jwt_required()
def get_learner_training_exercises(email):
    try:
        print("Get all training exercises for learner")
        exercises = TrainingExercises.objects(email=email)
        return Response(exercises.to_json(), mimetype="application/json", status=200)
    except TrainingExercises.DoesNotExist:
        return Response(
            json.dumps({"error": f"Failed to load {type} training exercises for learner"}),
            mimetype="application/json",
            status=404,
        )

@exercises.route("/training/count/<string:email>/<string:category>/<string:course>", methods=["GET"])
# @jwt_required()
def get_count_learner_training_exercises(email, category, course):
    try:
        print("Count all training exercises for learner by course", email, category, course)
        exercises = TrainingExercises.objects(email=email, category=category, course=course).count()
        return Response(str(exercises), mimetype="application/json", status=200)
    except TrainingExercises.DoesNotExist:
        return Response(
            json.dumps({"error": f"Failed to load all training exercises for learner by course"}),
            mimetype="application/json",
            status=404,
        )

@exercises.route("/learner/training/exercise/evaluation", methods=["PATCH"])
@jwt_required()
def set_evaluation_for_training_exercise():
    try: 
        print("Set evaluation for training exercise")
        data = request.json
        exercise = TrainingExercises.objects.get(id=data['id']['$oid'])
        exercise.evaluation = data["evaluation"]
        exercise.save()
        return Response(json.dumps({"exercise": exercise.to_json(), "msg": "Exercise evaluation is updated"}), status=200)
    except Exception as e:
            return Response(
                json.dumps({"error": f"Failed set evaluation for training exercise"}),
                mimetype="application/json",
                status=404,
            )
