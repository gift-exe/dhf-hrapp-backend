# dhf-hrapp-backend
Backend API for HR App

# Steps to run locally

##### Requirements (LOL)
- A computer
- Internet
- Python
- PostgreDB

#### Setup
Clone the repository:
```
git clone https://github.com/itcentralng/dhf-hrapp-backend.git
```

Enter Directory:
```
cd dhf-hrapp-backend
```

Create a virtual environment:
```
python -m venv env
```

Activate envvironment:
(for windows)
```
./env/Scripts/activate
```

(for linux/mac)
```
source env/bin/activate
```

Install dependencies:
```
pip install -r requirements.txt
```

Create a .env file in the home directory mocking the .env.example file

Alembic Stuff:
ps: Alembic is like magic to me... But try running this command. It should work

```
alembic init migrations
```
```
alembic revision --autogenerate -m "Initial Mirgration"
```
```
alembic upgrade head
```

Stat up the app:
```
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

For now, to view the endpoints, visit this link on your browser:

```
http://0.0.0.0:8000/docs
```
