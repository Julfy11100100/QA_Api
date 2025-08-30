from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.crud import QuestionCRUD, AnswerCRUD
from app.database import get_db
from app.schemas.qa_schemas import QuestionCreateRequest, QuestionCreateResponse, QuestionWithAnswers, \
    AnswerCreateRequest

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/", response_model=List[QuestionCreateResponse])
async def get_all_questions(db: AsyncSession = Depends(get_db)):
    """Получить список всех вопросов"""
    return await QuestionCRUD.get_all(db)


@router.post("/", response_model=QuestionCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_question(
        question: QuestionCreateRequest,
        db: AsyncSession = Depends(get_db)
):
    """Создать новый вопрос"""
    return await QuestionCRUD.create(db, question)


@router.get("/{question_id}", response_model=QuestionWithAnswers)
async def get_question_with_answers(
        question_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Получить вопрос со всеми ответами"""
    question = await QuestionCRUD.get_by_id(db, question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вопрос не найден"
        )
    answers = await AnswerCRUD.get_by_question_id(db, question_id)
    if not answers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ответы на вопрос не найдены"
        )
    return QuestionWithAnswers(question=question, answers=answers)


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(
        question_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Удалить вопрос (каскадно удаляются все ответы)"""
    success = await QuestionCRUD.delete(db, question_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вопрос не найден"
        )


@router.post("/{question_id}/answers", status_code=status.HTTP_201_CREATED)
async def add_answer_to_question(
        answer: AnswerCreateRequest,
        question_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Добавить ответы на вопрос"""
    question = await QuestionCRUD.get_by_id(db, question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вопрос не найден"
        )
    await AnswerCRUD.create(db, answer, question_id)
