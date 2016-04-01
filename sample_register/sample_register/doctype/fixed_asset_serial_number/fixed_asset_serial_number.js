frappe.ui.form.on("Fixed Asset Serial Number", {
	create_todo: function(doc, dt, dn) {
		if(cur_frm.doc.next_calibration_date){
			frappe.call({
				method: "sample_register.sample_register.doctype.fixed_asset_serial_number.fixed_asset_serial_number.create_todo",
				args: {
					item_code: cur_frm.doc.item_code,
					reference_name: cur_frm.doc.name,
					owner : cur_frm.doc.calibration_assigned_to,
					date: cur_frm.doc.next_calibration_date
				}
			})
		}
	}
})