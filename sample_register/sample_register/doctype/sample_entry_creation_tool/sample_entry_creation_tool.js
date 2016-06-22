cur_frm.add_fetch('order','customer','customer');
cur_frm.add_fetch('functional_location','functional_location_code','functional_location_code')
cur_frm.add_fetch('equipment','equipment_code','equipment_code');
cur_frm.add_fetch('equipment','equipment_make','equipment_make');
cur_frm.add_fetch('equipment','serial_number','serial_number');

// cur_frm.fields_dict['order'].get_query = function(doc) {
// 	return {
// 		filters: {			
// 			"customer": doc.customer
// 		}
// 	}
// }
// Return query for getting technical contact name in link field
cur_frm.fields_dict['technical_contact'].get_query = function(doc) {
	return {
		filters: {
			
			"technical_contact": 1,
			"customer":doc.customer
		}
	}
}
cur_frm.fields_dict['sample_entry_creation_tool_details'].grid.get_field("functional_location").get_query = function(doc) {
	return {
		filters: {
			
			"customer": doc.customer
		}
	}
}
cur_frm.fields_dict['sample_entry_creation_tool_details'].grid.get_field("equipment").get_query = function(doc) {
	return {
		filters: {
			
			"customer": doc.customer
		}
	}
}
frappe.ui.form.on("Sample Entry Creation Tool", {
	refresh: function(frm) {
		frm.disable_save();
	},
	
	set_date_of_receipt: function(frm) {
		return frappe.call({
			method: "set_date_of_receipt",
			doc: frm.doc,
			callback: function(r, rt){
				frm.refresh()
			}
		});
	},
	create_sample_entry: function(frm){
		return frappe.call({
			method: "create_sample_entry",
			doc: frm.doc,
			callback: function(r, rt){
				frm.refresh()
			}
		})
	},
	update_sample_entry: function(frm){
		return frappe.call({
			method: "update_sample_entry",
			doc: frm.doc,
			callback: function(r, rt){
				frm.refresh()
			}
		})
	},
	get_relevant_entries: function(frm) {
		return frappe.call({
			method: "get_details",
			doc: frm.doc,
			callback: function(r, rt) {
				frm.refresh()
			}
		});
	},

	date_of_receipt: function(frm){
		cur_frm.set_value("from_date", frm.doc.date_of_receipt);
		cur_frm.set_value("to_date", frm.doc.date_of_receipt);
		cur_frm.set_value("filter_based_on_date_of_receipt", 1);
		
	},
	to_date: function(frm){
		cur_frm.set_value("filter_based_on_date_of_receipt", 1);
		
	}
});

// frappe.ui.form.on("Contract", "closing_date", function(frm,doctype,name) {
// 	if(frm.doc.closing_date && frm.doc.start_date){
// 		var closing_date = new Date(frm.doc.closing_date);
// 		var order_date = new Date(frm.doc.start_date);
// 		if(closing_date<order_date){
// 			msgprint("Contract Closing Date must be greater than order date");
//                         validated = false;
//                }
// 	}

// });
// frappe.ui.form.on("Contract", "start_date", function(frm,doctype,name) {
// 	if(frm.doc.closing_date && frm.doc.start_date){
// 		var closing_date = new Date(frm.doc.closing_date);
// 		var order_date = new Date(frm.doc.start_date);
// 		if(order_date>closing_date){
// 			msgprint("Contract Start Date must be small than Closing Date");
//                         validated = false;
//                 }
// 	}

// });
// frappe.ui.form.on("Contract", "validate", function(frm,doctype,name) {
// 	if(frm.doc.closing_date && frm.doc.start_date){
// 		var closing_date = new Date(frm.doc.closing_date);
// 		var order_date = new Date(frm.doc.start_date);
// 		if(order_date>closing_date){
// 			msgprint("Contract Start Date must be small than Closing Date");
//                         validated = false;
//                 }
// 	}

// });
