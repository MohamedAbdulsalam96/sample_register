cur_frm.fields_dict['sample_id'].get_query = function(doc) {
	return {
		filters: {
			
			"job_card_status": "Not Available"
			}
	}
}

/*frappe.ui.form.on("Job Card Creation", {
	on_submit : function(frm){
		if(frm.doc.status == "Closed") {
		
		}
	}
})*/