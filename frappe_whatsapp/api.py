import frappe

@frappe.whitelist(allow_guest=True)
def whatsapp_data_deletion(user_id=None):
    if not user_id:
        frappe.throw("Missing user_id")

    # Get messages where the 'from' or 'to' field matches the user_id
    from_messages = frappe.get_all(
        "WhatsApp Message",
        filters={"from": user_id},
        pluck="name"
    )
    to_messages = frappe.get_all(
        "WhatsApp Message",
        filters={"to": user_id},
        pluck="name"
    )

    # Combine and remove duplicates
    all_messages = set(from_messages + to_messages)

    # Delete the messages
    for message_name in all_messages:
        frappe.delete_doc("WhatsApp Message", message_name, ignore_permissions=True)

    frappe.db.commit()

    # Return a success confirmation (Meta expects a URL usually)
    return {
        "url": f"http://127.0.0.1:8000/data-deletion-confirmation?user_id={user_id}"
    }
