	# Copyright (c) 2023, moh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta
class LeaveApplication(Document):

	def validate(self):
		self.total_leave_days_()
		self.leave_balance_()
		self.check_total_leave_days()
		self.check_from_date()
		self.max_continuous_days_allowed()

	def total_leave_days_(self):
		# Get total leave days
		from_date = datetime.strptime(self.from_date, '%Y-%m-%d')
		to_date = datetime.strptime(self.to_date, '%Y-%m-%d')
		self.total_leaves = (to_date - from_date).days + 1

	def leave_balance_(self):
		# Get leave allocation
		leave_allocation = frappe.get_doc("Leave Allocation", {"employee": self.employee})
		self.leave_balance_before_application = leave_allocation.total_leaves

	def check_total_leave_days(self):
		leave_type = frappe.get_doc("Leave Type", self.leave_type)
		# Validate if total leave days is more than leave balance before application
		if not leave_type.allow_negative_balance and self.total_leaves > self.leave_balance_before_application:
			frappe.throw("Total leave days cannot be more than leave balance before application")

	def check_from_date(self):
		# Check if 'From Date' is after 'To Date'
		from_date = datetime.strptime(self.from_date, '%Y-%m-%d')
		to_date = datetime.strptime(self.to_date, '%Y-%m-%d')
		if from_date > to_date:
			frappe.throw("'From Date' cannot be after 'To Date'")

		# Validate if applicable after is defined
		leave_type = frappe.get_doc("Leave Type", self.leave_type)
		if leave_type.applicable_after:
			applicable_after_days = leave_type.applicable_after
			frappe.throw(f"Cannot apply for leave before {applicable_after_days} working days")

		# Check if there is already an allocation with the same dates, employee, and leave type
		allocation = frappe.get_all("Leave Allocation", filters={
			"employee": self.employee,
			"leave_type": self.leave_type,
			"from_date": self.from_date,
			"to_date": self.to_date
		}, limit=1)
		if allocation:
			frappe.throw("Already have allocation to same Dates, Employee, and Leave Type")

	def max_continuous_days_allowed(self):
		# Get leave type
		leave_type = frappe.get_doc("Leave Type", self.leave_type)

		# Validate if max_continuous_days_allowed is defined
		if leave_type.max_continuous_days_allowed:
			# Validate if total leave days is more than max continuous days allowed
			if self.total_leaves > leave_type.max_continuous_days_allowed:
				frappe.throw(f"Total leave days cannot be more than {leave_type.max_continuous_days_allowed}")

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
@frappe.whitelist()
def get_total_leaves(employee=None ,leave_type=None ,from_date=None ,to_date=None):
	if employee and leave_type and from_date and to_date:
		leave_allocated = frappe.db.sql(""" SELECT total_leaves FROM `tabLeave Allocation`
		where employee = %s  and leave_type = %s  and from_date <= %s  and to_date >= %s  """,
									  (employee,leave_type, from_date, to_date), as_dict=1)
	if leave_allocated:
		return str(leave_allocated[0].total_leaves)
	else:
		return 0

