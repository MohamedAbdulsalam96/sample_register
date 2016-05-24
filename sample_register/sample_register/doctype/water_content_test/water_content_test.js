// Copyright (c) 2016, indictrans and contributors
// For license information, please see license.txt


cur_frm.add_fetch('item_code', 'item_name', 'item_name');
cur_frm.add_fetch('fixed_asset_serial_number', 'item_code', 'item_code');
cur_frm.add_fetch('fixed_asset_serial_number', 'calibration_status', 'calibration_status');
cur_frm.add_fetch('fixed_asset_serial_number', 'next_calibration_date', 'next_calibration_date');


cur_frm.fields_dict.lab_equipment_details.grid.get_field("item_code").get_query = function(doc,cdt,cdn) {
	var d  = locals[cdt][cdn];
		return {
			filters: {
                       "is_asset_item": 1
               }
		}
}
cur_frm.fields_dict.lab_equipment_details.grid.get_field("fixed_asset_serial_number").get_query = function(doc,cdt,cdn) {
	var d  = locals[cdt][cdn];
	if(d.item_code){
		return {
			filters: {
                       "item_code": d.item_code
               }
		}
	}
}
frappe.ui.form.on('Water Content Test', {
	refresh: function(frm) {

	}
});
