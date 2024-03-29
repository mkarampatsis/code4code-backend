from enum import Enum


class UserCategory(Enum):
    LEARNER = "learner"
    INSTRUCTOR = "instructor"
    # INSTITUTION = "institution"
    ADMINISTRATOR = "administrator"
    NONE = "none"


class UserCourse(Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    NONE = "none"


class UserLevel(Enum):
    NOVICE = "novice"
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    EXPERT = "expert"
    NONE = "none"
