
@frappe.whitelist()
def update_invoice_payment(invoice_name, payment_amount , openingEntry):
    
	# Fetch the POS Invoice by its name
	if isinstance(openingEntry, str):
		openingEntry = json.loads(openingEntry)







	# Create a new POS Invoice by duplicating the old one
	pos_invoice = frappe.get_doc('POS Invoice', invoice_name)

	# Create a new POS Invoice by duplicating the old one
	new_pos_invoice = frappe.copy_doc(pos_invoice)


	new_pos_invoice.user = openingEntry["user"]
	new_pos_invoice.pos_profile = openingEntry["pos_profile"]


	#override date to keep the old one
	new_pos_invoice.posting_date = pos_invoice.posting_date

	pos_invoice.cancel() #remove 
	frappe.db.commit()   #remove


	# Convert the outstanding amount to float for comparison
	outstanding_amount = float(new_pos_invoice.outstanding_amount)
	client_payment_amount = float(payment_amount)






















	# Check if the invoice has an outstanding amount
	if outstanding_amount > 0:










		
		if client_payment_amount == outstanding_amount :
			new_pos_invoice.payments[0].amount      += client_payment_amount
			new_pos_invoice.payments[0].base_amount += client_payment_amount
			new_pos_invoice.outstanding_amount      -= client_payment_amount
			new_pos_invoice.status = 'Paid'
			# Save the updated POS Invoice
			new_pos_invoice.save()
			frappe.db.commit()
			new_pos_invoice.submit()  # Resubmit the invoice
			return {
				'real_name'         : new_pos_invoice.name,
				'paid_amount'       : new_pos_invoice.paid_amount,
				'remaining'         : 0,
				'paid'              : new_pos_invoice.status
			}
		elif client_payment_amount > outstanding_amount :
			new_pos_invoice.payments[0].amount += outstanding_amount
			new_pos_invoice.payments[0].base_amount += outstanding_amount
			new_pos_invoice.outstanding_amount = 0
			new_pos_invoice.status = 'Paid'
			rest = client_payment_amount - outstanding_amount
			# Save the updated POS Invoice
			new_pos_invoice.save()
			frappe.db.commit()
			new_pos_invoice.submit()  # Resubmit the invoice
			return {
				'real_name'          : new_pos_invoice.name,
				'paid_amount'        : outstanding_amount,
				'outstanding_amount' : new_pos_invoice.outstanding_amount,
				'remaining'          : rest,
				'paid'               : new_pos_invoice.status
			}
		else:
			new_pos_invoice.payments[0].amount      += client_payment_amount
			new_pos_invoice.payments[0].base_amount += client_payment_amount
			new_pos_invoice.outstanding_amount      -= client_payment_amount
			# Save the updated POS Invoice
			new_pos_invoice.save()
			frappe.db.commit()
			new_pos_invoice.submit()  # Resubmit the invoice
		return {
			'real_name'          : new_pos_invoice.name,
			'paid_amount'        : client_payment_amount,
			'outstanding_amount' : new_pos_invoice.outstanding_amount,
			'remaining'          : 0,
			'paid'               : new_pos_invoice.status
		}
	else:
		return {'error': 'This invoice is already fully paid or has no outstanding amount.'}







