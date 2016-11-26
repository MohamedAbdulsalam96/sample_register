import frappe
from frappe.utils import flt,rounded,money_in_words
from frappe.model.mapper import get_mapped_doc
from frappe import throw, _
from erpnext.hr.doctype.process_payroll.process_payroll import get_month_details
import datetime

@frappe.whitelist()
def ping():
	frappe.msgprint("pong")

@frappe.whitelist()
def check_bottle_no(bottle_number,sample_id):
		dl_dga = frappe.db.sql("""select container_id\
			from `tabContainer Details`\
			where parent = '{0}'""".format(sample_id), as_list=1)
		b =[e[0] for e in dl_dga]
		if bottle_number:
			if bottle_number in b:
				pass
			else:
				frappe.msgprint("Please check bottle number {0} with container id entered in Sample Register Entry: {1}.".format(bottle_number,sample_id))