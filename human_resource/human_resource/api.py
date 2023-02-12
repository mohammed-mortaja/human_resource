
from __future__ import unicode_literals
import frappe

@frappe.whitelist(allow_guest=True)
def test_api():
    return ("test")