from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from config import settings

"""
Модели:
Question – вопрос:
id: int
text: str (текст вопроса)
created_at: datetime


Answer – ответ на вопрос:
id: int
question_id: int (ссылка на Question)
user_id: str (идентификатор пользователя, например uuid)
text: str (текст ответа)
created_at: datetime

"""


class QuestionBase(BaseModel):
    text: str = Field(..., min_length=settings.Q_MIN_LENGTH, max_length=settings.Q_MAX_LENGTH)


class QuestionCreateRequest(QuestionBase):
    pass


class QuestionCreateResponse(QuestionBase):
    id: int = Field(...)
    created_at: datetime = Field(...)

    # Для ORM
    class Config:
        from_attributes = True


class AnswerBase(BaseModel):
    text: str = Field(..., min_length=settings.A_MIN_LENGTH, max_length=settings.A_MAX_LENGTH)
    user_id: str = Field(..., min_length=1)


class AnswerCreateRequest(AnswerBase):
    pass


class AnswerCreateResponse(AnswerBase):
    id: int = Field(...)
    created_at: datetime = Field(...)
    question_id: int = Field(...)

    # Для ORM
    class Config:
        from_attributes = True


class QuestionWithAnswers(BaseModel):
    question: QuestionCreateResponse
    answers: List[AnswerCreateResponse]
