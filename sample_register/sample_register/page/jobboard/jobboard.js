frappe.provide('frappe.pages');
frappe.provide('frappe.views');
frappe.provide('sample_register');
frappe.require("assets/frappe/js/lib/slickgrid/slick.grid.js");
frappe.require("assets/frappe/js/lib/slickgrid/slick.grid.css");
frappe.require("assets/frappe/js/lib/slickgrid/slick.core.js");
frappe.require("assets/frappe/js/lib/slickgrid/slick.editors.js");
frappe.require("assets/frappe/js/lib/slickgrid/slick.formatters.js");
frappe.require("assets/frappe/js/lib/slickgrid/plugins/slick.checkboxselectcolumn.js");
frappe.require("assets/frappe/js/lib/slickgrid/plugins/slick.rowselectionmodel.js");
frappe.require("assets/frappe/js/lib/slickgrid/plugins/slick.autotooltips.js");
frappe.require("assets/frappe/js/lib/slickgrid/plugins/slick.cellrangedecorator.js");
frappe.require("assets/frappe/js/lib/slickgrid/plugins/slick.cellrangeselector.js");
frappe.require("assets/frappe/js/lib/slickgrid/plugins/slick.cellcopymanager.js");
frappe.require("assets/frappe/js/lib/slickgrid/plugins/slick.cellexternalcopymanager.js");
frappe.require("assets/frappe/js/lib/slickgrid/plugins/slick.cellselectionmodel.js");
frappe.require("assets/frappe/js/lib/slickgrid/plugins/slick.rowselectionmodel.js");
frappe.require("assets/frappe/js/lib/slickgrid/plugins/slick.cellselectionmodel.js");

var cur_page = null;
frappe.pages['jobboard'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Job Card Creation',
		single_column: true
	});
	var options = {
		doctype: "Sample Entry Register",
		parent: page
	};
	$("<table width='100%>\
  <tr>\
    <td valign='top' width='50%'>\
      <div id='myGrid' style='width:600px;height:500px;''></div>\
    </td>\
  </tr>\
</table>").appendTo($(wrapper).find('.layout-main-section'));
	setTimeout(function(){
		new new sample_register.JobCard(options, wrapper, page);	
	}, 1)
	frappe.breadcrumbs.add("Sample Register");

}

