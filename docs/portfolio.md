# Savanna Retail Group
KABOOKI MICHEAL | 2024-08-27300
[PAGE]
# Portfolio scope and recommendation
**KABOOKI MICHEAL — 2024-08-27300**

SRG should first make its monthly figures traceable and its customer records safe to use. I propose a central MySQL reporting service with a registry of source identities. Stores continue to transact locally. The programme consolidates reporting and definitions without moving every checkout into a service that depends on reliable internet.

The 18-month allowance is UGX 444M: UGX 306M in year one and UGX 138M in the next six months. The first release serves Finance and two pilot stores. Expansion depends on reconciliation and staff handover, with privacy audit preparation completed before month 12.

Only the assignment PDF was supplied. The practical evidence uses generated data with seed 27300: 5,000 customer rows, 1,200 product rows and 60,000 sales covering January–June 2026. The data and all numerical findings are simulated. The brief's 23% duplicate estimate and 8.4% stock variance remain scenario facts; they are not measured findings from these files.

MySQL is the DBMS. Python prepares and evaluates the source extracts; Tableau supplies the interactive presentation. Repository: https://github.com/Joshmute/srg-micheal-edm

The repository preserves scripts, source hashes, cleaned outputs and execution logs so a reviewer can rerun the calculation.

**AI assistance declaration:** OpenAI Codex assisted with drafting, programming, diagrams and verification. This portfolio does not claim that interviews, fieldwork or deployment at SRG occurred. Reusable MySQL and validation utilities share a technical foundation with the companion Joshua portfolio; this version has its own generated records, analysis, design choices and report.

[PAGE]
# A1 | Board memo, page 1 of 2
**To:** The Board of Savanna Retail Group
**From:** Enterprise Data Management Consultant
**Subject:** Approve a controlled reporting and identity programme

The immediate problem is that SRG cannot reliably explain how a transaction becomes a Board figure. Finance spends eleven days reconciling incompatible extracts. Different product codes describe the same item, and customer records cannot be trusted to direct loyalty benefits. A faster database will not settle those disagreements.

Traditional database management concerns storage, queries, backup and availability within a database. Enterprise data management establishes how information is defined, owned, checked, shared and retired across the company. SRG needs both. Hiring two database administrators may improve availability, but it will not authorise a product definition or decide who must report a lost customer export.

The Jinja incident shows why this distinction matters. An unencrypted laptop exposed 9,000 records, and internal reporting took eleven days. That is a failure of export control, device management and escalation. The proposed programme begins with those controls while developing a reconciled sales pipeline. Security cannot wait for the warehouse.

I would resist an immediate replacement of the 23 store systems. Four IT staff, only two with SQL skills, cannot safely support a large platform migration alongside normal retail operations. A central reporting service provides a manageable point for certification. Durable local queues keep stores operational when connectivity fails; the central view must show which stores have not synchronised.

The Board should assign owners now and fund a two-store trial. Finance owns net sales and reconciliation; procurement owns product and unit definitions; customer service owns identity corrections. Success at month 6 means two stores can repeat a daily load, explain every exception, restore their data and rehearse a faster close. A screenshot alone is insufficient evidence.

[PAGE]
# A1 | Board memo, page 2 of 2
## Diagnosis against DAMA-DMBOK
DAMA's knowledge areas [S8] expose gaps beyond database administration. **Governance** is weak because decisions and accountability are unclear. **Architecture** is fragmented across stores and applications. **Modelling** lacks consistent business identifiers. **Storage and operations** exist locally but need common recovery and extract controls.

**Data security** lacks effective protection outside databases. **Integration and interoperability** depend on manual transfers. **Document and content management** need version control for supplier spreadsheets. **Reference and master data management** are missing where customer identities and product codes conflict.

**Data warehousing and business intelligence** need certified measures instead of repeated spreadsheet reconciliation. **Metadata management** must record where measures came from and what they mean. **Data quality management** must prevent repeat defects and monitor exceptions. These are diagnoses from the case, not findings from staff interviews.

The least-developed functions appear to be governance, metadata, identity management and sustained quality control. Storage technology is already present, which is why another database purchase is an incomplete response.

## Authority and evidence
The COO should chair a small council, with the CFO able to withhold certification of financial data. Domain managers must approve definitions and corrections. The DPO needs a direct route to the CEO for unresolved privacy risk. IT implements decisions but should not be left to invent business policy.

At the next Board review, request source-to-report reconciliation, exception age, access-review results and a restore demonstration. Treat duplicate reduction as useful only when the identity method also protects people from false merges. This programme succeeds when ordinary staff can repeat and challenge its controls after the consultant leaves.

[PAGE]
# A1 | Customer information through its lifecycle
![Lifecycle and decision gates](diagrams/lifecycle.png)

At **collection**, cashiers and the loyalty application explain purpose and capture only necessary fields. A provisional local ID supports offline trading. The source stores the permission evidence separately from optional contact data.

During **storage**, IT protects local devices, the landing area and backups. Domain owners approve use in loyalty, support and reporting. A wrong-person match at the **use** stage can expose purchases and points, so identity corrections require review and reversal records.

At **sharing**, the DPO and procurement approve processor terms, destination and minimum fields. Mobile-money reconciliation needs references, not a wholesale customer export. The payer and shopper may be different people.

For **archive and deletion**, the record owner sets purpose-based schedules and holds. IT records deletion requests across sources, the registry and processors. Backups are isolated until expiry, and recovery must reapply deletion records before reconnecting. A forgotten spreadsheet can otherwise undo a valid deletion.

# A2 | Operating charter
The council's purpose is to settle definitions and risk decisions quickly enough for stores to follow them. It meets fortnightly during the pilot, then monthly. Membership uses existing roles: COO, CFO, IT manager, procurement manager and customer-service manager, with the DPO advising and store managers attending issues that affect operations.

The COO approves priorities within the Board's budget. The CFO certifies financial definitions. Procurement and customer service are accountable for their domains. IT maintains the platform and evidence. Stewards spend two protected hours each week investigating defects rather than treating corrections as spare-time work.

The council keeps one decision register, one issue queue and a short monthly control report. A critical privacy or payment incident bypasses the meeting schedule. Ordinary definition disputes go first to the relevant owner, then to the COO after five working days. The RACI in Appendix A covers twelve recurring activities with one accountable role each.

## Three enforceable policies
**Access and export policy.** Classify contact data, identity links and staff records as Restricted. Use individual accounts, least privilege and MFA for administrators. Only encrypted managed devices may receive approved extracts. An export records requester, purpose, recipient and expiry. IT blocks unmanaged access and the owner reviews access quarterly; the DPO samples export records monthly. Exceptions require a dated owner approval and compensating control.

