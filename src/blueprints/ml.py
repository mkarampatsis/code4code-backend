from flask import Blueprint, request, Response, jsonify
from src.ml.model_manager import ModelManager
from src.ml.definitions import ExerciseDef, ExerciseRsDef, QuestionDef, QuestionRsDef

ml = Blueprint("ml", __name__)


@ml.route("/user_assesment", methods=["POST"])
def user_assesmentd():
    user_assesment_data = request.get_json()
    user_assesment = QuestionDef(**user_assesment_data)
    model_manager = ModelManager()
    user_assesment_label = model_manager.label_student(user_assesment=user_assesment)

    return jsonify(
        {
            "student_id": user_assesment.student_id,
            "user_category": user_assesment_label,
        }
    )


@ml.route("exercise_category", methods=["POST"])
def exercise_category(exercise: ExerciseDef) -> ExerciseRsDef:
    model_manager = ModelManager()

    exercise_chapter = model_manager.label_exercise(exercise=exercise)

    return ExerciseRsDef(**{"id": exercise.id, "exercise_chapter": exercise_chapter})
