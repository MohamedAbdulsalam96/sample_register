# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "sample_register"
app_title = "Sample Register"
app_publisher = "indictrans"
app_description = "Detail Information of collected samples."
app_icon = "fa-book"
app_color = "grey"
app_email = "sambhaji.k@indictranstech.com"
app_version = "0.0.1"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/sample_register/css/sample_register.css"
# app_include_js = "/assets/sample_register/js/sample_register.js"

# include js, css files in header of web template
# web_include_css = "/assets/sample_register/css/sample_register.css"
# web_include_js = "/assets/sample_register/js/sample_register.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "sample_register.install.before_install"
# after_install = "sample_register.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

notification_config = "sample_register.sample_register.notifications.get_notification_config"

fixtures = ['Custom Field', 'Property Setter', "Custom Script","Print Format"]

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Job Card Creation": {
		"after_insert": "sample_register.sample_register.doctype.sample_entry_register.sample_entry_register.status_updator",
		"on_submit": "sample_register.sample_register.doctype.sample_entry_register.sample_entry_register.status_updator",
		"before_cancel": "sample_register.sample_register.doctype.sample_entry_register.sample_entry_register.status_updator"
	},
	"Stock Entry":{
		"on_submit": "sample_register.sample_register.doctype.fixed_asset_serial_number.fixed_asset_serial_number.make_new_asset"
	},
	"Purchase Receipt":{
		"on_submit": "sample_register.sample_register.doctype.fixed_asset_serial_number.fixed_asset_serial_number.new_fixed_asset"
	},
	"Employee":{
		"validate": "sample_register.sample_register.doctype.fixed_asset_serial_number.fixed_asset_serial_number.trufil_id"
	},
	"Quality Inspection":{
		"on_submit": "sample_register.custom_py_methods.send_verified_mail"
		# "onload":"sample_register.sample_register.doctype.fixed_asset_serial_number.fixed_asset_serial_number.schedular_event"
	},
	"Opportunity": {
		"on_update": "sample_register.custom_py_methods.activity_log",
		"validate": "sample_register.custom_py_methods.calculate_tot_amount"
	},
	"Sales Order": {
		"on_submit": "sample_register.custom_py_methods.check_attachment"
	},
	"Quotation": {
		"on_submit": "sample_register.custom_py_methods.quot_workflow"
	},
	"Product Bundle": {
		"on_trash": "sample_register.custom_py_methods.bundle_so_present"
	}
}

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
	"daily": [
		"sample_register.sample_register.doctype.fixed_asset_serial_number.fixed_asset_serial_number.change_calibration_status"
	]
}
# 	"daily": [
# 		"sample_register.tasks.daily"
# 	],
# 	"hourly": [
# 		"sample_register.tasks.hourly"
# 	],
# 	"weekly": [
# 		"sample_register.tasks.weekly"
# 	]
# 	"monthly": [
# 		"sample_register.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "sample_register.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "sample_register.event.get_events"
# }
