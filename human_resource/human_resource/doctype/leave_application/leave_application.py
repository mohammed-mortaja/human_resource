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

		def on_submit(self):
			# Update leave allocation total leaves
			leave_allocation = frappe.get_doc("Leave Allocation", {"employee": self.employee})
			leave_allocation.total_leaves -= self.total_leaves
			leave_allocation.save()
