# Exercise 2 — Live Shopify Listing SEO Auditing

## Scenario

Christine is preparing a batch of 10 new product listings for the Shopify storefront. Before publishing, she needs to cross-check every listing's metadata — title tags, meta descriptions, image alt text, and body copy — against a target keyword spreadsheet. The listing-verification skill will flag missing keywords, broken metadata, duplicate content, and SEO compliance gaps.

## Learning Objectives

- Parse structured product listing exports against keyword target tables
- Scan title tags, meta descriptions, body HTML, and image alt text for keyword presence
- Audit metadata length, brand suffix, and duplicate content
- Generate a per-product violation report with pass/fail grading
- Export a structured SEO audit report

## Dataset

### Product Listings (`shopify_listings_export.csv`)

```csv
sku,product_name,title_tag,meta_description,body_html,image_alt_tags,category,price,status
SKU-001,CloudSync Starter Kit,Cloud Sync Starter Kit | CloudSync,Start syncing your files across all devices with CloudSync Starter Kit. Fast setup.,"The CloudSync Starter Kit includes everything you need to get started with cloud storage. Features real-time backup and cross-platform access.",Starter kit box,SaaS > Cloud Storage,29.99,published
SKU-002,CloudSync Pro Bundle,"","Power users need the Pro Bundle. Features include unlimited storage and priority support.","Includes Pro software license, 2TB storage, and priority support line.","Pro bundle photo product image main product photo",SaaS > Cloud Storage,99.99,published
SKU-003,Enterprise Sync Server,Enterprise Sync Server Deployment | CloudSync,Deploy CloudSync Enterprise on your infrastructure. On-premise solution with full compliance.,"Enterprise-grade sync server for on-premise deployment. Supports LDAP, SAML, and custom retention policies.","Enterprise server rack installation photo hardware",SaaS > Enterprise,499.99,draft
SKU-004,USB Recovery Drive,USB Recovery Drive | CloudSync,Backup your recovery keys to a physical USB drive. Compatible with all CloudSync plans.,"Physical USB drive pre-loaded with recovery software. Plug and play setup.","USB drive flash drive recovery device",Accessories,19.99,published
SKU-005,CloudSync Mobile App License,Mobile App License - Annual Subscription | CloudSync,"Take your files on the go with the CloudSync mobile app. Access, share, and backup from your phone.","Annual subscription for CloudSync mobile app. Includes all premium features: offline access, auto-camera backup, and file sharing.","Mobile app phone screenshot cloud app icon",SaaS > Mobile,14.99,published
SKU-006,Team Collaboration Add-on,Team Collaboration Add-on | CloudSync,"Add team collaboration features to your CloudSync plan. Shared folders, comments, and activity feeds.","Team plan add-on enabling shared workspaces, real-time co-authoring, and audit logging.","Collaboration workspace team dashboard screenshot",SaaS > Business,49.99,published
SKU-007,CloudSync API Access,CloudSync API Access License | CloudSync,"Developer license for CloudSync API access. Build custom integrations and automations.","REST API access license with rate limit of 1000 req/min. Includes webhooks and SDK examples.","API documentation code snippet developer tools",SaaS > Developer,39.99,published
SKU-008,CloudSync Lifetime Plan,"","","One-time purchase for lifetime CloudSync access. Includes 500GB storage and all core features.","Lifetime plan special offer badge image",SaaS > Cloud Storage,299.99,draft
SKU-009,Enterprise Audit Module,Enterprise Audit Module | CloudSync,"Compliance auditing module for CloudSync Enterprise. Track all file access and modifications.","Audit module for Enterprise plan. Provides file access logs, modification history, and compliance reporting.","Audit log compliance dashboard analytics",SaaS > Enterprise,199.99,published
SKU-010,CloudSync Gift Card,"","Give the gift of CloudSync. Digital gift card delivered via email.","Digital gift card redeemable for any CloudSync plan or add-on.","Gift card design certificate email",Gifting,25.00,published
```

### Target Keywords (`keyword_targets.csv` — same file from `../data/`)

```csv
keyword,min_occurrences,field_focus
"cloud sync",3,title_tag+body_html
"real-time backup",2,body_html+meta_description
"enterprise security",2,title_tag+body_html
"cross-platform",1,body_html+meta_description
"file sharing",1,body_html
"cloud storage",1,title_tag+meta_description
```

