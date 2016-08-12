// Copyright (c) 2016, indictrans and contributors
// For license information, please see license.txt

frappe.ui.form.on('Dissolved Gas Analysis', {
	refresh: function(frm) {

	},
	onload: function(frm){
		if(frm.doc.gase_analysis_run1.length <3){
			var gases = { "gases" :["O2","N2","CO2","H2","CO","CH4",
						"C2H6","C2H4","C2H2","C3H8","C3H6"], 
						"gas_name": ["Oxygen","Nitrogen","Carbon","Hydrogen"," Carbon Monoxide","Methane",
						"Ethane","Ethylene","Acetelene","Propane","Propylene"]}

			$.each(gases["gases"], function(i, d) {
                var row = frappe.model.add_child(cur_frm.doc, "Dissolved Gas Analysis Gases Details", "gase_analysis_run1");
                row.gas = gases["gases"][i];
                row.gas_name = gases["gas_name"][i];
            })
            refresh_field("gase_analysis_run1");
		}
	},
	before_submit: function(frm) {
		if(!frm.doc.standard_operating_procedure || !frm.doc.bottle_number) {
			frappe.throw("Please enter Bottle Number & Standard Operating Procedure")
		}
	},
	validate: function(frm){
		var total_con_gas=0;
		var con_gas_length=0;
		if(frm.doc.gase_analysis_run1){
			for(i=0;i<frm.doc.gase_analysis_run1.length;i++){
				if(frm.doc.gase_analysis_run1[i].test_result_status=="Accept" && 
					frm.doc.gase_analysis_run1[i].gas=="H2"){
					total_con_gas += frm.doc.gase_analysis_run1[i].concentration;
					con_gas_length +=1;
				}
			}
			frm.set_value("hydrogen",frm.doc.total_gas_contents*100*(total_con_gas/con_gas_length));
		}
		var total_con_gas=0;
		var con_gas_length=0;
		if(frm.doc.gase_analysis_run1){
			for(i=0;i<frm.doc.gase_analysis_run1.length;i++){
				if(frm.doc.gase_analysis_run1[i].test_result_status=="Accept" && 
					frm.doc.gase_analysis_run1[i].gas=="O2"){
					total_con_gas += frm.doc.gase_analysis_run1[i].concentration;
					con_gas_length +=1;
				}
			}
			frm.set_value("oxygen",frm.doc.total_gas_contents*100*(total_con_gas/con_gas_length));
		}
		if(frm.doc.gase_analysis_run1){
			var total_con_gas=0;
			var con_gas_length=0;
			for(i=0;i<frm.doc.gase_analysis_run1.length;i++){
				if(frm.doc.gase_analysis_run1[i].test_result_status=="Accept" && 
					frm.doc.gase_analysis_run1[i].gas=="N2"){
					total_con_gas += frm.doc.gase_analysis_run1[i].concentration;
					con_gas_length +=1;
				}
			}
			frm.set_value("nitrogen",frm.doc.total_gas_contents*100*(total_con_gas/con_gas_length));
		}
		if(frm.doc.gase_analysis_run1){
			var total_con_gas=0;
			var con_gas_length=0;
			for(i=0;i<frm.doc.gase_analysis_run1.length;i++){
				if(frm.doc.gase_analysis_run1[i].test_result_status=="Accept" && 
					frm.doc.gase_analysis_run1[i].gas=="CO"){
					total_con_gas += frm.doc.gase_analysis_run1[i].concentration;
					con_gas_length +=1;
				}
			}
			frm.set_value("carbon_monoxide",frm.doc.total_gas_contents*100*(total_con_gas/con_gas_length));
		}
		if(frm.doc.gase_analysis_run1){
			var total_con_gas=0;
			var con_gas_length=0;
			for(i=0;i<frm.doc.gase_analysis_run1.length;i++){
				if(frm.doc.gase_analysis_run1[i].test_result_status=="Accept" && 
					frm.doc.gase_analysis_run1[i].gas=="CH4"){
					total_con_gas += frm.doc.gase_analysis_run1[i].concentration;
					con_gas_length +=1;
				}
			}
			frm.set_value("methane",frm.doc.total_gas_contents*100*(total_con_gas/con_gas_length));
		}
		if(frm.doc.gase_analysis_run1){
			var total_con_gas=0;
			var con_gas_length=0;
			for(i=0;i<frm.doc.gase_analysis_run1.length;i++){
				if(frm.doc.gase_analysis_run1[i].test_result_status=="Accept" && 
					frm.doc.gase_analysis_run1[i].gas=="CO2"){
					total_con_gas += frm.doc.gase_analysis_run1[i].concentration;
					con_gas_length +=1;
				}
			}
			frm.set_value("carbon",frm.doc.total_gas_contents*100*(total_con_gas/con_gas_length));
		}
		if(frm.doc.gase_analysis_run1){
			var total_con_gas=0;
			var con_gas_length=0;
			for(i=0;i<frm.doc.gase_analysis_run1.length;i++){
				if(frm.doc.gase_analysis_run1[i].test_result_status=="Accept" && 
					frm.doc.gase_analysis_run1[i].gas=="C2H6"){
					total_con_gas += frm.doc.gase_analysis_run1[i].concentration;
					con_gas_length +=1;
				}
			}
			frm.set_value("ethane",frm.doc.total_gas_contents*100*(total_con_gas/con_gas_length));
		}
		if(frm.doc.gase_analysis_run1){
			var total_con_gas=0;
			var con_gas_length=0;
			for(i=0;i<frm.doc.gase_analysis_run1.length;i++){
				if(frm.doc.gase_analysis_run1[i].test_result_status=="Accept" && 
					frm.doc.gase_analysis_run1[i].gas=="C2H4"){
					total_con_gas += frm.doc.gase_analysis_run1[i].concentration;
					con_gas_length +=1;
				}
			}
			frm.set_value("ethylene",frm.doc.total_gas_contents*100*(total_con_gas/con_gas_length));
		}
		if(frm.doc.gase_analysis_run1){
			var total_con_gas=0;
			var con_gas_length=0;
			for(i=0;i<frm.doc.gase_analysis_run1.length;i++){
				if(frm.doc.gase_analysis_run1[i].test_result_status=="Accept" && 
					frm.doc.gase_analysis_run1[i].gas=="C2H2"){
					total_con_gas += frm.doc.gase_analysis_run1[i].concentration;
					con_gas_length +=1;
				}
			}
			frm.set_value("acetelene",frm.doc.total_gas_contents*100*(total_con_gas/con_gas_length));
		}
		if(frm.doc.gase_analysis_run1){
			var total_con_gas=0;
			var con_gas_length=0;
			for(i=0;i<frm.doc.gase_analysis_run1.length;i++){
				if(frm.doc.gase_analysis_run1[i].test_result_status=="Accept" && 
					frm.doc.gase_analysis_run1[i].gas=="C3H8"){
					total_con_gas += frm.doc.gase_analysis_run1[i].concentration;
					con_gas_length +=1;
				}
			}
			frm.set_value("propane",frm.doc.total_gas_contents*100*(total_con_gas/con_gas_length));
		}
		if(frm.doc.gase_analysis_run1){
			var total_con_gas=0;
			var con_gas_length=0;
			for(i=0;i<frm.doc.gase_analysis_run1.length;i++){
				if(frm.doc.gase_analysis_run1[i].test_result_status=="Accept" && 
					frm.doc.gase_analysis_run1[i].gas=="C3H6"){
					total_con_gas += frm.doc.gase_analysis_run1[i].concentration;
					con_gas_length +=1;
				}
			}
			frm.set_value("propylene",frm.doc.total_gas_contents*100*(total_con_gas/con_gas_length));
		}


		frm.set_value("tdcg_per_tgc",(frm.doc.tdcg/10000)/frm.doc.total_gas_contents);
		var sum = 0;
		sum = (frm.doc.hydrogen + frm.doc.carbon_monoxide + frm.doc.methane + frm.doc.ethane + frm.doc.ethylene + frm.doc.acetelene + frm.doc.propane + frm.doc.propylene)
		frm.set_value("tdcg",sum);
		frm.set_value("tdcg_per_tgc",(frm.doc.tdcg/10000/frm.doc.total_gas_contents));
		frm.set_value("tdcg_per_tgc",(frm.doc.tdcg/10000/frm.doc.total_gas_contents));
	}
});



