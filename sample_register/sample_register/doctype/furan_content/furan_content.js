// Copyright (c) 2016, indictrans and contributors
// For license information, please see license.txt

frappe.ui.form.on('Furan Content', {
	refresh: function(frm) {

	},
	onload: function(frm){
		if(frm.doc.run_one.length <2){
			var gases = { "furans" :["5H2F","2FUR","2 FURALDEHYDE","2ACF","5M2F"], 
						"gas_name": ["Oxygen","Nitrogen","Carbon","Hydrogen"," Carbon Monoxide","Methane",
						"Ethane","Ethylene","Acetelene","Propane","Propylene"]}

			$.each(gases["furans"], function(i, d) {
                var row = frappe.model.add_child(cur_frm.doc, "Furan Content Test Details", "run_one");
                row.furans = gases["furans"][i];
                // row.gas_name = gases["gas_name"][i];
            })
            refresh_field("run_one");
		}
	},
});
