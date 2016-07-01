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
cur_frm.fields_dict.lab_equipment_details.grid.get_field("fixed_asset_serial_number").get_query = function(doc,cdt,cdn) {
	var d  = locals[cdt][cdn];
	if(d.item_code){
		return {
			filters: {
                       "item_code": d.item_code
               }
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
		var d = new frappe.prompt([
		    {'fieldname': 'test', 'fieldtype': 'HTML', 'label': 'test', 'reqd': 0},
			],
			function(values){
			    var c = d.get_values();
				var me = this;
		        var test_list = [];
		        //get checked 'Test' records
				
				$(".frappe-control input:checkbox:checked").each ( function() {
					test_list.push($(this).attr("name"));
				});

			// console.log("selectedData",selectedData)
			console.log("test_list",test_list);
        //create job card against each sample
		    frappe.call({
					method: "start_session",
					doc: frm.doc,
					 args: {
					 	"test_list":test_list,
					 },	
					callback: function(r) {

					}
			});
		},
		'Select Test to Create TRB Session',
		'Submit'
		);

		// var selectedData = [],
		// selectedIndexes;
		// selectedIndexes = grid.getSelectedRows();
		// jQuery.each(selectedIndexes, function (index, value) {
		// selectedData.push(grid.getDataItem(value));
		// });

			//set sales order items in popup
		frappe.call({
			method: "get_details_from_child_table",
			type: "GET",
			async:false,
			doc: frm.doc,
			callback: function(r){
				if(r.message.get_items){   
				console.log(r.message.get_items) 
				// console.log(r.message.get_items[3]["test_type"])                
                    //remove existing checked checkbox
					$('.frappe-control input:checkbox').removeAttr('checked');

				    html=""
				    html += '<div class="testCont"  style="max-height: 350px;overflow: auto;overflow-x: hidden;min-height:150px">'
				    for (var i = 0; i<r.message.get_items.length; i=i+1) {
				    	// html += "<input type='checkbox' class='select' id='_select' name='"+r.message.get_test_data[i][0]+"' value='"+r.message.get_test_data[i][0]+"'>"+r.message.get_test_data[i][0]+"<br>"
				    	// html += "<div class='row'>  <div class='col-sm-12'>"
				    	html += "<label style='font-weight: normal;'><input type='checkbox' class='select' id='_select' name='"
				    	+r.message.get_items[i]["test_name"]
				    	+"' value='"+r.message.get_items[i]["test_name"]+"'> "
				    	+ r.message.get_items[i]["sample_id"] +" ("
				    	+ r.message.get_items[i]["test_type"] +")"

						r.message.get_items[i]["priority"] ? html += " ("
						+ r.message.get_items[i]["priority"] +")":""

				    	html += "</label><br>"

				    }

				   	html += '</div>'	
                  	var wrapper = d.fields_dict.test.$wrapper;
                  	wrapper.empty();
					wrapper.html(html);


				 // selected_sample_html= "<p>Select Test to Create Job Card</p>"
				 //apend selected sample with sample id
				 // selected_sample_html='<div class="testSelect" style="max-height: 200px;overflow: auto;overflow-x: hidden;min-height:150px">'
				 // selected_sample_html+="<p>Selected sample to perform Test: </p>"
				 //  for(r in selectedData){
			  //      selected_sample_html+="<p>"+selectedData[r]["sampleid"]+"</p>"
			  //   }

			  //   selected_sample_html += '</div>'	
				// var wrapper_sample = d.fields_dict.select_test.$wrapper;
				// wrapper_sample.html(selected_sample_html);
				 //end of apend seleted sample

				}
			}
		});

		// return frappe.call({
		// 	method: "start_session",
		// 	doc: frm.doc,
		// 	callback: function(r, rt){
		// 		frm.refresh()
		// 	}
		// });
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
