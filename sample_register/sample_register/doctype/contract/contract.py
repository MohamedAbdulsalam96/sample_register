# -*- coding: utf-8 -*-
# Copyright (c) 2015, indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cstr, cint
from frappe import msgprint, _

class Contract(Document):
	pass

@frappe.whitelist()
def make_work_order(source_name, target_doc=None):
	def set_missing_values(source, target):
			work_order = frappe.get_doc(target)

	doclist = get_mapped_doc("Contract", source_name, {
		"Contract": {
			"doctype": "Order Register",
			"field_map": {
				# "name": "enq_no",
			}
		},
	}, target_doc, set_missing_values)

	return doclist