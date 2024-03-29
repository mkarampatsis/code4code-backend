from flask import Blueprint, request, Response, jsonify
from src.models.evaluation import EvalQuestion
import json

evalExercises = Blueprint("evaluation", __name__)

# Evaluation Questions
@evalExercises.route("/questions/<string:course>", methods=["GET"])
def get_eval_questions(course):
    try:
        print(">>>",course)
        questions = EvalQuestion.objects(course=course)
        return Response(questions.to_json(), mimetype="application/json", status=200)
    except EvalQuestion.DoesNotExist:
        return Response(
            json.dumps({"error": f"Questions for course {course} does not exist"}),
            mimetype="application/json",
            status=404,
        )