**Master-data policy.** Procurement owns the canonical SKU and unit list. Customer service owns identity links. Source IDs remain traceable, and conflicting values go to a review queue. A shared phone does not justify merging people. Every material correction records evidence, approver and affected systems. A points adjustment requires a separate ledger entry. Repeated violations trigger store coaching and entry-rule changes, not silent central repair.

**Retention and incident policy.** Before launch, owners must approve a schedule by purpose and applicable retention duty. Working customer exports expire after seven days unless renewed; closed support extracts are removed after thirty days. These are proposed operational limits, not statutory periods. Legal holds identify specific records and an owner. Suspected loss is reported immediately through phone or the incident channel. The DPO assesses external notification; managers may not postpone escalation while gathering a perfect account.

## Compliance gaps
Appendix B maps Uganda DPPA sections and regulations, GDPR articles and CCPA provisions to evidence gaps, responsible roles and actions. The EU partnership requires a territorial and transfer assessment; a foreign supplier does not automatically place every SRG operation under GDPR. CCPA is conditional on statutory scope and thresholds, not simply the presence of a Californian visitor [S1–S6,S10].

# A2 | CFO memorandum
**To:** CFO. **Decision requested:** Protect the first control release from cuts that only postpone cost.

The clearest avoidable costs are repeated reconciliation and loss response. For planning, assume eight Finance staff spend four of the eleven closing days on rework, at UGX 120,000 per staff-day. That is UGX 3.84M per close, or UGX 46.08M annually. A two-day reduction in that rework would release UGX 23.04M of annual staff capacity. It is not a cash saving unless overtime, backfill or headcount expenditure actually falls.

A laptop incident could require UGX 12M forensic support, UGX 8M legal and notification work, UGX 5M service-desk capacity and UGX 3M emergency replacement/security work: UGX 28M before compensation, fines or lost trust. These are scenario allowances, not invoices. Finance should obtain local quotations and record actual response hours.

Two enforcement examples show that protection failures can carry substantial consequences: the UK ICO fined British Airways £20M in 2020 and Marriott £18.4M in 2020 [S9]. They illustrate exposure, not a prediction of Uganda's sanction or a direct comparison with SRG's turnover. Do not convert them into a speculative SRG liability.

Approve staged spending and measure benefits against a signed baseline. Payment exceptions are investigation queues, not proven losses. Similarly, the case's 8.4% stock variance is not all recoverable shrinkage. A credible investment case separates released capacity, avoided incidents and independently verified loss reduction.

# B1 | Architecture choice
I recommend a **centralised analytical platform**, with local operational buffering and a source-identity registry. Centralisation describes ownership of certified reporting and processing, not the removal of local POS databases. There are no independently governed analytical marts at each store. The design accepts delayed visibility during outages instead of pretending every store is continuously connected.

Scores range from 1 (poor fit) to 5 (strong fit); weighted score is the sum of weight × score divided by 100.

| Criterion | Weight | Central | Decentral | Federated | Hub/spoke |
| Support effort | 30 | 5 | 1 | 2 | 3 |
| Ownership clarity | 25 | 5 | 2 | 3 | 4 |
| Cost predictability | 20 | 4 | 2 | 2 | 3 |
| Offline tolerance | 15 | 2 | 5 | 4 | 5 |
| Country expansion | 10 | 3 | 3 | 5 | 4 |
| Weighted result | 100 | 4.15 | 2.25 | 2.85 | 3.65 |

Support and ownership receive 55% together because staffing and repeated disagreement are the binding constraints. Local buffering mitigates the central option's weak connectivity score but does not remove delayed reporting. Hub-and-spoke offers flexibility at a higher coordination cost. Reconsider the choice if country teams acquire dedicated engineering capacity or national requirements prevent the planned consolidation.

# B1 | Operational models
![Conceptual retail relationships](diagrams/conceptual-er.png)

A customer may place many orders; an anonymous order has no linked customer. Each order belongs to one store and contains one or more lines. A product appears on many lines. An order may have several payments or none yet. A customer may hold one loyalty account. Products and suppliers have a many-to-many relationship. Circles mean optionality, bars one and forks many.

![Logical retail model](diagrams/logical-er.png)

The logical model resolves suppliers through ProductSupplier and preserves source identifiers through crosswalks. OrderLine uses the order key and line number; Payment has an independent key so split tender and reversals are possible. Foreign keys enforce links, while application transactions must enforce an order having at least one line. MySQL cannot express that last rule as a simple foreign key.

Three assumptions need attention. One customer per order fails for group purchasing; keep the purchaser separate from recipients. One active loyalty account per customer fails during account consolidation; archive previous accounts and transfer value through auditable ledger entries. A product's unit being stable fails when suppliers change pack size; version product attributes and require explicit conversion rather than rewriting historical quantities.

## From repeating groups to third normal form
Consider the simulated source row: order KMB-O000742, member KMB-C00821, Jinja branch, items “KMB-P0012 ×2 at 4,400; KMB-P0045 ×1 at 14,300”, supplier contacts and a repeated customer phone. These example prices illustrate structure and are not a claim about that generated order.

**1NF:** Split the item list into atomic order-line rows with no comma-separated products. **2NF:** Move order date, customer and store into Order because they depend on order_id, not the entire (order_id,line_no) key. Keep quantity and agreed unit price on OrderLine. **3NF:** Move customer contacts, store district and product descriptions to their own tables. Supplier contact depends on supplier_id and belongs in Supplier; ProductSupplier stores the supplier's code for that product.

For a frequent Board query, materialise a daily category/store/currency summary. It reduces repeated scans of order lines but can become stale or diverge after a refund. Rebuild affected dates transactionally and compare totals with the facts. Keep the line-level warehouse authoritative and display the summary's refresh time. A faster incorrect total is not an acceptable trade.

# B2 | Executed quality assessment
Seed 27300 deliberately creates 900 repeated customer rows and 60 repeated product rows. The cleaning process returns 4,100 customer identities and 1,140 products. Exact source-identity repeats can be removed safely; separate IDs with similar contacts remain review candidates.

Percentages below use the rules implemented in src/savanna/quality.py. Accuracy compares four customer attributes or three product attributes with generator truth after harmless formatting normalisation. Completeness is the filled share of required attributes. Validity and consistency apply the declared row-level rules; timeliness requires a parseable updated_at within ninety days of 30 June 2026. Uniqueness uses excess candidate rows for customers and repeated canonical SKUs for products. These differing denominators are retained in results.json.

