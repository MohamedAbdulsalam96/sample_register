// Copyright (c) 2016, indictrans and contributors
// For license information, please see license.txt
frappe.provide("sample_register.sample_register");
cur_frm.fields_dict.lab_equipment_details.grid.get_field("item_code").get_query = function(doc,cdt,cdn) {
	var d  = locals[cdt][cdn];
		return {
			filters: {
                       "is_asset_item": 1
               }
		}
}
frappe.ui.form.on("TRB Session", {

	refresh: function(frm) {
		frm.disable_save();
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
	update_sample_entry: function(frm){
		return frappe.call({
			method: "update_sample_entry",
			doc: frm.doc,
			callback: function(r, rt){
				frm.refresh()
			}
		})
	},
	start_session: function(frm) {
		return frappe.call({
			method: "start_session",
			doc: frm.doc,
			callback: function(r, rt){
				frm.refresh()
			}
		});
	},
});

sample_register.sample_register.TRBSession = frappe.ui.form.Controller.extend({
	onload: function() {
		this.setup_queries();
	},
	setup_queries: function(){
		var me = this;
		me.frm.set_query("test_type", "trb_session_details", function(doc, cdt, cdn) {
				return {
					filters: {"name": ["in", ["Dissolved Gas Analysis",
												"Water Content Test",
												"Neutralisation Value Test",
												"Flash point by Penskey Martin",
												"Interfacial Tension Test",
												"Furan Content"]]}
				}
		});
	}
});

cur_frm.script_manager.make(sample_register.sample_register.TRBSession);
