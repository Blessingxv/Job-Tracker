# The design of a Job Application Tracker

## Video Demo: <https://youtu.be/Aw-Wvljb6Jc>

### Description:

Job Tracker is a full stack web application built as my final project for CS50x: Introduction to Computer Science.
It's designed to help job seekers organize and monitor their job applications in one place by tracking company names, job titles, locations, application dates, deadlines, status, source and personal notes for each application.

The idea for this project came directly from my own experience as I've been applying to graduate programmes and internships in South Africa, I found myself losing track of which companies I'd applied to, what stage each application was at and when deadlines were coming up. Job Tracker solves that by giving users a single dashboard to manage everything.

### Features

+ User authentication - users can register, log in and log out securely. Each user only sees their own applications.
+ Full CRUD functionality - create, read, update and delete job applications.
+ Dashboard overview - a summary statistics section (Applied/Interview/Offer/Rejected/Total) displayed as stat cards, giving users an at a glance view of their job search progress.
+ Application tracking table - a clean, styled table listing all applications with color-coded status badges (Applied, Interview, Offer, Rejected) so users can quickly scan where each application stands.
+ Add and edit forms - styled forms for adding new applications and editing existing ones, with fields for company, title, location, date applied, deadline, status, source and notes.
+ Responsive design - built with Bootstrap 5's grid system, so the dashboard and forms adapt cleanly across desktop and mobile screen sizes.

### Tech Stack

+ Backend: Python, Flask
+ Database: SQLite
+ Templating: Jinja2
+ Frontend: JavaScript, HTML, custom CSS and Bootstrap 5

### File Structure

+ app.py - main Flask application which contains all routes (home, register, login, logout, dashboard, add, edit, delete) and database logic.
+ templates/ - Jinja2 HTML templates:
  + layout.html - base template with navbar and footer, extended by all other pages.
  + index.html - landing/home page.
  + register.html/login.html - authentication pages.
  + dashboard.html - main dashboard showing summary statistics and the applications table.
  + add.html - form for adding a new job application.
  + edit.html - form for editing an existing job application.
+ static/styles.css - custom CSS styling layered on top of Bootstrap, covering the hero section, feature cards, stat cards, status badges, form styling and buttons.
+ tracker.db - SQLite database storing users and job applications.
+ requirements.txt - Python dependencies needed to run the project.

### How to run

1. Clone the repository:

   git clone <YOUR REPO URL HERE>
   cd job-tracker

2. Create and activate a virtual environment:

   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows

3. Install dependencies:

   pip install -r requirements.txt

4. Run the application:

   flask run

5. Open your browser to http://127.0.0.1:5000/

### Design choices

I chose Flask over Django for this project because it's lightweight and gave me more hands-on visibility into how routing, sessions and database queries actually work under the hood which felt like the right fit as a first full-stack project. For styling, I used Bootstrap 5 for the responsive grid and utility classes, but layered custom CSS on top (stat cards, status badges, form inputs) rather than relying purely on default Bootstrap components, since I wanted the dashboard to have its own visual identity rather than looking like a generic Bootstrap template.

### Future improvements

+ Add search and filtering (e.g. filter applications by status or date range)
+ Add email/reminder notifications for upcoming deadlines
+ Deploy live so the app can be used beyond local development

### Author

Tlangelani Blessing Mhlongo
BEng Tech (Mechanical Engineering), University of Johannesburg - Aspiring software engineer.