| Dimension | Customers before | After | Products before | After |
| Accuracy | 92.61% | 100% | 96.81% | 100% |
| Completeness | 89.64% | 100% | 100% | 100% |
| Consistency | 25.00% | 100% | 0% | 100% |
| Timeliness | 80.00% | 80% | 100% | 100% |
| Validity | 84.00% | 100% | 0% | 100% |
| Uniqueness | 85.22% | 100% | 95% | 100% |

Product validity starts at zero because every generated unit uses an unapproved alias. This is a fixture design, not evidence that real SRG products are all unusable. Customer freshness stays at 80%; cleaning a date does not establish that a customer recently confirmed it.

The input contains 358 missing phone values, 268 malformed values, 802 national-format numbers, 1,250 bare international numbers, 1,072 with 00 and 1,250 with +. There are 200 invalid district rows. Date formats comprise 715 ambiguous slash values, 2,857 ISO and 1,428 year-first slash values. The POS contract establishes day-first parsing; without it, ambiguous dates are rejected.

The conservative candidate method finds 739 excess customer rows, or 14.78%, while the generator's identity ledger establishes 900 exact repeats, or 18%. Missing identifying values explain why these are different measures. Neither should be relabelled as the case's estimated 23% person duplication.

Standardisation fixes approved case, whitespace, phone, district, unit and date variants. Verified-contact simulation records support 1,210 missing/invalid attribute replacements with an audit trail. Generator truth is used for assessment rather than wholesale overwrite. Names, contacts and permissions are never guessed. The audit and retained exception files show what happened to each input.

## Prevent recurrence and investigate variance
Appendix C contains fourteen entry and integration checks, including owners and exception handling. Cashiers get actionable validation messages; supplier files receive a pre-import report. The steward reviews exceptions daily, the owner reviews recurring causes weekly, and the council reviews trends monthly. Monitor nulls, rejected dates, mapping gaps, false-match disputes, fresh-source coverage and reconciliation differences. Do not reward a lower exception count obtained by weakening checks.

![Stock variance cause analysis](diagrams/fishbone.png)

The 8.4% stock variance is a case estimate with no supplied denominator. Before attributing causes, reconcile a controlled count at one cutoff: opening stock + receipts + transfers in − transfers out − sales + returns. Check unit conversion and late arrivals first. Trace a sample from physical receipt through Odoo and POS. Separate systemic failures in timing, mapping and approval from entry mistakes in quantity or SKU. Theft remains a hypothesis until evidence supports it; a residual is not an accusation.

# B3 | Registry master data
A registry is the starting style. It records which local IDs refer to an approved enterprise identity while leaving attribute ownership with source systems. It is cheaper to introduce than mandatory central creation, and stores can continue issuing provisional IDs offline. Its limitation is that a correction may take time to reach every source. A read-only consolidated customer view applies agreed survivorship for analysis; that does not authorise silent operational overwrites.

Exact repeated source ID plus equivalent standardised values is an automatic technical duplicate. Across distinct source IDs, the proposed score is 40 for verified phone agreement, 25 for email, 25 for full-name agreement and 10 for district. Scores 85–100 go to priority human review; 60–84 require more evidence; below 60 remain separate. No score alone transfers loyalty value. The implementation exercises candidate scoring; review and consent propagation are design obligations, not a deployed workflow.

Use the most recent verified customer statement for a contact, an approved procurement record for a SKU, and the store register for district. Preserve previous values and provenance. A timestamp from an untrusted device does not automatically win. Marketing withdrawal takes precedence for its purpose; a new contact number is not fresh consent.

A shared phone is common enough to make automatic linking dangerous. Similar names and districts also disadvantage people with common names. Sample both accepted and rejected candidates across districts, script variants and missing-contact groups. Record reviewer disagreement and allow correction without requiring optional demographic fields. A false merge can reveal purchases or transfer points; a missed match leaves fragmentation but is usually easier to reverse.

![Registry exchanges](diagrams/mdm-flows.png)

POS and e-commerce submit local identifiers and verified-change events. Loyalty supplies account claims and points references. CRM consumes permitted contact views and returns purpose-specific changes. Versioned mapping acknowledgements show which systems applied a correction; failed consumers remain visible in the queue. Customer → account → transaction and country → district → branch are explicit hierarchies. Product category → product → supplier code is separate from identity matching. Household grouping is optional, permissioned and never treated as proof that household members are one person.

# B4 | Warehouse and integration
![Central analytical warehouse](diagrams/warehouse.png)

The sales star has one fact row per source/order/line, linked to Date, Customer, Product and Store dimensions. Channel and currency remain explicit. Customer analytical keys are pseudonymous. Returns retain negative quantities and amounts. Inventory snapshots and payment events have different grains and therefore separate fact tables; joining them directly to order lines without aggregation would multiply values.

Five source families supply the warehouse: POS transaction extracts, e-commerce orders, loyalty events, CRM attributes and Odoo inventory. Provider settlement events support the payment fact. Land immutable source copies with counts and hashes, apply source-specific contracts, validate references, resolve approved identities and load dimensions before facts.

![Reconciled batch flow](diagrams/etl.png)

The selected approach is ETL: minimise and validate before data enters the certified warehouse. A restricted landing zone still retains raw evidence. ELT would allow flexible analysis of raw fields after loading but expands sensitive access and warehouse processing responsibilities; SRG's staffing and privacy gaps make that premature.

Product and Store use SCD Type 2: surrogate key, natural key, valid_from, valid_to and current-version control. A changed category or store district closes the old interval and inserts a new row in one transaction. Facts resolve the version valid at business event time. Procedures lock the current row and reject out-of-order history changes for controlled correction. Repeating an unchanged update does not create another version. Tests cover these controls in MySQL.

The generated failure log illustrates three defects. A day-first POS date sent to an ISO parser fails conversion; a lower-case product ID misses an unnormalised lookup; and a retry duplicates already committed rows. Fix the parser using the source contract, canonicalise before lookup and enforce the (source,order,line) business key. Replay identical payloads as no-ops, quarantine conflicting payloads and advance the watermark only after reconciliation. Do not simply skip a failing batch.

The full fixture loads 60,000 accepted rows. Replaying it inserts none. Separate-currency totals are UGX 1,502,003,100; KES 609,850; RWF 5,975,822. The MySQL evidence compares those totals with independent Decimal aggregation. This demonstrates the pipeline on a simulation, not readiness for unknown production files.

