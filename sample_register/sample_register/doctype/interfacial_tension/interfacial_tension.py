# -*- coding: utf-8 -*-
# Copyright (c) 2015, indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import datetime
from sample_register.sample_register.trb_common import check_bottle_no

class InterfacialTension(Document):
	def validate(self):
		self.calculate_interfacial_tension()
		self.set_job_card_status()
		check_bottle_no(self.bottle_number,self.sample_id)

	def on_submit(self):
		self.set_job_card_status()
		if self.result_status == "Reject":
			current_trb = frappe.get_doc(self.doctype, self.name)
			new_trb = frappe.copy_doc(current_trb, ignore_no_copy=False)
			new_trb.remarks = " created from "+self.name
			new_trb.result_status = ""
			new_trb.trb_batch = ""
			new_trb.save()
		self.end_time = datetime.datetime.now()
		
	def calculate_interfacial_tension(self):
		import math
		ir=0
		ir_count=0
		for row in self.test_details:
			if row.test__result_status == "Accept":
				ir = ir+ row.ir_of_water
				ir_count = ir_count + 1
		if ir_count!=0:
			ir = float(ir/float(ir_count))
		if ir_count!=0:
			density_of_oil = self.density_of_oil * (1 + 0.00065 * (self.temp_of_oil - 27))
			factor = 0.725 +  math.sqrt( (0.01452*(10**5)*(ir/1000))/ ( self.circumference_of_ring\
			 				* self.circumference_of_ring * (self.density_of_water-self.density_of_oil*27) ) +\
			 				 0.04534 - (float(1.679)/float(self.radius_ratio)) )
			interfacial_tension = (ir*factor)/float(1000)
			self.interfacial_tension = interfacial_tension
			print "\n\ninterfacial_tension", interfacial_tension

	def set_job_card_status(self):
		if not self.result_status:
			frappe.throw("Please Enter status")
		if self.result_status and (self.result_status == "Accept" or self.result_status == "Reject" or self.result_status == "Select"):
			cond = """select name from `tabJob Card Creation Test Details` where parent = '%s'"""%(self.job_card)
			if self.test_group:
				cond += """ and test_group = '%s'"""%(self.test_group)
			if self.item_code:
				cond += """ and item_code = '%s'"""%(self.item_code)
			if self.item_name:
				cond += """ and item_name = '%s'"""%(self.item_name)
	
			job_card_details = frappe.db.sql(cond, as_dict=1)
			jc_name = job_card_details[0]['name']

			update_query = ("""
								update 
									`tabJob Card Creation Test Details` 
								set 
									status = '{0}', test_name = '{1}'
								where 
									name = '{2}'
							""".format(self.result_status,self.name,jc_name))
			frappe.db.sql(update_query)
		
		job_card = frappe.get_doc("Job Card Creation", self.job_card)
		status = True
		for test in job_card.test_details:
			if test.status != "Accept":
				status = False
		if status == True:
			frappe.db.set_value("Job Card Creation", self.job_card, "status", "Accept")
			frappe.db.set_value("Sample Entry Register", self.sample_id, "job_card_trb_status", "Accept")
