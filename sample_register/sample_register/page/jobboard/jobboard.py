from __future__ import unicode_literals
import frappe
from frappe.utils import cstr,now,add_days
import json
import datetime

@frappe.whitelist()
def get_items(sales_order):
	return {
	"get_items": frappe.db.sql("""select soi.item_code, i.test_type from `tabSales Order Item` soi, `tabItem` i
				where soi.item_code=i.item_code and soi.parent = '{0}'""".format(sales_order), as_list=1)
	}

@frappe.whitelist()
def get_sales_order():
	return {
	"get_sales_order": frappe.db.sql("""select name from `tabSales Order`""", as_list=1)
	}


@frappe.whitelist()
def get_sample_data(sales_order):
	print "in sample get get_sample_data"
	print sales_order
	return {
	"get_sample_data": frappe.db.sql("""select false, name, customer, type, priority, standards, sales_order, test_group,
		order_id,
		case when 5!=6 then (select sales_order from `tabService Request` where name=order_id)
		ELSE ""
		END AS 'sales_order'
	 from `tabSample Entry Register` where job_card_status="Not Available" and docstatus = 1 group by name having sales_order = '{0}' order by name""".format(sales_order), as_list=1)
	}

@frappe.whitelist()
def get_sample_data_with_job():
	return {
	"get_sample_data": frappe.db.sql("""select false, name, customer, type, priority, standards, test_group,order_id,
		case when 5!=6 then (select sales_order from `tabService Request` where name=order_id)
		ELSE ""
		END AS 'sales_order'
	 from `tabSample Entry Register` where job_card_status!="" order by name""", as_list=1)
	}

@frappe.whitelist()
def get_test_data(test_group):
	return {
	"get_test_data": frappe.db.sql("""select name from `tabTest Name` where test_group='%s' order by name"""%(test_group), as_list=1)
	}

@frappe.whitelist()
def create_job_card(selectedData,test_list_unicode):
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
	print test_list
	for r in selectedData_json:
		doc_job_card_creation=frappe.new_doc("Job Card Creation")
		doc_job_card_creation.sample_id = r.get("sampleid")
		doc_job_card_creation.customer = r.get("customer")
		doc_job_card_creation.type = r.get("type")
		doc_job_card_creation.priority = r.get("priority")
		doc_job_card_creation.standards = r.get("standard")
		doc_job_card_creation.creation_date = datetime.datetime.today()
		for test_type in test_list:
			test_req={
				"doctype": "Job Card Creation Test Details",
				"item_code":test_type,
				"item_name":frappe.db.get_value("Item", test_type, "item_name"),
				"test_type": frappe.db.get_value("Item", test_type, "test_type"),
				"test_group": frappe.db.get_value("Item", test_type, "test_group"),
			}
			doc_job_card_creation.append("test_details",test_req)
		doc_job_card_creation.save()
		sample_link="<a href='desk#Form/Sample Entry Register/"+r.get("sampleid")+"'>"+r.get("sampleid")+" </a>"
		job_link="<a href='desk#Form/Job Card Creation/"+doc_job_card_creation.name+"'>"+doc_job_card_creation.name+" </a>"
		frappe.msgprint("Job Card "+job_link+" is created successfuly for sample : "+sample_link);

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