## Event processing with limited resources
![Selective event architecture](diagrams/streaming.png)

The sensor fixture contains 728 events and 720 unique IDs; eight are replay duplicates. Its contract includes event_id, store_id, device_id, event_time_utc, count_delta, sequence and schema_version. Add ingestion time at the receiving service. Persist before acknowledgment, deduplicate by device/event ID, use five-minute event-time windows with a ten-minute lateness allowance and retain late-correction counts.

Footfall establishes activity, not stock or fraud. Stock requires sales, receipts, returns and transfers; payment alerts require authenticated provider events and settlement comparisons. Keep those topics separate. A duplicate reference, reversal after dispatch or unusual payment velocity opens a review case, never an automatic accusation. During outages, buffer events and show last-seen time; do not promise live values. Introduce this only at two stores after batch operations pass recovery and support gates.

# C1 | Definitions and lineage
The dictionary in Appendix D contains thirty technical and business elements with source, transformation, owner, frequency, quality condition and classification. Required tags are domain, sensitivity, lifecycle state and certification state. Tags describe obligations; MySQL grants and service controls enforce them. Dictionary changes belong in the same review as schema or KPI changes.

![Monthly active member lineage](diagrams/lineage.png)

A monthly active customer is a distinct resolved customer key with at least one positive-quantity purchase in that calendar month, using the Kampala business date. Anonymous transactions and unresolved identities are excluded and counted separately. Return-only activity does not qualify. Counts across months cannot be summed to obtain unique customers for the whole period.

Changing address from free text to district_code, country and delivery_detail affects checkout, matching inputs, delivery labels, CRM, rights searches, retention searches and district reporting. Introduce a versioned contract, maintain old/new fields during a measured transition and backfill only supported values. Test counts and district totals before retiring the old field. Monthly active customers should remain unchanged because address is not an identity key; a change would expose an unintended dependency.

Apache Atlas supports classifications and lineage APIs but requires hosting and integration capacity [S11]. Microsoft Purview reduces some platform administration while introducing metered-service and connector costs [S12]. I would defer both beyond the first release and operate a versioned dictionary with automatic schema checks. At month 12, assess Atlas if an existing supported platform can host it; otherwise test a capped Purview pilot. Tool adoption needs evidence that it reduces steward work, not just a searchable interface.

# C2 | Security and privacy design
The threat model follows the path from cashier device through transfer, restricted landing, MySQL, dashboards and exports. Attackers include an external intruder, dishonest employee, compromised supplier and finder of a stolen laptop. Honest mistakes and failed recovery are also threats. Appendix E scores twelve risks on likelihood and impact from 1 to 5, with owners and residual targets.

The analyst role can read a certified aggregate view but cannot read raw customer contacts, HR or write facts. Customer stewards can update contact columns, not consent. ETL can load approved retail objects and execute dimension procedures; it cannot administer roles or read HR. HR officers are limited to the HR schema. Cashiers use a store-scoped application account rather than direct SQL. Administrator access is separate, logged and reviewed.

MySQL GRANT/REVOKE scripts and denial evidence accompany the report [S13]. Positive permitted queries run before negative checks, preventing a broken login from being misreported as a successful access control. An administrator capable of changing roles or definer views remains privileged; these tests do not prove endpoint or application security.

Encrypt managed disks, database volumes and backups; require validated TLS in transit. Separate recovery keys from encrypted media and test recovery. HMAC masking removes names and direct contacts while replacing the analytical ID using a secret from the environment. It is pseudonymisation, since linked histories can still identify someone. Public dashboards must contain only the fictitious dataset here; real data needs private access and disclosure review.

The simulated HR extract has 46 employees and deliberately fictitious identifiers. Name, bank account, national ID, salary, health note and next-of-kin contact are Restricted. Health and financial data require especially narrow access. HR data is excluded from the customer pipeline and Tableau upload. Field-level classification is recorded with the execution evidence.

## DPIA for the EU-facing loyalty service
**Scope:** enrolment, points, account support and optional marketing. SRG is controller; the COO sponsors the assessment and the DPO maintains it. No production approval is claimed. Assess GDPR territorial scope and processor/transfer arrangements before launch [S4,S6].

A points service requires an account and transaction ledger, not a compulsory birth date or precise travel history. Offer ordinary purchasing and nonpersonalised rewards without marketing permission. Separate optional choices, explain them plainly and make withdrawal as easy as enrolment. Payment credentials and staff records are outside this purpose.

Initial person-centred risks are wrong merges (5×5=25), account takeover (4×4=16), unclear profiling (4×3=12), failed withdrawal (4×4=16) and difficult cross-border rights (3×4=12). Reviewable identity links, controlled account recovery, understandable notices, tested suppression and processor contracts aim to reduce these respectively to 10, 8, 6, 6 and 8. These are targets pending tests.

Consult shared-phone users, cashiers, customer support and the EU partner. Test a correction, withdrawal, access request and deletion across every processor. Record unresolved risks and alternatives. If unmitigated high risk triggers GDPR Article 36 consultation, wait for that process. Repeat the DPIA after new profiling, a new market or a significant incident. The CEO cannot substitute business acceptance for a legal duty.

## Incident response replacing the Jinja delay
At discovery, staff call the duty contact immediately, using phone/SMS if the network is unavailable. The incident lead records discovery, awareness and escalation times separately. IT revokes sessions, preserves logs and attempts managed lock or wipe without destroying evidence needed for investigation. The DPO assesses records, sensitivity, encryption and likely harm.

Uganda DPPA s23 requires immediate notification where the stated unauthorised-access/acquisition condition is met; Regulation 33 specifies Form 7 [S1,S2]. This must not be replaced by a generic 72-hour target. Where GDPR applies, Article 33 sets notification without undue delay and where feasible within 72 hours of awareness unless risk is unlikely; Article 34 addresses high-risk communication to people [S5]. Record reasons, phases and actual delays honestly.

For Jinja, escalate and assess notification now; the previous eleven-day delay cannot be erased. Do not wait for complete forensics. Communicate verified facts and practical steps without claiming misuse is proven. Within ten working days, the COO reviews why the export and silence occurred, assigns remedial owners and tests the new reporting route. The DPO retains independent escalation, and quarterly exercises include an offline store.

# C3 | Analytics questions and workflow
**Retention:** Which previously active members have stopped buying? Resolve identity, require ninety days of observation, calculate recency and compare cohorts; then test a consented intervention with a holdout.

