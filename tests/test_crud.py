import pytest
from app.core.crud import QuestionCRUD
from app.schemas.qa_schemas import QuestionCreateRequest
from app.models.qa_models import Question


@pytest.mark.asyncio
async def test_create_and_get_question(db_session):
    # Создаем вопрос
    q_create = QuestionCreateRequest(text="Тестовый вопрос")
    created = await QuestionCRUD.create(db_session, q_create)
    assert isinstance(created, Question)
    assert created.text == "Тестовый вопрос"

    # Получаем вопрос по id
    fetched = await QuestionCRUD.get_by_id(db_session, created.id)
    assert fetched is not None
    assert fetched.text == created.text


@pytest.mark.asyncio
async def test_get_all_questions(db_session):
    # Должно вернуть пустой список
    all_q = await QuestionCRUD.get_all(db_session)
    assert isinstance(all_q, list)
    assert len(all_q) == 0

    # Добавляем вопросы
    await QuestionCRUD.create(db_session, QuestionCreateRequest(text="1 Тестовый вопрос"))
    await QuestionCRUD.create(db_session, QuestionCreateRequest(text="2 Тестовый вопрос"))

    all_q = await QuestionCRUD.get_all(db_session)
    texts = [q.text for q in all_q]
    assert "1 Тестовый вопрос" in texts and "2 Тестовый вопрос" in texts


@pytest.mark.asyncio
async def test_delete_question(db_session):
    question = await QuestionCRUD.create(db_session, QuestionCreateRequest(text="Вопрос для удаления"))
    success = await QuestionCRUD.delete(db_session, question.id)
    assert success is True

    # Проверка, что вопрос удален
    deleted = await QuestionCRUD.get_by_id(db_session, question.id)
    assert deleted is None

    # Удаление несуществующего вопроса
    result = await QuestionCRUD.delete(db_session, 52)
    assert result is False
