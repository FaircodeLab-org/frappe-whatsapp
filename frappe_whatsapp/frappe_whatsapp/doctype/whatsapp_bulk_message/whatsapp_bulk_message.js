frappe.ui.form.on('Whatsapp bulk message', {
    refresh: function(frm) {
        console.log("🔥 Form Loaded");  
        frm.add_custom_button(__('Add All Leads'), function() {
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Lead",
                    fields: ["name", "whatsapp_no", "mobile_no", "phone"]
                },
                callback: function(response) {
                    if (response.message) {
                        console.log("Leads Fetched:", response.message);  // Debugging

                        // Clear only the Lead Recipients table
                        frm.clear_table("lead_recipients");

                        let leads = response.message;
                        leads.forEach(lead => {
                            let child = frm.add_child("lead_recipients");
                            child.lead = lead.name;
                            child.whatsapp_no = lead.whatsapp_no || lead.mobile_no || lead.phone || "";
                        });

                        frm.refresh_field("lead_recipients");
                        frappe.msgprint(`✅ Added ${leads.length} Leads.`);
                    }
                }
            });
        }).addClass("btn-primary");

        // Add All Customers Button
        frm.add_custom_button(__('Add All Customers'), function() {
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Customer",
                    fields: ["name", "whatsapp_no"]
                },
                callback: function(response) {
                    if (response.message) {
                        console.log("Customers Fetched:", response.message);  // Debugging

                        // Clear only the Customer Recipients table
                        frm.clear_table("customer_recipients");

                        let customers = response.message;
                        customers.forEach(customer => {
                            let child = frm.add_child("customer_recipients");
                            child.customer = customer.name;
                            child.whatsapp_no = customer.whatsapp_no || "";
                        });

                        frm.refresh_field("customer_recipients");
                        frappe.msgprint(`✅ Added ${customers.length} Customers.`);
                    }
                }
            });
        }).addClass("btn-primary");
    }
});


// Handling Lead Recipients Table
frappe.ui.form.on('Lead recipients', {
    lead: function(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        if (row.lead) {
            console.log("Fetching WhatsApp No for Lead:", row.lead);  // Debugging
            frappe.call({
                method: "frappe.client.get_value",
                args: {
                    doctype: "Lead",
                    filters: { name: row.lead },
                    fieldname: ["whatsapp_no"]
                },
                callback: function(response) {
                    console.log("Lead Response:", response);  // Debugging
                    if (response.message && response.message.whatsapp_no) {
                        frappe.model.set_value(cdt, cdn, "whatsapp_no", response.message.whatsapp_no);
                    } else {
                        frappe.msgprint("⚠️ WhatsApp number not found for this Lead.");
                    }
                }
            });
        }
    }
});

// Handling Customer Recipients Table
frappe.ui.form.on('Customer recipients', {
    customer: function(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        if (row.customer) {
            console.log("Fetching WhatsApp No for Customer:", row.customer);  // Debugging
            frappe.call({
                method: "frappe.client.get_value",
                args: {
                    doctype: "Customer",
                    filters: { name: row.customer },
                    fieldname: ["whatsapp_no"]
                },
                callback: function(response) {
                    console.log("Customer Response:", response);  // Debugging
                    if (response.message && response.message.whatsapp_no) {
                        frappe.model.set_value(cdt, cdn, "whatsapp_no", response.message.whatsapp_no);
                    } else {
                        frappe.msgprint("⚠️ WhatsApp number not found for this Customer.");
                    }
                }
            });
        }
    }
});
frappe.ui.form.on('Whatsapp bulk message', {
    refresh: function(frm) {
        // Add All Leads Button
        frm.add_custom_button(__('Add All Leads'), function() {
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Lead",
                    fields: ["name", "whatsapp_no", "mobile_no", "phone"]
                },
                callback: function(response) {
                    if (response.message) {
                        console.log("Leads Fetched:", response.message);  // Debugging

                        // Clear only the Lead Recipients table
                        frm.clear_table("lead_recipients");

                        let leads = response.message;
                        leads.forEach(lead => {
                            let child = frm.add_child("lead_recipients");
                            child.lead = lead.name;
                            child.whatsapp_no = lead.whatsapp_no || lead.mobile_no || lead.phone || "";
                        });

                        frm.refresh_field("lead_recipients");
                        frappe.msgprint(`✅ Added ${leads.length} Leads.`);
                    }
                }
            });
        }).addClass("btn-primary");

        // Add All Customers Button
        frm.add_custom_button(__('Add All Customers'), function() {
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Customer",
                    fields: ["name", "whatsapp_no"]
                },
                callback: function(response) {
                    if (response.message) {
                        console.log("Customers Fetched:", response.message);  // Debugging

                        // Clear only the Customer Recipients table
                        frm.clear_table("customer_recipients");

                        let customers = response.message;
                        customers.forEach(customer => {
                            let child = frm.add_child("customer_recipients");
                            child.customer = customer.name;
                            child.whatsapp_no = customer.whatsapp_no || "";
                        });

                        frm.refresh_field("customer_recipients");
                        frappe.msgprint(`✅ Added ${customers.length} Customers.`);
                    }
                }
            });
        }).addClass("btn-primary");
    }
});

frappe.ui.form.on('Whatsapp bulk message', {
    onload: function(frm) {
        // Prevent duplicate Leads in Lead Recipients Table
        frm.fields_dict["lead_recipients"].grid.get_field("lead").get_query = function(doc, cdt, cdn) {
            let existing_leads = (frm.doc.lead_recipients || [])
                .filter(row => row.lead)
                .map(row => row.lead);

            return {
                filters: [
                    ["Lead", "name", "not in", existing_leads]
                ]
            };
        };

        // Prevent duplicate Customers in Customer Recipients Table
        frm.fields_dict["customer_recipients"].grid.get_field("customer").get_query = function(doc, cdt, cdn) {
            let existing_customers = (frm.doc.customer_recipients || [])
                .filter(row => row.customer)
                .map(row => row.customer);

            return {
                filters: [
                    ["Customer", "name", "not in", existing_customers]
                ]
            };
        };
    }
});

frappe.ui.form.on('Whatsapp bulk message', {
    refresh: function(frm) {
        toggle_reference_doctype(frm);
    },

    show_leads: function(frm) {
        toggle_reference_doctype(frm);
    },

    show_customers: function(frm) {
        toggle_reference_doctype(frm);
    }
});

function toggle_reference_doctype(frm) {
    let show_leads = frm.doc.show_leads;
    let show_customers = frm.doc.show_customers;

    if (show_leads && show_customers) {
        // Hide reference_doctype if both are checked
        frm.toggle_display("reference_doctype", false);
    } else if (show_leads) {
        // Show reference_doctype and set it to Lead
        frm.toggle_display("reference_doctype", true);
        frm.set_value("reference_doctype", "Lead");
    } else if (show_customers) {
        // Show reference_doctype and set it to Customer
        frm.toggle_display("reference_doctype", true);
        frm.set_value("reference_doctype", "Customer");
    } else {
        // Hide reference_doctype if none are checked
        frm.toggle_display("reference_doctype", false);
    }
}
frappe.ui.form.on('Whatsapp bulk message', {
    template_name: function(frm) {
        if (frm.doc.template_name) {
            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "WhatsApp Templates",
                    name: frm.doc.template_name
                },
                callback: function(response) {
                    if (response.message) {
                        let template_content = response.message.template; // Adjust field name if different
                        frm.set_value("template_preview", template_content);
                    }
                }
            });
        } else {
            frm.set_value("template_preview", ""); // Clear preview if no template is selected
        }
    }
});
