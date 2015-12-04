frappe.provide('frappe.pages');
frappe.provide('frappe.views');

var cur_page = null;
frappe.pages['jobcard-creation'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Job Card Creation',
		single_column: true
	});
	$("<table width='100%>\
  <tr>\
    <td valign='top' width='50%'>\
      <div id='myGrid' style='width:600px;height:500px;''></div>\
    </td>\
  </tr>\
</table>").appendTo($(wrapper).find('.layout-main-section'));

	var options = {
		doctype: "Sample Entry Register",
		parent: page
	};

	page.selectview = new frappe.views.JobCard(options,wrapper);
	frappe.breadcrumbs.add("Sample Register");

}

frappe.views.JobCard = frappe.views.GridReport.extend({
	init: function(options, wrapper) {
		this._super({
			title: __("Support Analtyics"),
			page: wrapper,
			parent: $(wrapper).find('.layout-main'),
			page: wrapper.page,
			doctypes: ["Issue", "Fiscal Year"],
		});
	this.page.add_menu_item(__("Create Job"), function() {
		this.create_job();
		}, true);
	},
	make_fun: function(){
            this.page.set_title(__("Dashboard") + " - " + __("Job Card Creation"));

     },
    make: function(){
        this._super();
        this.make_fun();
    },
    create_job: function(){
    	frappe.msgprint("Creating job in JobCard")
     },

	filters: [

		{fieldtype:"Link", label: __("Sample Entry Register"),options:"Sample Entry Register"}
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
		this.columns = std_columns;
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
	var grid;
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
					 me.make_grid(r.message);
					me.waiting.toggle(false);
					  $(function () {
				    var data = [];

				    for (var i = 0; i<r.message.get_sample_data.length; i++) {
				      data[i] = {
				      	checked:false,
				        sampleid: r.message.get_sample_data[i][1],
				        customer: r.message.get_sample_data[i][2],
				        type: r.message.get_sample_data[i][3],
				        priority: 1,
				        standard: "1",
				        test_group: 1
				      };
				    }
				    grid = new Slick.Grid("#myGrid", data, columns, options);


				  })
				}
			}
		});

 this.wrapper.find('[type="checkbox"]').attr(data-id, '3');
$(".plot-check").hide() 
  //slick end

	

		//this.data = [total_tickets, days_to_close, hours_to_close, hours_to_respond];
	},
	//function split to make new grid from frappe.call
	make_grid:function(data){

	},
	//start select test

	  make_gridold:function(data1,doc){
    var me=this
    var query_report=document.getElementById('dynamic')
    var dataView;
    var grid;
    var data = [];

    var options = {
      editable: true,
      asyncEditorLoading: false,
      autoEdit: false,
      enableCellNavigation: true,
      showHeaderRow: true,
      headerRowHeight: 30,
      rowHeight:25,
      explicitInitialization: true,
      multiColumnSort: true,
      forceFitColumns:true,
      enableColumnReorder: false
    };

    var columnFilters = {};
    columns = me.get_columns(doc)

    // this.waiting = frappe.messages.waiting($(cur_frm.fields_dict.query_report.wrapper).find(".waiting-area").empty().toggle(true),
    //  "Loading Report...");

    function filter(item) {
      for (var columnId in columnFilters) {
        if (columnId !== undefined && columnFilters[columnId] !== "") {
          var c = selected_grid_data.getColumns()[selected_grid_data.getColumnIndex(columnId)];
          if (!me.compare_values(item[c.field],columnFilters[columnId],c)) {
            return false;
          }
        }
      }
      return true;
    }

    $(function () {
      var checkboxSelector = new Slick.CheckboxSelectColumn({
      cssClass: "slick-cell-checkboxsel"
    });
    columns.push(checkboxSelector.getColumnDefinition());

    for (var i = 0; i < data1.length; i++) {
      var d = (data[i] = {});
      d["id"] = i;
      for (var j = 0; j < columns.length; j++) {
        d[j] = data1[i][j];
        if(j==4 && d[j]=='1'){
          d[j] = 'Yes'
        }
        else if(j==4){
         d[j] = 'No'
        }
      }
      d[0]=i+1
    }
    dataView = new Slick.Data.DataView();
    this.grid = new Slick.Grid(query_report, dataView, columns, options);
    var me = this
    dataView.onRowCountChanged.subscribe(function (e, args) {
      me.grid.updateRowCount();
      me.grid.render();
    });

    dataView.onRowsChanged.subscribe(function (e, args) {
      me.grid.invalidateRows(args.rows);
      me.grid.render();
    });


    $(this.grid.getHeaderRow()).delegate(":input", "change keyup", function (e) {
      var columnId = $(this).data("columnId");
      if (columnId != null) {
        columnFilters[columnId] = $.trim($(this).val());
        dataView.refresh();
      }
    });

    this.grid.onHeaderRowCellRendered.subscribe(function(e, args) {
        $(args.node).empty();
        $("<input type='text'>")
           .data("columnId", args.column.id)
           .val(columnFilters[args.column.id])
           .appendTo(args.node);
    });

    this.grid.init();

    dataView.beginUpdate();
    dataView.setItems(data);
    dataView.setFilter(filter);
    dataView.endUpdate();
    this.grid.setSelectionModel(new Slick.RowSelectionModel({selectActiveRow: false}));
    this.grid.registerPlugin(checkboxSelector);
    this.grid.onSort.subscribe(function (e, args) {
      var cols = args.sortCols;
      data.sort(function (dataRow1, dataRow2) {
        for (var i = 0, l = cols.length; i < l; i++) {
          var field = cols[i].sortCol.field;
          var sign = cols[i].sortAsc ? 1 : -1;
          var value1 = dataRow1[field], value2 = dataRow2[field];
          var result = (value1 == value2 ? 0 : (value1 > value2 ? 1 : -1)) * sign;
          if (result != 0) {
            return result;
          }
        }
          return 0;
      });
      for (k=0;k<data.length;k++)
      {
        data[k][0]=k+1
      }
      dataView.setItems(data);
    });
      var columnpicker = new Slick.Controls.ColumnPicker(columns, this.grid, options);
      selected_grid_data = this.grid
    })

  },

  //end select test



});
