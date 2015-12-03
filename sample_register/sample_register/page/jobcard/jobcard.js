frappe.provide('frappe.pages');
frappe.provide('frappe.views');
frappe.provide('sample_register');

var cur_page = null;
frappe.pages['jobcard'].on_page_load = function(wrapper) {
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

		this.page.set_primary_action(__("Refresh"),
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
		var std_columns = [
    {id: "check", name: "Check", field: "_check", width: 30, formatter: this.check_formatter},
    {id: "sample_id", name: "Sample Id", field: "sampleid"},
    {id: "customer", name: "Customer", field: "customer"},
    {id: "type", name: "Type", field: "type"},
    {id: "priority", name: "Priority", field: "priority"},
    {id: "standard", name: "Standard", field: "standard"},
    {id: "test_group", name: "Test Group", field: "test_group"}

		];
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
		msgprint("refresh clicked");
		msgprint(this.page.fields_dict.sample_entry_register.get_parsed_value())
		msgprint(grid)

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
	var sam="sam";
	var columns = [
    {id: "check", name: "Check", field: "check", width: 30, formatter: this.check_formatter},
    {id: "sample_id", name: "Sample Id", field: "sampleid"},
    {id: "customer", name: "Customer", field: "customer"},
    {id: "type", name: "Type", field: "type"},
    {id: "priority", name: "Priority", field: "priority"},
    {id: "standard", name: "Standard", field: "standard"},
    {id: "test_group", name: "Test Group", field: "test_group"}
  ];
  var options = {
    enableCellNavigation: true,
    enableColumnReorder: false
  };

		var grid;
  		var data=[];
		 frappe.call({
			method: "sample_register.sample_register.page.dashboard.dashboard.get_sample_data",
			type: "GET",
			args: {
				args:{

				}
			},
			callback: function(r){
				if(r.message){
					me.data = r.message;
					//me.waiting.toggle(false);
					  $(function () {
				    var data = [];

				    for (var i = 0; i<r.message.get_sample_data.length; i++) {
				      data[i] = {
				      	checked:true,
				        sampleid: r.message.get_sample_data[i][1],
				        customer: r.message.get_sample_data[i][2],
				        type: r.message.get_sample_data[i][3],
				        priority: 1,
				        standard: "1",
				        test_group: 1
				      };
				    }
				    grid = new Slick.Grid("#myGrid", data, columns, options);
				    console.log("hiiiiiiiiiiiiiii")
				   console.log($(grid))
				  })
				}
			}
		});

 //this.wrapper.find('[type="checkbox"]').attr(data-id, '3');
//$(".plot-check").hide() 
  //slick end

	

		//this.data = [total_tickets, days_to_close, hours_to_close, hours_to_respond];
	},



});
