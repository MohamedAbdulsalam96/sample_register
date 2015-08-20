// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt



// Fetch customer code , manufactured by on selection of customer and equipmemt make on equipment master type
cur_frm.add_fetch('customer','customer_code','customer_code');
cur_frm.add_fetch('equipment_make','manufactured_by','manufactured_by');