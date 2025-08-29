from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.qa_models import Question, Answer
from app.schemas.qa_schemas import QuestionCreateRequest, AnswerCreateRequest
from typing import List, Optional


class QuestionCRUD:
    """CRUD операций для вопросов"""

    @staticmethod
    async def get_all(db: AsyncSession) -> List[Question]:
        result = await db.execute(select(Question))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, question_id: int) -> Optional[Question]:
        result = await db.execute(
            select(Question)
            .options(selectinload(Question.answers))
            .where(Question.id == question_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, question: QuestionCreateRequest) -> Question:
        db_question = Question(text=question.text)
        db.add(db_question)
        await db.commit()
        await db.refresh(db_question)
        return db_question

    @staticmethod
    async def delete(db: AsyncSession, question_id: int) -> bool:
        question = await QuestionCRUD.get_by_id(db, question_id)
        if question:
            await db.delete(question)
            await db.commit()
            return True
        return False


class AnswerCRUD:
    """CRUD операции для ответов"""

    @staticmethod
    async def get_by_id(db: AsyncSession, answer_id: int) -> Optional[Answer]:
        result = await db.execute(select(Answer).where(Answer.id == answer_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(
            db: AsyncSession,
            answer: AnswerCreateRequest,
            question_id: int
    ) -> Optional[Answer]:
        # Проверяем существование вопроса
        question = await QuestionCRUD.get_by_id(db, question_id)
        if not question:
            return None

        db_answer = Answer(
            text=answer.text,
            user_id=answer.user_id,
            question_id=question_id
        )
        db.add(db_answer)
        await db.commit()
        await db.refresh(db_answer)
        return db_answer

    @staticmethod
    async def delete(db: AsyncSession, answer_id: int) -> bool:
        answer = await AnswerCRUD.get_by_id(db, answer_id)
        if answer:
            await db.delete(answer)
            await db.commit()
            return True
        return False
