# -*- coding: utf-8 -*-
# Copyright (c) 2015, indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import flt, getdate, nowdate, now_datetime
from frappe import msgprint, _
from frappe.utils import flt, getdate, nowdate
from datetime import date

class SampleEntryCreationTool(Document):
	def get_details(self):
		if (self.filter_based_on_date_of_receipt and (not self.from_date or not self.to_date)):
			frappe.throw("Please select From Date and To Date")

		condition = ""

		if self.filter_based_on_date_of_receipt and self.from_date and self.to_date:
			condition = "and date_of_receipt>='"+self.from_date+"' and date_of_receipt<='"+self.to_date+"'"
		if self.show_job_card_created_entries:
			condition +="and job_card_status!='Not Available'"
		else:
			condition +="and job_card_status='Not Available'"

		dl = frappe.db.sql("""select name,customer,date_of_receipt,job_card,functional_location,functional_location_code,
			equipment,equipment_make,serial_number,equipment_code from `tabSample Entry Register` where order_id='%s' %s"""%(self.order, condition),as_dict=1, debug=1)

		self.set('sample_entry_creation_tool_details', [])
		# for d in dl:
		# 	sample_details={
		# 		"doctype": "Sample Entry Creation Tool Details",
		# 		"sample_id": d.name,
		# 		"customer": d.customer
		# 	}
		# 	self.append("sample_entry_creation_tool_details",sample_details)
		for d in dl:
			nl = self.append('sample_entry_creation_tool_details', {})
			nl.sample_id = d.name
			nl.customer = d.customer
			nl.job_card = d.job_card
			nl.functional_location=d.functional_location
			nl.functional_location_code = d.functional_location_code
			nl.equipment = d.equipment
			nl.equipment_make = d.equipment_make
			nl.serial_number =d.serial_number
			nl.equipment_code =d.equipment_code
			nl.date_of_receipt = d.date_of_receipt

	def create_sample_entry(self):
		if not self.date_of_receipt:
			frappe.throw("Please select Date of Receipt")

		for i in range(self.number_of_sample):
			doc_sample_entry=frappe.new_doc("Sample Entry Register")
			doc_sample_entry.customer = self.customer
			doc_sample_entry.order_id = self.order
			doc_sample_entry.date_of_receipt = self.date_of_receipt
			doc_sample_entry.technical_contact = self.technical_contact
			doc_sample_entry.type = self.type
			doc_sample_entry.conservation_protection_system = self.conservation_protection_system
			doc_sample_entry.save()
			sample_link="<a href='desk#Form/Sample Entry Register/"+doc_sample_entry.name+"'>"+doc_sample_entry.name+" </a>"
			frappe.msgprint(sample_link+"created")

	def update_sample_entry(self):
		sample_fl = []
		sample_equipment =[]
		sample_date_of_receipt = []
		for d in self.get('sample_entry_creation_tool_details'):
			if d.functional_location:
				# frappe.db.set_value("Sample Entry Register", d.sample_id, "functional_location:", d.functional_location)
				frappe.db.sql("""update `tabSample Entry Register` set functional_location = %s, modified = %s, functional_location_code= %s
				 	where name=%s and docstatus!=1""", (d.functional_location, now_datetime(), d.functional_location_code, d.sample_id))
				sample_fl.append(d.sample_id)
			if d.equipment:
				# frappe.db.set_value("Sample Entry Register", d.sample_id, "functional_location:", d.functional_location)
				frappe.db.sql("""update `tabSample Entry Register` set equipment = %s, equipment_make =%s,
					serial_number = %s, equipment_code = %s, modified = %s
				 	where name=%s and docstatus!=1""", (d.equipment, d.equipment_make , d.serial_number, d.equipment_code, now_datetime(), d.sample_id))
				sample_equipment.append(d.sample_id)
			if d.date_of_receipt:
				# frappe.db.set_value("Sample Entry Register", d.sample_id, "functional_location:", d.functional_location)
				frappe.db.sql("""update `tabSample Entry Register` set date_of_receipt = %s, modified = %s
				 	where name=%s and docstatus!=1""", (d.date_of_receipt, now_datetime(), d.sample_id))
				sample_date_of_receipt.append(d.sample_id)

		if sample_fl:
			msgprint("Functional Focation updated in: {0}".format(", ".join(sample_fl)))
		if sample_equipment:
			msgprint("Equipment updated in: {0}".format(", ".join(sample_equipment)))
		if sample_date_of_receipt:
			msgprint("Date of Receipt updated.")
		else:
			msgprint(_("Functional Location not mentioned"))



		# for d in self.get('sample_entry_creation_tool_details'):
		# 	if d.functional_location:
		# 		if d.functional_location and getdate(d.clearance_date) < getdate(d.cheque_date):
		# 			frappe.throw(_("Clearance date cannot be before check date in row {0}").format(d.idx))

		# 		frappe.db.set_value("Journal Voucher", d.voucher_id, "clearance_date", d.clearance_date)
		# 		frappe.db.sql("""update `tabJournal Voucher` set clearance_date = %s, modified = %s
		# 			where name=%s""", (d.clearance_date, nowdate(), d.voucher_id))
		# 		vouchers.append(d.voucher_id)

		# if vouchers:
		# 	msgprint("Clearance Date updated in: {0}".format(", ".join(vouchers)))
		# else:
		# 	msgprint(_("Clearance Date not mentioned"))

		# if not (self.clearance_date):
		# 	msgprint("Clearance Date is Mandatory"
		# 	return

		# condition = ""


		# dl = frappe.db.sql("""select t1.name, t1.cheque_no, t1.cheque_date, t2.debit,
		# 		t2.credit, t1.posting_date, t2.against_account, t1.clearance_date
		# 	from
		# 		`tabJournal Voucher` t1, `tabJournal Voucher Detail` t2
		# 	where
		# 		t2.parent = t1.name and t2.account = %s
		# 		and t1.clearance_date= %s and t1.docstatus=1
		# 		and ifnull(t1.is_opening, 'No') = 'No' %s order by t1.posting_date, t1.cheque_no""" %
		# 		('%s', '%s', condition), (self.bank_account, self.clearance_date), as_dict=1)

		# self.set('entries', [])
		# self.total_amount = 0.0
		# self.total_reconciled_credit = 0.0
		# self.total_reconciled_debit = 0.0

		# for d in dl:
		# 	nl = self.append('entries', {})
		# 	nl.posting_date = d.posting_date
		# 	nl.voucher_id = d.name
		# 	nl.cheque_number = d.cheque_no
		# 	nl.cheque_date = d.cheque_date
		# 	nl.debit = d.debit
		# 	nl.credit = d.credit
		# 	nl.against_account = d.against_account
		# 	nl.clearance_date = d.clearance_date
		# 	self.total_amount += flt(d.debit) - flt(d.credit)

  #                       if d.clearance_date: 
  #                       	self.total_reconciled_debit += flt(d.debit)
  #                       	self.total_reconciled_credit += flt(d.credit)
