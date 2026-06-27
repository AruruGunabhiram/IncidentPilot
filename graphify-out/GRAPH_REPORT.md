# Graph Report - IncidentPilot  (2026-06-26)

## Corpus Check
- 49 files · ~18,453 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 429 nodes · 900 edges · 25 communities (20 shown, 5 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 12 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d6b88a92`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]

## God Nodes (most connected - your core abstractions)
1. `_investigate()` - 28 edges
2. `IncidentReport` - 26 edges
3. `read_ci_log()` - 24 edges
4. `resolve_safe_path()` - 20 edges
5. `IncidentIntake` - 19 edges
6. `redact_text()` - 18 edges
7. `redact_secrets()` - 18 edges
8. `search_repo()` - 18 edges
9. `EvidenceItem` - 15 edges
10. `CILogResult` - 15 edges

## Surprising Connections (you probably didn't know these)
- `test_github_issue_request_defaults_dry_run_true()` --calls--> `GitHubIssueRequest`  [EXTRACTED]
  tests/test_schemas.py → app/schemas/approval.py
- `_evidence()` --references--> `EvidenceItem`  [EXTRACTED]
  tests/test_schemas.py → app/schemas/findings.py
- `test_incident_intake_minimal()` --calls--> `IncidentIntake`  [EXTRACTED]
  tests/test_schemas.py → app/schemas/incident.py
- `test_number_lines_basics()` --calls--> `number_lines()`  [EXTRACTED]
  tests/test_ci_log_reader.py → app/tools/ci_log_reader.py
- `test_no_failed_line_returns_none()` --calls--> `extract_failing_pytest_test()`  [EXTRACTED]
  tests/test_ci_log_reader.py → app/tools/ci_log_reader.py

## Import Cycles
- None detected.

## Communities (25 total, 5 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.09
Nodes (39): investigate_incident(), Run the deterministic investigation and return the grounded report., CodeFinding, FixPlan, LogFinding, Evidence and agent finding schemas.  Every agent output carries grounded ``Evide, Base for any agent output that must be safety-reviewable., Output of the Log Investigator agent. (+31 more)

### Community 1 - "Community 1"
Cohesion: 0.29
Nodes (9): Incident control-plane routes: trigger, investigate, approve.  Handlers stay thi, Load the scenario's intake fixture and register a new incident., trigger_incident(), IncidentTriggerRequest, IncidentTriggerResponse, API request body for triggering an incident investigation., API response returned when an incident investigation is created., create_incident() (+1 more)

### Community 2 - "Community 2"
Cohesion: 0.32
Nodes (9): create_github_issue(), GitHub issue route — approval- and safety-gated, dry-run by default.  This endpo, Preview (never create) the GitHub issue for an approved, grounded report., get_settings(), Settings, settings_dependency(), BaseSettings, GitHubIssueResult (+1 more)

### Community 3 - "Community 3"
Cohesion: 0.14
Nodes (25): test_empty_log_needs_human_review(), test_extracts_assertion_error(), test_extracts_failing_pytest_test(), test_extracts_primary_attribute_error(), test_extracts_stack_trace_block(), test_loads_fixture_and_numbers_lines(), test_missing_log_file_raises(), test_no_failed_line_returns_none() (+17 more)

### Community 4 - "Community 4"
Cohesion: 0.19
Nodes (11): create_payment(), get_user(), Payment, PaymentRequest, Demo payments router for IncidentPilot's demo_repo fixture.  Simulates a tiny Fa, Minimal user record returned by the fake data layer., Return a ``User`` for a known id, or ``None`` when no such user exists.      NOT, A payment being created. ``user_id`` is filled in from the looked-up user. (+3 more)

### Community 5 - "Community 5"
Cohesion: 0.11
Nodes (29): A secret-bearing CI log is redacted while evidence is still extracted.      The, test_phase3_redacts_secrets_from_ci_log(), test_clean_text_returns_same_text_and_zero_redactions(), test_findings_do_not_leak_full_secret(), test_redaction_is_idempotent(), test_redacts_api_key_key_value(), test_redacts_bearer_token(), test_redacts_database_url() (+21 more)

### Community 6 - "Community 6"
Cohesion: 0.09
Nodes (56): Path, An allowed root directory with one nested file., root(), test_allows_nested_valid_file(), test_allows_normal_file_inside_root(), test_blocks_absolute_path_outside_root(), test_blocks_deep_parent_traversal(), test_blocks_single_parent_traversal() (+48 more)

### Community 7 - "Community 7"
Cohesion: 0.08
Nodes (43): Any, _build_issue_preview(), _build_minimal_report(), Phase 3 deterministic toolchain integration check.  Proves the Phase 3 tools wor, End-to-end deterministic run over the broken_api_route fixtures., Assemble a minimal, fully grounded report dict for the serializer.      Every ev, test_phase3_toolchain_end_to_end(), test_ensure_report_safe_redacts_text() (+35 more)

### Community 16 - "Community 16"
Cohesion: 0.11
Nodes (45): datetime, EvidenceItem, A single grounded piece of evidence returned by a deterministic tool., IncidentIntake, Incident intake schemas., Normalized representation of an incoming incident to investigate., The requested demo scenario has no intake fixture., ScenarioNotFound (+37 more)

### Community 17 - "Community 17"
Cohesion: 0.09
Nodes (38): TestClient, client(), _investigated(), Phase 4 control-plane API audit (strict).  Exercises the FastAPI control plane e, Investigating must not create or require any on-disk incident state., The whole trigger->investigate->approve->issue flow is deterministic., Fresh client over a reset, in-memory store (no cross-test leakage)., Trigger + investigate a scenario; return (incident_id, report json). (+30 more)

### Community 18 - "Community 18"
Cohesion: 0.13
Nodes (21): Report retrieval route., Return the stored, grounded incident report (after /investigate)., read_incident_report(), Exception, ApprovalRequired, IncidentError, IncidentNotFound, Domain errors for the incident control plane.  Services raise these plain except (+13 more)

### Community 19 - "Community 19"
Cohesion: 0.15
Nodes (17): ApprovalRecord, A stored approval decision for one incident + action., _assign_incident_id(), get_approval(), get_incident(), IncidentState, In-memory incident store for the IncidentPilot control plane.  Phase 4 keeps all, Store a human approval decision, keyed by its action. (+9 more)

### Community 20 - "Community 20"
Cohesion: 0.18
Nodes (14): approve_incident(), Record a human approval for ``create_github_issue`` (empty body = approve)., BaseModel, ApprovalDecision, ApprovalRequest, ApprovalResponse, GitHubIssueOptions, GitHubIssueRequest (+6 more)

### Community 21 - "Community 21"
Cohesion: 0.26
Nodes (8): Phase 2 demo fixture sanity tests.  These verify the demo incident fixtures exis, _read(), test_ambiguous_error_report_is_low_confidence(), test_broken_api_route_ci_log_has_attribute_error(), test_broken_api_route_report_mentions_root_cause_and_file(), test_json_files_parse(), test_secret_in_logs_ci_log_has_fake_secrets(), test_secret_in_logs_report_has_no_raw_secrets()

### Community 22 - "Community 22"
Cohesion: 0.33
Nodes (5): handle_incident_error(), IncidentPilot FastAPI application (Phase 4 control plane).  Registers the determ, Map control-plane domain errors to their HTTP status + detail., JSONResponse, Request

### Community 23 - "Community 23"
Cohesion: 0.33
Nodes (5): Tests for the demo payments service.  These are demo_repo FIXTURE tests, not par, Happy path: a known user can create a payment (HTTP 201)., Unknown user reproduces the production incident.      ``get_user`` returns ``Non, test_create_payment_succeeds_for_known_user(), test_create_payment_with_unknown_user_reproduces_incident()

## Knowledge Gaps
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `redact_secrets()` connect `Community 16` to `Community 3`, `Community 5`, `Community 7`?**
  _High betweenness centrality (0.121) - this node is a cross-community bridge._
- **Why does `read_ci_log()` connect `Community 3` to `Community 16`, `Community 5`, `Community 6`, `Community 7`?**
  _High betweenness centrality (0.110) - this node is a cross-community bridge._
- **Why does `IncidentReport` connect `Community 0` to `Community 1`, `Community 7`, `Community 16`, `Community 18`, `Community 19`, `Community 20`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `IncidentReport` (e.g. with `CodeFinding` and `FixPlan`) actually correct?**
  _`IncidentReport` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `IncidentPilot backend package.`, `GitHub issue route — approval- and safety-gated, dry-run by default.  This endpo`, `Preview (never create) the GitHub issue for an approved, grounded report.` to the rest of the system?**
  _139 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.08748615725359911 - nodes in this community are weakly interconnected._
- **Should `Community 3` be split into smaller, more focused modules?**
  _Cohesion score 0.14245014245014245 - nodes in this community are weakly interconnected._