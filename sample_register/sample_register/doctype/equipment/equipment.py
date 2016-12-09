# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Equipment(Document):
	
	def before_insert(self):
		self.generate_equipment_code()

	def validate(self):
		self.generate_equipment_code()
		self.generate_model_no()
		self.validate_serial_number()


	# Generate equipment code with combination of manufactured by and serial number
	def generate_equipment_code(self):
		if self.serial_number and self.manufactured_by:
			self.equipment_code = self.manufactured_by + '-' + self.serial_number


	# Generate model number as per the formula shared like HV?LV?LLV V; Rating1/Rating2 kVA ;/Phase
	def generate_model_no(self):
		model_no = ''
		s = '/'
		if self.hv:
			model_no += self.hv + '/'

		if self.lv and not self.llv:
			model_no += self.lv + ' Volts;'
		if self.lv and self.llv:
			model_no += self.lv + '/'

		if self.llv:
			model_no += self.llv + ' Volts; '

		if self.rating1 and not self.rating2:
			model_no += self.rating1 + ' kVA;'
		if self.rating1 and self.rating2:
			model_no += self.rating1 + '/'

		if self.rating2:
			model_no += self.rating2 + ' kVA;'

		if self.phase:
			model_no += self.phase

		self.model_no = model_no


	# Validate unique serial number is assigned for each equipment is not.
	def validate_serial_number(self):
		if frappe.db.sql("""select name from `tabEquipment` where name!='%s' and serial_number='%s'"""%(self.name,self.serial_number)):
			frappe.msgprint("Serial number '%s' is already assigned for another Equipment"%self.serial_number,raise_exception=1)