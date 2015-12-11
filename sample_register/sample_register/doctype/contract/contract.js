cur_frm.add_fetch('customer','customer_name','customer_name');
cur_frm.add_fetch('customer','customer_code','customer_code');

frappe.ui.form.on("Contract", "closing_date", function(frm,doctype,name) {
	if(frm.doc.closing_date && frm.doc.start_date){
		var closing_date = new Date(frm.doc.closing_date);
		var order_date = new Date(frm.doc.start_date);
		if(closing_date<order_date){
			msgprint("Contract Closing Date must be greater than order date");
                        validated = false;
               }
	}

});
frappe.ui.form.on("Contract", "start_date", function(frm,doctype,name) {
	if(frm.doc.closing_date && frm.doc.start_date){
		var closing_date = new Date(frm.doc.closing_date);
		var order_date = new Date(frm.doc.start_date);
		if(order_date>closing_date){
			msgprint("Contract Start Date must be small than Closing Date");
                        validated = false;
                }
	}

});
frappe.ui.form.on("Contract", "validate", function(frm,doctype,name) {
	if(frm.doc.closing_date && frm.doc.start_date){
		var closing_date = new Date(frm.doc.closing_date);
		var order_date = new Date(frm.doc.start_date);
		if(order_date>closing_date){
			msgprint("Contract Start Date must be small than Closing Date");
                        validated = false;
                }
	}

});
