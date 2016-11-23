# -*- coding: utf-8 -*-
# Copyright (c) 2015, indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class InterfacialTension(Document):
	def validate(self):
		self.calculate_interfacial_tension()

	def calculate_interfacial_tension(self):
		import math
		ir=0
		ir_count=0
		for row in self.test_details:
			if row.test__result_status == "Accept":
				ir = ir+ row.ir_of_water
				ir_count = ir_count + 1
		ir = float(ir/float(ir_count))
		density_of_oil = self.density_of_oil * (1 + 0.00065 * (self.temp_of_oil - 27))
		factor = 0.725 +  math.sqrt( (0.01452*(10**5)*(ir/1000))/ ( self.circumference_of_ring\
		 				* self.circumference_of_ring * (self.density_of_water-self.density_of_oil*27) ) +\
		 				 0.04534 - (float(1.679)/float(self.radius_ratio)) )
		interfacial_tension = (ir*factor)/float(1000)
		self.interfacial_tension = interfacial_tension
		print "\n\ninterfacial_tension", interfacial_tension