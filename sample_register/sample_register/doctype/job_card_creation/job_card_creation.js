cur_frm.add_fetch('item_code', 'item_name', 'item_name');
cur_frm.add_fetch('item_code', 'test_group', 'test_group');
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
		cur_frm.set_query("item_code", "test_details", function(doc) {
			var sales_order = doc.sales_order
			if(doc.sales_order) {
				return{
					query: "sample_register.sample_register.doctype.job_card_creation.job_card_creation.so_item_code",
					filters: {'parent':sales_order}
				}
			}
		});
	}
})


