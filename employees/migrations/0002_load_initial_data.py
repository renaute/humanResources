from django.db import migrations
import csv
from employees.models import Employee, EmployeeHistory, Document


def load_initial_data(app, schema_editor):
    with open('employees/migrations/employees.csv', 'r', encoding='utf-8') as input_file:
        input_file.readline()
        reader = csv.reader(input_file, delimiter=';')
        for row in reader:
            employee = Employee(emp_no=int(row[0]),
                                first_name=row[1], surname=row[2],
                                birth_date=row[3],
                                sex=row[4],
                                street=row[5],
                                house_no=row[6],
                                apart_no=row[7],
                                city=row[8],
                                zip_code=row[9],
                                post=row[10],
                                email=row[11])

            employee.save()

    with open('employees/migrations/employeesHistory.csv', 'r', encoding='utf-8') as input_file_emp_hist:
        input_file_emp_hist.readline()
        reader = csv.reader(input_file_emp_hist, delimiter=';')
        for row in reader:
            employee = Employee.objects.get(id=int(row[0]))
            employeeHistory = EmployeeHistory(emp=employee,  # przypisanie instancji klasy EmployeeHistory
                                              date_from=row[1], date_to=row[2],
                                              hire_date=row[3],
                                              termination_date=row[4],
                                              position=row[5],
                                              salary=float(row[6]),
                                              employment_type=row[7],
                                              )

            employeeHistory.save()

    with open('employees/migrations/documents.csv', 'r', encoding='utf-8') as documents_file:
        documents_file.readline()
        reader = csv.reader(documents_file, delimiter=';')
        for row in reader:
            employee = Employee.objects.get(id=int(row[0]))
            document = Document(emp=employee,  # przypisanie instancji klasy EmployeeHistory
                                document_type=row[1],
                                document_year=row[2],
                                document_details=row[3]
                                )

            document.save()


class Migration(migrations.Migration):
    dependencies = [
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_initial_data)

    ]
