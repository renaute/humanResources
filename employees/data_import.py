import datetime
import csv
from . import models


def import_salary_from_csv(employee_id, effective_day, new_salary):
    employee = models.Employee.objects.get(pk=employee_id)
    # print(employee)

    all_emp_hist = employee.employeehistory_set.all()  # zwraca wszystkie zapisy historyczne dla pracownika
    latest_emp_hist = all_emp_hist.latest(
        'date_from')  # latest filtruje po dacie zwracając zapis historyczny z najpóźniejszą datą
    latest_date = latest_emp_hist.date_from

    if latest_date == effective_day:

        latest_emp_hist.salary = new_salary
        latest_emp_hist.save()
        save_to_log(f'Zaktualizowano stawkę Pracownika {employee.first_name} {employee.surname} od {effective_day}', 1)



    elif latest_date < effective_day:
        latest_emp_hist.date_to = effective_day - datetime.timedelta(days=1)
        latest_emp_hist.save()
        models.EmployeeHistory.objects.create(date_from=effective_day,
                                              date_to='2999-12-31',
                                              hire_date=latest_emp_hist.hire_date,
                                              termination_date=latest_emp_hist.termination_date,
                                              position=latest_emp_hist.position,
                                              employment_type=latest_emp_hist.employment_type,
                                              salary=new_salary,
                                              emp_id=employee_id)
        save_to_log(f'Dodano nowy zapis historyczny dla Pracowika {employee.first_name} {employee.surname} od {effective_day}', 1)

    else:
        save_to_log(f'Pracownik {employee.first_name} {employee.surname} posiada późniejsze (niż {effective_day}) zapisy historyczne.', 0)


def save_to_log(message: str, status: int):
    new_record = [[message, status]]

    filename = 'import_log.csv'
    with open(filename, 'a', encoding='UTF-8',newline='') as output:
        writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerows(new_record)
