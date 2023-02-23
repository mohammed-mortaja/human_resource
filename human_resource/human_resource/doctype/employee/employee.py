# Copyright (c) 2023, moh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime

class Employee(Document):
	def validate(self):
		# make full name read-only
		self.flags.ignore_mandatory = True
		self.full_name = self.first_name + " " + self.middle_name + " " + self.last_name
		self.flags.ignore_mandatory = False
		
		# validate status and age
		today = datetime.datetime.now().date()
		date_of_birth_str = self.date_of_birth.strftime('%Y-%m-%d')
		date_of_birth = datetime.datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
		if self.status == "Active" and (today.year - date_of_birth.year) > 60:
			frappe.throw("Cannot save Employee with status Active and age more than 60 years")
		
		# validate mobile
		if not self.mobile.startswith("059") or len(self.mobile) != 10:
			frappe.throw("Mobile must start with 059 and must be 10 digits long")

		if len(self.employee_education) < 2:
			frappe.throw("Employee must have at least two Education entries")
			
