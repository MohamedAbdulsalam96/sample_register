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
				{
					"type": "doctype",
					"name": "Job Card Creation",
					"description": _("All Job Card related information."),
				},
				{
					"type": "doctype",
					"name": "Test Book",
					"description": _("All Test Book related information."),
				},
				{
					"type": "doctype",
					"name": "Test Certificate",
					"description": _("All Test Certificate related information."),
				},
				{
					"label": _("Work Order"),
					"type": "doctype",
					"name": "Order Register",
					"description": _("Customer orders list."),
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
					"label": "Code Designation",
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
		{
			"label": _("Tools"),
			"icon": "icon-wrench",
			"items": [
				{
					"type": "doctype",
					"name": "Sample Entry Creation Tool",
					"description": _("Create/Update Sample Entry"),
				},
				{
					"type": "page",
					"name": "jobboard",
					"icon": "icon-sitemap",
					"label": _("Job Card Creation"),
					"description": _("Create Job Card and Set Priority, Standard Details"),
				},
				{
					"type": "page",
					"name": "jobcard",
					"icon": "icon-sitemap",
					"label": _("Job Card Submission"),
					"description": _("Submit Job Card and Set Priority"),
				},
				{
					"type": "doctype",
					"name": "Standard Operating Procedure",
					"label": _("Standard Operating Procedure"),
					"description": _("create Standard Operating Procedure")
				},
			]
		},

	]
