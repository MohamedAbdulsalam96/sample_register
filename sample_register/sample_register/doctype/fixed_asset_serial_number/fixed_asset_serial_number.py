# -*- coding: utf-8 -*-
# Copyright (c) 2015, indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname

class FixedAssetSerialNumber(Document):
	def autoname(self):
		if self.fixed_asset_serial_number:	
			self.name = make_autoname(self.fixed_asset_serial_number+'.###')
		else:
			self.name = make_autoname('Asset'+'.###')

@frappe.whitelist()
def make_new_asset(doc, method):
	if doc.purpose == "Material Receipt":
		for i, ele in enumerate (doc.items):
			item  = frappe.get_doc("Item", ele.item_code)
			if item.fixed_asset_serial_number and item.is_asset_item:
				for qty in range(int(ele.qty)):
					asset_doc = frappe.new_doc("Fixed Asset Serial Number")
					asset_doc.item_code = item.item_code
					asset_doc.fixed_asset_serial_number = item.fixed_asset_serial_number
					asset_doc.save(ignore_permissions=True)

@frappe.whitelist()
def new_fixed_asset(doc, method):
	if doc.items:
		for i, ele in enumerate (doc.items):
			item  = frappe.get_doc("Item", ele.item_code)
			if item.fixed_asset_serial_number and item.is_asset_item:
				for qty in range(int(ele.qty)):
					asset_doc = frappe.new_doc("Fixed Asset Serial Number")
					asset_doc.item_code = item.item_code
					asset_doc.fixed_asset_serial_number = item.fixed_asset_serial_number
					asset_doc.save(ignore_permissions=True)





