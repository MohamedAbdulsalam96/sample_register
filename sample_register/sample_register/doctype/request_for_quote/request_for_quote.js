
// Fetch company details
cur_frm.add_fetch('company','address','registered_address');
cur_frm.add_fetch('company','phone_no','contact_number');

// Fetch Item details
cur_frm.add_fetch('item_code','item_name','item_name');
cur_frm.add_fetch('item_code','description','item_description');

//fetch terms and confition
cur_frm.add_fetch('tc_name','terms','terms');

//fetch email id
cur_frm.add_fetch('contact','email_id','email_id');


//filter contact
cur_frm.fields_dict["rfq_supplier_details"].grid.get_field("contact").get_query = function(doc,cdt,cdn){
	var item = frappe.get_doc(cdt, cdn);
	return {
               filters:{
                       "supplier": item.supplier
               }
       }
}

//add all supplier email in 'To' field of email
frappe.views.CommunicationComposer =  frappe.views.CommunicationComposer.extend({
    make_fun: function(){
         var me = this;
         var recipients_field = me.dialog.fields_dict.recipients; 

         var custom_rec="";
         for(i=0;i<cur_frm.doc.rfq_supplier_details.length;i++){
         	if(cur_frm.doc.rfq_supplier_details[i].email_id){
         		custom_rec += cur_frm.doc.rfq_supplier_details[i].email_id +","
         	}
         }
         // if(cur_frm.doc.contact_email_ii){custom_rec = custom_rec + ","+cur_frm.doc.contact_email_ii}

         recipients_field.set_input(custom_rec)
    },
    make: function(){
        this._super();
        this.make_fun();
    }
});