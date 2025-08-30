import pytest

from starlette import status


@pytest.mark.asyncio
async def test_get_all_questions_empty(client):
    resp = await client.get("/questions/")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == []


@pytest.mark.asyncio
async def test_create_question_201(client):
    payload = {"text": "Первый вопрос"}
    resp = await client.post("/questions/", json=payload)
    assert resp.status_code == status.HTTP_201_CREATED
    body = resp.json()
    assert "id" in body and body["id"] > 0
    assert body["text"] == "Первый вопрос"


@pytest.mark.asyncio
async def test_get_all_questions_after_created(client):
    await client.post("/questions/", json={"text": "Q1"})
    await client.post("/questions/", json={"text": "Q2"})
    resp = await client.get("/questions/")
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    texts = {q["text"] for q in data}
    assert "Q1" in texts and "Q2" in texts


@pytest.mark.asyncio
async def test_get_question_with_answers(client):
    # создаём вопрос
    q_resp = await client.post("/questions/", json={"text": "Вопрос с ответами"})
    assert q_resp.status_code == status.HTTP_201_CREATED
    qid = q_resp.json()["id"]

    # добавляем два ответа
    a1 = {"text": "Ответ 1", "user_id": "1"}
    a2 = {"text": "Ответ 2", "user_id": "2"}
    r1 = await client.post(f"/questions/{qid}/answers", json=a1)
    r2 = await client.post(f"/questions/{qid}/answers", json=a2)
    assert r1.status_code == status.HTTP_201_CREATED
    assert r2.status_code == status.HTTP_201_CREATED

    # получаем вопрос с ответами
    resp = await client.get(f"/questions/{qid}")
    assert resp.status_code == status.HTTP_200_OK
    body = resp.json()
    assert body["question"]["id"] == qid
    texts = {a["text"] for a in body["answers"]}
    assert "Ответ 1" in texts and "Ответ 2" in texts


@pytest.mark.asyncio
async def test_get_question_with_answers_404_when_question_not_found(client):
    resp = await client.get("/questions/999999")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    assert resp.json()["detail"] == "Вопрос не найден"


@pytest.mark.asyncio
async def test_get_question_with_answers_404_when_no_answers(client):
    q_resp = await client.post("/questions/", json={"text": "Без ответов"})
    assert q_resp.status_code == status.HTTP_201_CREATED
    qid = q_resp.json()["id"]

    resp = await client.get(f"/questions/{qid}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    assert resp.json()["detail"] == "Ответы на вопрос не найдены"


@pytest.mark.asyncio
async def test_delete_question_204_then_404(client):
    q_resp = await client.post("/questions/", json={"text": "Удалить меня"})
    assert q_resp.status_code == status.HTTP_201_CREATED
    qid = q_resp.json()["id"]

    del_resp = await client.delete(f"/questions/{qid}")
    assert del_resp.status_code == status.HTTP_204_NO_CONTENT

    del_again = await client.delete(f"/questions/{qid}")
    assert del_again.status_code == status.HTTP_404_NOT_FOUND
    assert del_again.json()["detail"] == "Вопрос не найден"

