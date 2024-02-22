import pickle

import spacy
import numpy as np
from src.ml.definitions import (
    ExerciseDef,
    QuestionDef,
    QuestionRsDef,
    ExerciseRsDef,
)


nlp = spacy.load("en_core_web_lg")

labels_map: dict = {
    0: "data types",
    1: "expressions and operators",
    2: "lists",
    3: "syntax variables scope",
}


def extract_exercise_embedd(code: str) -> np.ndarray:
    doc = nlp(code)

    return doc.vector


def extract_descript_embedd(descript: str) -> np.ndarray:
    doc = nlp(descript[0])

    return doc.vector


class ModelManager:
    def label_exercise(self, exercise: ExerciseDef):
        code_embeddings = extract_exercise_embedd(exercise.code)
        description_embeddings = extract_descript_embedd(exercise.description)

        intro_embeddings = extract_descript_embedd(exercise.introduction)

        full_embeddings = np.concatenate(
            [
                code_embeddings[None, :],
                description_embeddings[None, :],
                intro_embeddings[None, :],
            ],
            axis=1,
        )

        with open("src/ml/models/code_category_classifier.pkl", "rb") as f:
            clf = pickle.load(f)

        with open("src/ml/models/code_category_pca_full.pkl", "rb") as f:
            pca = pickle.load(f)

        pca_embeddings = pca.transform(full_embeddings)

        exercise_label = clf.predict(pca_embeddings)

        exercise_chapter = labels_map.get(exercise_label[0])

        return exercise_chapter

    def label_student(self, user_assesment: QuestionDef):
        user_dict = {0: "beginner", 1: "intermediate", 2: "expert"}
        file = open("src/ml/models/user_asses_scaler.pkl", "rb")
        scaler = pickle.load(file)

        file = open("src/ml/models/user_asses_pca.pkl", "rb")
        pca = pickle.load(file)

        file = open("src/ml/models/user_asses_knn_classifier.pkl", "rb")
        model = pickle.load(file)

        data = [
            [
                user_assesment.guess,
                user_assesment.correct,
                user_assesment.total,
                user_assesment.perc,
            ]
        ]
        data = scaler.transform(data)
        data = pca.transform(data)
        predict = model.predict(data)

        return user_dict[predict[0]]
