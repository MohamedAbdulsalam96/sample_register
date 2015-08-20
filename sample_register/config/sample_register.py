from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Documents"),
			"icon": "icon-star",
			"items": [
				{
					"type": "doctype",
					"name": "Sample Entry Register",
					"description": _("All samples related information."),
				},
			]
		},
		{
			"label": _("Masters"),
			"icon": "icon-wrench",
			"items": [
				{
					"type": "doctype",
					"name": "Equipment",
					"description":_("Equipment Details."),
				},
				{
					"type": "doctype",
					"name": "Equipment Type",
					"description":_("Equipment Type."),
				},
				{
					"type": "doctype",
					"name": "Equipment Make",
					"description":_("Equipment Make."),
				},
				{
					"type": "doctype",
					"name": "Functional Location",
					"description":_("Functional Location Details."),
				},
			]
		},

	]
