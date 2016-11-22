# -*- coding: utf-8 -*-
# Copyright (c) 2015, indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class FlashpointbyPenskeyMartin(Document):
	def validate(self):
		ir=0
		ir_count=0
		for row in self.test_details:
			if row.test__result_status == "Accept":
				ir = ir+ row.instrument_reading
				ir_count = ir_count + 1
		ir = float(ir/float(ir_count))
		self.flash_point = ir + 0.025 * (1013 + self.barometric_pressure)