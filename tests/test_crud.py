import pytest
from app.core.crud import QuestionCRUD, AnswerCRUD
from app.schemas.qa_schemas import QuestionCreateRequest, AnswerCreateRequest
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


@pytest.mark.asyncio
async def test_answer_crud_full(db_session):
    # Сначала вопрос
    q = await QuestionCRUD.create(db_session, QuestionCreateRequest(text="Вопрос для ответа"))
    # Ответ вопросу
    answer_data = AnswerCreateRequest(text="Ответ", user_id="user1")
    answer = await AnswerCRUD.create(db_session, answer_data, q.id)
    assert answer is not None
    assert answer.text == "Ответ"
    assert answer.user_id == "user1"
    assert answer.question_id == q.id

    # Получить по id
    answer_loaded = await AnswerCRUD.get_by_id(db_session, answer.id)
    assert answer_loaded is not None
    assert answer_loaded.text == answer.text

    # Попытка создать ответ к несуществующему вопросу
    fake = await AnswerCRUD.create(db_session, answer_data, 52)
    assert fake is None

    # Удалить
    deleted = await AnswerCRUD.delete(db_session, answer.id)
    assert deleted is True
    not_found = await AnswerCRUD.get_by_id(db_session, answer.id)
    assert not_found is None

    # Удалить несуществующий снова
    deleted2 = await AnswerCRUD.delete(db_session, answer.id)
    assert deleted2 is False


@pytest.mark.asyncio
async def test_cascade_delete_answers(db_session):
    # Проверка каскадного удаления
    question = await QuestionCRUD.create(db_session, QuestionCreateRequest(text="Вопрос?"))
    answer1 = await AnswerCRUD.create(db_session, AnswerCreateRequest(text="1", user_id="user1"), question.id)
    answer2 = await AnswerCRUD.create(db_session, AnswerCreateRequest(text="2", user_id="user1"), question.id)

    exists1 = await AnswerCRUD.get_by_id(db_session, answer1.id)
    exists2 = await AnswerCRUD.get_by_id(db_session, answer2.id)
    assert exists1 is not None and exists2 is not None

    # Удалить вопрос
    await QuestionCRUD.delete(db_session, question.id)

    # Ответы должны исчезнуть
    gone1 = await AnswerCRUD.get_by_id(db_session, answer1.id)
    gone2 = await AnswerCRUD.get_by_id(db_session, answer2.id)
    assert gone1 is None and gone2 is None


@pytest.mark.asyncio
async def test_answers_by_question_id(db_session):
    # Сначала вопрос
    q = await QuestionCRUD.create(db_session, QuestionCreateRequest(text="Вопрос для ответа"))

    # Ответы на вопрос
    answer_data_1 = AnswerCreateRequest(text="Ответ 1", user_id="user1")
    answer_data_2 = AnswerCreateRequest(text="Ответ 2", user_id="user1")
    answer_1 = await AnswerCRUD.create(db_session, answer_data_1, q.id)
    answer_2 = await AnswerCRUD.create(db_session, answer_data_2, q.id)
    # Проверяем наличие ответов
    assert answer_1 is not None and answer_2 is not None
    assert answer_1.text == "Ответ 1" and answer_2.text == "Ответ 2"
    assert answer_1.question_id == q.id and answer_2.question_id == q.id

    # Получаем все ответы по id вопроса
    all_a = await AnswerCRUD.get_by_question_id(db_session, q.id)
    texts = [a.text for a in all_a]
    assert all_a is not None
    assert len(all_a) == 2
    assert "Ответ 1" in texts and "Ответ 2" in texts
