# Exercise 3 — Customs Tariff & Margin Auditing

## Scenario

Sunny's company imports electronic components from overseas suppliers. The customs broker has been assigning HS (Harmonized System) codes to incoming shipments, but a spot audit revealed several misclassifications that could lead to overpaid duties or customs penalties. Sunny needs to cross-reference every line item on a supplier invoice against the master tariff table and flag discrepancies.

## Learning Objectives

- Cross-reference line-item HS codes against a regulatory tariff table
- Calculate correct duty amounts and compare against charged amounts
- Flag missing country-of-origin data
- Identify misclassified goods that could result in duty overpayment or penalties

## Dataset

### Master Tariff Table (`tariff_regulatory_table.csv`)

```csv
hs_code,description,duty_rate_pct,restrictions
8523.80,Data storage devices (USB, SSD),0.0,none
8471.30,Portable digital computers,0.0,export_license_required
8542.31,Integrated circuits (processors),0.0,none
8536.69,Electrical connectors (USB, HDMI),2.5,none
8504.40,Power supply units (PSU),1.5,none
8517.62,Networking equipment (routers, switches),0.0,export_license_required
9030.33,Testing and measurement equipment,0.0,none
8473.30,Computer parts and accessories,3.5,none
8525.80,Cameras and imaging modules,0.0,none
8507.60,Lithium-ion batteries,3.9,hazardous_material
```

### Supplier Invoice (`supplier_invoice_june.csv`)

```csv
line_id,po_number,item_description,hs_code_declared,quantity,unit_price,line_total,country_of_origin,duty_charged
INV-1,PO-8801,USB 3.0 Flash Drive 128GB,8523.80,500,8.50,4250.00,CN,0.00
INV-2,PO-8801,External SSD 1TB,8523.80,200,45.00,9000.00,CN,0.00
INV-3,PO-8802,Processor Chip X100,8542.31,1000,12.00,12000.00,TW,0.00
INV-4,PO-8802,Processor Chip X200,8542.31,500,28.00,14000.00,,0.00
INV-5,PO-8803,Industrial Power Supply 500W,8504.40,50,85.00,4250.00,CN,63.75
INV-6,PO-8803,Network Switch 24-Port,8517.62,25,320.00,8000.00,CN,0.00
INV-7,PO-8804,USB-C Cable 2m,8536.69,2000,2.50,5000.00,CN,125.00
INV-8,PO-8804,HDMI Cable 3m,8536.69,1500,3.20,4800.00,CN,120.00
INV-9,PO-8805,Laptop Computer Model Z,8471.30,30,850.00,25500.00,CN,0.00
INV-10,PO-8805,Lithium Battery Pack 12V,8507.60,200,35.00,7000.00,CN,273.00
INV-11,PO-8806,Multimeter Digital,9030.33,100,22.00,2200.00,,0.00
INV-12,PO-8806,Motherboard Assembly,8473.30,200,95.00,19000.00,CN,0.00
INV-13,PO-8807,USB-C Hub 7-in-1,8536.69,300,18.00,5400.00,CN,135.00
INV-14,PO-8807,Wireless Router AX6000,8517.62,40,180.00,7200.00,CN,0.00
INV-15,PO-8808,Raspberry Pi Compute Module,8471.30,500,35.00,17500.00,CN,0.00
```

### Known Issues Planted in the Data

| Issue | Detail |
|---|---|
| Misclassified HS code | INV-12 Motherboard should be 8473.30 (3.5%) but duty_charged = 0.00 — possibly declared as 8471.30 (0%) |
| Missing country of origin | INV-4 and INV-11 have blank country_of_origin — customs may reject |
| Export license not checked | INV-6 and INV-14 are networking equipment (8517.62) — restricted, no export license noted |
| Wrong duty calculated | INV-10 8507.60 batteries: 7000.00 * 3.9% = 273.00 (correct) but check others |
| Zero duty on accessories | INV-12 declared as 8473.30 with 0 duty — should be 3.5% × 19000 = 665.00 |

## Walkthrough Steps

```
claude tariff_regulatory_table.csv supplier_invoice_june.csv
```

**Step 1 — Load and join:**
```
Step 1 Prompt:
Load both files. Perform a LEFT JOIN of the supplier invoice against
the tariff table on hs_code (hs_code_declared = hs_code).
Show: line_id, item_description, hs_code_declared, duty_rate_pct,
country_of_origin, line_total, duty_charged.
Flag any row where the hs_code_declared doesn't match any tariff entry.
```

**Step 2 — Calculate correct duty:**
```
Step 2 Prompt:
For each row with a valid tariff match, calculate:
  correct_duty = line_total * (duty_rate_pct / 100)

Compare to duty_charged. Flag any row where:
- abs(correct_duty - duty_charged) > 0.01 (discrepancy)
- duty_charged = 0 but correct_duty > 0 (undercharged)
- country_of_origin is blank

Show: line_id, item_description, correct_duty, duty_charged, deviation, flag.
```

**Step 3 — Identify restrictions and compliance issues:**
```
Step 3 Prompt:
For each row where the tariff table lists a restriction:
- "export_license_required": Flag for compliance — no license evidence exists
- "hazardous_material": Flag for special handling documentation

Show: line_id, item_description, hs_code, restriction, compliance_status.
```

**Step 4 — Calculate total financial impact:**
```
Step 4 Prompt:
Calculate:
1. Total duty_charged across all line items
2. Total correct_duty across all line items
3. Net underpayment or overpayment

Group by hs_code to see which classifications have the largest discrepancies.
Which single line item has the biggest duty gap?
```

**Step 5 — Export audit report:**
```
Step 5 Prompt:
Write a CSV called tariff_audit_report.csv with columns:
line_id, po_number, item_description, hs_code_declared, duty_rate_pct,
country_of_origin, line_total, correct_duty, duty_charged, deviation,
restrictions, compliance_flag, notes

Then print a terminal summary:

=== CUSTOMS TARIFF AUDIT REPORT ===
Total line items:         XX
Correct as declared:      XX
Misclassified (duty gap): X
Missing country of origin: X
Compliance flags:          X

Duty Impact:
  Total charged:          $X,XXX.XX
  Total correct duty:     $X,XXX.XX
  Net underpayment:       $X,XXX.XX  (or overpayment)
  Max single discrepancy: $X,XXX.XX on [item]

Recommended action: [describe next steps]
```
