# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return {
		"Sample Register": {
			"color": "#1abc9c",
			"icon": "icon-book",
			"type": "module",
			"label": _("Back Office")
		},
		"Lab Operation": {
			"color": "#3498db",
			"icon": "icon-list-alt ",
			"type": "module",
			"label": _("Lab Operation")
		}
	}
