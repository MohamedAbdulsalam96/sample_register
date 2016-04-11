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
									test = %s
							""", (self.job_card, self.test_group, self.test))

