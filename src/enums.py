from enum import Enum


class UserCategory(Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    INSTITUTION = "institution"
    NONE = "none"


class UserCourse(Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    NONE = "none"


class UserLevel(Enum):
    IGNORANT = "ignorant"
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    EXPERT = "expert"
    NONE = "none"
