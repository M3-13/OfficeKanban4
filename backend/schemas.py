from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=100)


class UserResponse(BaseModel):
    id: int
    username: str

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    username: str
    password: str


class BoardCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)


class BoardUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=100)


class BoardResponse(BaseModel):
    id: int
    title: str
    owner_id: int

    model_config = {"from_attributes": True}


class ColumnCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    position: int = 0


class ColumnUpdate(BaseModel):
    title: str | None = None
    position: int | None = None


class ColumnResponse(BaseModel):
    id: int
    title: str
    position: int
    board_id: int

    model_config = {"from_attributes": True}


class CardCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = ""
    position: int = 0


class CardUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    position: int | None = None
    column_id: int | None = None


class CardResponse(BaseModel):
    id: int
    title: str
    description: str
    position: int
    column_id: int

    model_config = {"from_attributes": True}
