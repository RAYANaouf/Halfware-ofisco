


@frappe.whitelist()
def update_invoice_payment(invoice_name, payment_amount , openingEntry):

	if isinstance(openingEntry, str):
		openingEntry = json.loads(openingEntry)








	try:
		pos_invoice = frappe.get_doc('POS Invoice', invoice_name)
		new_pos_invoice = frappe.copy_doc(pos_invoice)

		new_pos_invoice.user = openingEntry["user"]
		new_pos_invoice.pos_profile = openingEntry["pos_profile"]
		new_pos_invoice.posting_date = pos_invoice.posting_date





















		outstanding_amount = float(new_pos_invoice.outstanding_amount)
		client_payment_amount = float(payment_amount)

























		if outstanding_amount <= 0:
			return {'error': 'This invoice is already fully paid or has no outstanding amount.'}














		if not new_pos_invoice.payments:
			new_pos_invoice.append("payments", {
				"mode_of_payment": "Cash",
				"amount": 0,
				"base_amount": 0
			})

		# Do the cancellation after the new copy is ready and validated.
		# Everything below stays inside one transaction so the original is
		# not left cancelled if the new one cannot be submitted.
		pos_invoice.cancel()

		rest = 0
		if client_payment_amount >= outstanding_amount:
			new_pos_invoice.payments[0].amount += outstanding_amount
			new_pos_invoice.payments[0].base_amount += outstanding_amount
			new_pos_invoice.outstanding_amount = 0
			new_pos_invoice.status = 'Paid'
			rest = client_payment_amount - outstanding_amount
		else:
			new_pos_invoice.payments[0].amount += client_payment_amount
			new_pos_invoice.payments[0].base_amount += client_payment_amount
			new_pos_invoice.outstanding_amount -= client_payment_amount

		new_pos_invoice.save()
		new_pos_invoice.submit()

		return {
			'real_name'          : new_pos_invoice.name,
			'paid_amount'        : new_pos_invoice.paid_amount,
			'outstanding_amount' : new_pos_invoice.outstanding_amount,
			'remaining'          : rest,
			'paid'               : new_pos_invoice.status
		}

	except Exception:
		frappe.db.rollback()
		raise


