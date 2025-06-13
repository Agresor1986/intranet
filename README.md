This is my final year project – a **web-based intranet system** developed primarily for a small company. The application is written in **Slovak**, as it was created as part of my graduation project at a Slovak technical high school.

You can try a **live demo** at: https://www.firma-intranet.great-site.net/. Please note that the project is hosted on **free hosting** (Render), so the website may load slowly or be temporarily unavailable. The database is reset every month, which means any added content or user data may be deleted.

To log in to the demo, use the following credentials:

**Username**: visitor

**Password**: .12visit34.

Note that some features are disabled for this demo account, such as file uploads and email sending.

The source code is available on GitHub: https://github.com/Agresor1986/intranet

This intranet system includes **several key features**:

•	User authentication and authorization

•	Role-based permissions (admin, groups, regular users)

•	Internal chat (both private and group conversations)

•	Notification system with read/unread states

•	Calendar with categorized, color-coded events

•	Forum for discussions

•	Polls and voting system

•	File and document management

•	Email sending support and notifications

•	Admin interface using Django’s built-in admin panel for full control over users, events, files, and more

If you want to run the project locally, clone the repository and follow these steps:
Create a virtual environment, install the dependencies from requirements.txt, and configure your environment variables either using a .env file or by editing settings.py directly (for email and database configuration). Then run the database migrations and create a superuser account. The application uses a PostgreSQL database (hosted on Render) by default, but you can change it to SQLite or any other database engine for local development. In addition, you will need to adjust some settings in settings.py that are specific to the deployed version (CSRF_TRUSTED_ORIGINS, ALLOWED_HOSTS etc. )

This project was created mainly for learning purposes and to demonstrate the functionality of an internal system suitable for small companies. Feel free to explore it or build upon it.

Created with passion by a Slovak student as part of a final year graduation project.
