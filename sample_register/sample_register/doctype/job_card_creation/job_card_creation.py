# -*- coding: utf-8 -*-
# Copyright (c) 2015, indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc


class JobCardCreation(Document):
	def validate(self):
		self.check_sample_status_if_sample_id_changed()

	def before_insert(self):
		self.check_sample_status()

	def on_submit(self):
		for r in self.test_details:
			doc_test_book=frappe.new_doc("Test Book")
			doc_test_book.job_card = self.name
			doc_test_book.sample_id = self.sample_id
			doc_test_book.customer = self.customer
			doc_test_book.type = self.type
			doc_test_book.priority = self.priority
			doc_test_book.standards = self.standards
			doc_test_book.test = r.test
			doc_test_book.test_group = r.test_group
			doc_test_book.save()
			test_book_link="<a href='desk#Form/Test Book/"+doc_test_book.name+"'>"+doc_test_book.name+" </a>"
			job_link="<a href='desk#Form/Job Card Creation/"+doc_test_book.job_card+"'>"+doc_test_book.job_card+" </a>"
			frappe.msgprint("For Job Card "+job_link+", Test Book "+test_book_link+ " created for Test "+ r.test)

	def check_sample_status(self):
		if self.sample_id and (self.docstatus==0):
			sample_entry_doc=frappe.get_doc("Sample Entry Register",self.sample_id)
			if(sample_entry_doc.job_card_status == "Created"):
				frappe.throw("Job Card "+sample_entry_doc.job_card +" is allready Created for "+self.sample_id)
			if(sample_entry_doc.job_card_status == "Submitted"):
				frappe.throw("Job Card "+sample_entry_doc.job_card +" is allready Submitted for "+self.sample_id)

	def check_sample_status_if_sample_id_changed(self):
		if self.sample_id and (self.docstatus==0):
			sample_entry_doc=frappe.get_doc("Sample Entry Register",self.sample_id)
			if(self.name!=sample_entry_doc.job_card):
				if(sample_entry_doc.job_card_status == "Created"):
					frappe.throw("Job Card "+sample_entry_doc.job_card +" is allready Created for "+self.sample_id)
				if(sample_entry_doc.job_card_status == "Submitted"):
					frappe.throw("Job Card "+sample_entry_doc.job_card +" is allready Submitted for "+self.sample_id)