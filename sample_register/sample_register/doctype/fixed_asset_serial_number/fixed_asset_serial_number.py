# -*- coding: utf-8 -*-
# Copyright (c) 2015, indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from datetime import datetime, timedelta

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

@frappe.whitelist()
def notify_user(doc_name, comment_doc):
	frappe.reload_doctype("Comment")
	comment_data = frappe.db.sql("""select comment_by_fullname, comment from `tabComment` where comment_docname = %s""",comment_doc, as_dict=1)
	subject = "Material Request Detils"
	message = """<p>Hello ,</p><p>Material Request No : %s </p><p>Details given below :</p>"""%(doc_name)
	for i in range(len(comment_data)):		
		message_row = """<p> %s : %s, </p>"""%(comment_data[i]['comment_by_fullname'], comment_data[i]['comment'])
		message = message + message_row   
	# print message
	# user_list = frappe.db.sql("""select parent from `tabUserRole` where role = '{0}'""".format('Purchase Manager'), as_dict=1)
	# print user_list		
	frappe.sendmail(recipients=frappe.session.user, subject=subject, message =message)
	
	return frappe.session.user


	