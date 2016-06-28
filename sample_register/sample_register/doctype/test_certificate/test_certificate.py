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
		dl = frappe.db.get_value("Water Content Test",{"sample_id":self.sample_id, "result_status":"Accept"},"avg(final_result)")
		self.water_content = dl;
		# print "DLLLLLLLLLLLL",dl
		dl_dga = frappe.db.sql("""select * from `tabDissolved Gas Analysis`
			where sample_id = '{0}' and result_status = 'Accept'""".format(self.sample_id), as_dict=1)
		# print "DLLLLLLLLLLLL2",dl2
		dga_test_result = dl_dga[0]
		print "\n\nhugrogen",dl_dga[0]["oxygen"],"\n\n"
		print "dga_test_result",dga_test_result
		print "dga_test_result ox",dga_test_result["oxygen"]
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