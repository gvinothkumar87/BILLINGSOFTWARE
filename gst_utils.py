def einvoice_json(invoice, items, company, customer):
    # Skeleton mapper — extend as per NIC specification
    return {
        "Version": "1.1",
        "TranDtls": {"TaxSch": "GST", "SupTyp": "B2B"},
        "DocDtls": {"Typ": "INV", "No": invoice.invoice_no, "Dt": invoice.date.strftime("%d/%m/%Y")},
        "SellerDtls": {"Gstin": company.get("gstin"), "LglNm": company.get("name"), "Addr1": company.get("address")},
        "BuyerDtls": {"Gstin": customer.get("gstin") or "URP", "LglNm": customer.get("name"), "Addr1": customer.get("address")},
        "ItemList": [
            {
                "SlNo": str(i+1),
                "PrdDesc": it.get("name"),
                "HsnCd": it.get("hsn"),
                "Qty": it.get("qty"),
                "Unit": it.get("unit") or "NOS",
                "UnitPrice": it.get("rate"),
                "TotAmt": round(it.get("qty") * it.get("rate"), 2),
                "GstRt": it.get("tax_percent"),
            } for i, it in enumerate(items)
        ],
        "ValDtls": {"AssVal": invoice.subtotal, "CgstVal": round(invoice.tax_total/2,2), "SgstVal": round(invoice.tax_total/2,2), "TotInvVal": invoice.grand_total},
    }

def ewaybill_json(invoice, items, company, customer):
    # Skeleton mapper — extend fields as per e-way bill API spec
    return {
        "supplyType": "O",
        "docType": "INV",
        "docNo": invoice.invoice_no,
        "docDate": invoice.date.strftime("%d/%m/%Y"),
        "fromGstin": company.get("gstin"),
        "fromTrdName": company.get("name"),
        "fromAddr1": company.get("address"),
        "toGstin": customer.get("gstin") or "URP",
        "toTrdName": customer.get("name"),
        "toAddr1": customer.get("address"),
        "totalValue": invoice.subtotal,
        "totalInvoiceValue": invoice.grand_total,
        "itemList": [
            {"productName": it.get("name"), "hsnCode": it.get("hsn"), "quantity": it.get("qty"), "taxRate": it.get("tax_percent")}
            for it in items
        ]
    }