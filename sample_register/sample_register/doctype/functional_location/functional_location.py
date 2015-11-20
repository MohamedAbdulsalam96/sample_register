# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class FunctionalLocation(Document):
	def validate(self):
		self.set_functional_location_code()
		self.verify_functional_code()


	# Generate functional location code with combination of plant which is optional + substation + location
	def set_functional_location_code(self):
		if self.substation and self.location:
			if self.plant:
				self.functional_location_code = self.plant + '-' + self.substation + '-' + self.location
			else:
				self.functional_location_code = self.substation + '-' + self.location


	# Validate unique functional ocation code is assigned for each functional loaction record/entry
	def verify_functional_code(self):
		if self.functional_location_code:
			if frappe.db.sql("""select name from `tabFunctional Location` where name!='%s' and functional_location_code='%s'"""%(self.name,self.functional_location_code)):
				frappe.msgprint("Same functional location code '%s' is already assigned against another functional location"%self.functional_location_code,raise_exception=1)

