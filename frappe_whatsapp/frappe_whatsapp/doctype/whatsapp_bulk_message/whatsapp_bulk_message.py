# import frappe
# import requests
# from frappe.model.document import Document

# class Whatsappbulkmessage(Document):
#     def before_save(self):
#         print("🔥 before_save triggered!")  # Debugging
#         frappe.msgprint("before_save triggered!")  # UI Debugging
        
#         if self.status == "Draft":  # Avoid resending on updates
#             self.send_whatsapp_messages()

#     def send_whatsapp_messages(self):
#         try:
#             # Fetch WhatsApp Settings
#             settings = frappe.get_single("WhatsApp Settings")
#             print(f"Fetched WhatsApp Settings: {settings.as_dict()}")  # Debugging

#             # Securely fetch the access token
#             access_token = settings.get_password("token")  # Use get_password() to fetch securely
#             print(f"Access Token: {access_token[:5]}... (Hidden for security)")  # Debugging

#             # Construct API URL
#             whatsapp_url = f"{settings.url}/{settings.version}/{settings.phone_id}/messages"
#             print(f"API URL: {whatsapp_url}")  # Debugging

#             headers = {
#                 "Authorization": f"Bearer {access_token}",
#                 "Content-Type": "application/json"
#             }

#             # Handle template name format
#             template_parts = self.template_name.rsplit("-", 1)  # Splitting at last hyphen
#             template_name = template_parts[0]  # Extract "hello_world"
#             language_code = template_parts[1] if len(template_parts) > 1 else "en"  # Extract "en_US" or default

#             print(f"Template Name: {template_name}")  # Debugging
#             print(f"Language Code: {language_code}")  # Debugging

#             # Convert parameters from string to list
#             parameters = frappe.parse_json(self.parameters) if self.parameters else []
#             print(f"Parameters: {parameters}")  # Debugging

#             # Convert recipient field into a list (supporting CSV or JSON format)
#             recipients = []
#             try:
#                 recipients = frappe.parse_json(self.recipient)  # JSON format: ["12345", "67890"]
#             except:
#                 recipients = [num.strip() for num in self.recipient.split(",")]  # CSV format: "12345, 67890"

#             print(f"Recipients: {recipients}")  # Debugging

#             failed_numbers = []
#             for recipient in recipients:
#                 payload = {
#                     "messaging_product": "whatsapp",
#                     "recipient_type": "individual",
#                     "to": recipient,
#                     "type": "template",
#                     "template": {
#                         "name": template_name,  # Fixed template name
#                         "language": {"code": language_code},  # Fixed language code
#                         "components": [
#                             {
#                                 "type": "body",
#                                 "parameters": [{"type": "text", "text": param} for param in parameters]
#                             }
#                         ]
#                     }
#                 }
#                 print(f"Sending to {recipient} with Payload: {payload}")  # Debugging

#                 # Send API request
#                 response = requests.post(whatsapp_url, json=payload, headers=headers)
#                 result = response.json()
#                 print(f"API Response for {recipient}: {result}")  # Debugging

#                 if not result.get("messages"):
#                     failed_numbers.append(recipient)
#                     error_msg = result.get("error", {}).get("message", "Unknown Error")
#                     frappe.msgprint(f"❌ Failed to send message to {recipient}: {error_msg}")
#                     print(f"Error: {result.get('error', {})}")  # Debugging

#             # Update status based on success/failure
#             if failed_numbers:
#                 self.status = "Partially Sent" if len(failed_numbers) < len(recipients) else "Failed"
#                 frappe.msgprint(f"Some messages failed: {', '.join(failed_numbers)}")
#             else:
#                 self.status = "Sent"
#                 frappe.msgprint("✅ WhatsApp Messages Sent Successfully!")

#         except Exception as e:
#             print(f"Exception occurred: {e}")  # Debugging
#             frappe.msgprint(f"❌ Exception: {str(e)}")
#             self.status = "Failed"

#         self.save()
#         frappe.db.commit()
#         print("✅ Message status updated and committed.")  # Debugging
# import frappe
# import requests
# from frappe.model.document import Document

