# -*- coding: utf-8 -*-
# Copyright (c) 2015, indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class TestCertificate(Document):
	def get_test_details(self):
		# dl2 = frappe.db.sql("""select avg(final_result) from `tabWater Content Test`
		#  where sample_id = '{0}' and result_status = 'Accept'""".format(self.sample_id), as_list=1)
		dl = frappe.db.get_value("Water Content Test",{"sample_id":self.sample_id, "result_status":"Accept", "test_type" : "Sample"},"avg(final_result)")
		if dl:
			self.water_content = dl*1
		dl_dga = frappe.db.sql("""select * from `tabDissolved Gas Analysis`
			where sample_id = '{0}' and result_status = 'Accept' and test_type = 'Sample'""".format(self.sample_id), as_dict=1)
		if dl_dga:
			dga_test_result = dl_dga[0]
			print "\n\nhugrogen",dl_dga[0]["oxygen"],"\n\n"
			print "dga_test_result",dga_test_result
			print "dga_test_result ox",dga_test_result["oxygen"]
			self.total_gas_contents = dga_test_result["total_gas_contents"]
			self.total_dissolved_combustible_gases = dga_test_result["tdcg"]
			self.tdcg_per_tgc = dga_test_result["tdcg_per_tgc"]

			self.hydrogen = dga_test_result["hydrogen"]
			self.oxygen = dga_test_result["oxygen"]
			self.nitrogen = dga_test_result["nitrogen"]
			self.carbon_monoxide = dga_test_result["carbon_monoxide"]
			self.methane = dga_test_result["methane"]
			self.carbon = dga_test_result["carbon"]
			self.ethane = dga_test_result["ethane"]
			self.ethylene = dga_test_result["ethylene"]
			self.acetelene = dga_test_result["acetelene"]
			self.propane = dga_test_result["propane"]
			self.propylene = dga_test_result["propylene"]
		
		self.save()
		frappe.msgprint("Test Certificate " +self.name+" is updated")
		return {"water_content":dl}
		
@frappe.whitelist()
def create_test_certificate(sample_id,job_card):	
	doc_sample_entry_register = frappe.get_doc("Sample Entry Register",sample_id)
	doc_job_card = frappe.get_doc("Job Card Creation",job_card)
	if doc_sample_entry_register.test_certificate:
		doc_test_certificate = frappe.get_doc("Test Certificate",doc_sample_entry_register.test_certificate)
	else:
		doc_test_certificate = frappe.new_doc("Test Certificate")

	doc_test_certificate.sample_id = sample_id
	doc_test_certificate.customer = doc_sample_entry_register.customer
	doc_test_certificate.code_designation = doc_sample_entry_register.functional_location
	doc_test_certificate.equipment = doc_sample_entry_register.equipment
	doc_test_certificate.type = doc_sample_entry_register.type
	doc_test_certificate.weather_condition_during_sampling = doc_sample_entry_register.weather_condition_during_sampling
	doc_test_certificate.date_of_receipt = doc_sample_entry_register.date_of_receipt
	doc_test_certificate.date_of_collection = doc_sample_entry_register.date_of_collection
	doc_test_certificate.condition_of_sample = doc_sample_entry_register.sample_condition
	doc_test_certificate.drawn_by = doc_sample_entry_register.drawn_by
	doc_test_certificate.drawn_from = doc_sample_entry_register.drawn_from
	doc_test_certificate.placed_at = doc_sample_entry_register.placed_at
	doc_test_certificate.cust_sample_id = doc_sample_entry_register.cust_sample_id
	doc_test_certificate.designation = doc_sample_entry_register.designation
	doc_test_certificate.work_order_no = doc_sample_entry_register.order_id
	doc_test_certificate.serial_number = doc_sample_entry_register.serial_number
	doc_test_certificate.model_no = doc_sample_entry_register.model_no
	doc_test_certificate.equipment_make = doc_sample_entry_register.equipment_make
	doc_test_certificate.customer_code = doc_sample_entry_register.customer
	doc_test_certificate.technical_contact = doc_sample_entry_register.technical_contact
	doc_test_certificate.technical_contact_details = doc_sample_entry_register.technical_contact_details
	import datetime
	doc_test_certificate.certificate_date = datetime.datetime.today()
	doc_test_certificate.get_test_details()
	doc_test_certificate.observations_from_oil_screening_test = doc_job_card.observations_from_oil_screening_test
	doc_test_certificate.observation_from_dissolved_gas_analysis = doc_job_card.observation_from_dissolved_gas_analysis
	doc_test_certificate.next_test_due_on = doc_job_card.next_test_due_on
	doc_test_certificate.observation_from_furan_analysis = doc_job_card.observation_from_furan_analysis
	doc_test_certificate.overall_recommendation = doc_job_card.overall_recommendation
	doc_test_certificate.trufil_remarks = doc_job_card.trufil_remarks
	
	doc_test_certificate.save()

	frappe.db.set_value("Job Card Creation", job_card, "test_certificate",doc_test_certificate.name)
	frappe.db.set_value("Sample Entry Register", sample_id, "test_certificate_status", "Created")
	frappe.db.set_value("Sample Entry Register", sample_id, "test_certificate", doc_test_certificate.name)

