# Graph Report - IncidentPilot  (2026-06-27)

## Corpus Check
- 54 files · ~22,750 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 520 nodes · 1080 edges · 26 communities (20 shown, 6 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 21 edges (avg confidence: 0.53)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `59924b83`
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
- [[_COMMUNITY_Community 25|Community 25]]

## God Nodes (most connected - your core abstractions)
1. `IncidentReport` - 38 edges
2. `_investigate()` - 28 edges
3. `read_ci_log()` - 24 edges
4. `resolve_safe_path()` - 24 edges
5. `IncidentIntake` - 22 edges
6. `redact_secrets()` - 22 edges
7. `redact_text()` - 18 edges
8. `search_repo()` - 18 edges
9. `build_markdown_report()` - 16 edges
10. `EvidenceItem` - 15 edges

## Surprising Connections (you probably didn't know these)
- `_evidence()` --references--> `EvidenceItem`  [EXTRACTED]
  tests/test_schemas.py → app/schemas/findings.py
- `test_incident_intake_minimal()` --calls--> `IncidentIntake`  [EXTRACTED]
  tests/test_schemas.py → app/schemas/incident.py
- `build_summary()` --references--> `IncidentReport`  [EXTRACTED]
  scripts/run_demo.py → app/schemas/report.py
- `test_number_lines_basics()` --calls--> `number_lines()`  [EXTRACTED]
  tests/test_ci_log_reader.py → app/tools/ci_log_reader.py
- `test_no_failed_line_returns_none()` --calls--> `extract_failing_pytest_test()`  [EXTRACTED]
  tests/test_ci_log_reader.py → app/tools/ci_log_reader.py

## Import Cycles
- None detected.

## Communities (26 total, 6 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.08
Nodes (42): investigate_incident(), Run the deterministic investigation and return the grounded report., Report retrieval route., Return the stored, grounded incident report (after /investigate)., read_incident_report(), CodeFinding, FixPlan, LogFinding (+34 more)

### Community 1 - "Community 1"
Cohesion: 0.15
Nodes (19): build_summary(), main(), Return the ``(json_path, markdown_path)`` for ``incident_id``., Return a clean, redacted console summary of the investigation., Run the demo investigation. Return ``0`` on success, non-zero on failure.      O, _report_paths(), run_demo(), _env_without_secrets_or_network() (+11 more)

### Community 2 - "Community 2"
Cohesion: 0.10
Nodes (27): create_github_issue(), GitHub issue route — approval- and safety-gated, dry-run by default.  This endpo, Preview (never create) the GitHub issue for an approved, grounded report., get_settings(), Settings, settings_dependency(), BaseModel, BaseSettings (+19 more)

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
Cohesion: 0.05
Nodes (86): Exception, Path, _coerce_report(), ensure_storage_dirs(), InvalidIncidentIdError, list_reports(), load_report_json(), In-memory incident store for the IncidentPilot control plane.  Phase 4 keeps all (+78 more)

### Community 7 - "Community 7"
Cohesion: 0.09
Nodes (42): Any, _build_minimal_report(), Phase 3 deterministic toolchain integration check.  Proves the Phase 3 tools wor, End-to-end deterministic run over the broken_api_route fixtures., Assemble a minimal, fully grounded report dict for the serializer.      Every ev, test_phase3_toolchain_end_to_end(), test_ensure_report_safe_redacts_text(), test_markdown_includes_summary_evidence_confidence() (+34 more)

### Community 16 - "Community 16"
Cohesion: 0.05
Nodes (78): approve_incident(), Incident control-plane routes: trigger, investigate, approve.  Handlers stay thi, Load the scenario's intake fixture and register a new incident., Record a human approval for ``create_github_issue`` (empty body = approve)., trigger_incident(), datetime, ApprovalResponse, Response for ``POST /incidents/{id}/approve``. (+70 more)

### Community 17 - "Community 17"
Cohesion: 0.09
Nodes (38): TestClient, client(), _investigated(), Phase 4 control-plane API audit (strict).  Exercises the FastAPI control plane e, Investigating must not create or require any on-disk incident state., The whole trigger->investigate->approve->issue flow is deterministic., Fresh client over a reset, in-memory store (no cross-test leakage)., Trigger + investigate a scenario; return (incident_id, report json). (+30 more)

### Community 18 - "Community 18"
Cohesion: 0.10
Nodes (19): Tests for the deterministic investigation service (Phase 5).  These exercise :fu, The scenario name alone is enough; it is auto-registered., Secrets are redacted everywhere, yet the report is still persisted., An ungrounded failure must escalate, not fabricate a confident diagnosis., If the repo cannot be read, no code evidence may be invented., The on-disk JSON re-validates straight through the IncidentReport schema., The Markdown report is written and never leaks a raw secret., A crafted scenario id cannot escape demo/incidents/. (+11 more)

### Community 19 - "Community 19"
Cohesion: 0.25
Nodes (8): _assign_incident_id(), get_incident(), IncidentState, Everything the control plane tracks for a single incident., Return a stable id for ``scenario`` (known map first, else sequential)., Create (or refresh) the incident for ``scenario`` and return its state.      Tri, Return the incident state for ``incident_id``, or ``None`` if unknown., register_incident()

### Community 20 - "Community 20"
Cohesion: 0.18
Nodes (10): Tests for the Phase 5 durable, JSON-first report storage.  Every test targets an, Return a minimal, schema-valid IncidentReport dict for tests., test_invalid_incident_id_cannot_escape(), test_list_reports_is_sorted_and_filtered(), test_no_raw_secret_in_saved_json(), test_overwrite_is_explicit(), test_save_and_load_report_json_round_trips(), test_save_report_json_accepts_model_and_dict() (+2 more)

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
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `IncidentReport` connect `Community 0` to `Community 1`, `Community 2`, `Community 6`, `Community 16`, `Community 18`, `Community 19`, `Community 20`?**
  _High betweenness centrality (0.135) - this node is a cross-community bridge._
- **Why does `redact_secrets()` connect `Community 16` to `Community 1`, `Community 3`, `Community 5`, `Community 6`, `Community 7`?**
  _High betweenness centrality (0.119) - this node is a cross-community bridge._
- **Why does `read_ci_log()` connect `Community 3` to `Community 16`, `Community 5`, `Community 6`, `Community 7`?**
  _High betweenness centrality (0.079) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `IncidentReport` (e.g. with `CodeFinding` and `FixPlan`) actually correct?**
  _`IncidentReport` has 10 INFERRED edges - model-reasoned connections that need verification._
- **What connects `IncidentPilot backend package.`, `GitHub issue route — approval- and safety-gated, dry-run by default.  This endpo`, `Preview (never create) the GitHub issue for an approved, grounded report.` to the rest of the system?**
  _172 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.07955596669750231 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.1471861471861472 - nodes in this community are weakly interconnected._