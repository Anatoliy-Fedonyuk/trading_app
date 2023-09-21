import pytest, time
from httpx import AsyncClient

from tests.conftest import cache_initialized


async def test_add_specific_operations(ac: AsyncClient):
    response = await ac.post("/operations", json={
        "id": 1,
        "quantity": "25.5",
        "figi": "figi_CODE",
        "instrument_type": "bond",
        "date": "2023-02-01T00:00:00",
        "type": "Выплата купонов",
    })
    assert response.status_code == 200
    assert response.json()["status"] == "Add operation success"


@pytest.mark.asyncio
async def test_get_specific_operations(ac: AsyncClient, cache_initialized):
    # Замеряем время выполнения первого запроса
    start_time = time.time()
    response = await ac.get("/operations", params={"operation_type": "Выплата купонов"})
    end_time = time.time()
    first_request_duration = end_time - start_time

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert len(response.json()["data"]) == 1

    # Замеряем время выполнения второго запроса
    start_time = time.time()
    response_cached = await ac.get("/operations", params={"operation_type": "Выплата купонов"})
    end_time = time.time()
    second_request_duration = end_time - start_time

    assert response_cached.status_code == 200
    assert response_cached.json()["status"] == "success"
    assert len(response_cached.json()["data"]) == 1

    # Сравниваем время выполнения
    print(f'{second_request_duration=} < {first_request_duration=}')
    assert second_request_duration < first_request_duration


if __name__ == '__main__':
    pytest.main()
