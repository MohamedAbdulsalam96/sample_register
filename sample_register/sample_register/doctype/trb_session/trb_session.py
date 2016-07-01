# -*- coding: utf-8 -*-
# Copyright (c) 2015, indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import datetime,json

class TRBSession(Document):
	def get_details(self):
		# if (self.filter_based_on_date_of_receipt and (not self.from_date or not self.to_date)):
		# 	frappe.throw("Please select From Date and To Date")
		# if not self.order:
		# 	frappe.throw("Please select Order")
		# if not self.customer:
		# 	frappe.throw("Please select Customer")
		# if self.filter_based_on_date_of_receipt and self.from_date and self.to_date:
		# 	condition = "and date_of_receipt>='"+self.from_date+"' and date_of_receipt<='"+self.to_date+"'"
		# if self.show_job_card_created_entries:
		# 	condition +="and job_card_status!='Not Available'"
		# else:
		# 	condition +="and job_card_status='Not Available'"

		# dl = frappe.db.sql("""select name,customer,date_of_receipt, date_of_collection,job_card,functional_location,functional_location_code,
		# 	equipment,equipment_make,serial_number,equipment_code,
		# 	conservation_protection_system, sample_taken_from, oil_temperature, winding_temperature,
		# 	remarks from `tabSample Entry Register` where order_id='%s' %s"""%(self.order, condition),as_dict=1, debug=1)

		test_type = ["Water Content Test","Furan Content","Dissolved Gas Analysis"]
		dl_list = []
		for i in test_type:
			#get TRB with service request and TRB filter
			# dl = frappe.db.sql("""select name,job_card,final_result,result_status,sample_id, '{0}' as test_type 
			# 			from `tab{0}` where sample_id in 
			# 			(select name from `tabSample Entry Register` where order_id='{1}')""".format(i,self.order),as_dict=1, debug=1)
			dl = frappe.db.sql("""select name,job_card,final_result,result_status,sample_id, '{0}' as test_type, priority 
						from `tab{0}` order by priority""".format(i),as_dict=1, debug=1)
		
			#get TRB with Test Type filter
			if dl:
				dl_list.append(dl)

		print "\ndl_list",dl_list	

		self.set('trb_session_details', [])

		list_of_lists=dl_list
		print "dl_list",dl_list
		flattened = []
		for sublist in list_of_lists:
		    for val in sublist:
		        flattened.append(val)

		# for d in [d[0] for d in dl_list]:
		for d in flattened:
			if self.test_type:
				if d.test_type == self.test_type:
					nl = self.append('trb_session_details', {})
					nl.sample_id = d.sample_id
					nl.job_card = d.job_card
					nl.test_name = d.name
					nl.reported_ir = d.final_result
					nl.test_type = d.test_type
					nl.result_status = d.result_status
					nl.priority = d.priority
			else:
				nl = self.append('trb_session_details', {})
				nl.sample_id = d.sample_id
				nl.job_card = d.job_card
				nl.test_name = d.name
				nl.reported_ir = d.final_result
				nl.test_type = d.test_type
				nl.result_status = d.result_status

	def get_details_from_child_table(self):
		return {
		"get_items": self.get('trb_session_details')
		}


	def update_sample_entry(self):
		for d in self.get('trb_session_details'):
			entry_doc = frappe.get_doc(d.test_type, d.test_name)
			if entry_doc.docstatus == 0:
				entry_doc.result_status = d.result_status
				entry_doc.save()
		frappe.msgprint("TRB Status updated")

	def start_session(self,test_list):
		for d in self.get('trb_session_details'):
			if d.test_name in test_list:
				entry_doc = frappe.get_doc(d.test_type, d.test_name)
				if entry_doc.docstatus == 0:
					entry_doc.start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
					entry_doc.lab_equipment_details = []
					for de in self.get("lab_equipment_details"):
						test_req={
							"doctype": "Lab Equipment Details",
							"item_code": de.item_code,
							"fixed_asset_serial_number": de.fixed_asset_serial_number
						}
						entry_doc.append("lab_equipment_details",test_req)
			# 		entry_doc.result_status = d.result_status
					entry_doc.save()
		frappe.msgprint("TRB Session created and Lab Equipment Details updated")