# TeeTree Setup Prerequisites and Installation

This guide explains what a second PC or laptop needs installed to run this project locally, plus the exact setup steps.

## What the device needs installed

1. Python 3.10 or newer.
2. MongoDB Community Server running locally on `localhost:27017`, or another reachable MongoDB instance.
3. Git, if the project will be cloned from a repository.
4. A modern browser such as Chrome, Edge, or Firefox.
5. Optional but recommended: VS Code for editing and running the project.

## Project requirements

The backend depends on the Python packages listed in `requirements.txt`, including:

- FastAPI and Uvicorn
- Motor and PyMongo for MongoDB access
- Pydantic and Pydantic Settings
- JWT/authentication libraries
- Pandas, NumPy, SciPy, Scikit-learn
- Pillow, httpx, aiofiles, python-multipart

## Environment variables

Create a `.env` file in the project root with these values:

```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=wild_tea_tree
SECRET_KEY=change-this-to-a-long-random-string
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

The app reads these values automatically when it starts.

## Setup steps

### 1. Install the prerequisites

Install Python and MongoDB first. If MongoDB is installed as a service, make sure it is started before launching the app.

### 2. Get the project files

Clone the repository or copy the project folder to the target machine.

### 3. Open a terminal in the project root

The project root is the folder that contains `main.py` and `requirements.txt`.

### 4. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 5. Install the Python dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure the `.env` file

Add the environment variables shown above. If MongoDB is running on a different host or port, update `MONGODB_URL` accordingly.

### 7. Start MongoDB

Make sure the MongoDB server is running before starting the FastAPI app.

### 8. Seed sample data, if needed

The project includes a seed script that can populate sample tea tree records and demo data.

```bash
python seed_data.py
```

If you want the alternate India-specific dataset, use:

```bash
python india_seed_data.py
```

### 9. Start the application

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 10. Open the app in a browser

Visit:

```text
http://localhost:8000
```

## First-run checklist

- MongoDB is running.
- `.env` exists in the project root.
- Virtual environment is activated.
- `pip install -r requirements.txt` completed successfully.
- The backend starts without errors.

## Notes for another laptop

- The project is local-first and does not require external paid APIs.
- Open-Meteo and NASA POWER are used without API keys.
- Uploaded images are stored in the `uploads/` folder, so that folder must remain writable.
- If port `8000` is already in use, start Uvicorn on another port, for example `--port 8001`.

## Quick troubleshooting

- If the app cannot connect to MongoDB, verify the database service is running and `MONGODB_URL` is correct.
- If PowerShell blocks activation scripts, run `Set-ExecutionPolicy -Scope Process RemoteSigned` and activate the virtual environment again.
- If a package install fails, upgrade pip first with `python -m pip install --upgrade pip`.
