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
		if not self.order:
			frappe.throw("Please select Order")
		if not self.customer:
			frappe.throw("Please select Customer")

		condition = ""

		if self.filter_based_on_date_of_receipt and self.from_date and self.to_date:
			condition = "and date_of_receipt>='"+self.from_date+"' and date_of_receipt<='"+self.to_date+"'"
		if self.show_job_card_created_entries:
			condition +="and job_card_status!='Not Available'"
		else:
			condition +="and job_card_status='Not Available'"

		dl = frappe.db.sql("""select name,customer,date_of_receipt,job_card,functional_location,functional_location_code,
			equipment,equipment_make,serial_number,equipment_code,
			conservation_protection_system, sample_taken_from, oil_temperature, winding_temperature,
			remarks from `tabSample Entry Register` where order_id='%s' %s"""%(self.order, condition),as_dict=1, debug=1)

		self.set('sample_entry_creation_tool_details', [])

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
			nl.conservation_protection_system = d.conservation_protection_system
			nl.sample_taken_from = d.sample_taken_from
			nl.oil_temperature = d.oil_temperature
			nl.winding_temperature = d.winding_temperature
			nl.remarks = d.remarks

	def create_sample_entry(self):
		if not self.date_of_collection:
			frappe.throw("Please select Date of Collection")

		# sample_count_allowed=frappe.db.sql("""select total_samples from `tabOrder Register` where name=%s""",(self.order),as_list=1)
		# sample_count=frappe.db.sql("""select count(name) from `tabSample Entry Register` where order_id=%s""",(self.order),as_list=1)
		# s_create = sample_count[0][0]+self.number_of_sample
		# if s_create >= sample_count_allowed[0][0]:
		# 	frappe.msgprint("limit exceed")
		# if (sample_count_allowed[0][0] <= int(sample_count[0][0])):
		# 	frappe.msgprint(sample_count[0][0]+self.number_of_sample)
		# 	frappe.throw("Please increase Total Samples in Work Order "+ self.order+"<br>Currently sample collected in system: "+str(sample_count[0][0])) 

		for i in range(self.number_of_sample):
			doc_sample_entry=frappe.new_doc("Sample Entry Register")
			doc_sample_entry.customer = self.customer
			doc_sample_entry.order_id = self.order
			doc_sample_entry.date_of_receipt = self.date_of_receipt
			doc_sample_entry.technical_contact = self.technical_contact
			doc_sample_entry.type = self.type
			doc_sample_entry.date_of_collection = self.date_of_collection
			doc_sample_entry.weather_condition_during_sampling = self.weather_condition
			doc_sample_entry.drawn_by = self.drawn_by			
			doc_sample_entry.save()
			sample_link="<a href='desk#Form/Sample Entry Register/"+doc_sample_entry.name+"'>"+doc_sample_entry.name+" </a>"
			frappe.msgprint(sample_link+"created")

	def update_sample_entry(self):
		sample_fl = []
		container_detail = []

		#check duplicate combination for code designation, equipment and sample drawn
		code_designation_combination_check = []

		for d in self.get("sample_entry_creation_tool_details"):
			if d.functional_location and d.equipment and d.sample_taken_from:
				if (d.functional_location+d.equipment+d.sample_taken_from) in code_designation_combination_check:
					frappe.msgprint("Duplicate Code Designation Combination <br> '%s' is not allowed at row '%s'"%((d.functional_location+"-"+d.equipment+ "-"+d.sample_taken_from),d.idx),raise_exception=1)
				else:
					code_designation_combination_check.append(d.functional_location+d.equipment+d.sample_taken_from)

		for d in self.get('sample_entry_creation_tool_details'):
				sample_entry_doc=frappe.get_doc("Sample Entry Register", d.sample_id)
				if sample_entry_doc.docstatus == 0: 
					sample_entry_doc.functional_location = d.functional_location
					sample_entry_doc.functional_location_code = d.functional_location_code
					sample_entry_doc.equipment = d.equipment
					sample_entry_doc.equipment_make = d.equipment_make
					sample_entry_doc.serial_number = d.serial_number
					sample_entry_doc.equipment_code = d.equipment_code
					sample_entry_doc.date_of_receipt = d.date_of_receipt
					sample_entry_doc.conservation_protection_system = d.conservation_protection_system
					sample_entry_doc.sample_taken_from = d.sample_taken_from
					sample_entry_doc.oil_temperature = d.oil_temperature
					sample_entry_doc.winding_temperature = d.winding_temperature
					sample_entry_doc.remarks = d.remarks
					if d.container_type_i and d.container_id_i:
						del sample_entry_doc.container_details[:]
						container_detail = {
								"doctype": "Container Details",
								"container_type": d.container_type_i,
								"container_id":d.container_id_i
								}
						sample_entry_doc.append("container_details", container_detail)
						if d.container_type_ii and d.container_id_ii:
							container_detail = {
									"doctype": "Container Details",
									"container_type": d.container_type_ii,
									"container_id":d.container_id_ii
									}
							sample_entry_doc.append("container_details", container_detail)
						if d.container_type_iii and d.container_id_iii:
							container_detail = {
									"doctype": "Container Details",
									"container_type": d.container_type_iii,
									"container_id":d.container_id_iii
									}
							sample_entry_doc.append("container_details", container_detail)
					sample_entry_doc.save()
		frappe.msgprint("Sample Entry updated")

		# if d.functional_location:
		# 	frappe.db.sql("""update `tabSample Entry Register` set functional_location = %s, modified = %s, functional_location_code= %s
		# 	 	where name=%s and docstatus!=1""", (d.functional_location, now_datetime(), d.functional_location_code, d.sample_id))
		# 	sample_fl.append(d.sample_id)

		# if sample_fl:
		# 	msgprint("Functional Focation updated in: {0}".format(", ".join(sample_fl)))