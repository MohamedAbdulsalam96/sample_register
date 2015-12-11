from __future__ import unicode_literals
import frappe
from frappe.utils import cstr,now,add_days
import json

@frappe.whitelist()
def get_sample_data():
	return {
	"get_sample_data": frappe.db.sql("""select false, name, customer, type, priority, standards, test_group from `tabSample Entry Register` where job_card_status="" order by name""", as_list=1)
	}

@frappe.whitelist()
def get_sample_data_with_job():
	return {
	"get_sample_data": frappe.db.sql("""select false, name, customer, type, priority, standards, job_card, job_card_status, test_group, CASE job_card_status WHEN 'Not Available' THEN 1 WHEN 'Created' THEN 2 WHEN 'Submitted' THEN 3 ELSE 5 END as id from `tabSample Entry Register` order by id, name desc""", as_list=1,debug=1)
	}

@frappe.whitelist()
def get_test_data(test_group):
	return {
	"get_test_data": frappe.db.sql("""select name from `tabTest Name` where test_group='%s' order by name"""%(test_group), as_list=1)
	}

@frappe.whitelist()
def create_job_card(test_group,selectedData,test_list_unicode):
	print test_list_unicode
	test_list=json.loads(test_list_unicode)
	# for test in test_list:
	# 	frappe.msgprint("test is: "+ test)
	# frappe.msgprint(test_list[0])
	# print type(selectedData)
	# frappe.msgprint("Job Card "+bank.name+" created successfuly for : "+test_group);
	#frappe.msgprint(type(selectedData))
	# print selectedData
	# frappe.msgprint(selectedData)
	selectedData_json = json.loads(selectedData)
	for r in selectedData_json:
		doc_job_card_creation=frappe.new_doc("Job Card Creation")
		doc_job_card_creation.sample_id = r.get("sampleid")
		doc_job_card_creation.customer = r.get("customer")
		doc_job_card_creation.type = r.get("type")
		doc_job_card_creation.priority = r.get("priority")
		doc_job_card_creation.standards = r.get("standard")
		for test in test_list:
			test_req={
				"doctype": "Job Card Creation Test Details",
				"test_group": test_group,
				"test": test
			}
			doc_job_card_creation.append("test_details",test_req)
		doc_job_card_creation.save()
		sample_link="<a href='desk#Form/Sample Entry Register/"+r.get("sampleid")+"'>"+r.get("sampleid")+" </a>"
		job_link="<a href='desk#Form/Job Card Creation/"+doc_job_card_creation.name+"'>"+doc_job_card_creation.name+" </a>"
		frappe.msgprint("Job Card "+job_link+" is created successfuly for sample : "+sample_link);

@frappe.whitelist()
def submit_job_card(selectedData):
	selectedData_json = json.loads(selectedData)
	if (len(selectedData_json)==0):
		frappe.msgprint("Please Select Sample ID whose Job Card need to submit")
	for r in selectedData_json:
		if(r.get("job_card")):
			doc_job_card_creation=frappe.get_doc("Job Card Creation",r.get("job_card"))
			doc_job_card_creation.submit()

@frappe.whitelist()
def set_sample_data(priority,standards,selectedData):
	selectedData_json = json.loads(selectedData)
	for r in selectedData_json:
		if r.get("sampleid"):
			sample_entry_doc=frappe.get_doc("Sample Entry Register",r.get("sampleid"))
			sample_entry_doc.priority = priority
			sample_entry_doc.standards = standards
			sample_entry_doc.save()

@frappe.whitelist()
def set_priority_data(priority,selectedData):
	selectedData_json = json.loads(selectedData)
	for r in selectedData_json:
		if r.get("sampleid"):
			sample_entry_doc=frappe.get_doc("Sample Entry Register",r.get("sampleid"))
			sample_entry_doc.priority = priority
			sample_entry_doc.save()

@frappe.whitelist()
def set_standards_data(standards,selectedData):
	selectedData_json = json.loads(selectedData)
	for r in selectedData_json:
		if r.get("sampleid"):
			sample_entry_doc=frappe.get_doc("Sample Entry Register",r.get("sampleid"))
			sample_entry_doc.standards = standards
			sample_entry_doc.save()


