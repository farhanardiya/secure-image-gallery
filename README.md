# Secure Image Gallery

## Description

This project contains the following functional features:

* User registration
* User login
* Personal image gallery
  * Display images
  * Upload image
  * Delete image

The security measures for this project:

* JWT based authentication
* Username and password complexity requirements
* Token based identity validation (prevents IDOR)
* Password hashing using bcrypt
* Image encryption at rest using AES-256
* Image type validation
  * File name
  * File extension
  * MIME type
  * File size

## Architecture

This project consists of 3 main components:

* Database
* Backend
* Frontend

### Database

This project uses PostgreSQL as its database. To initialize the database, you can create a database and then import the schema.sql file.

```
psql db_project < schema.sql
```

### Backend

The backend used is Flask RestX with SQL Alchemy as its ORM. Steps to install and run:

Install dependencies

```
cd backend
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Configure secrets in /app/config.py. Modify database credentials and encryption key accordingly.

Run the application

```
flask run
```

The application will run on localhost port 5000

You can access the swagget at http://localhost:5000/api/v1/doc

### Frontend

The frontend uses Nuxt 3 with Vuetify. Ensure that you have installed node. Steps to install and run:

Install packages

```
cd frontend
npm install
```

Run the application

```
npm run dev
```

The application will run on localhost port 3000
