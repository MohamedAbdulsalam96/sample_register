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
	validate: function(frm) {
		// var total_drift=0;
		// var total_volume=0;
		var total_ir=0;
		var total_length=0;
		if(frm.doc.water_content_test_details){
			for(i=0;i<frm.doc.water_content_test_details.length;i++){
				if(frm.doc.water_content_test_details[i].test__result_status=="Accept"){
					// total_drift += frm.doc.water_content_test_details[i].drift_measured;
					// total_volume += frm.doc.water_content_test_details[i].volume_of_oil;
					total_ir += frm.doc.water_content_test_details[i].instrument_reading;
					total_length +=1;
				}
			}
			// frm.set_value("drift_measured",total_drift/total_length)
			// frm.set_value("volume_of_oil",total_volume/total_length)
			frm.set_value("avg_instrument_reading",total_ir/total_length)
			frm.set_value("final_result",frm.doc.avg_instrument_reading / (frm.doc.volume_of_oil*frm.doc.density_of_oil))

		}

	},
	before_submit: function(frm) {
		if(!frm.doc.standard_operating_procedure || !frm.doc.bottle_number) {
			frappe.throw("Please enter Bottle Number & Standard Operating Procedure")
		}
	},
});
