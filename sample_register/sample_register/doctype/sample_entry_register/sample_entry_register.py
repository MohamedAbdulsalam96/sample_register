# -*- coding: utf-8 -*-
# Copyright (c) 2015, indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class SampleEntryRegister(Document):
	def validate(self):
		self.validate_container_id()

	def before_insert(self):
		if self.order_id:
			self.check_total_sample_count()

	def validate_container_id(self):
		container_id = []
		for d in self.get("container_details"):
			if d.container_id in container_id:
				frappe.msgprint("Duplicate container id '%s' is not allowed in container details table at row '%s'"%(d.container_id,d.idx),raise_exception=1)
			else:
				container_id.append(d.container_id)

	def check_total_sample_count(self):
		sample_count_allowed=frappe.db.sql("""select total_samples from `tabOrder Register` where name=%s""",(self.order_id),as_list=1)
		sample_count=frappe.db.sql("""select count(name) from `tabSample Entry Register` where order_id=%s""",(self.order_id),as_list=1)
		if sample_count >= sample_count_allowed:
			frappe.throw("Please increase Total Samples in Work Order "+ self.order_id+"<br>Currently sample collected in system: "+str(sample_count[0][0])) 
 # frappe.db.sql("""select name from `tabTest Name` where test_group='%s' order by name"""%(test_group), as_list=1)




@frappe.whitelist(allow_guest=True)
def status_updator(self, method):
	# frappe.msgprint("in save"+self.sample_id)
	if self.sample_id and (self.docstatus==0):
		# frappe.msgprint("in save"+self.sample_id)
		sample_entry_doc=frappe.get_doc("Sample Entry Register",self.sample_id)
		sample_entry_doc.job_card_status = "Created"
		sample_entry_doc.job_card=self.name
		sample_entry_doc.save()
	if self.sample_id and (self.docstatus==1):
		# frappe.msgprint("in submit"+self.sample_id)
		sample_entry_doc=frappe.get_doc("Sample Entry Register",self.sample_id)
		sample_entry_doc.job_card_status = "Submitted"
		sample_entry_doc.job_card=self.name
		sample_entry_doc.save()
	if self.sample_id and (self.docstatus==2):
		# frappe.msgprint("in submit"+self.sample_id)
		sample_entry_doc=frappe.get_doc("Sample Entry Register",self.sample_id)
		sample_entry_doc.job_card_status = "Cancelled"
		sample_entry_doc.job_card=self.name
		sample_entry_doc.save()
		# bill_list = frappe.db.sql("""select name from `tabPurchase Invoice` where bill_no=%s and docstatus =1 and is_recurring='0'""",
			# self.bill_no)

