frappe.ui.form.on("Quality Inspection", {
	verified: function(frm) {
		frm.set_value("verified_by_name", frappe.user.full_name(frm.doc.verified));
	},

	inspected_by: function(frm) {
		frm.set_value("inspecter_name",frappe.user.full_name(frm.doc.inspected_by))
	},
})

frappe.ui.form.on("Quality Inspection", "validate", function(frm) {
		if(!(frm.doc.inspected_by) || !(frm.doc.verified) && frm.doc.workflow_state == "Inspected"){
			var dialog = new frappe.ui.Dialog({
				title: __("Quality Inspection"),
				fields: [
					{"fieldtype": "Link", "label": __("Inspected By"), "fieldname": "inspected_by", 
					"options":"User", reqd: 1},
					{"fieldtype": "Link", "label": __("Verified By"), "fieldname": "verified",
					 "options":"User", reqd: 1},
					{"fieldtype": "Button", "label": __("Update"), "fieldname": "update"},
				]
			})
			dialog.fields_dict.update.$input.click(function() {
				args = dialog.get_values();
				if(!args) return;
				console.log(args.inspected_by)
				console.log(args.verified)
				cur_frm.set_value("inspected_by",args.inspected_by)
				cur_frm.set_value("verified",args.verified)
				cur_frm.save();
				dialog.hide();
			})
			dialog.show();
		}
		if(frm.doc.inspected_by && frm.doc.workflow_state == "Inspected"){
			frappe.call({
				method: "sample_register.custom_py_methods.send_inspection_mail",
				args: {
					item: frm.doc.item_code,
					inspector: frm.doc.inspected_by,
					verifier: frm.doc.verified,
					name: frm.doc.name
				}
			});
		}
	})

cur_frm.cscript.custom_onload = function(doc, cdt, cdn) {
	if(doc.doctype=="Salary Slip"){	
		frappe.call({
			method: "sample_register.custom_py_methods.absent_days",
			args: {
				"employee": doc.employee,
				"month": doc.month,
				"fiscal_year": doc.fiscal_year
			},
			callback: function(r) {
				if(r.message){
					cur_frm.set_value("absent_days",r.message)
				}
			}
		});
		cur_frm.refresh_fields();
	}
}