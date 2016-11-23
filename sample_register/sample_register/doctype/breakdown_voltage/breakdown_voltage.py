# -*- coding: utf-8 -*-
# Copyright (c) 2015, indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class BreakdownVoltage(Document):
	def validate(self):
		# frappe.msgprint("Test Saved")
		self.calculate_result()

	def calculate_result(self):
		import math
		instrument_reading=0
		ir_count=0
		for row in self.test_details:
			if row.test__result_status == "Accept":
				instrument_reading = instrument_reading+ row.instrument_reading
				ir_count = ir_count + 1
		instrument_reading = float(instrument_reading/float(ir_count))
		self.breakdown_voltage = instrument_reading
