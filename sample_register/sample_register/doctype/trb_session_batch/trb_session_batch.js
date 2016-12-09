// Copyright (c) 2016, indictrans and contributors
// For license information, please see license.txt
frappe.provide("sample_register.sample_register");

frappe.ui.form.on("TRB Session Batch", {
	onload: function(frm) {
		return frappe.call({
			method: "get_last_batch",
			doc: frm.doc,
			callback: function(r, rt) {
				console.log(r.message)
				cur_frm.set_value("trb_batch",r.message)
			}
		});

	},
	refresh: function(frm) {
		frm.disable_save();
		frappe.meta.get_docfield("Lab Equipment Details","item_code", cur_frm.doc.name).read_only = 1;
		frappe.meta.get_docfield("Lab Equipment Details","fixed_asset_serial_number", cur_frm.doc.name).read_only = 1;
	},
	// get_relevant_entries: function(frm) {
	// 	return frappe.call({
	// 		method: "get_details",
	// 		doc: frm.doc,
	// 		callback: function(r, rt) {
	// 			frm.refresh()
	// 		}
	// 	});
	// },
	trb_batch: function(frm) {
		get_batch_entries_function(frm)
	},
	get_batch_entries: function(frm) {
		get_batch_entries_function(frm)
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
	close_batch: function(frm) {
		var me = this;
		var d = new frappe.prompt([
		    {'fieldname': 'test', 'fieldtype': 'HTML', 'label': 'test', 'reqd': 0},
			],
			function(values){
			    var c = d.get_values();
				var me = this;
		        var test_list = [];
				$(".frappe-control input:checkbox:checked").each ( function() {
					test_list.push($(this).attr("name"));
				});
			console.log("test_list",test_list);
		    frappe.call({
					method: "close_batch",
					doc: frm.doc,
					 args: {
					 	"test_list":test_list,
					 },	
					callback: function(r) {
						get_batch_entries_function(frm)
					}
			});
		},
		'Select Test to Create TRB Session',
		'Submit'
		);

		frappe.call({
			method: "get_details_from_child_table",
			doc: frm.doc,
			callback: function(r){
				if(r.message.get_items){   

				console.log("get itemsssss",r.message.get_items) 
					$('.frappe-control input:checkbox').removeAttr('checked');

				    html=""
				    html += "<div class='testCont'  style='max-height: 350px;overflow: auto;overflow-x: hidden;min-height:150px'>"
				    for (var i = 0; i<r.message.get_items.length; i=i+1) {
				    	html += "<label style='font-weight: normal;'><input type='checkbox' class='select' id='_select' name='"
				    	+r.message.get_items[i][0]
				    	+"' value='"+r.message.get_items[i][0]+"'> "
				    	+ r.message.get_items[i][1] +" ("
				    	+ r.message.get_items[i][2] +")"
						r.message.get_items[i][3] ? html += " ("
						+ r.message.get_items[i][3] +")":""
				    	html += "</label><br>"
				    }
				   	html += '</div>'	
                  	var wrapper = d.fields_dict.test.$wrapper;
                  	wrapper.empty();
					wrapper.html(html);
				}
			}
		});
	},
});

get_batch_entries_function = function(frm){
			return frappe.call({
			method: "get_batch_entries",
			doc: frm.doc,
			callback: function(r, rt) {
				console.log("\nf",r.message)
				html = frappe.render_template("html_table",{"data":r.message})
				console.log("\nhtml",html)
				frm.refresh();
				$(cur_frm.fields_dict.html_table.wrapper).html(html)

				add_verify_entry($(cur_frm.fields_dict.html_table.wrapper))


			}
		});
},
add_verify_entry = function(wrapper){		
	wrapper.find($('.add-comment').click(function() {
		frappe.call({
			method: "create_verify_entry",
			doc: cur_frm.doc,
			args: {
				test_name: $(this).attr("test-name"),
				test_type: $(this).attr("test-type"),
			},
			callback: function(r, rt) {
				get_batch_entries_function(cur_frm)
			}
		});
    }))
		
}

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
