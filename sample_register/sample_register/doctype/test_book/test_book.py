# -*- coding: utf-8 -*-
# Copyright (c) 2015, indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class TestBook(Document):
	def on_submit(self):
		if self.status and self.status == "Completed":
			frappe.db.sql(	"""
								update 
									`tabJob Card Creation Test Details` 
								set 
									status = "Closed" 
								where 
									parent = %s 
								and 
									test_group = %s
								and 
									item_code = %s
							""", (self.job_card, self.test_group, self.item_code))
		
		job_card = frappe.get_doc("Job Card Creation", self.job_card)
		status = True
		for test in job_card.test_details:
			if test.status != "Closed":
				status = False
		if status == True:
			frappe.db.set_value("Job Card Creation", self.job_card, "status", "Closed")


