# -*- coding: utf-8 -*-
# Copyright (c) 2015, indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class TRBBatch(Document):
	def validate(self):
		# frappe.msgprint("TRB Batch {0} updated".format(self.name))
		if self.test_type:
			test_count = frappe.db.sql("""select count(name) as test_count from `tab{0}` where trb_batch='{1}' and docstatus=0""".format(self.test_type,self.name), as_dict=1,debug=1)
			# print "\n\ncount",test_count
			test_count = test_count[0]["test_count"]
			self.open_test = test_count
			if test_count == 0:
				self.status = "Close"
			else:
				self.status = "Open"

	def after_insert(self):
		if self.test_type:
			test_count = frappe.db.sql("""select count(name) as test_count from `tab{0}` where trb_batch='{1}' and docstatus=0""".format(self.test_type,self.name), as_dict=1,debug=1)
			# print "\n\ncount",test_count
			test_count = test_count[0]["test_count"]
			self.open_test = test_count
			if test_count == 0:
				self.status = "Close"
			else:
				self.status = "Open"