from django.db import models


# Create your models here.
class Employee(models.Model):
    emp_no = models.IntegerField()
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    birth_date = models.DateField()
    sex = models.CharField(max_length=10)
    street = models.CharField(max_length=100)
    house_no = models.CharField(max_length=10)
    apart_no = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    post = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f'{self.first_name} {self.surname}'


class EmployeeHistory(models.Model):
    date_from = models.DateField()
    date_to = models.DateField()
    hire_date = models.DateField()
    termination_date = models.DateField(null=True)
    position = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    employment_type = models.CharField(max_length=100)
    emp = models.ForeignKey(Employee, on_delete=models.CASCADE)


class Document(models.Model):
    document_type = models.CharField(max_length=50)
    document_year = models.IntegerField()
    document_details = models.TextField()
    emp = models.ForeignKey(Employee, on_delete=models.CASCADE)
