# -*- coding: utf-8 -*-
# Copyright (c) 2015, indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, getdate, nowdate,now_datetime
from frappe.model.naming import make_autoname
from datetime import datetime

class ServiceRequest(Document):
	def validate(self):
		if self.order_date and self.contract:
			contract_doc=frappe.get_doc("Contract",self.contract)
			if getdate(self.order_date) < getdate(contract_doc.contract_start_date):
				frappe.throw("Service Request Date < Contract Start Date")

		if self.sr_ref_date and self.sales_order:
			so_date_unicode = frappe.db.get_value("Sales Order", self.sales_order, "order_end_date")
			if so_date_unicode:
				so_date = datetime.strptime(str(so_date_unicode), '%Y-%m-%d')
				if so_date < datetime.strptime(str(self.sr_ref_date), '%Y-%m-%d') and so_date:
					frappe.throw("Service Request Ref Date should be less than Sales Order End Date")

	def check_contract_value(self):
		contract_value_unicode = frappe.db.get_value("Sales Order", self.sales_order, "contract_value")
		if contract_value_unicode and self.sales_order:
			existing_sample_qty = frappe.db.sql("""
												select 
													sum(total_samples)
												from 
													`tabService Request` 
												where 
													sales_order = '%s'
												and 
													docstatus = 1
												and
													name <> '%s'
											"""%(self.sales_order, self.name), as_list=1)
			print flt(existing_sample_qty[0][0]),"existing_sample_qty"
			print contract_qty_unicode,"contract_qty_unicode"
			if flt(existing_sample_qty) > flt(contract_qty_unicode):
				frappe.throw("Total Samples Ordered should be less than equal to Contract Qty")


	def check_contract_qty(self):
		contract_qty_unicode = frappe.db.get_value("Sales Order", self.sales_order, "contract_quantities")
		if contract_qty_unicode and self.sales_order:
			existing_sample_qty = frappe.db.sql("""
												select 
													sum(total_samples)
												from 
													`tabService Request` 
												where 
													sales_order = '%s'
												and 
													docstatus = 1
												and
													name <> '%s'
											"""%(self.sales_order, self.name), as_list=1)
			if flt(existing_sample_qty) > flt(contract_qty_unicode):
				frappe.throw("Total Samples Ordered should be less than equal to Contract Qty")

	def check_contract_value(self):
		contract_value_unicode = frappe.db.get_value("Sales Order", self.sales_order, "contract_value")
		if contract_value_unicode and self.sales_order:
			existing_wo_value = frappe.db.sql("""
												select 
													sum(work_order_value)
												from 
													`tabService Request` 
												where 
													sales_order = '%s'
												and 
													docstatus = 1
												and
													name <> '%s'
											"""%(self.sales_order, self.name), as_list=1)
			if flt(existing_wo_value[0][0]) > flt(contract_value_unicode):
				frappe.throw("Total Service Request Value should be less than equal to Contract Value in Sales Order")


	def autoname(self):
		year = int(now_datetime().strftime("%Y"))
		self.name = make_autoname("TF-SR-"+str(year)+"-"+'.#####')

	def before_submit(self):
		self.check_contract_value()

	def on_submit(self):
		self.check_total_samples()
		self.sales_order_ref()
		self.check_contract_qty()
		self.check_contract_value()
		self.reload()

	def sales_order_ref(self):
		user = str(frappe.session['user'])
		user_role =  frappe.get_roles(user)
		assign_to = frappe.db.sql("""select owner from `tabToDo` where reference_name = '%s' """%(self.name))
		if (not self.sales_order) and (not assign_to):
			frappe.throw("Sales Order reference is not given please assign to someone");
		if (not self.approved_status == "Approved") and (not "Sales Manager" in user_role):
			frappe.throw("Only Sales Manager can Approved and submit this");
		else:
			pass

	def check_total_samples(self):
		so_total_qty =	frappe.db.sql("""
							select 
								sum(soi.rate) as sum_of_rate, 
								so.total_qty as so_qty
							from 
								`tabSales Order Item` soi, 
								`tabSales Order` so 
							where 
								soi.parent = so.name 
							and 
								so.name = '%s' 
						"""%(self.sales_order), as_dict=1)
		
		existing_sample_qty = frappe.db.sql("""
												select 
													sum(total_samples)
												from 
													`tabService Request` 
												where 
													sales_order = '%s'
												and 
													docstatus = 1
												and
													name <> '%s'
											"""%(self.sales_order, self.name), as_list=1)
		if self.sales_order and so_total_qty[0]['so_qty']:
			so_qty = flt(so_total_qty[0]['so_qty'])
			existing_qty = flt(existing_sample_qty[0][0])
			
			if so_qty < (existing_qty + self.total_samples):
				frappe.throw("Total Samples exceed's than {0}'s Total Qty".format(self.sales_order))
			else:
				sum_of_rate = so_total_qty[0]['sum_of_rate']
				frappe.db.set_value("Sales Order", self.sales_order, "actual_quantity", (existing_qty + self.total_samples))
				frappe.db.set_value("Sales Order", self.sales_order, "actual_order_value", ((existing_qty + self.total_samples) * sum_of_rate))
				frappe.db.set_value("Service Request", self.name, "work_order_value", ((self.total_samples) * sum_of_rate))	

			if (so_qty) == (existing_qty + self.total_samples):
				frappe.db.set_value("Sales Order", self.sales_order, "so_status", "Closed")
			else:
				frappe.db.set_value("Sales Order", self.sales_order, "so_status", "In Progress")



#Getting contact details after selecting contact name
@frappe.whitelist()
def get_contact_details(contact):
	contact = frappe.get_doc("Contact", contact)
	out = {
		"contact_person": contact.get("name") or " ",
		"contact_display": " ".join(filter(None,
			[contact.get("first_name"), contact.get("last_name")])) or " ",
		"contact_email": contact.get("email_id") or " ",
		"contact_mobile": contact.get("mobile_no")or " ",
		"contact_phone": contact.get("phone") or " ",
		"contact_designation": contact.get("designation") or " ",
		"contact_department": contact.get("department") or " ",
		"contact_personal_email" : contact.get("personal_email") or " "
	}
	return out

@frappe.whitelist()
def get_total_sample(sales_order):
	qty_query =	"""
					select
						total_qty
					from
						`tabSales Order`
					where
						name = '%s'
				"""%(sales_order)
	query = """
				select
					ifnull(sum(total_samples), 0)
				from
					`tabService Request`
				where
					sales_order = '%s'
			"""%(sales_order)
	so_total_qty = frappe.db.sql(qty_query, as_list=1)
	existing_sample_qty = frappe.db.sql(query, as_list=1)
	if so_total_qty and existing_sample_qty:
		return (flt(so_total_qty[0][0]) - existing_sample_qty[0][0])

@frappe.whitelist()
def create_sample_entry(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.customer = source.customer
		target.order_id = source.name
		

	doclist = get_mapped_doc("Service Request", source_name, {
			"Service Request": {
				"doctype": "Sample Entry Register",
				"validation": {
					"docstatus": ["=", 1]
				}
			}
		}, target_doc, set_missing_values, ignore_permissions=False)
	return doclist