**Segment growth:** Are Occasional, Routine and Frequent members contributing more purchases or larger baskets? Join versioned segment definitions to sales, compare equivalent periods and separate counts from value. A segment name is an artificial fixture label, not an inferred demographic trait.

**Stock allocation:** Which branch/category combinations warrant a transfer review? Combine net units, reconciled on-hand stock, lead times and transfer cost. Reject stale inputs. Strong sales alone cannot prove stock-outs or profitable transfers.

**Payment review:** Which references fail reconciliation? Link provider events to orders and settlement, retain refunds and age exceptions. Review missing and duplicate references before referring suspected fraud.

**Expansion:** Where would a new outlet be commercially defensible? Combine comparable-store contribution, catchment, rent, distribution costs and market evidence in scenarios. The sales fixture tests the workflow but cannot establish a Kenya or Rwanda investment case.

Prepare native dates using each source's contract, canonical product IDs, signed Decimal amounts and separate currencies. Upload only the approved simulation fields. The dashboard emphasises category mix and branch performance rather than assuming a smooth growth story. Dashboard evidence, native workbook and live URL are recorded in Appendix F after publication.

## Executive findings from the simulation
**The May peak did not persist.** UGX sales fell from 313,275,600 in May to 211,676,900 in June, a 32.43% decline. January was 274,417,200. The Commercial Manager should separate order frequency, returns and basket mix before extending May's staffing or buying plan. The simulation intentionally changes monthly volume; it does not establish seasonality.

**Inactivity deserves a controlled test.** At 1 July, 600 of 4,096 members with sufficient observation had no positive purchase for ninety days: 14.65%. Verify links and permission before outreach. Use a holdout and measure incremental purchases rather than counting every response as recovered business.

**Reconciliation needs an owner.** The UGX queue has 470 unmatched electronic-payment rows with net value UGX 12,017,000. Finance should distinguish absent references, timing and refunds. The six KES and six RWF cases remain in their own currencies. Exceptions are not confirmed fraud or recoverable loss.

These actions depend on real source validation. The dataset contains 3,993 negative-quantity return lines, so omitting returns would overstate performance. No foreign-exchange rate or production refresh claim is introduced.

## Technology and maturity decisions
A managed MySQL service merits a limited pilot because patching and backup operations can consume scarce staff time. It still needs tested recovery, access controls, regional pricing and a transfer assessment. Cap the experiment within the platform allowance; retain an export-and-restore exit plan. Microsoft architecture guidance is a pattern reference, not an SRG quotation [S14].

AI-assisted matching is deferred for automatic decisions. A masked category-suggestion experiment may be worthwhile if measured against a deterministic baseline. Require reviewer acceptance, subgroup error checks and a stop rule for harmful suggestions. A model must not invent missing contacts or infer marketing permission.

On an explicit five-stage scale—ad hoc, repeatable, defined, measured, optimised—the brief suggests an ad hoc starting point. Month 6 targets repeatable loads and incident handling; month 12 defined ownership and contracts; month 24 measured quality and recovery service levels. Optimisation follows trustworthy histories and demonstrable capacity, not a purchased product.

Following Tufte's emphasis on clear data presentation and Few's dashboard principles, reject a 3D pie comparing 23 stores. Depth distorts area and small wedges obstruct comparison. Use ranked zero-baseline bars for branches, a common chronological axis for monthly change and restrained colour for categories. Show currency, period and simulation status; do not use a dual axis to imply that footfall caused sales.

# D1 | Delivery plan and budget
All figures below are UGX millions, including planning allowances rather than supplier quotes. Existing payroll is excluded but protected staff time is required. The Board must fund continuing operations beyond month 18 separately.

| Work package | Months 1–12 | Months 13–18 | Total |
| Engineer and handover | 84 | 30 | 114 |
| Platform and recovery | 30 | 18 | 48 |
| Device and account controls | 42 | 12 | 54 |
| Store connectivity and power | 24 | 12 | 36 |
| Integration and testing | 30 | 18 | 48 |
| Steward training and backfill | 24 | 12 | 36 |
| Privacy and audit support | 24 | 12 | 36 |
| BI pilot and documentation | 12 | 6 | 18 |
| CFO-held contingency | 36 | 18 | 54 |
| Total | 306 | 138 | 444 |

The programme is UGX 36M below a conservative 480M total ceiling and also respects the stated annual limit. Do not double-count contingency as an additional phase budget. The CFO reviews commitments, forecast-to-complete and reserve use monthly.

**Months 1–3, UGX 90M:** stop unmanaged exports, appoint owners, establish incident reporting and source contracts, inventory devices and test recovery. **Months 4–6, UGX 96M:** pilot two stores, reconcile sales and payments, review customer links and rehearse a close within six working days. These quick wins depend on definitions approved in the first phase.

**Months 7–12, UGX 120M:** extend through groups of five stores as checks pass, complete dictionary and rights tests, and prepare audit evidence by month 11. **Months 13–18, UGX 138M:** stabilise all 23 stores, hand over support and trial selective event processing. Ceilings total 444M. Expansion pauses if reconciliation, recovery or support fails.

The two SQL-capable employees each reserve half a day twice weekly; other staff retain checkout support. Domain stewards need two hours weekly, with business managers covering operational duties. Month 18 targets a four-working-day close, 98% of expected daily extracts accounted for, and every critical incident exercise escalated promptly. These are proposed acceptance targets, not achieved outcomes.

## Dependencies across the programme
The product owner defines units; entry checks reject inconsistent packs; the registry preserves source mappings; ETL resolves them into facts; metadata explains each measure; security restricts its use; the dashboard exposes reconciled results. Failure at one step weakens the later steps. A catalogue cannot repair a wrong receipt, and a dashboard cannot make an unreviewed identity link safe.

Measure stock variance only after signing its denominator and cutoff. A target below 5% is provisional until counts establish a baseline. Similarly, duplicate reduction must be accompanied by reviewed precision and correction outcomes. Maintain exceptions visibly rather than driving a dashboard to green through relaxed rules.

# D2 | Red-team assessment
A central reporting service may become the very bottleneck this programme is meant to remove. The two SQL-capable employees could spend their protected time restoring failed store devices. A contractor might understand the load logic better than anyone employed by SRG. After the contract ends, a seemingly simple platform could wait days for a small correction. The budget includes training, but attendance is not competence.

That objection should change the acceptance criteria. A staff member must restore the database, explain a rejected file and replay a load without the contractor operating the keyboard. Demonstrations should include an unfamiliar error and a realistic time limit. Until two employees can perform those tasks, the rollout stays at the pilot. This may delay benefits. Pretending that delivery and handover are separate milestones would conceal the larger risk.

