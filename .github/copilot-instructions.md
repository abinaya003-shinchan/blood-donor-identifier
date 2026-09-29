# Copilot Instructions

## Project
- This is a small server-rendered Flask application for registering blood donors, searching compatible donors by city, and managing donor availability.
- `app.py` owns Flask routes and blood-group compatibility behavior.
- `database/database.py` owns SQLite connection and schema initialization. The `donors` table has `id`, `name`, `age`, `blood_group`, `phone`, `city`, and `availability` fields.
- Jinja templates are in `templates/`; browser assets belong under `static/`.

## Working conventions
- Keep changes focused and consistent with the existing Flask, SQLite, and Jinja patterns. Avoid adding frameworks or abstractions for this small application without a clear need.
- Use parameterized SQL for values. If SQL needs a dynamic number of placeholders, generate only the placeholders and continue binding all values separately.
- Preserve the existing donor availability values (`Available` and `Not Available`) and blood-group spelling unless a change explicitly updates the application contract.
- Treat donor contact details as sensitive; do not expose them in new views or logs beyond the app's intended donor search/admin workflows.
- There is no test suite or substantive README documentation at present. Add focused tests when introducing nontrivial behavior, and do not claim tests passed unless they were run.

## Running locally
- Install dependencies with `python -m pip install -r requirements.txt`.
- Start the development app with `python app.py` and open `http://127.0.0.1:5000/`.
- The application initializes its SQLite schema when `app.py` is imported. The database connection currently uses the relative path `database/blood_donor.db`, so run it from the repository root.
