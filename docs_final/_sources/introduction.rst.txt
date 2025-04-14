Introduction
============

Overview
--------

The Exam Planning System is a comprehensive web application designed to streamline the process of scheduling and managing university exams. It provides an intuitive interface for professors, students, and administrative staff to coordinate exam scheduling effectively.

The system is built with a modern tech stack:

* **Backend**: FastAPI (Python)
* **Database**: PostgreSQL
* **Frontend**: React
* **Containerization**: Docker

Purpose
-------

The primary purpose of this system is to simplify the complex task of exam scheduling by:

1. Allowing student group leaders to propose exam dates
2. Enabling professors to review and confirm proposed exams
3. Providing administrative staff with tools to manage the entire process
4. Offering a clear calendar view of all scheduled exams

User Roles
----------

The system supports three distinct user roles, each with specific permissions:

1. **STUDENT**: 
   * View exams for their group
   * View the exam calendar
   * Access their profile information

2. **PROFESSOR**:
   * View all exams related to their courses
   * Confirm or cancel proposed exams
   * View the exam calendar
   * Access their profile information

3. **SECRETARIAT** (Administrative Staff):
   * Full access to all system features
   * Create, edit, and delete exams
   * Manage users, rooms, courses, and groups
   * Schedule exams automatically
   * Access all system information

Group Leader Functionality
-------------------------

A special feature of the system is the group leader role. Each student group can have a designated leader who is responsible for communicating with professors about exam scheduling. This leader:

* Must be a student (have the STUDENT role)
* Is linked to a specific group via the `leader_id` field in the `grupa` table
* Can propose exam dates on behalf of their group
* Acts as a representative for the entire group

This functionality creates a more realistic workflow where student representatives can propose exam dates, which are then confirmed by professors and the secretariat.
