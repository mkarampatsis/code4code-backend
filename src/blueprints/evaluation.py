from flask import Blueprint, request, Response, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from src.models.evaluation import EvalQuestion
from src.models.user import User
import json

evalExercises = Blueprint("evaluation", __name__)

# Evaluation Questions
@evalExercises.route("/questions/<string:course>", methods=["GET"])
@jwt_required()
def get_eval_questions(course):
    try:
        questions = EvalQuestion.objects(course=course)
        return Response(questions.to_json(), mimetype="application/json", status=200)
    except EvalQuestion.DoesNotExist:
        return Response(
            json.dumps({"error": f"Questions for course {course} does not exist"}),
            mimetype="application/json",
            status=404,
        )

@evalExercises.route("/user_evaluation", methods=["PATCH"])
@jwt_required()
def setUserEvaluations():
    user = User.get_user_by_email(get_jwt_identity())
    data = request.json
    print (data)
    user.update(evaluations=[data])
    user.reload()
    user = user.to_mongo_dict()
    return Response(json.dumps({"user": user, "msg": "User profile is updated"}), status=200)