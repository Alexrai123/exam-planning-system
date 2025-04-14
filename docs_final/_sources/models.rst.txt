Models
======

This section documents the data models used in the Exam Planning System.

User Model
---------

.. py:class:: User

   Represents a user in the system.

   .. py:attribute:: id
      :type: Integer

      Primary key for the user.

   .. py:attribute:: name
      :type: String(100)

      The user's full name.

   .. py:attribute:: email
      :type: String(100)

      The user's email address (unique).

   .. py:attribute:: password
      :type: String

      The user's hashed password.

   .. py:attribute:: role
      :type: UserRole

      The user's role in the system (STUDENT, PROFESSOR, or SECRETARIAT).

   .. py:attribute:: professor
      :type: relationship

      One-to-one relationship with Professor model (if the user is a professor).

   .. py:attribute:: led_groups
      :type: relationship

      One-to-many relationship with Grupa model (if the user is a group leader).

.. py:class:: UserRole

   Enum representing the possible user roles in the system.

   .. py:attribute:: STUDENT
      
      Student role.

   .. py:attribute:: PROFESSOR
      
      Professor role.

   .. py:attribute:: SECRETARIAT
      
      Administrative staff role.

Professor Model
-------------

.. py:class:: Professor

   Represents a professor in the system.

   .. py:attribute:: name
      :type: String(100)

      The professor's name (primary key).

   .. py:attribute:: specialization
      :type: String(100)

      The professor's area of specialization.

   .. py:attribute:: title
      :type: String(50)

      The professor's academic title.

   .. py:attribute:: user_id
      :type: Integer

      Foreign key referencing the User model.

   .. py:attribute:: courses
      :type: relationship

      One-to-many relationship with Course model.

   .. py:attribute:: user
      :type: relationship

      Many-to-one relationship with User model.

Grupa Model
---------

.. py:class:: Grupa

   Represents a student group in the system.

   .. py:attribute:: name
      :type: String(50)

      The group's name (primary key, e.g., "CS101").

   .. py:attribute:: year
      :type: Integer

      The academic year of the group.

   .. py:attribute:: specialization
      :type: String(100)

      The group's field of study.

   .. py:attribute:: leader_id
      :type: Integer

      Foreign key referencing the User model (the group leader).

   .. py:attribute:: exams
      :type: relationship

      One-to-many relationship with Exam model.

   .. py:attribute:: leader
      :type: relationship

      Many-to-one relationship with User model.

Sala Model
--------

.. py:class:: Sala

   Represents a room in the system.

   .. py:attribute:: name
      :type: String(50)

      The room's name (primary key, e.g., "A101").

   .. py:attribute:: capacity
      :type: Integer

      The room's seating capacity.

   .. py:attribute:: building
      :type: String(50)

      The building where the room is located.

   .. py:attribute:: floor
      :type: Integer

      The floor where the room is located.

   .. py:attribute:: exams
      :type: relationship

      One-to-many relationship with Exam model.

Course Model
----------

.. py:class:: Course

   Represents a course in the system.

   .. py:attribute:: id
      :type: Integer

      Primary key for the course.

   .. py:attribute:: name
      :type: String(100)

      The course name.

   .. py:attribute:: profesor_name
      :type: String(100)

      Foreign key referencing the Professor model.

   .. py:attribute:: credits
      :type: Integer

      The number of credits for the course.

   .. py:attribute:: professor
      :type: relationship

      Many-to-one relationship with Professor model.

   .. py:attribute:: exams
      :type: relationship

      One-to-many relationship with Exam model.

Exam Model
--------

.. py:class:: Exam

   Represents an exam in the system.

   .. py:attribute:: id
      :type: Integer

      Primary key for the exam.

   .. py:attribute:: course_id
      :type: Integer

      Foreign key referencing the Course model.

   .. py:attribute:: grupa_name
      :type: String(50)

      Foreign key referencing the Grupa model.

   .. py:attribute:: date
      :type: Date

      The date of the exam.

   .. py:attribute:: time
      :type: Time

      The time of the exam.

   .. py:attribute:: sala_name
      :type: String(50)

      Foreign key referencing the Sala model.

   .. py:attribute:: status
      :type: ExamStatus

      The status of the exam.

   .. py:attribute:: course
      :type: relationship

      Many-to-one relationship with Course model.

   .. py:attribute:: grupa
      :type: relationship

      Many-to-one relationship with Grupa model.

   .. py:attribute:: sala
      :type: relationship

      Many-to-one relationship with Sala model.

.. py:class:: ExamStatus

   Enum representing the possible exam statuses in the system.

   .. py:attribute:: PROPOSED
      
      Exam has been proposed by a group leader.

   .. py:attribute:: CONFIRMED
      
      Exam has been confirmed by a professor.

   .. py:attribute:: CANCELLED
      
      Exam has been cancelled.

   .. py:attribute:: COMPLETED
      
      Exam has been completed.
