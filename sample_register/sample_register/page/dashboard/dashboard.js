frappe.pages['dashboard'].on_page_load = function(wrapper) {
	frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Dashboard',
		single_column: true
	});
	$("<div class='meter5' id='job_title' style='padding: 5px;display: inline-block;'>Job Creation</div>").appendTo($(wrapper).find('.layout-main-section'));
	$("<table class='table table-bordered' style='height:350px;'padding: 15px; width:100%;'>\
	<tr width='100%'>\
	<td width='100%' rowspan='2'><div class='c3' id ='i3'>c3</div></td>\
	</tr>\
  <tr width='100%'>\
  <td width='25%'><div class='c4'  id ='i4'></div></td>\
  </tr>\
	</table>").appendTo($(wrapper).find('.layout-main-section'));
	new frappe.assign(wrapper);

}	

frappe.assign = Class.extend({
	init: function(wrapper) {
		this.wrapper = wrapper;
		this.body = $(this.wrapper).find(".assignt");

		this.setup_page();
    this.todo_details();
	},
	setup_page: function(ftv){
		var me = this;
		
		$(me.wrapper).find('.assignr').empty();	 


        // table for My details
        $("<h4>Portal</h4><table class='table table-bordered' style='padding: 5px; width:100%;'>\
        	<tr width='100%'><td colspan='1'><a href='desk#Form/User/Administrator'><font color='blue'><u>My Profile</u></a></td></tr><tr width='100%'>\
          <td colspan='2'><a href='desk#List/Attendance%20Record'><font color='blue'><u>My Cell Meeting's</u></a></td></tr>\
        	<tr width='100%'><td colspan='2'><a href='desk#List/Attendance%20Record'><font color='blue'><u>My Church Meeting's</u></a></td></tr>\
        	</table>").appendTo($(me.wrapper).find('.c1'));
        $(me.wrapper).find('.c1').animate({  width: "100%", opacity: 1.5, fontSize: "1em",  borderWidth: "10px"  }, 1000 );
        $(me.wrapper).find('.c2').animate({  width: "100%", opacity: 1.5, fontSize: "1em",  borderWidth: "10px"  }, 1000 );
        $(me.wrapper).find('.c3').animate({  width: "100%", opacity: 1.5, fontSize: "1em",  borderWidth: "10px"  }, 1000 );
        $(me.wrapper).find('.c4').animate({  width: "100%", opacity: 1.5, fontSize: "1em",  borderWidth: "10px"  }, 1000 );
        $(me.wrapper).find('.c5').animate({  width: "100%", opacity: 1.5, fontSize: "1em",  borderWidth: "10px"  }, 1000 );
		
	} ,

   todo_details:function(){
      frappe.call({
        method:"sample_register.sample_register.page.dashboard.dashboard.get_sample_data",
        callback: function(r) {
        mydata=["<h4>ToDo's</h4><table cellspacing='10'>"];
        for(i=0;i<r.message.get_sample_data.length;i++) {
            str="<tr><td ><p><a href='desk#Form/Sample Entry Register/"+r.message.get_sample_data[i][1]+"'><font color='blue'>"+r.message.get_sample_data[i][1]+"</font>&nbsp;&nbsp;&nbsp;</a> </td><td> "+r.message.get_sample_data[i][2]+"&nbsp;&nbsp;&nbsp;</td><td>"+r.message.get_sample_data[i][3]+"</p></tr>";
            mydata.push(str);
        } 
        $('.c3').html(mydata);
      }
      });
    
   },


});
