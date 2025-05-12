import pytest
from httpx import AsyncClient, ASGITransport

from main import app 


@pytest.mark.asyncio
async def test_get_all_books():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.get("/books")
        assert res.status_code == 200

        data = res.json()
        assert len(data) != 0


@pytest.mark.asyncio
async def test_add_book():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.post("/books", json={
            "title": "The Brothers Karamazov", 
            "author": "Fyodor Dostoevsky"
        })
        assert res.status_code == 200

        data = res.json()
        assert data == {"success": True, "message": "Book has been added"}