sample_register.JobCard = Class.extend({
	init: function(opts, wrapper,page) {
		$.extend(this, opts);
		this.make_filters(wrapper);
		this.prepare_data();
			this.page.main.find(".page").css({"padding-top": "0px"});
	//this.page.add_menu_item(__("Create Job"), function() {this.create_job();	}, true);
	},
	make_fun: function(){
            this.page.set_title(__("Dashboard") + " - " + __("Job Card Creation"));

     },
    make: function(){
        this._super();
        this.make_fun();
    },
    make_filters: function(wrapper){
		var me = this;
		this.page = wrapper.page;
		this.page.set_primary_action(__("Create Job Card"),
			function() { me.refresh(); }, "icon-refresh")

		this.department = this.page.add_field({fieldtype:"Link", label:"Sample Entry Register",
			fieldname:"sample_entry_register", options:"Sample Entry Register"});
	},
    create_job: function(){
    	frappe.msgprint("Creating job in JobCard")
     },

	filters: [

		//{fieldtype:"Link", label: __("Sample Entry Register"),options:"Sample Entry Register"}
	],

	setup_columns: function() {
		var std_columns = [];
		//this.make_date_range_columns();
		//this.columns = std_columns;
	},
	check_formatter: function(row, cell, value, columnDef, dataContext) {
		return repl('<input type="checkbox" data-id="%(id)s" \
			class="plot-check" %(checked)s>', {
				"id": dataContext.id,
				"checked": dataContext.checked ? 'checked="checked"' : ""
			})
	},
	refresh: function(){
		//this.check_mandatory_fields()
		var me = this;
		//this.waiting.toggle(true);
		//msgprint(this.page.fields_dict.sample_entry_register.get_parsed_value());
		//msgprint(grid);
		//test selection
//t3 start
			var selectedData = [],
			    selectedIndexes;

			selectedIndexes = grid.getSelectedRows();
			jQuery.each(selectedIndexes, function (index, value) {
			  selectedData.push(grid.getData()[value]);
			});
			//msgprint(selectedData);
			//msgprint("selected samples are:");
			// for(r in selectedData){
			 	//msgprint(selectedData[0]["sampleid"])   //print selected sample id
			// }
			//msgprint(selectedData[0]["sampleid"]);  //selected data contains row data of currently selected checkbox
//t3 end
           // var rows = grid.getData();
            //msgprint(rows[0]["sampleid"]);
           // msgprint(rows[1]["sampleid"]);
            //msgprint(rows[2]["sampleid"]);
            //msgprint(rows);

        //for (r in rows) {
         //       msgprint(rows[r]["sampleid"]); //print all sample id
         //   }
        
		    
		 // frappe prompt box code
		 	var d = frappe.prompt([
	    {label:__("Test Group"), fieldtype:"Link",
						options: "Test Group",
						fieldname:"test_group"},
	    {fieldtype: "Column Break"},
	    {'fieldname': 'select_test', 'fieldtype': 'HTML',options: "Select Test Group<br>", 'label': 'Select Test', 'reqd': 0},
	    {fieldtype: "Section Break"},
	   // {'fieldname': 'comment', 'fieldtype': 'Text', 'label': 'Selected Test', 'reqd': 1},
	    {'fieldname': 'test', 'fieldtype': 'HTML',options: "", 'label': 'test', 'reqd': 0},
	  //  {'fieldtype': 'Button',	'label': __('Add')}, 
	],
	function(values){
	    var c = d.get_values();
		var me = this;
	   //submision of prompt box
        var test_list = [];
        //test_list.push("test_1");
        //test_list.push("test_2");
        //test_list.push("test_3");
        //msgprint(test_list);

        //var test_list_1 = [];
		$(".frappe-control input:checkbox:checked").each ( function() {
			test_list.push($(this).val());
		 	//alert ( $(this).val() );
		});

	   //getting check test
       //msgprint(c.test_group)
       //msgprint(selectedData)
        //create job card against each sample
	     frappe.call({
				method: "sample_register.sample_register.page.jobboard.jobboard.create_job_card_1",
				 args: {
				 	"test_group": c.test_group,
				 	"selectedData":selectedData,
				 	"test_list_unicode":test_list
				 },	
				callback: function(r) {
				if (cur_frm) {
							cur_frm.reload_doc();
						}
				}
			});

	  //   return frappe.call({
			// 	method: "sample_register.sample_register.page.jobboard.jobboard.create_job_card",
			// 	 args: {
			// 	 	"test_group": c.test_group
			// 	 },	
			// 	callback: function(r) {
			// 	if (cur_frm) {
			// 				cur_frm.reload_doc();
			// 			}
			// 	}
			// });
	},
	'Select Test',
	'Submit'
	);
		d.get_input("test_group").on("change", function() {
		var test_group = d.get_value("test_group");
//get test data

		 frappe.call({
			method: "sample_register.sample_register.page.jobboard.jobboard.get_test_data",
			type: "GET",
			args: {
				"test_group": test_group
			},
			callback: function(r){
				if(r.message){
					me.test_data = r.message;

				// $.each(r.message, function(idx, val){
				// 	 $("<input type='checkbox' name='"+val[0]+"' value='Bike'>"+val[0]+"<br>").appendTo(d.fields_dict.test.wrapper);
				// });
				//for loop to apend data
				    for (var i = 0; i<r.message.get_test_data.length; i++) {
				    	$("<input type='checkbox' class='select' id='_select' name='"+r.message.get_test_data[i][0]+"' value='"+r.message.get_test_data[i][0]+"'>"+r.message.get_test_data[i][0]+"<br>").appendTo(d.fields_dict.test.wrapper);
				    }
				 //end of for loop to apend data

				 //apend selected sample
				$("<p>Selected sample to perform Test: </p>").appendTo(d.fields_dict.select_test.wrapper);
			    for(r in selectedData){
			       $("<p>"+selectedData[r]["sampleid"]+"</p>").appendTo(d.fields_dict.select_test.wrapper);
			    }
				 //end of apend seleted sample

				}
			}
		});
//end of get test data

		//d.set_value("comment", "test related to test group "+test_group); //setting comment
		//d.set_value("test", "test related to test group "+test_group);

		//msgprint("selected test group: "+test_group)

		return false;
	});
//disply selected sample id
		d.get_input("test_group").on("change", function() {

//Working script, will fetch checked value
  // $(".frappe-control input[type=checkbox]:checked").each ( function() {
  //    alert ( $(this).val() );
  // });
	});

//end of display seleted sample id
		 // end of frappe prompt box code
		//test selection

	},

	prepare_data: function() {
		// add Opening, Closing, Totals rows
		// if filtered by account and / or voucher
		var me = this;
	//slick start
	        function requiredFieldValidator(value) {
                if (value == null || value == undefined || !value.length) {
                    return {valid: false, msg: "This is a required field"};
                } else {
                    return {valid: true, msg: null};
                }
            }
	var columns = [];
  var options = {
    enableCellNavigation: true,
    enableColumnReorder: false
  };

		var grid;
  		var data=[];
		 frappe.call({
			method: "sample_register.sample_register.page.jobboard.jobboard.get_sample_data",
			type: "GET",
			args: {
				args:{

				}
			},
			callback: function(r){
				if(r.message){
					me.data = r.message;
					me.make_grid(r.message,columns,options)
					//me.waiting.toggle(false);

				}
			}
		});

 //this.wrapper.find('[type="checkbox"]').attr(data-id, '3');
//$(".plot-check").hide() 
  //slick end

	

		//this.data = [total_tickets, days_to_close, hours_to_close, hours_to_respond];
	},
	//function split to make new grid from frappe.call
	make_grid:function(data1,columns,options){
			$(function () {
		    var data = [];

		    for (var i = 0; i<data1.get_sample_data.length; i++) {
		      data[i] = {
		      	checked:true,
		        sampleid: data1.get_sample_data[i][1],
		        customer: data1.get_sample_data[i][2],
		        type: data1.get_sample_data[i][3],
		        priority: "",
		        standard: "",
		        test_group: ""
		      };
		    }
		    grid = new Slick.Grid("#myGrid", data, columns, options);
		    
		        var checkboxSelector = new Slick.CheckboxSelectColumn({
      			cssClass: "slick-cell-checkboxsel"
   				 });
    			columns.push(checkboxSelector.getColumnDefinition());
			      columns.push(
    {id: "sample_id", name: "Sample Id", field: "sampleid"},
    {id: "customer", name: "Customer", field: "customer"},
    {id: "type", name: "Type", field: "type"},
    {id: "priority", name: "Priority", field: "priority"},
    {id: "standard", name: "Standard", field: "standard"},
    {id: "test_group", name: "Test Group", field: "test_group"}
			       );

			grid = new Slick.Grid("#myGrid", data, columns, options);	
		    grid.setSelectionModel(new Slick.RowSelectionModel({selectActiveRow: false}));
		    grid.registerPlugin(checkboxSelector);

	        var columnpicker = new Slick.Controls.ColumnPicker(columns, grid, options);


		  })


	},
	//new grid end frappe.call
});