Centralisation also concentrates damage. A stolen administrator credential could expose the registry and interrupt reporting across the group. Separate schemas are not a complete security boundary against the database administrator. Encryption helps with stolen media but does little when an authorised session is misused. A small team may find privileged-account review burdensome and allow convenient shared accounts to return.

The response is to separate ordinary work from privileged maintenance, require named accounts, record elevated changes and test restoration from protected backups. Keep source systems capable of trading without the reporting database. An independent reviewer should sample administrative activity. Even with those measures, some privileged risk remains. The Board should understand it instead of reading a low residual score as a guarantee.

The registry design has a subtler weakness: it preserves local ownership but may leave conflicting contact details in circulation. A customer corrects a phone at checkout, yet CRM still uses the old number. A mapping acknowledgement proves that a message was received, not that the business process now behaves correctly. During a long outage, a suppression change may not reach a store before another campaign interaction.

For that reason, marketing must use the centrally approved permission view and fail closed when permission is uncertain. Operational contact updates need end-to-end tests from request to each consumer. Track unapplied corrections by age, and give customer service a clear route to stop use while a dispute is resolved. The plan accepts delayed consistency for reporting; it cannot casually accept delayed withdrawal for optional marketing.

The cost case is also vulnerable. The UGX 444M total is arithmetic built from allowances. It does not prove that available suppliers will deliver secure connectivity, support and privacy advice at those figures. Taxes, exchange-rate changes and weak power can absorb the reserve quickly. Continuing expenditure after month 18 may be more politically difficult than the initial project allocation.

Procurement should therefore quote the smallest working release first, including support and exit. The CFO should approve commitments against a rolling forecast rather than the original spreadsheet alone. Defer event processing and catalogue software if costs rise; keep recovery, privacy and reconciliation funded. Released staff capacity must not be sold as cash savings without evidence that expenditure actually falls.

Finally, simulated data can make every control appear more reliable than it is. Known identifiers, deliberately injected errors and stable source contracts favour the implemented cleaner. Real records contain contradictions the generator never imagined. A 100% post-cleaning accuracy score is agreement with a constructed truth set, not proof of operational perfection. Before deployment, profile genuine authorised samples, test adverse cases and revise the contracts. The defensible claim is that the repository demonstrates a repeatable method. It does not show that SRG's unknown data has already been repaired.

# D2 | Reflection on enterprise data practice
The case makes the limits of a purely technical response difficult to ignore. I can describe a well-indexed table and still be unable to explain who may change a product's unit or whether a customer agreed to a marketing message. That gap is where enterprise data management becomes a management discipline. The database records a decision; it does not supply the authority or evidence for making it.

My starting point would be to make a small number of measures dependable. An eleven-day close suggests that people are repeatedly negotiating what the data means. A shorter close will only be trustworthy if that negotiation moves into approved definitions and exception handling. Otherwise, automation may produce an uncertain answer sooner. I would rather explain one unresolved source than issue a polished total that hides its absence.

Working with the simulated quality results also requires care in how success is described. The customer output reaches complete and valid contact fields because a deliberately constructed verification source supplies the missing evidence. That would not happen automatically in a real business. Staff would need to contact customers through an appropriate process, record provenance and respect a refusal to provide optional information. The unchanged freshness score is useful because it prevents the cleaning process from claiming an improvement it did not establish.

Identity management raises the strongest ethical concern for me. Two people can share a telephone, a household or a common name. Joining their purchase histories may look efficient while exposing information to the wrong person or moving loyalty value unfairly. An algorithm's high score does not remove that risk. The proposed registry preserves uncertainty and allows review. Its inconvenience is part of the cost of treating customers as people rather than rows that should always fit neatly together.

Uganda's retail conditions also affect what a responsible design looks like. Connectivity and power problems cannot be treated as rare exceptions when staff encounter them during ordinary work. A process that only works online encourages paper notes, shared accounts and informal exports when the network fails. Those workarounds then become data-quality and privacy risks. Local queues, phone-based incident escalation and visible freshness are therefore governance decisions as well as engineering choices.

The Jinja incident changes how I would discuss accountability. It is tempting to focus on the employee who lost the laptop or delayed reporting. Those actions matter, but an organisation also decides whether sensitive exports are permitted, whether devices are managed and whether reporting a mistake leads to blame. A workable response process should make early reporting easier while preserving responsibility for deliberate misuse. Rehearsals and practical contact routes are more useful than a policy that nobody can locate during an incident.

I also need to distinguish what has been tested from what has merely been designed. The SQL tests can show that a particular analyst account is refused a prohibited query. They cannot establish that an administrator will never misuse access or that a device is encrypted. A simulated replay can demonstrate an idempotent loader without proving that every future source will follow the contract. I would keep that boundary explicit in presentations, because exaggerated assurance makes later failures harder to explain and correct.

For professional development, the DAMA framework gives me a way to connect technical skills with ownership, quality, architecture and security. Preparing toward CDMP would require more than memorising the knowledge areas. I would use the framework to examine why a control exists, who needs its result and what evidence shows that it works. Practice with modelling, stewardship and data ethics would be as important as SQL exercises. Certification could structure learning, but it would not substitute for judgement under real operational constraints.

My practical learning priorities would be temporal data modelling, recovery testing and clear communication with nontechnical owners. A slowly changing dimension is easy to describe until a late correction arrives after reports have been issued. Recovery is easy to promise until keys, backups and deletion instructions must work together. I would practise those difficult cases and write short explanations that allow Finance or customer service to decide what trade-off is acceptable.

I would also develop the habit of keeping decisions reversible where possible. A source crosswalk, a versioned definition and an auditable points adjustment make correction less destructive. They preserve the history needed to explain why a result changed. This is particularly valuable when the first design rests on incomplete information, as it does here. The absence of instructor datasets should remain visible rather than being covered by realistic-looking invented results.

The outcome I would want at SRG is modest but useful: staff can trace a figure, a customer can challenge an incorrect record, a lost device is reported promptly, and a failed load can be recovered without one indispensable specialist. Those capabilities create room for more ambitious analytics later. They also give me a clearer standard for my own work: make claims proportional to evidence, state uncertainty plainly and leave a process that other people can operate and question.

[PAGE]
# Appendix A | Responsibility assignment
A = accountable; R = responsible; C = consulted; I = informed. Role names use existing organisational positions; DPO denotes the designated privacy responsibility.

