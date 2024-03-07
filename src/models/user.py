from src.config import MONGO_DBNAME
from src.enums import UserCategory, UserCourse, UserLevel
import mongoengine as me


class UserAssessment(me.EmbeddedDocument):
    course = me.EnumField(UserCourse, required=True)
    level = me.EnumField(UserLevel, required=True)


class UserEvaluationAnswer(me.EmbeddedDocument):
    question_id = me.StringField(required=True)
    answer_text = me.StringField(required=True)
    correct = me.BooleanField(required=True)


class UserEvaluation(me.EmbeddedDocument):
    course = me.EnumField(UserCourse, required=True)
    score = me.FloatField(required=True)
    date = me.DateTimeField(required=True)
    answers = me.ListField(me.EmbeddedDocumentField(UserEvaluationAnswer), required=True)


class User(me.Document):
    email = me.EmailField(required=True, unique=True)
    firstName = me.StringField(required=True)
    lastName = me.StringField(required=True)
    name = me.StringField(required=True)
    googleId = me.StringField(required=True)
    photoUrl = me.StringField(required=True)
    provider = me.StringField(required=True, choices=["GOOGLE"], default="GOOGLE")
    isAdmin = me.BooleanField(required=True, default=False)
    isEnabled = me.BooleanField(required=True, default=False)
    category = me.EnumField(UserCategory, required=True, default=UserCategory.NONE)
    assessments = me.ListField(me.EmbeddedDocumentField(UserAssessment))
    evaluations = me.ListField(me.EmbeddedDocumentField(UserEvaluation))

    meta = {"collection": "users", "db_alias": MONGO_DBNAME}

    def to_mongo_dict(self):
        mongo_dict = self.to_mongo().to_dict()
        mongo_dict.pop("_id")
        return mongo_dict

    @staticmethod
    def get_user_by_google_id(googleId: str) -> "User":
        return User.objects(googleId=googleId).first()
