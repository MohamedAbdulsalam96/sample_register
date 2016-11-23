# -*- coding: utf-8 -*-
# Copyright (c) 2015, indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class SpecificResistivity(Document):
	def validate(self):
		# frappe.msgprint("Test Saved")
		self.calculate_result()

	def calculate_result(self):
		import math
		ir_dial=0
		ir_power=0
		ir_count=0
		for row in self.test_details:
			if row.test__result_status == "Accept":
				ir_dial = ir_dial+ row.ir_dial
				ir_power = ir_power+ row.ir_power
				ir_count = ir_count + 1
		ir_dial = float(ir_dial/float(ir_count))
		ir_power = float(ir_power/float(ir_count))

		self.specific_resistivity = ir_dial*(10**ir_power)