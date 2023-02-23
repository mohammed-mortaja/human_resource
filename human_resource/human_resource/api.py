
from __future__ import unicode_literals
import frappe
import datetime

import frappe

# @frappe.whitelist(allow_guest=True)
# def test_api():
#     return ("test")
#
#******************************
#token and secret : token 8b6dcb3b87d7f63:a758cfdcca5e8c6
# 
@frappe.whitelist()
def create_attendance(attendance_date, check_in, check_out, ):
    api_key = str(frappe.get_request_header("Authorization")).split(':')[0].split(' ')[-1]
    user = frappe.db.sql(f"""select * from tabUser where api_key = '{api_key}' """, as_dict=1)[0].name
    employee = frappe.db.sql(f""" select name from `tabEmployee` where user = '{user}' """, as_dict=1)[0].name
    doc = frappe.new_doc('Attendance')
    doc.employee = employee
    doc.attendance_date = datetime.datetime.strptime(str(attendance_date).strip(), '%d-%m-%Y')
    doc.check_in = check_in
    doc.check_out = check_out
    doc.save()
    doc.submit()


    return doc.as_dict()
