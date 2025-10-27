# BGU Mart: Supermarket Management System

## 📘 Project Overview
* A Python + SQLite system for managing a supermarket chain.
* Handles employees, suppliers, products, branches, and sales or supply activities.
* Stores all data in a single local database file bgumart.db.

## 🧩 Components & Features
* initiate.py – Builds a fresh bgumart.db and loads initial data from a configuration file.
* action.py – Executes sales (negative quantity) or supply (positive quantity) actions and updates product inventory.
* printdb.py – Prints all database tables and generates summary reports.
* persistence.py, dbtools.py, ProductDao.py – Internal database access layer (DAO, repository, and schema definitions).

## ⚙️ Running Instructions
The project runs as three independent command-line modules, with the following sequence required for setup and reporting:
1. Database Initialization (initiate.py)
   Creates a new bgumart.db and loads initial data from config.txt.
3. Transaction Processing (action.py)
   Applies supply and sales actions from actions.txt, updating quantities and recording activities.
4. Reporting (printdb.py)
   Prints all tables and generates summary and detailed reports.
