// Fetch order date ,order name and order expiry date on selection of order id on 'Sample Register Entry' form
cur_frm.add_fetch('work_order_no','order_date','work_order_date');
cur_frm.add_fetch('work_order_no','customer','customer');
cur_frm.add_fetch('work_order_no','admin_address','address');
cur_frm.add_fetch('work_order_no','admin_address_details','admin_address_details');

cur_frm.cscript.address = function(doc,cdt,cdn){

	erpnext.utils.get_address_display(this.frm, "address","admin_address_details");
}

cur_frm.add_fetch('sample_id','customer','customer');
cur_frm.add_fetch('sample_id','functional_location','code_designation');
cur_frm.add_fetch('sample_id','equipment','equipment');
cur_frm.add_fetch('sample_id','type','type');
cur_frm.add_fetch('sample_id','weather_condition_during_sampling','weather_condition_during_sampling');
cur_frm.add_fetch('sample_id','date_of_receipt','date_of_receipt');
cur_frm.add_fetch('sample_id','date_of_collection','date_of_collection');
cur_frm.add_fetch('sample_id','sample_condition','condition_of_sample');
cur_frm.add_fetch('sample_id','drawn_by','collected_by');
cur_frm.add_fetch('sample_id','serial_number','serial_number');
cur_frm.add_fetch('sample_id','equipment','equipment');
cur_frm.add_fetch('sample_id','model_no','model_no');
cur_frm.add_fetch('equipment','serial_number','serial_number');
cur_frm.add_fetch('sample_id','equipment_make','manufactured_by');
cur_frm.add_fetch('sample_id','technical_contact','technical_contact');
cur_frm.add_fetch('sample_id','technical_contact_details','technical_contact_details');
cur_frm.add_fetch('customer','customer_code','customer_code');



cur_frm.fields_dict['technical_contact'].get_query = function(doc) {
	return {
		filters: {
			
			"technical_contact": 1,
			"customer":doc.customer
		}
	}
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

// cur_frm.add_fetch('order_id','po_no','order_reference_number');
// cur_frm.add_fetch('order_id','order_expiry_date','order_expiry_date');

// //fetch equipment code ,make,serial_number,model_no and functional code after selecting equipment, functional location and customer
// cur_frm.add_fetch('functional_location','functional_location_code','functional_location_code')
// cur_frm.add_fetch('equipment','equipment_code','equipment_code');
// cur_frm.add_fetch('equipment','equipment_make','equipment_make');
// cur_frm.add_fetch('equipment','serial_number','serial_number');
// cur_frm.add_fetch('equipment','model_no','model_no');
// cur_frm.add_fetch('customer','customer_name','customer_name');
