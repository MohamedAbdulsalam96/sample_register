# -*- coding: utf-8 -*-
# Copyright (c) 2015, indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, getdate, nowdate,now_datetime
from frappe.model.naming import make_autoname
from sample_register.sample_register.doctype.test_certificate.test_certificate import create_test_certificate

class JobCardCreation(Document):
	def autoname(self):
		year = int(now_datetime().strftime("%Y"))
		self.name = make_autoname("TF-JC-"+str(year)+"-"+'.#####')

	def validate(self):
		self.check_sample_status_if_sample_id_changed()

	def before_update_after_submit(self):
		if self.status == "Accept":
			create_test_certificate(self.sample_id,self.name)

	def before_insert(self):
		self.check_sample_status()

	def view_result(self):
		# abc = frappe.render_template("templates/includes/cart/view_result.html",{"context":"aa","aa":"aaaa"})
		water_content = frappe.db.get_value("Water Content Test",{"sample_id":self.sample_id, "result_status":"Accept", "test_type" : "Sample"},"avg(final_result)")
		if water_content:
			water_content = '%.2f'%water_content
		dl_dga = frappe.db.sql("""select * from `tabDissolved Gas Analysis`
					where sample_id = '{0}' and result_status = 'Accept' and test_type = 'Sample'""".format(self.sample_id), as_dict=1)
		dga_test_result = {}
		# print "/n/ndl",dl_dga
		if len(dl_dga)>0:
			dga_test_result = dl_dga[0]
			# print "/n/n/ndga",dl_dga
			abc = frappe.render_template("sample_register/sample_register/doctype/job_card_creation/view_result_with_dga.html",{"water_content":water_content,"dga_test_result":dga_test_result}, is_path=True)
		else:
			abc = frappe.render_template("sample_register/sample_register/doctype/job_card_creation/view_result.html",{"water_content":water_content,"dga_test_result":dga_test_result}, is_path=True)
		frappe.msgprint(abc)

	def view_detail_result(self):
		# abc = frappe.render_template("templates/includes/cart/view_result.html",{"context":"aa","aa":"aaaa"})
		service_request = frappe.db.get_value('Sample Entry Register',self.sample_id,'order_id')

		#Current Job Card Test
		water_content = frappe.db.get_value("Water Content Test",{"sample_id":self.sample_id, "result_status":"Accept", "test_type" : "Sample"},"avg(final_result)")
		if water_content:
			water_content = '%.2f'%water_content

		dl_dga = frappe.db.sql("""select * from `tabDissolved Gas Analysis`
					where sample_id = '{0}' and result_status = 'Accept' and test_type = 'Sample'""".format(self.sample_id), as_dict=1)
		dga_test_result = {}

		#last Test Result
		last1 = frappe.db.sql("""select name,sample_id,creation from `tabJob Card Creation` where functional_location='{0}' order by creation desc limit 1,2""".format(self.functional_location), as_dict=1)

		dl_dga_last1 = {}
		if last1:
			dl_dga_last1 = frappe.db.sql("""select * from `tabDissolved Gas Analysis`
				where sample_id = '{0}' and result_status = 'Accept' and test_type = 'Sample'""".format(last1[0]["sample_id"]), as_dict=1)

		#last second
		last2 = frappe.db.sql("""select name,sample_id,creation from `tabJob Card Creation` where functional_location='{0}' order by creation desc limit 2,3""".format(self.functional_location), as_dict=1)
		# frappe.msgprint(last2[0]["sample_id"])
		dl_dga_last2 = {}
		if last2:
			dl_dga_last2 = frappe.db.sql("""select * from `tabDissolved Gas Analysis`
				where sample_id = '{0}' and result_status = 'Accept' and test_type = 'Sample'""".format(last2[0]["sample_id"]), as_dict=1)

		if len(dl_dga)>0:
			dga_test_result = dl_dga[0]
			dga_test_result_last1 = dl_dga_last1[0] if (len(dl_dga_last1)>0) else   {}
			dga_test_result_last2 = dl_dga_last2[0] if (len(dl_dga_last2)>0) else   {}
			
			abc = frappe.render_template("sample_register/sample_register/doctype/job_card_creation/view_detail_result_with_dga.html",{"water_content":water_content,"dga_test_result":dga_test_result,"dga_test_result_last1":dga_test_result_last1,"dga_test_result_last2":dga_test_result_last2,"service_request":service_request}, is_path=True)
		else:
			abc = frappe.render_template("sample_register/sample_register/doctype/job_card_creation/view_result.html",{"water_content":water_content,"dga_test_result":dga_test_result,"service_request":service_request}, is_path=True)

		#oild test result
		density = frappe.db.sql("""select * from `tabDensity Test` where job_card = '{0}' AND test_type='Sample' and result_status='Accept' LIMIT 1""".format(self.name),as_dict=1)
		if density:
			density = density[0]

		ddf = frappe.db.sql("""select dielectric_dissipation_factor_at_dt1 from `tabDielectric Dissipation Factor` where job_card = '{0}' AND test_type='Sample' and result_status='Accept' LIMIT 1""".format(self.name),as_dict=1)
		if ddf:
			ddf = ddf[0]["dielectric_dissipation_factor_at_dt1"]

		specific_resistivity = frappe.db.sql("""select specific_resistivity from `tabSpecific Resistivity` where job_card = '{0}' AND test_type='Sample' and result_status='Accept' LIMIT 1""".format(self.name),as_dict=1)
		if specific_resistivity:
			specific_resistivity = specific_resistivity[0]["specific_resistivity"]

		it = frappe.db.sql("""select interfacial_tension,temp_of_oil from `tabInterfacial Tension` where job_card = '{0}' AND test_type='Sample' and result_status='Accept' LIMIT 1""".format(self.name),as_dict=1)
		interfacial_tension = " "
		if it:
			interfacial_tension = it[0]

		bdv = frappe.db.sql("""select breakdown_voltage from `tabBreakdown Voltage` where job_card = '{0}' AND test_type='Sample' and result_status='Accept' LIMIT 1""".format(self.name),as_dict=1)
		breakdown_voltage = " "
		if bdv:
			breakdown_voltage = bdv[0]["breakdown_voltage"]

		nvt = frappe.db.sql("""select neutralization_value from `tabNeutralisation Value Test` where job_card = '{0}' AND test_type='Sample' and result_status='Accept' LIMIT 1""".format(self.name),as_dict=1)
		neutralization_value = " "
		if nvt:
			neutralization_value = nvt[0]["neutralization_value"]

		flash_point = " "
		fp = frappe.db.sql("""select flash_point from `tabFlash point by Penskey Martin` where job_card = '{0}' AND test_type='Sample' and result_status='Accept' LIMIT 1""".format(self.name),as_dict=1)
		if fp:
			flash_point = fp[0]["flash_point"]

		oil_test_result = frappe.render_template("sample_register/sample_register/doctype/job_card_creation/view_result_with_oil_test.html",{"water_content":water_content,"service_request":service_request,"density":density, "ddf":ddf,"specific_resistivity":specific_resistivity, "interfacial_tension":interfacial_tension, "breakdown_voltage":breakdown_voltage, "neutralization_value":neutralization_value, "flash_point":flash_point}, is_path=True)
		
		# select avg(concentration) from `tabFuran Content Test Details` where parent = (select name from `tabFuran Content` where job_card='TF-JC-2016-00082') and furans='5H2F'
		
		#Fural Content Result
		furan = frappe.db.sql("""select avg(concentration),furans from `tabFuran Content Test Details` where parent = (select name from `tabFuran Content` where job_card='{0}' AND test_type='Sample' and result_status='Accept' LIMIT 1) group by furans""".format(self.name), as_dict=1)
		b  = {}
		for i in furan:
			b[i["furans"]] = i["avg(concentration)"]
		furan = b

		furans_details = []
		furans_details = frappe.db.sql("""select * 
										from `tabFuran Content` 
											where job_card='{0}' 
												and test_type='Sample' 
												and result_status='Accept' 
												limit 1""".format(self.name), as_dict=1)
		
		# import datetime
		# print "\n\nfurans_details",furans_details
		# test_date = datetime.datetime.strptime(str(furans_details[0]["date_of_testing"]), '%Y-%m-%d')
		# print "\n\n\n","furans_details",furans_details
		if len(furans_details)>0:
			furans_details[0]["date_of_testing"] = furans_details[0]["date_of_testing"].strftime('%d-%m-%Y')
			furans_details = furans_details[0]
		# print "\n\n\nfuran",furan
		furan_content_result = frappe.render_template("sample_register/sample_register/doctype/job_card_creation/view_result_with_furan_content.html",{"furan":furan, "service_request":service_request,"furans_details":furans_details}, is_path=True)
		self.furan_result = furan_content_result
		self.oil_screening_tests_result = oil_test_result
		self.dga_result = abc
		self.save()

	def before_submit(self):
		sample_entry_doc=frappe.get_doc("Sample Entry Register",self.sample_id)
		if(not sample_entry_doc.date_of_collection) or (not sample_entry_doc.date_of_receipt):
			frappe.throw("Collection Date or Receipt Date not Present in "+self.sample_id)

		for r in self.test_details:
			if r.test_type:
				doc_test_book=frappe.new_doc(r.test_type)
				doc_test_book.job_card = self.name
				doc_test_book.sample_id = self.sample_id
				# doc_test_book.customer = self.customer
				doc_test_book.type = self.type
				doc_test_book.priority = self.priority
				doc_test_book.standards = self.standards
			else:
				frappe.throw("Please select test using Job card Creation Tool")
			# doc_test_book.item_code = r.item_code
			# doc_test_book.test_group = r.test_group
			doc_test_book.item_name = r.item_name
			# doc_test_book.test = r.test
			doc_test_book.save()
			test_book_link="<a href='desk#Form/"+ doc_test_book.doctype+"/"+doc_test_book.name+"'>"+doc_test_book.name+" </a>"
			job_link="<a href='desk#Form/Job Card Creation/"+doc_test_book.job_card+"'>"+doc_test_book.job_card+" </a>"
			frappe.msgprint("For Job Card "+job_link+", TRB "+test_book_link+ " created")
			# r.test_book = doc_test_book.name
		
	def check_sample_status(self):
		if self.sample_id and (self.docstatus==0):
			sample_entry_doc=frappe.get_doc("Sample Entry Register",self.sample_id)
			if(sample_entry_doc.job_card_status == "Created"):
				frappe.throw("Job Card "+sample_entry_doc.job_card +" is allready Created for "+self.sample_id)
			if(sample_entry_doc.job_card_status == "Submitted"):
				frappe.throw("Job Card "+sample_entry_doc.job_card +" is allready Submitted for "+self.sample_id)

	def check_sample_status_if_sample_id_changed(self):
		if self.sample_id and (self.docstatus==0):
			sample_entry_doc=frappe.get_doc("Sample Entry Register",self.sample_id)
			if(self.name!=sample_entry_doc.job_card):
				if(sample_entry_doc.job_card_status == "Created"):
					frappe.throw("Job Card "+sample_entry_doc.job_card +" is allready Created for "+self.sample_id)
				if(sample_entry_doc.job_card_status == "Submitted"):
					frappe.throw("Job Card "+sample_entry_doc.job_card +" is allready Submitted for "+self.sample_id)
	
	def on_update_after_submit(self):
		if self.status and self.status == "Closed" and self.docstatus == 1:
			status = True
			for row in self.test_details:
				if row.status != "Closed":
					status = False
			if status == False:
				frappe.msgprint("All Test's are not Closed yet")
				self.status = " "

@frappe.whitelist()
def so_item_code(doctype, txt, searchfield, start, page_len, filters):
	pi_item = frappe.db.sql("""select item_code from `tabPacked Item` where parent = '%s'"""%(filters.get("parent")))
	soi_item_query = """select item_code from `tabSales Order Item` where parent='%s'"""%(filters.get("parent"))
	if pi_item:
		soi_item_query += """ and item_code not in (select parent_item from `tabPacked Item` where parent='%s')"""%filters.get("parent")
	soi_item = frappe.db.sql(soi_item_query)
	
	return pi_item+soi_item