# class Whatsappbulkmessage(Document):
#     def before_save(self):
#         print("🔥 before_save triggered!")  # Debugging
#         frappe.msgprint("before_save triggered!")  # UI Debugging
        
#         if self.status == "Draft":  # Avoid resending on updates
#             self.send_whatsapp_messages()

#     def send_whatsapp_messages(self):
#         try:
#             # Fetch WhatsApp Settings
#             settings = frappe.get_single("WhatsApp Settings")
#             print(f"Fetched WhatsApp Settings: {settings.as_dict()}")  # Debugging

#             # Securely fetch the access token
#             access_token = settings.get_password("token")  # Use get_password() to fetch securely
#             print(f"Access Token: {access_token[:5]}... (Hidden for security)")  # Debugging

#             # Construct API URL
#             whatsapp_url = f"{settings.url}/{settings.version}/{settings.phone_id}/messages"
#             print(f"API URL: {whatsapp_url}")  # Debugging

#             headers = {
#                 "Authorization": f"Bearer {access_token}",
#                 "Content-Type": "application/json"
#             }

#             # Handle template name format
#             template_parts = self.template_name.rsplit("-", 1)  # Splitting at last hyphen
#             template_name = template_parts[0]  # Extract "hello_world"
#             language_code = template_parts[1] if len(template_parts) > 1 else "en"  # Extract "en_US" or default

#             print(f"Template Name: {template_name}")  # Debugging
#             print(f"Language Code: {language_code}")  # Debugging

#             # Convert parameters from string to list
#             parameters = frappe.parse_json(self.parameters) if self.parameters else []
#             print(f"Parameters: {parameters}")  # Debugging

#             # ✅ Fetch recipients from both lead and customer tables
#             lead_recipients = [row.whatsapp_no for row in (self.get("lead_recipients") or []) if row.whatsapp_no]
#             customer_recipients = [row.whatsapp_no for row in (self.get("customer_recipients") or []) if row.whatsapp_no]

#             # Combine both lists, removing duplicates
#             recipients = list(set(lead_recipients + customer_recipients))
#             print(f"Recipients from Lead & Customer Tables: {recipients}")  # Debugging

#             if not recipients:
#                 frappe.msgprint("⚠️ No recipients found in the child tables!", alert=True)
#                 return

#             failed_numbers = []
#             for recipient in recipients:
#                 payload = {
#                     "messaging_product": "whatsapp",
#                     "recipient_type": "individual",
#                     "to": recipient,
#                     "type": "template",
#                     "template": {
#                         "name": template_name,  # Fixed template name
#                         "language": {"code": language_code},  # Fixed language code
#                         "components": [
#                             {
#                                 "type": "body",
#                                 "parameters": [{"type": "text", "text": param} for param in parameters]
#                             }
#                         ]
#                     }
#                 }
#                 print(f"Sending to {recipient} with Payload: {payload}")  # Debugging

#                 # Send API request
#                 response = requests.post(whatsapp_url, json=payload, headers=headers)
#                 result = response.json()
#                 print(f"API Response for {recipient}: {result}")  # Debugging

#                 if not result.get("messages"):
#                     failed_numbers.append(recipient)
#                     error_msg = result.get("error", {}).get("message", "Unknown Error")
#                     frappe.msgprint(f"❌ Failed to send message to {recipient}: {error_msg}")
#                     print(f"Error: {result.get('error', {})}")  # Debugging

#             # Update status based on success/failure
#             if failed_numbers:
#                 self.status = "Partially Sent" if len(failed_numbers) < len(recipients) else "Failed"
#                 frappe.msgprint(f"Some messages failed: {', '.join(failed_numbers)}")
#             else:
#                 self.status = "Sent"
#                 frappe.msgprint("✅ WhatsApp Messages Sent Successfully!")

#         except Exception as e:
#             print(f"Exception occurred: {e}")  # Debugging
#             frappe.msgprint(f"❌ Exception: {str(e)}")
#             self.status = "Failed"

import frappe
import requests
from frappe.model.document import Document