| Activity | A | R | C | I |
| Approve priorities | COO | Council | CFO, IT | Board |
| Define net sales | CFO | Finance analyst | Store managers | COO |
| Approve product units | Procurement manager | Product steward | Suppliers, IT | Stores |
| Correct customer links | Customer-service manager | Customer steward | DPO | IT |
| Operate extracts | IT manager | SQL staff | Stores | CFO |
| Certify monthly close | CFO | Finance analyst | IT | Board |
| Review access | Domain owner | IT | DPO | COO |
| Report privacy breach | DPO | Incident lead | IT, counsel | CEO |
| Fulfil rights requests | DPO | Customer service | IT | COO |
| Apply retention | Domain owner | IT | DPO | Council |
| Test recovery | IT manager | SQL staff | CFO | COO |
| Approve supplier sharing | Procurement manager | Procurement staff | DPO | Council |

# Appendix B | Compliance register
Priorities: P1 before access/launch; P2 before the month-12 audit. Applicability must be documented rather than presumed.

| Obligation | Gap and action | Owner |
| DPPA ss3,7 | Purpose and processing basis unclear; document notices and appropriate basis, P1 | DPO |
| DPPA ss18,20 | Retention and security evidence absent; schedules, encryption and access review, P1 | IT and owners |
| DPPA s19 | Overseas processing needs assessment and safeguards, P1 | DPO |
| DPPA s23; Reg33 | Jinja notification gap; assess immediately and use Form7, P1 | DPO |
| DPPA ss24,26,28 | Access, correction and marketing objection routes unproven; test requests, P1 | Customer service |
| DPPA s29 | Registration status not supplied; establish and complete applicable registration, P1 | DPO |
| GDPR Arts3,6,13–14 | EU scope, basis and notices need assessment, P1 | DPO |
| GDPR Arts15–22,25 | Rights and privacy by design need end-to-end tests, P1 | DPO and IT |
| GDPR Arts28,32 | Processor terms and security assurance absent, P1 | Procurement and IT |
| GDPR Arts33–36 | Breach and DPIA gates needed; high-risk consultation where required, P1 | DPO |
| GDPR Arts44–49 | Transfer mechanism and assessment unresolved, P1 | DPO |
| CCPA §§1798.100–.135, .140 | Check business scope and rights; sale/share and sensitive-use controls if applicable, P2 | DPO |

# Appendix C | Preventive validation catalogue
| Rule | Check and exception response | Owner |
| V01 | Nonblank source/customer ID; quarantine missing identity key | Customer service |
| V02 | Canonical Uganda phone format; ask for correction, never invent | Customer service |
| V03 | Email syntax when supplied; retain optionality | Customer service |
| V04 | Approved district code; return unknown labels for review | Store manager |
| V05 | Explicit date contract; quarantine ambiguity | IT |
| V06 | Canonical SKU exists; block orphan line | Procurement |
| V07 | Approved unit and pack conversion; hold uncertain receipt | Procurement |
| V08 | Signed quantity permitted only for declared sale/return type | Finance |
| V09 | Nonnegative unit price and accepted currency | Finance |
| V10 | Unique source/order/line; compare replay payload | IT |
| V11 | Provider/reference unique where supplied; cash may be null | Finance |
| V12 | No overlapping dimension validity intervals | IT |
| V13 | Marketing purpose and evidence required; withdrawal suppresses | DPO |
| V14 | Source totals, row counts and hashes reconciled before certification | Finance |

# Appendix D | Data dictionary
The accompanying CSV is the machine-readable dictionary. Refresh codes: B=batch daily, E=event or approved change, M=monthly. Classifications: I=Internal, C=Confidential, R=Restricted. Every entry carries its domain and provisional/certified status; a failed gate changes status to quarantined.

| Element and type | Meaning; source and transformation | Owner; refresh; rule; class |
| core.customer.customer_id / varchar(64) | Member source identity; Enrolment; trim and crosswalk | Customer service; E; Nonblank key; R |
| core.customer.name / varchar(200) | Declared name; Customer; trim only | Customer service; E; Evidence for changes; R |
| core.customer.phone / varchar(16) | Contact number; Customer; canonical format | Customer service; E; Valid if supplied; R |
| core.customer.email / varchar(254) | Optional email; Customer; normalise case | Customer service; E; Syntax if supplied; R |
| core.customer.district / varchar(100) | Member district; Customer; approved lookup | Customer service; E; Reference-list match; R |
| core.customer.consent_marketing / boolean | Purpose-specific choice; Loyalty; withdrawal first | DPO; E; Evidence required; R |
| core.product.product_id / varchar(64) | Canonical product; Procurement; map source SKU | Procurement; E; Unique approved key; I |
| core.product.unit / varchar(10) | Comparable unit; Supplier; approved alias | Procurement; E; No guessed pack ratio; I |
| core.supplier.supplier_id / varchar(64) | Supplier identifier; Register; preserve key | Procurement; E; Unique key; C |
| dim_date.date_key / date | Kampala business date; Order; source date parser | CFO; B; Plausible date; I |
| dim_date.month_start / date | Calendar month; Date; first day | CFO; B; Derived consistently; I |
| dim_customer.customer_key / bigint | Analytical member key; Registry; approved lookup | Customer service; B; Resolved or null; C |
| dim_customer.customer_token / char(64) | Pseudonymous identifier; Identity; HMAC in production | DPO; B; Secret-managed key; R |
| dim_customer.segment / varchar(64) | Assigned segment; CRM; approved label | Commercial manager; B; Known label; C |
| dim_product.product_key / bigint | Historical product version; History; event-time lookup | Procurement; B; Version exists; I |
| dim_product.category / varchar(100) | Reporting category; Procurement; approved alias | Procurement; E; Reference match; I |
| dim_product.valid_from / datetime(6) | Inclusive version start; Approved change; timestamp | IT; E; Before end; I |
| dim_product.valid_to / datetime(6) | Exclusive version end; Change; close prior interval | IT; E; No overlap; I |
| dim_store.store_key / bigint | Branch version key; Register; event-time lookup | Operations; B; Version exists; I |
| dim_store.district / varchar(100) | Branch district; Register; canonical label | Operations; E; Reference match; I |
| fact_sales.source / varchar(32) | Origin system; Manifest; retain code | IT; B; Approved contract; C |
| fact_sales.source_order_id / varchar(64) | Order reference; Order; retain reference | Finance; B; Unique with source/line; C |
| fact_sales.line_no / int | Line identifier; Order; positive integer | Finance; B; Unique within order; C |
| fact_sales.quantity / decimal(14,3) | Signed retail units; Line; preserve returns | Finance; B; Declared sign convention; C |
| core.order_line.unit_price / decimal(18,2) | Agreed unit price; Line; parse money notation | Finance; B; Nonnegative; C |
| fact_sales.currency / char(3) | Denomination; Order; uppercase ISO code | Finance; B; UGX/KES/RWF separate; C |
| fact_sales.net_amount / decimal(18,2) | Signed line value; Quantity × price; Decimal | Finance; B; Reconcile totals; C |
| stage_sales.payment_ref_present / boolean | Reference indicator; Payment; nonblank test | Finance; B; Cash null permitted; C |
| fact_inventory_snapshot.on_hand / decimal(14,3) | Snapshot stock balance; Odoo; align unit/time | Operations; B; Movement reconciliation; C |
| MAC / integer KPI | Monthly purchasing members; Facts; distinct key qty>0 | Commercial manager; M; Exclude anonymous; C |

