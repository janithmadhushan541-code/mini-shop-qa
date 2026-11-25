# EC4206 — Mini Shop software testing and quality assurance
## 3.1 Test plan
Objective: verify catalog browsing, search, filtering, sorting, cart arithmetic, persistence and theme. In scope: Vue frontend, Pinia store and product API integration. Out of scope: payment processing, authentication and external API internals (not implemented/owned). Target ISO 25010 attributes: functional suitability, reliability, usability, performance efficiency and security. Resources: Node 22, Chromium, GitHub Actions, JMeter, SonarQube. Proposed schedule: day 1 requirements/design, day 2 unit and UI tests, day 3 automation and quality scan, day 4 defect retest and closure. Verification: code review/typecheck; validation: user-flow execution.
## 3.2 STLC
Requirements: identify above flows; planning: scope and tools; design: cases below; environment: Linux Node 22.16.0, in-memory localStorage for unit tests; execution: npm run coverage; closure: 12 passed, integration gates outstanding. Browser target Chromium; use fresh storage and deterministic product fixtures for UI tests.
| ID | Preconditions | Steps | Expected | Actual/status |
|---|---|---|---|---|
| TC01 | Empty cart | Read totals | 0 | 0 / Pass |
| TC02 | Empty cart | Add $10 product | $22 total, open cart | As expected / Pass |
| TC03 | Empty cart | Add same product twice | One row, quantity 2, $32 | As expected / Pass |
| TC04 | Quantity 2 | Decrease | Quantity 1 | As expected / Pass |
| TC05 | Quantity 1 | Decrease | Empty, total 0 | As expected / Pass |
| TC06 | Empty | Decrease unknown ID | No change | As expected / Pass |
| TC07 | Product added | Clear | Zero items | As expected / Pass |
| TC08 | Product added | Save and recreate store | Quantity 1 | As expected / Pass |
| TC09 | Stored object instead of array | Load | Empty cart | As expected / Pass |
| TC10 | Stored negative quantity | Load | Empty cart | As expected / Pass |
| TC11 | Formatting utility | Format 12 and skin-care | $12.00, Skin Care | As expected / Pass |
| TC12 | Empty cart | Open, close, toggle | Correct visibility | As expected / Pass |
| UI01 | Catalog loaded | Search matching title | Matching products | Not run |
| UI02 | Catalog loaded | Search nonexistent term | No products found | Not run |
| UI03 | Catalog loaded | Select category, sort price | Matching category, ascending prices | Not run |
## 3.3 Black-box design
Equivalence partitions: search empty (all), matching (subset), nonmatching (none); category all, existing, nonexistent (none); stored quantity positive integer (valid), zero/negative/fraction (invalid). Boundary quantity 0, 1, 2: absent item no-op, one removed, two becomes one (TC06, TC05, TC04). No date input exists.
Decision table for decreaseQuantity:
| Item exists | Quantity >1 | Action |
|---|---|---|
| No | N/A | No change |
| Yes | Yes | Decrement |
| Yes | No | Remove |
## 3.4 White-box
For decreaseQuantity, two decisions (missing item, quantity >1), hence cyclomatic complexity 3. TC04–06 cover all three independent paths and both outcomes of both decisions. Node coverage for cart.ts: line 95.65%, branch 94.44%, functions 100%; format.ts 100% across these metrics. Line coverage is not a measured statement-coverage metric; statement coverage design exercises all decreaseQuantity statements.
## 3.5 Unit and BDD
Node native test runner selected for TypeScript; 12 tests executed. Gherkin scenarios in tests/cart.feature; Cucumber execution pending. No claim of historical test-first development.
## 3.6 Automation and CI
Workflow in .github/workflows/qa.yml. Remote pipeline not executed; push to your repository and capture the green workflow after resolving dependencies. Selenium script provided; browser execution pending. Local typecheck passed; Vite build blocked by missing Linux Rolldown native binding in uploaded Windows dependencies; offline npm installation also failed. Package manifest/lock version mismatch requires clean npm install and commit refreshed lockfile.
## 3.7 Performance, security, usability
JMeter plan: local preview endpoint GET /, 10 threads, 5-second ramp, 10 iterations; report p95, throughput, errors; do not load-test third-party API. Not run. Manual source review: client-side storage is untrusted (invalid cart shape/negative quantity fixed); no payment/auth backend, so access control cannot be validated. Vue interpolation escapes text by default; runtime XSS checks pending. Usability: check mobile layout, keyboard focus, theme and cart controls; checkout button has no handler (observed in source), should be disabled or explicitly labeled unavailable.
## 3.8 Defects
BUG-01: malformed stored cart object causes array operations to fail. Root cause: unchecked JSON cast. Fix: validate array and item quantity/price/id. Verified by TC09–10 on updated code. Proposed lifecycle New → Assigned → Fixed → Verified → Closed (external issue tracking not performed; closure requires team approval).
BUG-02: missing product brand can crash search when title does not match. Root cause: unconditional brand.toLowerCase(). Fix: nullish fallback. UI retest pending. BUG-03: checkout button has no action; open, scope decision needed. Log these in GitHub Issues and capture lifecycle screenshots.
## 3.9 Quality metrics
SonarQube not run; coverage above is limited to exercised modules, not whole application. Defect density, code smells and technical debt not measured. Suggested improvements based on source review (not Sonar findings): validate API data, extract filtering into a pure tested function, make checkout availability explicit. Run scanner and replace pending metrics with actual dashboard values.
## 3.10 Reflection
Use short Agile iterations with acceptance criteria and regression tests; review defects in sprint planning, automate test/build gates on pull requests, and use quality reports to prioritize technical debt. Release only after required gates pass.
