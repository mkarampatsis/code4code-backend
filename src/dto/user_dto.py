from pydantic import BaseModel


class UserDTO(BaseModel):
    id: str = None
    email: str = None
    name: str = None
    firstName: str = None
    lastName: str = None
    photoUrl: str = None
    category: str = None
    institution: str = None
    linkedin: str = None
    provider: str = None
