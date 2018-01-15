from django.db import models
import uuid

from . import Punch

class EmployeePunch:
    @classmethod
    def employee_punch_queryset(cls):
        return Punch.objects.raw(
            '''
            select * from Attendence_Employee as Emp 
            join Attendence_Punch as Pun on Emp.employee_id = Pun.employee_id;
            ''')