class Whatsappbulkmessage(Document):
    def before_save(self):
        frappe.msgprint("before_save triggered!")
        if self.status == "Draft":  # Avoid resending on updates
            self.send_whatsapp_messages()

    def send_whatsapp_messages(self):
        try:
            print("Fetching WhatsApp settings...")
            settings = frappe.get_single("WhatsApp Settings")
            access_token = settings.get_password("token")
            whatsapp_url = f"{settings.url}/{settings.version}/{settings.phone_id}/messages"

            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }

            # Extract template name and language code
            print("🔹 Extracting template name and language code...")
            template_parts = self.template_name.rsplit("-", 1)
            template_name = template_parts[0]
            language_code = template_parts[1] if len(template_parts) > 1 else "en"
            print(f"✅ Template Name: {template_name}, Language Code: {language_code}")

            # Fetch reference doctype from parent document
            reference_doctype = self.reference_doctype
            print(f"🔹 Reference Doctype: {reference_doctype}")

            # Collect recipients from both lead and customer tables
            recipients = []
            
            # Fetch lead recipients
            print("🔹 Fetching lead recipients...")
            for row in (self.get("lead_recipients") or []):
                if row.whatsapp_no:
                    recipients.append((row.whatsapp_no, reference_doctype, row.lead))
                    print(f"Lead Row: {row.as_dict()}")

            # Fetch customer recipients
            print("🔹 Fetching customer recipients...")
            for row in (self.get("customer_recipients") or []):
                if row.whatsapp_no:
                    recipients.append((row.whatsapp_no, reference_doctype, row.customer))
                    print(f"Customer Row: {row.as_dict()}")

            print(f"✅ Recipients Extracted: {recipients}")

            if not recipients:
                frappe.msgprint("⚠️ No recipients found!", alert=True)
                return

            failed_numbers = []
            for recipient, ref_doctype, ref_name in recipients:
                print(f"📨 Fetching data for: {recipient}, Reference: {ref_doctype}, Doc Name: {ref_name}")

                # Fetch reference document
                try:
                    reference_doc = frappe.get_doc(ref_doctype, ref_name)
                    print(f"✅ Reference Document Fetched: {reference_doc.name}")
                except Exception as e:
                    print(f"❌ Error fetching reference document {ref_name}: {str(e)}")
                    failed_numbers.append(recipient)
                    continue

                # Extract parameters dynamically from WhatsApp Message Fields child table
                parameters = []
                print(f"🔹 Extracting parameters for {recipient}...")

                for param in self.get("parameters") or []:  # Accessing child table "parameters"
                    if param.field_name:
                        field_name = param.field_name.strip()
                        
                        # Debugging: Check if the field exists in the document
                        if hasattr(reference_doc, field_name):
                            field_value = getattr(reference_doc, field_name, "")
                            print(f"✅ Found {field_name}: {field_value}")
                        else:
                            field_value = f"[{field_name}]"  # Placeholder for missing fields
                            print(f"⚠️ Field {field_name} not found in {ref_doctype} ({ref_name})")
                        
                        parameters.append(str(field_value))  # Ensure it's a string

                print(f"📌 Final Parameters for {recipient}: {parameters}")

                # Construct payload
                payload = {
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": recipient,
                    "type": "template",
                    "template": {
                        "name": template_name,
                        "language": {"code": language_code},
                    }
                }

                # Only add components if parameters exist
                if parameters:
                    payload["template"]["components"] = [
                        {"type": "body", "parameters": [{"type": "text", "text": param} for param in parameters]}
                    ]

                print(f"📤 Sending payload to {recipient}: {payload}")

                # Send request
                response = requests.post(whatsapp_url, json=payload, headers=headers)
                result = response.json()
                print(f"📨 Response: {result}")

                if not result.get("messages"):
                    failed_numbers.append(recipient)
                    error_msg = result.get("error", {}).get("message", "Unknown Error")
                    frappe.msgprint(f"❌ Failed to send message to {recipient}: {error_msg}")
                else:
                    print(f"✅ Message sent successfully to {recipient}")

            # Update status
            self.status = "Sent" if not failed_numbers else "Failed"
            frappe.msgprint("✅ Messages sent successfully!" if not failed_numbers else f"Some messages failed: {', '.join(failed_numbers)}")

        except Exception as e:
            frappe.msgprint(f"❌ Exception: {str(e)}")
            print(f"❌ Exception: {str(e)}")
            self.status = "Failed"
