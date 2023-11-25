from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_employees, name='all_employees'),
    path('<int:id>', views.employee_details, name='employee_details'),
    path('<int:id>/documents', views.documents_for_employee, name='documents_for_employee'),
    path('reports', views.reports, name='reports'),
    path('reports/<int:id>', views.generate_raport, name='generate_raport'),
    path('import', views.import_data, name='import_data'),
    path('documents', views.all_documents, name='all_documents'),
    path('documents/<int:id>', views.document_details, name='document_details'),
    path('documents/<int:id>/generate-pdf', views.document_generate_pdf, name='document_generate_pdf')
]