### Known Issues Planted in the Data

| Issue | Detail |
|---|---|
| Missing title tag | SKU-002 (Pro Bundle) — empty title_tag, will not display in SERP |
| Missing meta description | SKU-008 (Lifetime Plan), SKU-010 (Gift Card) — empty meta_description |
| Generic alt text | SKU-001: "Starter kit box", SKU-003: "Enterprise server rack installation photo hardware", SKU-004: "USB drive flash drive recovery device" — not SEO-optimized |
| Missing target keywords | "enterprise security" not found in any listing copy |
| Duplicate body_html pattern | SKU-007 and SKU-009 share similar "license" / "access" phrasing structure |
| Short title tags | SKU-004 (USB Recovery Drive) title tag has no descriptive keyword beyond product name |
| Published listing with missing metadata | SKU-002 is published but has empty title_tag and generic alt text |

## Walkthrough Steps

```
claude shopify_listings_export.csv --skill listing-verification
```

**Step 1 — Load and inspect listing data:**
```
Step 1 Prompt:
Load shopify_listings_export.csv. Show me:
- Total listings and their statuses (published vs. draft)
- All unique categories
- Which listings have empty or missing title_tag values
- Which listings have empty or missing meta_description values

List all structural issues before running the keyword scan.
```

**Step 2 — Metadata technical audit:**
```
Step 2 Prompt:
For every published listing, run a technical metadata audit:

1. Title tag length — flag any under 30 or over 60 characters
2. Title tag brand suffix — does it end with "| CloudSync"?
3. Meta description length — flag any under 120 or over 158 characters
4. Duplicate title tags — flag any two SKUs sharing the same title tag
5. Missing CTA in meta_description — does it contain a micro-CTA?

Show a table: sku, title_length, title_ok, meta_length, meta_ok, brand_suffix, duplicates
```

**Step 3 — Image alt text audit:**
```
Step 3 Prompt:
Audit every listing's image_alt_tags field:

1. Are any alt tags empty? (non-compliance)
2. Are any alt tags generic? ("image", "photo", "pic", "product image")
3. Does at least one alt tag per listing contain a relevant keyword?
4. Count alt tags per listing — are all images accounted for?

Flag any listing where alt text is generic or missing entirely.
Show: sku, alt_tags_count, has_keyword, generic_flags, status
```

**Step 4 — Keyword compliance scan:**
```
Step 4 Prompt:
Using the target keyword list:

keyword,min_occurrences,field_focus
"cloud sync",3,title_tag+body_html
"real-time backup",2,body_html+meta_description
"enterprise security",2,title_tag+body_html
"cross-platform",1,body_html+meta_description
"file sharing",1,body_html
"cloud storage",1,title_tag+meta_description

Scan every published listing and for each keyword report:
- Occurrences by field (title_tag, meta_description, body_html)
- Whether min_occurrences is met per field
- Per-keyword pass/fail across all listings

Grade each keyword per listing: ✅ Present, ⚠️ Underused, ❌ Missing
```

**Step 5 — Export audit report:**
```
Step 5 Prompt:
Write a CSV called listing_audit_report.csv with all violations found.
Columns: sku, field, issue_type, severity, recommendation.

Then print a terminal summary:

=== LISTING SEO AUDIT REPORT ===
Products scanned:      10
Pass (0 violations):   X
Warnings (1-2):        X
Failed (3+):           X

MOST COMMON ISSUES:
  - Missing target keyword in meta_description   (X products)
  - Empty/missing title_tag                       (X products)
  - Generic alt text                              (X products)
  - Duplicate body_html                           (X products)
  - Missing brand suffix in title_tag             (X products)

KEYWORD COMPLIANCE:
  "cloud sync":         X of 10 listings ✅
  "real-time backup":   X of 10 listings ✅
  "enterprise security": X of 10 listings ❌ (not found in any listing)
  "cross-platform":     X of 10 listings ✅
  "file sharing":       X of 10 listings ✅
  "cloud storage":       X of 10 listings ✅

OVERALL SEO READINESS: [strong / needs work / poor]
```
