import frappe
from frappe.utils import rounded,money_in_words
from frappe.model.mapper import get_mapped_doc
from frappe import throw, _
from erpnext.hr.doctype.process_payroll.process_payroll import get_month_details


@frappe.whitelist()
def send_inspection_mail(item, inspector, name, verifier):
	try:
		subject = "Quality Inspection"
	 	message = """<p>Hello ,</p><p>Quality Inspection  : %s </p>
	 	<p> For Item: %s </p>
	 	<p>Inspected By : %s </p>"""%(name, item, inspector)
	 	recipients = inspector, verifier
	 	# frappe.sendmail(recipients=recipients, subject=subject, message =message)
	except Exception, e:
		import traceback
		print "notify", traceback.format_exc()
		return False


@frappe.whitelist()
def send_verified_mail(doc, method):
	if doc.verified:
		try:
			if doc.verified and doc.inspected_by:
				subject = "Quality Inspection Verified"
			 	message = """<p>Hello ,</p><p>Quality Inspection  : %s </p>
			 	<p> For Item: %s </p>
			 	<p>Verified By : %s </p>"""%(doc.name, doc.item_code, doc.verified )

			 	# frappe.sendmail(recipients=doc.verified, subject=subject, message =message)
		except Exception, e:
			import traceback
			print "notify", traceback.format_exc()
			return False

@frappe.whitelist()
def absent_days(employee, month, fiscal_year):
	m = get_month_details(fiscal_year, month)
	absent = frappe.db.sql("""
		select att_date from `tabAttendance` where employee = %s and status = "Absent" and att_date between %s and %s
		""", (employee, m.month_start_date, m.month_end_date), as_list=1)
	return len(absent)