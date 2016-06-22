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
					"label": _("Service Request"),
					"type": "doctype",
					"name": "Service Request",
					"description": _("Customer Service Request list."),
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
					"type": "doctype",
					"name": "TRB Session",
					"description": _("Create/Update TRB"),
				},
				{
					"type": "page",
					"name": "jobcard",
					"icon": "icon-sitemap",
					"label": _("Job Card Submission"),
					"description": _("Submit Job Card and Set Priority"),
				},
				{
					"type": "report",
					"name":"TRB Session Report",
					"doctype": "Job Card Creation",
					"is_query_report": True,
				},
				{
					"type": "doctype",
					"name": "Standard Operating Procedure",
					"label": _("Standard Operating Procedure"),
					"description": _("create Standard Operating Procedure")
				},
			]
		},
		{
			"label": _("Test Result Book"),
			"icon": "icon-star",
			"items": [
				{
					"type": "doctype",
					"name": "Water Content Test",
					"description": _("Water Content Test"),
				},
				{
					"type": "doctype",
					"name": "Neutralisation Value Test",
					"description": _(" Neutralisation Value Test"),
				},
				{
					"type": "doctype",
					"name": "Flash point by Penskey Martin",
					"description": _(" Flash point by Penskey Martin"),
				},
				{
					"type": "doctype",
					"name": "Interfacial Tension Test",
					"description": _("Interfacial Tension Test"),
				},
				{
					"type": "doctype",
					"name": "Furan Content",
					"description": _("Furan Content Test"),
				},
				{
					"type": "doctype",
					"name": "Dissolved Gas Analysis",
					"description": _("Dissolved Gas Analysis"),
				},
			]
		},

	]
