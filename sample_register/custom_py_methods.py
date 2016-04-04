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

@frappe.whitelist()
def add_oppo_comment(docname, reason=None, stage=None, probability=None):
	doc = frappe.get_doc("Opportunity", docname)
	reason_comm = ""
	stage_comm = ""
	probability_comm = ""

	if reason:
		doc.old_reason = reason
		reason_comm = """<b>Reason for Change:</b> """ + reason
		
	if stage:
		doc.old_stage = stage
		stage_comm = """<b>Opportunity Stage Print:</b> """ + stage

	if probability:
		doc.old_probability = probability
		probability_comm = """<b>Probability:</b> """ + probability + "%"

	if reason_comm or stage_comm or probability_comm:
		comment = """<p>{0}</p> <p>{1}</p> <p>{2}</p>""".format(reason_comm, stage_comm, probability_comm)
		doc.add_comment(comment)

@frappe.whitelist()
def activity_log(doc, method):
	reason_comm = ""
	stage_comm = ""
	probability_comm = ""

	if (doc.to_discuss != doc.old_reason) or (doc.to_discuss and not doc.old_reason):
		doc.old_reason = doc.to_discuss
		reason_comm = """<b>Reason for Change:</b> """ + doc.to_discuss
		
	if (doc.opportunity_stage != doc.old_stage) or (doc.opportunity_stage and not doc.old_stage):
		doc.old_stage = doc.opportunity_stage
		stage_comm = """<b>Opportunity Stage:</b> """ + doc.opportunity_stage

	if (doc.probability != doc.old_probability) or (doc.probability and not doc.old_probability):
		doc.old_probability = doc.probability
		probability_comm = """<b>Probability:</b> """ + doc.probability + "%"

	if reason_comm or stage_comm or probability_comm:
		comment = """<p>{0}</p> <p>{1}</p> <p>{2}</p>""".format(reason_comm, stage_comm, probability_comm)
		doc.add_comment(comment)