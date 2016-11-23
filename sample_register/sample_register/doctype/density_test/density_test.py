# -*- coding: utf-8 -*-
# Copyright (c) 2015, indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class DensityTest(Document):
	def validate(self):
		# frappe.msgprint("Test Saved")
		self.calculate_result()

	def calculate_result(self):
		import math
		ir=0
		ir_count=0
		for row in self.test_details:
			if row.test__result_status == "Accept":
				ir = ir+ row.instrument_reading
				ir_count = ir_count + 1
		ir = float(ir/float(ir_count))
		self.density_of_oil_at_dt1 = ir*(1 + 0.00065*float(self.oil_temperature-self.desired_temperature_1))
		self.density_of_oil_at_dt2 = ir*(1 + 0.00065*float(self.oil_temperature-self.desired_temperature_2))
