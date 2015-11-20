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
					"label": "Code Designation"
					"description":_("Functional Location Details."),
				},
				{
					"type": "doctype",
					"name": "Test Group",
					"description":_("Test Group"),
				},
				{
					"type": "doctype",
					"name": "Test Name",
					"description":_("Test Name"),
				},
				{
					"type": "doctype",
					"name": "Oil Type",
					"description":_("Type Of oil"),
				},
				{
					"type": "doctype",
					"name": "Standard",
					"description":_("Standard"),
				},
				{
					"type": "doctype",
					"name": "Test",
					"description":_("Test Master"),
				},
			]
		},

	]
