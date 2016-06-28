// Copyright (c) 2016, indictrans and contributors
// For license information, please see license.txt

frappe.ui.form.on('Dissolved Gas Analysis', {
	refresh: function(frm) {

	},
	validate: function(frm){
		frm.set_value("tdcg_per_tgc",(frm.doc.tdcg/10000)/frm.doc.total_gas_contents)
	}
});
