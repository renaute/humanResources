import datetime
import os
import json
import io
import csv
from . import data_import
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from . import models
from django.core.files.storage import FileSystemStorage


# Create your views here.
def all_employees(request):
    name = request.GET.get('name')
    if name:
        employees = models.Employee.objects.filter(surname__contains=name)
    else:
        employees = models.Employee.objects.all()

    return render(request, 'employees/all_employees.html',
                  {'employees': employees,
                   'filter_name': name})


def employee_details(request, id):
    min_day = datetime.date(1900, 1, 1)
    max_day = datetime.date(2999, 12, 31)
    found_employee = get_object_or_404(models.Employee, pk=id)
    found_emp_hist = found_employee.employeehistory_set.all()

    return render(request, 'employees/employee_details.html',
                  {'employee': found_employee,
                   'empl_history': found_emp_hist,
                   'first_day': min_day,
                   'last_day': max_day,
                   }
                  )


def reports(request):
    reports = {1: 'Dane wszystkich pracowników', 2: 'Dane dotyczące aktualnego zatrudnienia'}
    return render(request, 'employees/reports.html', {'reports': reports})


def generate_raport(request, id):
    response = HttpResponse(content_type='text/csv;charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename="raport.csv"'

    writer = csv.writer(response)

    if id == 1:
        headers = ['numer pracownika', 'imię', 'nazwisko', 'data urodzenia', 'płeć', 'email', 'ulica',
                   'numer domu', 'miejscowość', 'kod pocztowy', 'poczta']
        employees = models.Employee.objects.all().values_list('emp_no', 'first_name', 'surname', 'birth_date', 'sex',
                                                              'email', 'street', 'house_no', 'apart_no', 'city',
                                                              'zip_code',
                                                              'post')
    elif id == 2:
        today = datetime.date.today()
        headers = ['numer pracownika', 'imię', 'nazwisko', 'data obowiązywania', 'data zatrudnienia', 'data zwolnienia',
                   'rodzaj umowy',
                   'stanowisko', 'stawka']
        employees = models.EmployeeHistory.objects.all().values_list('emp__emp_no', 'emp__first_name', 'emp__surname',
                                                                     'emp_id', 'date_from', 'hire_date',
                                                                     'termination_date',
                                                                     'employment_type',
                                                                     'position', 'salary') \
            .filter(date_from__lte=today, date_to__gte=today)

    writer.writerow(headers)
    for employee in employees:
        writer.writerow(employee)

    return response


def import_data(request):
    if request.method == 'POST' and request.FILES['upload_file']:
        upload_file = request.FILES['upload_file']
        fs = FileSystemStorage()
        filename = fs.save(upload_file.name, upload_file)
        uploaded_file_path = fs.path(filename)
        required_column = ['emp_no', 'date_from', 'new_salary']
        message = None

        with open(filename, 'r', encoding='utf-8-sig') as input_file:

            reader = csv.DictReader(input_file, delimiter=';')
            if set(required_column).issubset(reader.fieldnames):

                for row in reader:
                    try:
                        employee_id = models.Employee.objects.get(emp_no=int(row['emp_no'])).id
                        employee = models.Employee.objects.get(pk=employee_id)
                        effective_day = datetime.datetime.strptime(row['date_from'], '%Y-%m-%d').date()
                        new_salary = int(row['new_salary'])
                        data_import.import_salary_from_csv(employee_id, effective_day, new_salary)
                    except:
                        data_import.save_to_log(
                            f'Nie zaktualizowno Pracownika {employee.first_name} {employee.surname}. Niepoprawny format danych.',
                            0)
                        continue

                message = 'Plik został zaimportowany'
                input_file.close()
                fs.delete(uploaded_file_path)

                with open('./import_log.csv', encoding='UTF-8', newline='') as log_file:
                    headers = ['message', 'status']
                    reader = csv.DictReader(log_file, delimiter=',', fieldnames=headers)
                    logs = list(reader)
                os.remove('./import_log.csv')
                return render(request, 'employees/import.html', {'message': message, 'logs': logs})

            else:
                message_failed = 'Niepoprawne nagłówki w pliku'

        fs.delete(uploaded_file_path)
        return render(request, 'employees/import.html', {
            'message_failed': message_failed
        })
    return render(request, 'employees/import.html')


def all_documents(request):
    name = request.GET.get('name')
    if name:
        documents = models.Document.objects.all().values('id', 'emp__emp_no', 'emp__first_name',
                                                         'emp__surname', 'document_type',
                                                         'document_year').filter(emp__surname__contains=name)

    else:
        documents = models.Document.objects.all().values('id', 'emp__emp_no', 'emp__first_name',
                                                         'emp__surname', 'document_type',
                                                         'document_year')

    return render(request, 'employees/all_documents.html', {'documents': documents, 'filter_name': name})


def document_details(request, id):
    found_document = get_object_or_404(models.Document, id=id)
    document = models.Document.objects.all().values('id', 'emp__emp_no', 'emp__first_name',
                                                    'emp__surname', 'document_type',
                                                    'document_year').filter(id__exact=id)
    doc_details = found_document.document_details
    details = json.loads(doc_details)
    empl_data = (details['Deklaracja_PIT11'])['Dane_podatnika']
    empl_income = ((details['Deklaracja_PIT11'])['Dochody_podatnika'])['Naleznosci_stosunek_pracy']
    return render(request, 'employees/document_details.html', {'document': document,
                                                               'empl_data': empl_data,
                                                               'empl_income': empl_income,
                                                               'doc_id': id})


def documents_for_employee(request, id):
    documents = models.Document.objects.all().values('id', 'emp__emp_no', 'emp__first_name',
                                                     'emp__surname', 'document_type',
                                                     'document_year').filter(emp__id=id)

    return render(request, 'employees/all_documents.html', {'documents': documents})


def document_generate_pdf(request, id):
    found_document = get_object_or_404(models.Document, id=id)
    doc_details = found_document.document_details
    details = json.loads(doc_details)
    empl_data = (details['Deklaracja_PIT11'])['Dane_podatnika']
    empl_income = ((details['Deklaracja_PIT11'])['Dochody_podatnika'])['Naleznosci_stosunek_pracy']

    buffer = io.BytesIO()

    p = canvas.Canvas(buffer, pagesize=A4)
    text_object = p.beginText()
    text_object.setTextOrigin(30, 800)
    text_object.setFont('Times-Bold', 14)
    text_object.textLine('Dane podatnika:')
    text_object.textLine()

    text_object.setFont('Times-Roman', 12)
    for key, value in empl_data.items():
        if value != '':
            text_object.textLine(text=f'{key} : {value}'.encode('utf-8'))

    text_object.textLine()
    text_object.setFont('Times-Bold', 14)
    text_object.textLine('Dochody podatnika:')
    text_object.textLine()
    text_object.setFont('Times-Roman', 12)

    for key, value in empl_income.items():
        if value != 0:
            text_object.textLine(text=f'{key} : {value}')

    p.drawText(aTextObject=text_object)

    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="document_pit.pdf")
