from src.config import MONGO_DBNAME
import mongoengine as me

class ExerciseCategory(me.EmbeddedDocument):
    chapter = me.StringField()
    # subchapter = me.ListField(me.EmbeddedDocumentField(ExerciseSubchapter))

    # meta = {'allow_inheritance': True}

class ExerciseSubchapter(ExerciseCategory):
    chapter = me.StringField()
    subchapter = me.ListField(me.StringField())

class ExerciseHint(me.EmbeddedDocument):
    text = me.StringField(required=True)
    code = me.StringField(required=True)
    penalty = me.BooleanField(required=True)

class ExerciseAuthor(me.EmbeddedDocument):
    name = me.StringField(required=True)
    email = me.StringField(required=True)

class Exercise(me.Document):
    introduction = me.ListField(me.StringField(required=True))
    subintroduction = me.ListField(me.StringField(required=True))
    exercise_description= me.ListField(me.StringField(required=True))
    category = me.EmbeddedDocumentField(ExerciseCategory)
    hints = me.ListField(me.EmbeddedDocumentField(ExerciseHint), required=True)
    author = me.EmbeddedDocumentField(ExerciseAuthor, required=True)
    exercise = me.StringField(required=True)
    type = me.StringField(required=True)
    code = me.StringField(required=True)
    output = me.ListField(me.StringField())
    difficulty = me.StringField(required=True)

    meta = {"collection": "exercises", "db_alias": MONGO_DBNAME}