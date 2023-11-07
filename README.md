# tester-ai

1. python -m venv venv
2. source venv/Scripts/activate
3. pip install -r requirements.txt
4. alembic revision -m "Add new table"
5. alembic upgrade head
6. uvicorn runserver --reload
