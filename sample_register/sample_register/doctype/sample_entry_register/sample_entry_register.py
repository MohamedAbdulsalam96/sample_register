# -*- coding: utf-8 -*-
# Copyright (c) 2015, indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class SampleEntryRegister(Document):
	def validate(self):
		self.validate_container_id()

	def validate_container_id(self):
		container_id = []
		for d in self.get("container_details"):
			if d.container_id in container_id:
				frappe.msgprint("Duplicate container id entry is not allowed",raise_exception=1)
			else:
				container_id.append(d.container_id)
