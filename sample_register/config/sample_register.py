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
			"label": _("Master"),
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
					"description":_("Equipment Type Details."),
				},
				{
					"type": "doctype",
					"name": "Equipment Make",
					"description":_("Equipment Make Details."),
				},
			]
		},

	]
