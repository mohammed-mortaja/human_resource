	# Copyright (c) 2023, moh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta

class LeaveApplication(Document):

	def validate(self):
			# Get total leave days and leave balance before application
			from_date = datetime.strptime(self.from_date, '%Y-%m-%d')
			to_date = datetime.strptime(self.to_date, '%Y-%m-%d')
			self.total_leaves = (to_date - from_date).days + 1
			leave_allocation = frappe.get_doc("Leave Allocation", {"employee": self.employee})
			self.leave_balance_before_application = leave_allocation.total_leaves

			# Validate if total leave days is more than leave balance before application
			if self.total_leaves > self.leave_balance_before_application:
				frappe.throw("Total leave days cannot be more than leave balance before application")

			leave_type = frappe.get_doc("Leave Type", self.leave_type)
			if leave_type.applicable_after_days:
				applicable_after_date = datetime.now() + timedelta(days=leave_type.applicable_after_days)
				if from_date < applicable_after_date:
						frappe.throw(f"Cannot apply for leave before {applicable_after_days} working days")


			if self.from_date > self.to_date:
				frappe.throw("'From Date' cannot be after 'To Date'")
			# check if there is already an allocation with the same dates, employee, and leave type
			allocation = frappe.get_all("Leave Allocation", filters={
				"employee": self.employee,
				"leave_type": self.leave_type,
				"from_date": self.from_date,
				"to_date": self.to_date
			}, limit=1)
			if allocation:
				frappe.throw("Already have allocation to same Dates, Employee, and Leave Type")

			# Get leave type
			leave_type = frappe.get_doc("Leave Type", self.leave_type)

			# Get total leave days and leave balance before application
			from_date = datetime.strptime(self.from_date, '%Y-%m-%d')
			to_date = datetime.strptime(self.to_date, '%Y-%m-%d')
			self.total_leaves = (to_date - from_date).days + 1
			
			# Validate if max_continuous_days_allowed is defined
			if leave_type.max_continuous_days_allowed:
				# Validate if total leave days is more than max continuous days allowed
				if self.total_leaves > leave_type.max_continuous_days_allowed:
					frappe.throw(f"Total leave days cannot be more than {leave_type.max_continuous_days_allowed}")
			

			# Get leave type
			leave_type = frappe.get_doc("Leave Type", self.leave_type)

			# Get total leave days and leave balance before application
			from_date = datetime.strptime(self.from_date, '%Y-%m-%d')
			to_date = datetime.strptime(self.to_date, '%Y-%m-%d')
			self.total_leaves = (to_date - from_date).days + 1
			
			# Validate if max_continuous_days_allowed is defined
			if leave_type.max_continuous_days_allowed:
				# Validate if total leave days is more than max continuous days allowed
				if self.total_leaves > leave_type.max_continuous_days_allowed:
					frappe.throw(f"Total leave days cannot be more than {leave_type.max_continuous_days_allowed}")
			
			# Get leave allocation
			leave_allocation = frappe.get_doc("Leave Allocation", {"employee": self.employee})
			self.leave_balance_before_application = leave_allocation.total_leaves
			
			# Validate if total leave days is more than leave balance before application
			if not leave_type.allow_negative_balance and self.total_leaves > self.leave_balance_before_application:
				frappe.throw("Total leave days cannot be more than leave balance before application")
			

	def on_submit(self):
			# Update leave allocation total leaves
			leave_allocation = frappe.get_doc("Leave Allocation", {"employee": self.employee})
			leave_allocation.total_leaves -= self.total_leaves
			leave_allocation.save()

	def on_cancel(self):
			# Update leave allocation total leaves
			leave_allocation = frappe.get_doc("Leave Allocation", {"employee": self.employee})
			leave_allocation.total_leaves += self.total_leaves
			leave_allocation.save()
		
	
		