# -*- coding: utf-8 -*-
# Copyright (c) 2015, indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class TestBook(Document):
	def on_submit(self):
		if not self.status:
			frappe.throw("Please Enter status")
		if self.status and self.status == "Completed":
			cond = """select name from `tabJob Card Creation Test Details` where parent = '%s'"""%(self.job_card)
			if self.test_group:
				cond += """ and test_group = '%s'"""%(self.test_group)
			if self.item_code:
				cond += """ and item_code = '%s'"""%(self.item_code)
			if self.item_name:
				cond += """ and item_name = '%s'"""%(self.item_name)
	
			job_card_details = frappe.db.sql(cond, as_dict=1)
			jc_name = job_card_details[0]['name']

			update_query = """
								update 
									`tabJob Card Creation Test Details` 
								set 
									status = "Closed" 
								where 
									name = %s
							"""
			frappe.db.sql(update_query, (jc_name ))
		
		job_card = frappe.get_doc("Job Card Creation", self.job_card)
		status = True
		for test in job_card.test_details:
			if test.status != "Closed":
				status = False
		if status == True:
			frappe.db.set_value("Job Card Creation", self.job_card, "status", "Closed")


