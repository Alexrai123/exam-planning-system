API Reference
=============

This section documents the API endpoints provided by the Exam Planning System backend.

Authentication
-------------

.. http:post:: /api/v1/auth/register

   Register a new user.

   **Example request**:

   .. code-block:: http

      POST /api/v1/auth/register HTTP/1.1
      Host: localhost:8000
      Content-Type: application/json

      {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "securepassword",
        "role": "STUDENT"
      }

   **Example response**:

   .. code-block:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "role": "STUDENT"
      }

.. http:post:: /api/v1/auth/login

   OAuth2 compatible token login, get an access token for future requests.

   **Example request**:

   .. code-block:: http

      POST /api/v1/auth/login HTTP/1.1
      Host: localhost:8000
      Content-Type: application/x-www-form-urlencoded

      username=john.doe@example.com&password=securepassword

   **Example response**:

   .. code-block:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer"
      }

Users
-----

.. http:get:: /api/v1/users/

   Get all users. Only accessible by secretariat.

   **Example request**:

   .. code-block:: http

      GET /api/v1/users/ HTTP/1.1
      Host: localhost:8000
      Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

   **Example response**:

   .. code-block:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      [
        {
          "id": 1,
          "name": "Admin User",
          "email": "admin@example.com",
          "role": "SECRETARIAT"
        },
        {
          "id": 2,
          "name": "John Smith",
          "email": "john.smith@example.com",
          "role": "PROFESSOR"
        }
      ]

.. http:get:: /api/v1/users/(int:user_id)

   Get a specific user by ID.

   **Example request**:

   .. code-block:: http

      GET /api/v1/users/1 HTTP/1.1
      Host: localhost:8000
      Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

   **Example response**:

   .. code-block:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
        "id": 1,
        "name": "Admin User",
        "email": "admin@example.com",
        "role": "SECRETARIAT"
      }

Exams
-----

.. http:get:: /api/v1/exams/

   Get all exams with optional filtering.

   **Example request**:

   .. code-block:: http

      GET /api/v1/exams/?grupa_name=CS101&status=CONFIRMED HTTP/1.1
      Host: localhost:8000
      Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

   **Example response**:

   .. code-block:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      [
        {
          "id": 1,
          "course_id": 1,
          "grupa_name": "CS101",
          "date": "2025-06-15",
          "time": "09:00:00",
          "sala_name": "A101",
          "status": "CONFIRMED"
        }
      ]

.. http:post:: /api/v1/exams/

   Create a new exam. Only accessible by secretariat.

   **Example request**:

   .. code-block:: http

      POST /api/v1/exams/ HTTP/1.1
      Host: localhost:8000
      Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
      Content-Type: application/json

      {
        "course_id": 1,
        "grupa_name": "CS101",
        "date": "2025-06-15",
        "time": "09:00:00",
        "sala_name": "A101",
        "status": "PROPOSED"
      }

   **Example response**:

   .. code-block:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
        "id": 1,
        "course_id": 1,
        "grupa_name": "CS101",
        "date": "2025-06-15",
        "time": "09:00:00",
        "sala_name": "A101",
        "status": "PROPOSED"
      }

.. http:put:: /api/v1/exams/(int:exam_id)

   Update an exam. Secretariat can update all fields, professors can only update status.

   **Example request**:

   .. code-block:: http

      PUT /api/v1/exams/1 HTTP/1.1
      Host: localhost:8000
      Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
      Content-Type: application/json

      {
        "status": "CONFIRMED"
      }

   **Example response**:

   .. code-block:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
        "id": 1,
        "course_id": 1,
        "grupa_name": "CS101",
        "date": "2025-06-15",
        "time": "09:00:00",
        "sala_name": "A101",
        "status": "CONFIRMED"
      }

Groups
------

.. http:get:: /api/v1/groups/

   Get all groups.

   **Example request**:

   .. code-block:: http

      GET /api/v1/groups/ HTTP/1.1
      Host: localhost:8000
      Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

   **Example response**:

   .. code-block:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      [
        {
          "name": "CS101",
          "year": 1,
          "specialization": "Computer Science",
          "leader_id": 5
        }
      ]

.. http:get:: /api/v1/groups/(string:name)

   Get a specific group by name.

   **Example request**:

   .. code-block:: http

      GET /api/v1/groups/CS101 HTTP/1.1
      Host: localhost:8000
      Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

   **Example response**:

   .. code-block:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
        "name": "CS101",
        "year": 1,
        "specialization": "Computer Science",
        "leader_id": 5
      }

Rooms
-----

.. http:get:: /api/v1/rooms/

   Get all rooms.

   **Example request**:

   .. code-block:: http

      GET /api/v1/rooms/ HTTP/1.1
      Host: localhost:8000
      Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

   **Example response**:

   .. code-block:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      [
        {
          "name": "A101",
          "capacity": 50,
          "building": "A",
          "floor": 1
        }
      ]

Courses
-------

.. http:get:: /api/v1/courses/

   Get all courses.

   **Example request**:

   .. code-block:: http

      GET /api/v1/courses/ HTTP/1.1
      Host: localhost:8000
      Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

   **Example response**:

   .. code-block:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      [
        {
          "id": 1,
          "name": "Introduction to Programming",
          "profesor_name": "John Smith",
          "credits": 6
        }
      ]
