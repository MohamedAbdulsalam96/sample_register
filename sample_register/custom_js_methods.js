frappe.ui.form.on("Quality Inspection", {
	verified: function(frm) {
		frm.set_value("verified_by_name", frappe.user.full_name(frm.doc.verified));
	},

	inspected_by: function(frm) {
		frm.set_value("inspecter_name",frappe.user.full_name(frm.doc.inspected_by))
	},

	validate: function(frm) {
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
	}
})
