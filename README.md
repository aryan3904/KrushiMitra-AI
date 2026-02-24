# Krushi Mitra AI

This Flask application assists Indian farmers with crop planning, disease detection, and treatment
recommendations.  The project uses a MySQL database to manage users and roles.

## Features added

* Role-based signup with three roles: `farmer`, `fertilizer_store_head`, `admin`
* Login using phone number and password
* Logout and session management
* Chat‑style authentication UI built entirely with Flask/Jinja — login/signup pages mimic the chatbot conversation and use advanced CSS matching the main theme.
* Main chat options are protected with `@login_required` so the crop/disease features only appear after a successful signin.
* Database initialization script to create `users` table automatically
* Templates for signup and login, with links available across the site

## Setup

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure MySQL credentials**
   The application reads the following environment variables (defaults in parentheses):
   - `MYSQL_HOST` (`localhost`)
   - `MYSQL_USER` (`root`)
   - `MYSQL_PASSWORD` (empty)
   - `MYSQL_DB` (`krushimitraai`)

   Make sure the database `krushimitraai` already exists. You can create it via phpMyAdmin or
   the MySQL CLI:
   ```sql
   CREATE DATABASE krushimitraai;
   ```

   The first time the Flask app runs it will create the `users` table automatically.

3. **Run the Flask development server**
   ```bash
   set FLASK_APP=app.py        # Windows
   set FLASK_ENV=development
   flask run
   ```
   or
   ```bash
   python app.py
   ```

4. **Visit the app** in your browser at `http://localhost:5000`.  Use the links in the header to
   sign up or log in.

## Database schema

```sql
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    phone VARCHAR(20) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('farmer','fertilizer_store_head','admin') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;
```

## Next steps

* Add role-specific authorization checks (`@role_required`) to sensitive routes
* Enhance the UI with a shared layout or navigation component
* Use migrations (`Flask-Migrate` / Alembic) for more complex schema changes
* Secure configuration with `.env`/`config.py` and better secret management

