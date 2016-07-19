# -*- coding: utf-8 -*-
# Copyright (c) 2015, indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class TRBSessionBatch(Document):
	def get_details(self):
		test_type = ["Water Content Test","Furan Content","Dissolved Gas Analysis"]
		dl_list = []
		for i in test_type:
			#get TRB with service request and TRB filter
			# dl = frappe.db.sql("""select name,job_card,final_result,result_status,sample_id, '{0}' as test_type 
			# 			from `tab{0}` where sample_id in 
			# 			(select name from `tabSample Entry Register` where order_id='{1}')""".format(i,self.order),as_dict=1, debug=1)
			dl = frappe.db.sql("""select name,job_card,final_result,result_status,sample_id, '{0}' as test_type, priority 
						from `tab{0}` where docstatus = 0 and trb_batch is null order by priority""".format(i),as_dict=1, debug=1)
		
			#get TRB with Test Type filter
			if dl:
				dl_list.append(dl)

		print "\ndl_list",dl_list	

		self.set('trb_session_details', [])

		list_of_lists=dl_list
		# print "dl_list",dl_list
		flattened = []
		for sublist in list_of_lists:
		    for val in sublist:
		        flattened.append(val)

		# for d in [d[0] for d in dl_list]:
		for d in flattened:
			nl = self.append('trb_session_details', {})
			nl.sample_id = d.sample_id
			nl.job_card = d.job_card
			nl.test_name = d.name
			nl.reported_ir = d.final_result
			nl.test_type = d.test_type
			nl.result_status = d.result_status
			nl.priority = d.priority




	def get_batch_entries(self):
		test_type = ["Water Content Test","Furan Content","Dissolved Gas Analysis"]
		dl_list = []
		for i in test_type:
			dl = frappe.db.sql("""select name,job_card,final_result,result_status,sample_id, '{0}' as test_type, priority 
						from `tab{0}` where docstatus = 0 and trb_batch = '{1}' order by priority""".format(i, self.trb_batch),as_dict=1, debug=1)
		
			if dl:
				dl_list.append(dl)

		self.set('trb_session_details', [])

		list_of_lists=dl_list
		flattened = []
		for sublist in list_of_lists:
		    for val in sublist:
		        flattened.append(val)

		for d in flattened:
			if self.trb_batch:
				nl = self.append('trb_session_details', {})
				nl.sample_id = d.sample_id
				nl.job_card = d.job_card
				nl.test_name = d.name
				nl.reported_ir = d.final_result
				nl.test_type = d.test_type
				nl.result_status = d.result_status
				nl.priority = d.priority
		
		for d in self.get('trb_session_details'):
			print d.test_type
			print d.test_name
			dl = frappe.db.sql("""select start_time,tested_by 
				from `tab{0}` where name = '{1}'""".format(d.test_type,d.test_name),as_dict=1, debug=1)
			print dl[0]["start_time"]
			self.start_time = dl[0]["start_time"]
			self.tested_by = dl[0]["tested_by"]

			dl = frappe.db.sql("""select item_code,fixed_asset_serial_number,item_name,calibration_status,next_calibration_date
				   	from `tabLab Equipment Details` where parent = '{0}'""".format(d.test_name),as_dict=1, debug=1)
			print "lab",dl
		self.set('lab_equipment_details', [])

		for d in dl:
			print d
			nl = self.append('lab_equipment_details', {})
			print "item_code",nl.item_code
			nl.item_code = d.item_code
			nl.item_name = d.item_name
			nl.fixed_asset_serial_number = d.fixed_asset_serial_number
			nl.calibration_status = d.calibration_status	

	def get_details_from_child_table(self):
		get_items = []
		X2 = []
		for d in self.get('trb_session_details'):
			print d.test_name
			print d.sample_id
			print d.test_type
			X1=[d.test_name,d.sample_id,d.test_type, d.priority]
			get_items.append(X1)

		return {
		"get_items": get_items
		}


	def update_sample_entry(self):
		for d in self.get('trb_session_details'):
			entry_doc = frappe.get_doc(d.test_type, d.test_name)
			if entry_doc.docstatus == 0:
				entry_doc.result_status = d.result_status
				entry_doc.save()
		frappe.msgprint("TRB Status updated")

	def start_session(self,test_list):
		trb_batch = frappe.new_doc("TRB Batch")
		trb_batch.owner = frappe.session.user
		trb_batch.test_type = self.test_type
		trb_batch.save()
		trb_batch_name = trb_batch.name
		print "\n\ntrb batch",trb_batch.name
		print "\n\ntrb_batch_name",trb_batch_name
		for d in self.get('trb_session_details'):
			if d.test_name in test_list:
				entry_doc = frappe.get_doc(d.test_type, d.test_name)
				if entry_doc.docstatus == 0:
					entry_doc.start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
					entry_doc.trb_batch = trb_batch.name
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
		frappe.msgprint("TRB Session created and Lab Equipment Details updated and assigned \nBatch: "+trb_batch_name)