// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt


// Fetch order date ,order name and order expiry date on selection of order id on 'Sample Register Entry' form
cur_frm.add_fetch('order_id','order_date','order_date');
cur_frm.add_fetch('order_id','po_no','order_reference_number');
cur_frm.add_fetch('order_id','customer','customer');
/*cur_frm.add_fetch('order_id','order_expiry_date','order_expiry_date');*/

//fetch equipment code ,make,serial_number,model_no and functional code after selecting equipment, functional location and customer
cur_frm.add_fetch('functional_location','functional_location_code','functional_location_code')
cur_frm.add_fetch('equipment','equipment_code','equipment_code');
cur_frm.add_fetch('equipment','equipment_make','equipment_make');
cur_frm.add_fetch('equipment','serial_number','serial_number');
cur_frm.add_fetch('equipment','model_no','model_no');
cur_frm.add_fetch('equipment','equipment_address','equipment_address');
cur_frm.add_fetch('customer','customer_name','customer_name');
cur_frm.add_fetch('customer','customer_code','customer_code');

// Return query for getting technical contact name in link field
cur_frm.fields_dict['technical_contact'].get_query = function(doc) {
	return {
		filters: {
			
			"technical_contact": 1,
			"customer":doc.customer
		}
	}
}

// Return query for getting tech address
cur_frm.fields_dict['technical_address'].get_query = function(doc) {
		return {
			filters: {
				'technical_address': 1,
				'customer': doc.customer
			}
		}
	}

// Return query for getting functional location related to specified customer
cur_frm.fields_dict['functional_location'].get_query = function(doc) {
	return {
		filters: {
			
			"customer": doc.customer
		}
	}
}

// Return query for getting equipment against specified customer.
cur_frm.fields_dict['equipment'].get_query = function(doc) {
	return {
		filters: {
			
			"customer": doc.customer
		}
	}
}
			
cur_frm.cscript.technical_address = function(doc,cdt,cdn){

	erpnext.utils.get_address_display(this.frm, "technical_address","address_details");
}



//frappe call for retriveing technical contact details and setting all details to a field
cur_frm.cscript.technical_contact = function(doc,cdt,cdn){
	frappe.call({
			method:"erpnext.crm.doctype.order_register.order_register.get_contact_details",
			args:{"contact": doc.technical_contact},
			callback: function(r) {
				if (r.message){
					doc.technical_contact_details = (r.message['contact_display'] + '<br>' + r.message['contact_person'] + '<br>' + r.message['contact_email'] + '<br>' + r.message['contact_mobile'] + '<br>' + r.message['contact_personal_email'])
					refresh_field('technical_contact_details')
				}
				
			}
		});

}

//without specifying customer sample entry will not be taken
cur_frm.cscript.container_id = function(doc,cdt,cdn){
	var d = locals[cdt][cdn];
	if(doc.customer == null)
		msgprint(__("Please specify") + ": " +
						"customer" + __("Without Customer details No samples can be entered."));
}

cur_frm.cscript.refresh = function(doc, cdt, cdn) {
	if(doc.docstatus == 1 && doc.job_card_status == "Not Available") {
		cur_frm.add_custom_button(__("Create Job Card"),
			function() {
				frappe.model.open_mapped_doc({
						method: "sample_register.sample_register.doctype.sample_entry_register.sample_entry_register.create_job_card",
						frm: cur_frm
				})
			})
		}
	}

frappe.ui.form.on("Sample Entry Register", {
	refresh: function(frm) {
		if(frm.doc.docstatus===0) {
			cur_frm.add_custom_button(__("From Service Request"),
			function() {
				frappe.model.map_current_doc({
					method: "sample_register.sample_register.doctype.service_request.service_request.create_sample_entry",
					source_doctype: "Service Request",
					get_query_filters: {
						docstatus: 1,
						customer: cur_frm.doc.customer || undefined,
						company: cur_frm.doc.company
					}
				})
			}, "icon-download", "btn-default")
		}
	},

	before_submit: function(frm) {
		if(!frm.doc.date_of_collection || !frm.doc.date_of_receipt) {
			frappe.throw("Please enter Date Of Collection & Date of Receipt")
		}
	},
	// Return query for getting order aginst specified customer
	customer: function(frm) {
		if (frm.doc.customer) {
			cur_frm.fields_dict['order_id'].get_query = function(doc) {
				return {
					filters: {
						"customer": doc.customer,
						"docstatus": 1,
						"order_status" : ["in", ["In-Progress", "Open"]]
					}
				}
			}
		}
		else {
			cur_frm.fields_dict['order_id'].get_query = function(doc) {
				return {
					filters: {
						"docstatus": 1,
						"order_status" : ["in", ["In-Progress", "Open"]]
					}
				}
			}
		}
	}
})