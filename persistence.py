import sqlite3
import atexit
from dbtools import Dao
from ProductDao import ProductDao
 
# Data Transfer Objects:
class Employee(object):
   def __init__(self, id, name, salary, branche):
     self.id = id
     self.name = name
     self.salary = salary
     self.branche= branche

   def __str__(self):
        return f"({self.id}, '{self.name}', {self.salary}, {self.branche})" 

class Supplier(object):
    def __init__(self,id, name, contact_information):
        self.id = id
        self.name = name
        self.contact_information = contact_information

    def __str__(self):
        return f"({self.id}, '{self.name}', '{self.contact_information}')"

class Product(object):
    def __init__(self,id, description, price, quantity):
        self.id = id
        self.description = description
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"({self.id}, '{self.description}', {self.price}, {self.quantity})"
        

class Branche(object):
    def __init__(self,id, location, number_of_employees):
        self.id = id
        self.location = location
        self.number_of_employees = number_of_employees
    
    def __str__(self):
        return f"({self.id}, '{self.location}', {self. number_of_employees})"

class Activitie(object):
     def __init__(self, product_id, quantity, activator_id, date):
        self.product_id = product_id
        self.quantity = quantity
        self.activator_id = activator_id
        self.date = date 

     def __str__(self):
        return f"({self.product_id}, {self.quantity}, {self. activator_id}, '{self. date}')"
class EmployeeReport(object):
    def __init__(self, name, salary, working_location, total_sales_income):
        self.name = name
        self.salary = salary
        self.working_location = working_location
        self.total_sales_income = total_sales_income
        
    def __str__(self):
        return f"{self.name} {self.salary} {self. working_location} {self. total_sales_income}"

class ActivitieReport(object):
     def __init__(self, date, description, quantity, name_of_seller, name_of_supplier):
        self.date = date
        self.description= description
        self.quantity = quantity
        self.name_of_seller = name_of_seller
        self.name_of_supplier= name_of_supplier
     def __str__(self):
        return (f"('{self.date}', '{self.description}', "
            f"{self.quantity}, "
            f"{'None' if self.name_of_seller is None else f'\'{self.name_of_seller}\''}, "
            f"{'None' if self.name_of_supplier is None else f'\'{self.name_of_supplier}\''})")

 
 
#Repository
class Repository(object):
    def __init__(self):
        self._conn = sqlite3.connect('bgumart.db')
        self.employees = Dao(Employee,self._conn)
        self.suppliers = Dao(Supplier,self._conn)
        self.products = ProductDao(Product,self._conn)
        self.branches = Dao(Branche,self._conn)
        self.activities = Dao(Activitie,self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()
 
    def create_tables(self):
        self._conn.executescript("""
            CREATE TABLE employees (
                id              INT         PRIMARY KEY,
                name            TEXT        NOT NULL,
                salary          REAL        NOT NULL,
                branche    INT REFERENCES branches(id)
            );
    
            CREATE TABLE suppliers (
                id                   INTEGER    PRIMARY KEY,
                name                 TEXT       NOT NULL,
                contact_information  TEXT
            );

            CREATE TABLE products (
                id          INTEGER PRIMARY KEY,
                description TEXT    NOT NULL,
                price       REAL NOT NULL,
                quantity    INTEGER NOT NULL
            );

            CREATE TABLE branches (
                id                  INTEGER     PRIMARY KEY,
                location            TEXT        NOT NULL,
                number_of_employees INTEGER
            );
    
            CREATE TABLE activities (
                product_id      INTEGER REFERENCES products(id),
                quantity        INTEGER NOT NULL,
                activator_id    INTEGER NOT NULL,
                date            TEXT    NOT NULL
            );
        """)

    def execute_command(self, script: str) -> list:
        return self._conn.cursor().execute(script).fetchall()
    
    def update_product(self, product_id, newQuantity):
       self.products.update(product_id, quantity=newQuantity)

    def get_tables(self):
        cursor = self._conn.cursor()
        tables = [
        ("Activities", [Activitie (*row) for row in cursor.execute("SELECT * FROM activities ORDER BY date").fetchall()]),
        ("Branches", [Branche (*row) for row in cursor.execute("SELECT * FROM branches ORDER BY id").fetchall()]),
        ("Employees",[Employee (*row) for row in cursor.execute("SELECT * FROM employees ORDER BY id").fetchall()]),
        ("Products", [Product (*row) for row in cursor.execute("SELECT * FROM products ORDER BY id").fetchall()]),
        ("Suppliers", [Supplier(*row) for row in cursor.execute("SELECT * FROM suppliers ORDER BY id").fetchall()])
        ]
        return tables
    
    def get_employees_report(self):

        str = """
        SELECT e.name, e.salary, b.location, 
        SUM(CASE WHEN a.quantity < 0 THEN -a.quantity * p.price ELSE 0 END) AS total_sales_income
        FROM employees e
        JOIN branches b ON e.branche = b.id
        LEFT JOIN activities a ON e.id = a.activator_id
        LEFT JOIN products p ON a.product_id = p.id
        GROUP BY e.id
        ORDER BY e.name;
        """
        
        r = self.execute_command(str)
        return [EmployeeReport(*row) for row in r]


    def get_activitys_report(self):
        query = """
        SELECT activities.date, products.description, activities.quantity, 
               CASE WHEN activities.quantity < 0 THEN employees.name ELSE NULL END AS seller,
               CASE WHEN activities.quantity > 0 THEN suppliers.name ELSE NULL END AS supplier
        FROM activities
        LEFT JOIN products ON activities.product_id = products.id
        LEFT JOIN employees ON activities.activator_id = employees.id
        LEFT JOIN suppliers ON activities.activator_id = suppliers.id
        ORDER BY activities.date
        """

        r = self.execute_command(query)
        return [ActivitieReport(*row) for row in r]


# singleton
repo = Repository()
atexit.register(repo._close)