from flask import Blueprint, request, Response, jsonify
from src.models.exercise import Exercise
import json

exercises = Blueprint("exercises", __name__)


@exercises.route("/one/<string:code>", methods=["GET"])
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
def get_all_exercises_by_type(type):
    try:
        exercises = Exercise.objects(type=type)
        return Response(exercises.to_json(), mimetype="application/json", status=200)
    except Exercise.DoesNotExist:
        return Response(
            json.dumps({"error": f"Failed to load {type} exercises"}),
            mimetype="application/json",
            status=404,
        )
