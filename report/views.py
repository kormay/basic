from django.template.loader import *
from attendence.models import Employee
from rlextra.rml2pdf import rml2pdf
from django.db import connection
# Create your views here.


def createPDF():
    template = get_template('attendence/user.rml')
    cursor = connection.cursor()
    cursor.execute("""
                    select  AE.user_name ,
                            dayofweek(min(punch_date)) - 1 as weeknum ,
                            date(min(punch_date)) as datenum ,
                            min( AP.punch_date) as punch_in_date ,
                            max(AP.punch_date) as punch_out_date
                    from    attendence_punch AP
                            inner join attendence_employee AE on AP.employee_id = AE.employee_id
                    group by AE.user_name ,
                            date(AP.punch_date)
        """)
    rml = template.render(context={'source': list(cursor.fetchall())}) 
    open('temp.rml', mode='w').write(rml)
    rml2pdf.go(rml)
