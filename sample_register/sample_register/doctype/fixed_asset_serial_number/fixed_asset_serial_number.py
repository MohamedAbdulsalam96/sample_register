# -*- coding: utf-8 -*-
# Copyright (c) 2015, indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from datetime import datetime, timedelta
from frappe import throw, _

class FixedAssetSerialNumber(Document):
	def autoname(self):
		if self.fixed_asset_serial_number:	
			self.name = make_autoname('TF-'+'.###')

@frappe.whitelist()
def make_new_asset(doc, method):
	if doc.purpose == "Material Receipt":
		fixed_asset = [] 
		for i, ele in enumerate (doc.items):
			item  = frappe.get_doc("Item", ele.item_code)
			if item.fixed_asset_serial_number and item.is_asset_item:
				for qty in range(int(ele.qty)):
					asset_doc = frappe.new_doc("Fixed Asset Serial Number")
					asset_doc.item_code = item.item_code
					asset_doc.fixed_asset_serial_number = item.fixed_asset_serial_number
					asset_doc.save(ignore_permissions=True)
					fixed_asset.append(asset_doc.name)
				frappe.msgprint(_("Fixed Asset Serial Number Created"))
				for i in fixed_asset: frappe.msgprint(_(i))

@frappe.whitelist()
def new_fixed_asset(doc, method):
	if doc.items:
		for i, ele in enumerate (doc.items):
			item  = frappe.get_doc("Item", ele.item_code)
			if item.fixed_asset_serial_number and item.is_asset_item:
				fixed_asset = [] 
				for qty in range(int(ele.qty)):
					asset_doc = frappe.new_doc("Fixed Asset Serial Number")
					asset_doc.item_code = item.item_code
					asset_doc.fixed_asset_serial_number = item.fixed_asset_serial_number
					asset_doc.save(ignore_permissions=True)
					fixed_asset.append(asset_doc.name)
				frappe.msgprint(_("Fixed Asset Serial Number Created"))
				for i in fixed_asset: frappe.msgprint(_(i))

		for d in doc.get('items'):		 #Enter inspection date for all items that require inspection
			if frappe.db.get_value("Item", d.item_code, "inspection_required") and not d.qa_no:
				frappe.throw(_("Quality Inspection required for Item {0}").format(d.item_code))
			elif d.qa_no:
				quality_inspection = frappe.get_doc("Quality Inspection", d.qa_no)
				if quality_inspection.docstatus != 1:
					frappe.throw(_("Quality Inspection not Submitted"))

# @frappe.whitelist()
# def material_reject_mail(doc_name, owner):
# 	frappe.reload_doctype("Comment")
# 	comment_data = frappe.db.sql("""select comment_by_fullname, comment from `tabComment` where comment_docname = %s""",doc_name, as_dict=1)
# 	subject = "Material Request Detils"
# 	message = """<p>Hello ,</p><p>Material Request No : %s </p><p>Details given below :</p>"""%(doc_name)
# 	for i in range(len(comment_data)):		
# 		message_row = """<p> %s : %s, </p>"""%(comment_data[i]['comment_by_fullname'], comment_data[i]['comment'])
# 		message = message + message_row   
# 	frappe.sendmail(recipients=owner, subject=subject, message =message)
	
# 	return frappe.session.user

# @frappe.whitelist()
# def material_request_mail(doc_name, owner):

# 	subject = "Material Request"
# 	message = """<p>Hello ,</p><p>Material Request  : %s </p>
# 	<p>owner : %s </p>
# 	<p>Send for Approval By : %s </p>"""%(doc_name, owner, frappe.session.user)

# 	purchase_manager = frappe.db.sql("""select t1.email from `tabUser` t1 join `tabUserRole` t2  on t2.parent = t1.name and t2.role = 'Purchase Manager';""", as_list=1)
# 	for manager in purchase_manager:
# 		print manager[0]
# 		frappe.sendmail(recipients=manager[0], subject=subject, message =message)	


@frappe.whitelist()
def trufil_id(doc, method):
	if not doc.trufil_id:	
		doc.trufil_id = make_autoname('.####')
	else:
		doc.trufil_id = doc.trufil_id

@frappe.whitelist()
def create_todo(item_code, reference_name, owner):
	todo = frappe.new_doc("ToDo")
	todo.description = item_code
	todo.reference_type = "Fixed Asset Serial Number"
	todo.reference_name = reference_name
	todo.owner = owner
	todo.save(ignore_permissions=True)

