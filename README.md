# FastAPI Calculator with Secure User Model

A FastAPI calculator app with a secure user model, built for Module 10. Users are stored in PostgreSQL with SQLAlchemy, user data is validated with Pydantic, and passwords are hashed with bcrypt before they are saved. GitHub Actions tests the code, scans the Docker image, and pushes it to Docker Hub.

## Docker Hub

Image: **https://hub.docker.com/r/atharhanjra/assignment10**

```
docker pull atharhanjra/assignment10:latest
docker run -p 8000:8000 atharhanjra/assignment10:latest
```

Then open http://localhost:8000.

## What's Included

- **User model** (`app/models/user.py`): `username`, `email`, `password_hash`, and `created_at`, with unique constraints on username and email
- **Pydantic schemas** (`app/schemas/user.py`): `UserCreate` (username, valid email, password) and `UserRead` (never includes the password or hash)
- **Password hashing** (`app/security.py`): `hash_password` and `verify_password` using bcrypt
- **User functions** (`app/user_service.py`): `create_user` saves only the hashed password; `authenticate_user` checks a login

## Running the Tests Locally

1. Set up the project:
   ```
   git clone https://github.com/atharhanjra/assignment10.git
   cd assignment10
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python -m playwright install --with-deps chromium
   ```
2. Start the PostgreSQL database (Docker Desktop must be running):
   ```
   docker compose up -d db
   ```
3. Run the tests:
   ```
   pytest
   ```
   Or by type:
   ```
   pytest tests/unit/
   pytest tests/integration/
   pytest tests/e2e/
   ```

- **Unit tests** check hashing and schema validation.
- **Integration tests** use the real PostgreSQL database to check user creation, duplicate usernames and emails, invalid emails, and login.
- **End-to-end tests** use Playwright to test the calculator in a browser.

## CI/CD Pipeline

The workflow in `.github/workflows/test.yml` runs on every push to `main`:

1. **test:** runs all tests with a PostgreSQL service container
2. **security:** builds the Docker image and scans it with Trivy
3. **deploy:** pushes the image to Docker Hub as `atharhanjra/assignment10`