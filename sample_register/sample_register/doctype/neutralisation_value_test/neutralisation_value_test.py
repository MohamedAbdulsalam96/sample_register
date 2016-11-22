# -*- coding: utf-8 -*-
# Copyright (c) 2015, indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import datetime

class NeutralisationValueTest(Document):
	def validate(self):
		ir=0
		ir_count=0
		for row in self.test_details:
			if row.test__result_status == "Accept":
				ir = ir+ row.ir
				ir_count = ir_count + 1
		ir = float(ir/float(ir_count))
		self.neutralization_value = (ir * self.normality_of_koh * self.molecular_weight_of_koh)/(self.volume_of_oil*self.density_of_oil)