cur_frm.fields_dict['sample_id'].get_query = function(doc) {
	return {
		filters: {
			"job_card_status": "Not Available",
			docstatus : 1
			}
	}
}

frappe.ui.form.on("Job Card Creation", {
	refresh: function(frm) {
		if(frm.doc.docstatus===0) {
			cur_frm.add_custom_button(__("From Sample Entry"),
			function() {
				frappe.model.map_current_doc({
					method: "sample_register.sample_register.doctype.sample_entry_register.sample_entry_register.create_job_card",
					source_doctype: "Sample Entry Register",
					get_query_filters: {
						docstatus: 1,
						customer: cur_frm.doc.customer || undefined,
						company: cur_frm.doc.company
					}
				})
			}, "icon-download", "btn-default")
		}
	}
})