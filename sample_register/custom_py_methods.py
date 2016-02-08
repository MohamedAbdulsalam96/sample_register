import frappe
from frappe.utils import rounded,money_in_words
from frappe.model.mapper import get_mapped_doc
from frappe import throw, _

@frappe.whitelist()
def notify_quality_insp(doc, method):
	for d in doc.get('items'):		 #Enter inspection date for all items that require inspection
			if frappe.db.get_value("Item", d.item_code, "inspection_required") and not d.qa_no:
				frappe.throw(_("Quality Inspection required for Item {0}").format(d.item_code))
			elif d.qa_no:
				quality_inspection = frappe.get_doc("Quality Inspection", d.qa_no)
				if quality_inspection.docstatus != 1:
					frappe.throw(_("Quality Inspection not Submitted"))

@frappe.whitelist()
def send_inspection_mail(item, inspector, name, verifier):
	try:
		subject = "Quality Inspection"
	 	message = """<p>Hello ,</p><p>Quality Inspection  : %s </p>
	 	<p> For Item: %s </p>
	 	<p>Inspected By : %s </p>"""%(name, item, inspector)
	 	recipients = inspector, verifier
	 	frappe.sendmail(recipients=recipients, subject=subject, message =message)
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

			 	frappe.sendmail(recipients=doc.verified, subject=subject, message =message)
		except Exception, e:
			import traceback
			print "notify", traceback.format_exc()
			return False