# Appendix E | Risk register
Likelihood and impact use a five-point scale; residual values are targets after controls, not measured certification.

| Risk | Initial L×I | Response and owner | Residual |
| Lost device export | 5×5=25 | Managed encryption and export expiry; IT | 2×5=10 |
| Wrong person merge | 4×5=20 | Human review and reversible ledger; Customer service | 2×5=10 |
| Privileged misuse | 3×5=15 | Separate named accounts and review; IT | 2×5=10 |
| Phishing takeover | 4×4=16 | MFA and drills; IT | 2×4=8 |
| Backup unavailable | 4×5=20 | Isolated copy and restore exercise; IT | 2×5=10 |
| Delayed breach report | 4×5=20 | Duty contact and rehearsal; DPO | 2×4=8 |
| Incorrect unit mapping | 4×4=16 | Procurement approval and receipt checks | 2×4=8 |
| Duplicate load | 4×3=12 | Business-key control and replay tests; IT | 1×3=3 |
| Unreported stale store | 4×4=16 | Expected-file register and freshness; IT | 2×3=6 |
| Unlawful sharing | 3×5=15 | Destination and processor review; DPO | 2×4=8 |
| Excess HR access | 3×5=15 | HR schema isolation and denied-query tests; HR | 1×5=5 |
| Cost/support overrun | 4×4=16 | Phased quotations and handover gate; CFO | 2×4=8 |

# Appendix F | Dashboard evidence
Dashboard publication and verification in progress.

# Appendix G | Decisions and assumptions
| Decision | Reason and alternative | Revisit when |
| Central reporting | Four-person team; reject independent store marts | Country teams gain engineering staff |
| Registry MDM | Retain local ownership; defer mandatory central creation | Conflicts exceed correction capacity |
| Human identity review | False-merge harm outweighs convenience | Representative tests justify narrower automation |
| ETL before certification | Minimise sensitive certified fields; defer broad ELT | Governed analytical demand increases |
| SCD2 product/store | Preserve event-time reporting; avoid overwriting history | Approved retroactive correction required |
| Nightly first | Affordable support; defer universal streaming | Measured benefit exceeds operating cost |
| Dictionary before tool | Avoid unsupported catalogue platform | Pilot shows lower stewardship effort |
| Currency-separated totals | No supplied FX policy; reject simple addition | Finance approves rates and valuation date |
| Two-store pilot | Demonstrate support and weak-network behaviour | Acceptance gates passed |
| HMAC analytics IDs | Reduce direct exposure; avoid plain identifier hashes | Threat model or key compromise changes |

The plan assumes store extracts can be lawfully obtained, source contracts can be agreed, two employees receive protected SQL time and domain managers accept accountability. No claim is made that customer consent, supplier prices, current registration or a production cloud region has been verified. There is no instructor dataset or DPIA template beyond the brief. Validate these assumptions before procurement or deployment. Supplier codes may be reused, households may share contacts and late transactions may change historical totals; the model and review process must tolerate those cases.

# References
[S1] Parliament of Uganda. Data Protection and Privacy Act, 2019. Sections cited in the compliance register. https://bills.parliament.ug/attachments/Data%20Protection%20and%20Privacy%20Act%202019.pdf

[S2] PDPO. Data Protection and Privacy Regulations, 2021. Registration and breach notification, including regulation 33. https://pdpo.go.ug/media/2022/03/Data_Protection_and_Privacy_Regulations-2021.pdf

[S3] PDPO. Registration Classification and Guidance Notes. Renewal and annual reporting. https://pdpo.go.ug/media/2022/01/20102021105143-Registration_Classification_and_Guidance_Notes.pdf

[S4] European Data Protection Board. Guidelines 3/2018 on territorial scope of GDPR, final version. https://www.edpb.europa.eu/documents/guideline/guidelines-32018-on-the-territorial-scope-of-the-gdpr-article-3-version-adopted_en

[S5] EDPB. Data breaches: small business guide; Guidelines 9/2022. https://www.edpb.europa.eu/sme/assess-the-risks/data-breaches_en

[S6] EDPB. Respect individuals' rights; GDPR Article 6 legal-basis guidance. https://www.edpb.europa.eu/sme/be-compliant/respect-individuals-rights_en

[S7] EDPB. Standard contractual clauses. https://www.edpb.europa.eu/topics/international-transfers-and-international-cooperation/standard-contractual-clauses_en

[S8] DAMA International. DAMA-DMBOK and CDMP examination framework. https://dama.org/learning-resources/dama-data-management-body-of-knowledge-dmbok/ ; https://dama.org/certification/exam-information-and-pricing/

[S9] UK ICO. Annual report 2020/21, regulatory action, p30. https://ico.org.uk/media2/migrated/2620166/hc-354-information-commissioners-ara-2020-21.pdf

[S10] California Department of Justice. CCPA overview and rights. https://oag.ca.gov/privacy/ccpa

[S11] Apache Atlas. Features: classifications, lineage and metadata APIs. https://atlas.apache.org/

[S12] Microsoft Learn. Data governance billing in Microsoft Purview. https://learn.microsoft.com/purview/ms-purview-dg-pricing-concepts

[S13] MySQL 8.4 Reference Manual. Using Roles and Stored Object Access Control. https://dev.mysql.com/doc/refman/8.4/en/roles.html ; https://dev.mysql.com/doc/refman/8.4/en/stored-objects-security.html

[S14] Microsoft Learn. Modern data warehouses for small/medium businesses. https://learn.microsoft.com/en-us/azure/architecture/example-scenario/data/small-medium-data-warehouse
