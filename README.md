# bot-task-reward
Telegram bot for completing various tasks and getting points

## Run the application
```bash
# Creating a virtual environment
> python -m venv venv
# Activating the virtual environment
> ./venv/Scripts/activate
# Installing dependencies
> pip install -r ./requirements.txt
# Run the application
> uvicorn main:app --host 0.0.0.0 --port 80
```
------------

alembic revision -m "init" --autogenerate
alembic upgrade head

pytest
