from persistence import *
from persistence import repo
import sqlite3

def print_tables():
        all_data = repo.get_tables()
        for table_name, rows in all_data:
            print(f"{table_name}")
            for item in rows:
                print(item)
        print()

def print_employees_report():
    report_data = repo.get_employees_report()
    print("Employees report")
    for item in report_data:
        print(item)
    print()

def print_activity_report():
     print("Activities report")
     activity_report = repo.get_activitys_report()
     for report in activity_report:
        print(report)
     print()

def main():
    print_tables() 
    print_employees_report()
    print_activity_report()
   



if __name__ == '__main__':
    main()