Database Schema
===============

This section documents the database schema used in the Exam Planning System.

Overview
--------

The database schema has been designed with a focus on intuitive, meaningful primary keys and relationships. Instead of using abstract numeric IDs for many tables, we use meaningful identifiers like names, which makes the schema more intuitive and easier to understand.

Entity Relationship Diagram
--------------------------

.. code-block:: text

    ┌───────────┐       ┌───────────┐       ┌───────────┐
    │   User    │       │ Professor │       │  Course   │
    ├───────────┤       ├───────────┤       ├───────────┤
    │ id (PK)   │◄──┐   │ name (PK) │◄─────►│ id (PK)   │
    │ name      │   └──►│ user_id   │       │ name      │
    │ email     │       │ special...│       │ profesor..│
    │ password  │       │ title     │       │ credits   │
    │ role      │       └───────────┘       └─────┬─────┘
    └─────┬─────┘                                 │
          │                                       │
          │                                       │
    ┌─────▼─────┐                           ┌─────▼─────┐
    │   Grupa   │                           │   Exam    │
    ├───────────┤                           ├───────────┤
    │ name (PK) │◄─────────────────────────►│ id (PK)   │
    │ year      │                           │ course_id │
    │ special...│                           │ grupa_name│
    │ leader_id │                           │ date      │
    └───────────┘                           │ time      │
                                            │ sala_name │
    ┌───────────┐                           │ status    │
    │   Sala    │                           └─────┬─────┘
    ├───────────┤                                 │
    │ name (PK) │◄─────────────────────────┘
    │ capacity  │
    │ building  │
    │ floor     │
    └───────────┘

Tables
------

users
~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 20 40 20

   * - Column
     - Type
     - Description
     - Constraints
   * - id
     - Integer
     - User identifier
     - Primary Key
   * - name
     - String(100)
     - User's full name
     - Not Null
   * - email
     - String(100)
     - User's email address
     - Unique, Not Null
   * - password
     - String
     - Hashed password
     - Not Null
   * - role
     - Enum
     - User role (STUDENT, PROFESSOR, SECRETARIAT)
     - Not Null

professors
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 20 40 20

   * - Column
     - Type
     - Description
     - Constraints
   * - name
     - String(100)
     - Professor's name
     - Primary Key
   * - specialization
     - String(100)
     - Area of specialization
     - Nullable
   * - title
     - String(50)
     - Academic title
     - Nullable
   * - user_id
     - Integer
     - Reference to users table
     - Foreign Key, Nullable

grupa
~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 20 40 20

   * - Column
     - Type
     - Description
     - Constraints
   * - name
     - String(50)
     - Group name (e.g., "CS101")
     - Primary Key
   * - year
     - Integer
     - Academic year
     - Nullable
   * - specialization
     - String(100)
     - Field of study
     - Nullable
   * - leader_id
     - Integer
     - Reference to users table (group leader)
     - Foreign Key, Nullable

sala
~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 20 40 20

   * - Column
     - Type
     - Description
     - Constraints
   * - name
     - String(50)
     - Room name (e.g., "A101")
     - Primary Key
   * - capacity
     - Integer
     - Seating capacity
     - Nullable
   * - building
     - String(50)
     - Building name
     - Nullable
   * - floor
     - Integer
     - Floor number
     - Nullable

courses
~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 20 40 20

   * - Column
     - Type
     - Description
     - Constraints
   * - id
     - Integer
     - Course identifier
     - Primary Key
   * - name
     - String(100)
     - Course name
     - Not Null
   * - profesor_name
     - String(100)
     - Reference to professors table
     - Foreign Key, Not Null
   * - credits
     - Integer
     - Number of credits
     - Nullable

exams
~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 20 40 20

   * - Column
     - Type
     - Description
     - Constraints
   * - id
     - Integer
     - Exam identifier
     - Primary Key
   * - course_id
     - Integer
     - Reference to courses table
     - Foreign Key, Not Null
   * - grupa_name
     - String(50)
     - Reference to grupa table
     - Foreign Key, Not Null
   * - date
     - Date
     - Exam date
     - Not Null
   * - time
     - Time
     - Exam time
     - Not Null
   * - sala_name
     - String(50)
     - Reference to sala table
     - Foreign Key, Not Null
   * - status
     - Enum
     - Exam status (PROPOSED, CONFIRMED, CANCELLED, COMPLETED)
     - Not Null

Key Design Decisions
------------------

1. **Meaningful Primary Keys**:
   
   We use meaningful identifiers as primary keys for several tables:
   
   - `grupa` table uses `name` (e.g., "CS101") as the primary key
   - `sala` table uses `name` (e.g., "A101") as the primary key
   - `professors` table uses `name` as the primary key
   
   This makes the schema more intuitive and easier to understand, with direct references to meaningful identifiers rather than abstract IDs.

2. **Group Leader Functionality**:
   
   Each group (`grupa`) can have a designated leader who is responsible for communicating with professors about exam scheduling. This is implemented as a `leader_id` field in the `grupa` table that references a user in the `users` table.

3. **Intuitive Relationships**:
   
   - `exams` table references groups by `grupa_name`
   - `exams` table references rooms by `sala_name`
   - `courses` table references professors by `profesor_name`
   
   These relationships are more intuitive than using numeric IDs.
