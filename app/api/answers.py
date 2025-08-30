from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.crud import AnswerCRUD
from app.database import get_db
from app.schemas.qa_schemas import AnswerCreateResponse

router = APIRouter(prefix="/answers", tags=["answers"])


@router.get("/{answer_id}", response_model=AnswerCreateResponse)
async def get_answer_by_id(
        answer_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Получить вопрос по id"""
    answer = await AnswerCRUD.get_by_id(db, answer_id)
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ответ не найден"
        )
    return answer


@router.delete("/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_answer(
        answer_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Удалить вопрос (каскадно удаляются все ответы)"""
    success = await AnswerCRUD.delete(db, answer_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вопрос не найден"
        )
