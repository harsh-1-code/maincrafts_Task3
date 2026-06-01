# maincrafts_Task3
task3 
# Database-Driven CRUD Application - Task 3

## Overview
This project is an end-to-end full stack web application built with Python and Flask. It builds upon a secure user authentication system (Task 2) to introduce a complete, database-driven **Student Management System** (Task 3). The application allows authorized users to perform CRUD (Create, Read, Update, Delete) operations, mimicking how real-world admin panels and employee dashboards function in production environments.

## Technologies Used
* **Backend:** Python (v3.10+), Flask
* **Frontend:** HTML5, CSS3, Jinja2 Templating
* **Database:** SQLite
* **Security:** Flask Sessions, Werkzeug (Password Hashing)

## Project Structure
The application strictly follows standard Flask project architecture to ensure a clean separation between backend logic, static assets, and frontend templates:

```text
python-fullstack-task3/
│
├── app.py                 # Core backend application, routing, and CRUD logic
├── database.db            # SQLite database file (contains 'users' and 'students' tables)
│
├── static/
│   └── style.css          # Global CSS styling for all frontend pages
│
└── templates/             # HTML templates rendered dynamically via Jinja2
    ├── add_student.html   # Form interface to create a new student
    ├── dashboard.html     # Welcome dashboard accessible post-login
    ├── edit_student.html  # Form interface pre-filled to update student details
    ├── login.html         # User login form
    ├── register.html      # User registration form
    └── students.html      # Data table displaying all students with edit/delete actions


Project Flow & Security
The application ensures that data is protected and strictly manages how users interact with the system.

Initialization & Routing: When the Flask server starts, the default route / automatically redirects visitors to the /register or /login page, ensuring no one can access the system without an account.

Authentication: Users securely register using Werkzeug password hashing. Upon logging in with correct credentials, the server creates an active "session" for that specific user.

Protected Access: Every single dashboard and CRUD route checks for this active session. If a user attempts to manually enter a protected URL without being logged in, the server automatically rejects the request and redirects them to the login page.

The CRUD Flow (Student Management)
Once authenticated, the user can navigate to the /students dashboard to perform the following operations:

Create (Add Student): Clicking "Add Student" takes the user to /add-student. When the form is submitted, the Flask application extracts the name, email, and course via an HTTP POST request and executes an INSERT INTO SQL command to save the new record permanently in the SQLite database.

Read (View Students): The /students route serves as the main data dashboard. The backend runs a SELECT * query to fetch all student records from the database and uses Jinja2 templating to dynamically render this data into an HTML table.

Update (Edit Student): Clicking "Edit" next to a student triggers the /edit/<id> route. The application first runs a SELECT query using that specific student's ID to pre-fill the HTML form with their current details. Upon submission, it executes an UPDATE query to overwrite the existing data with the newly provided information.

Delete (Remove Student): Clicking "Delete" triggers the /delete/<id> route. The application takes the specific student's ID from the URL and executes a DELETE FROM query, permanently removing that record from the database before redirecting the user back to the updated dashboard.

Phase 1: The Gateway (Authentication)Before anyone can see your data, they must pass through your security checkpoints.Arrival: When a user visits your app's root URL (http://127.0.0.1:5000/), our custom redirect automatically sends them to the /register or /login page.Registration: The user submits a username and password. Before storing anything, your Flask backend uses Werkzeug to securely scramble (hash) the password . It then saves the username and the hashed password into the users table of your SQLite database .  Login: The user attempts to log in. The backend fetches the user's record from the database and uses check_password_hash to compare the entered password with the stored hash .
 Phase 2: The Digital ID Badge (Sessions)Granting Access: If the login credentials match, Flask creates a session for that user. Think of a session as a digital ID badge that your browser holds onto.  The Bouncer: Every time the user tries to load a protected page (like the dashboard or the student list), the very first line of code your server runs is a security check (if 'user' not in session). If they don't have that ID badge, they get immediately kicked back to the login screen.



https://github.com/user-attachments/assets/6e2c754d-c56f-4701-a2e3-799578237d58

Phase 3: The Engine Room (CRUD Operations)Once the user is logged in and holding their session badge, they can navigate to the /students page and interact with the database.Read (Viewing Data): When the /students page loads, the backend executes a SELECT * FROM students SQL query . It takes all those records and hands them to your Jinja2 HTML template, which loops through the data to dynamically build your visual table.  Create (Adding Data): The user clicks "Add Student" and fills out the form at /add-student. When they hit submit, an HTTP POST request sends the name, email, and course to the backend. The server executes an INSERT INTO query to save this permanently to the database, then redirects the user back to the updated table .  Update (Editing Data): The user clicks "Edit" next to a specific student (e.g., student ID #3). The app loads /edit/3. It first runs a SELECT query to grab Student #3's info and pre-fills the form . When the user submits changes, the app runs an UPDATE query targeting only ID #3, overwriting the old data .  Delete (Removing Data): The user clicks "Delete" on Student #3. The app hits the /delete/3 route, grabs the ID from the URL, and executes a DELETE FROM students WHERE id=3 query, wiping that row from the database completely .

 Phase 4: Exiting (Logout)Logging Out: When the user is finished and clicks "Logout", they are sent to the /logout route.  Destroying the Badge: The server completely destroys their active session (session.pop('user', None)). Without that session, they can no longer access the CRUD pages and are redirected safely back to the login screen.
