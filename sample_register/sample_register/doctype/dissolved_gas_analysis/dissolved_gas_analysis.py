# -*- coding: utf-8 -*-
# Copyright (c) 2015, indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import datetime

class DissolvedGasAnalysis(Document):
	def on_submit(self):
		self.end_time = datetime.datetime.now()

	def validate(self):
		# frappe.msgprint("hi")
		print "hi"
