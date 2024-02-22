from typing import Union, Literal
from pydantic import BaseModel

# Student assesment
class QuestionDef(BaseModel):
    student_id:str
    guess: int
    correct: float
    total: float
    perc: float

class QuestionRsDef(BaseModel):
    student_id:str
    user_category: Literal["expert", "intermediate", "beginner"]


# Chapter assesment
class ExerciseDef(BaseModel):
    id: str
    code: str
    introduction: str
    description: str


class ExerciseRsDef(BaseModel):
    id: str
    exercise_chapter: str
