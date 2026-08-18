from pydantic import BaseModel

class SubmitQuery(BaseModel):
    text: str

