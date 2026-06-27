# Graph Report - IncidentPilot  (2026-06-27)

## Corpus Check
- 69 files · ~32,596 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 719 nodes · 1613 edges · 44 communities (37 shown, 7 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 84 edges (avg confidence: 0.51)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0dbf8b1e`
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
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]

## God Nodes (most connected - your core abstractions)
1. `IncidentReport` - 79 edges
2. `EvidenceIndex` - 32 edges
3. `run_agent_investigation()` - 30 edges
4. `_investigate()` - 28 edges
5. `resolve_safe_path()` - 26 edges
6. `redact_secrets()` - 26 edges
7. `AgentOutcome` - 25 edges
8. `read_ci_log()` - 24 edges
9. `ModelClient` - 23 edges
10. `IncidentIntake` - 22 edges

## Surprising Connections (you probably didn't know these)
- `CodeContextObjectShapeClient` --uses--> `EvidenceIndex`  [INFERRED]
  tests/test_agents.py → app/agents/base.py
- `DocumentedShapeClient` --uses--> `EvidenceIndex`  [INFERRED]
  tests/test_agents.py → app/agents/base.py
- `InvalidJSONClient` --uses--> `EvidenceIndex`  [INFERRED]
  tests/test_agents.py → app/agents/base.py
- `InventedPathClient` --uses--> `EvidenceIndex`  [INFERRED]
  tests/test_agents.py → app/agents/base.py
- `LowConfidenceClient` --uses--> `EvidenceIndex`  [INFERRED]
  tests/test_agents.py → app/agents/base.py

## Import Cycles
- None detected.

## Communities (44 total, 7 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.11
Nodes (29): CodeFinding, FixPlan, LogFinding, Evidence and agent finding schemas.  Every agent output carries grounded ``Evide, Base for any agent output that must be safety-reviewable., Output of the Log Investigator agent., Output of the Code Context agent., A single grounded root-cause hypothesis. (+21 more)

### Community 1 - "Community 1"
Cohesion: 0.15
Nodes (19): build_summary(), main(), Return the ``(json_path, markdown_path)`` for ``incident_id``., Return a clean, redacted console summary of the investigation., Run the demo investigation. Return ``0`` on success, non-zero on failure.      O, _report_paths(), run_demo(), _env_without_secrets_or_network() (+11 more)

### Community 2 - "Community 2"
Cohesion: 0.28
Nodes (10): create_github_issue(), GitHub issue route — approval- and safety-gated, dry-run by default.  This endpo, Preview (never create) the GitHub issue for an approved, grounded report., get_settings(), Settings, settings_dependency(), BaseSettings, GitHubIssueResult (+2 more)

### Community 3 - "Community 3"
Cohesion: 0.13
Nodes (27): test_empty_log_needs_human_review(), test_extracts_assertion_error(), test_extracts_failing_pytest_test(), test_extracts_primary_attribute_error(), test_extracts_stack_trace_block(), test_loads_fixture_and_numbers_lines(), test_missing_log_file_raises(), test_no_failed_line_returns_none() (+19 more)

### Community 4 - "Community 4"
Cohesion: 0.19
Nodes (11): create_payment(), get_user(), Payment, PaymentRequest, Demo payments router for IncidentPilot's demo_repo fixture.  Simulates a tiny Fa, Minimal user record returned by the fake data layer., Return a ``User`` for a known id, or ``None`` when no such user exists.      NOT, A payment being created. ``user_id`` is filled in from the looked-up user. (+3 more)

### Community 5 - "Community 5"
Cohesion: 0.11
Nodes (28): A secret-bearing CI log is redacted while evidence is still extracted.      The, test_phase3_redacts_secrets_from_ci_log(), test_clean_text_returns_same_text_and_zero_redactions(), test_findings_do_not_leak_full_secret(), test_redaction_is_idempotent(), test_redacts_api_key_key_value(), test_redacts_bearer_token(), test_redacts_database_url() (+20 more)

### Community 6 - "Community 6"
Cohesion: 0.09
Nodes (57): Path, The same guard protects the real demo repo root used by the pipeline., An allowed root directory with one nested file., root(), test_allows_nested_valid_file(), test_allows_normal_file_inside_root(), test_blocks_absolute_path_outside_root(), test_blocks_deep_parent_traversal() (+49 more)

### Community 7 - "Community 7"
Cohesion: 0.08
Nodes (43): _build_minimal_report(), Phase 3 deterministic toolchain integration check.  Proves the Phase 3 tools wor, End-to-end deterministic run over the broken_api_route fixtures., Assemble a minimal, fully grounded report dict for the serializer.      Every ev, test_phase3_toolchain_end_to_end(), test_ensure_report_safe_redacts_text(), test_markdown_includes_summary_evidence_confidence(), test_missing_optional_fields_do_not_crash() (+35 more)

### Community 16 - "Community 16"
Cohesion: 0.13
Nodes (39): EvidenceItem, A single grounded piece of evidence returned by a deterministic tool., IncidentIntake, Normalized representation of an incoming incident to investigate., _api_evidence(), _build_code_finding(), _build_fix_plan(), _build_log_finding() (+31 more)

### Community 17 - "Community 17"
Cohesion: 0.09
Nodes (38): TestClient, client(), _investigated(), Phase 4 control-plane API audit (strict).  Exercises the FastAPI control plane e, Investigating must not create or require any on-disk incident state., The whole trigger->investigate->approve->issue flow is deterministic., Fresh client over a reset, in-memory store (no cross-test leakage)., Trigger + investigate a scenario; return (incident_id, report json). (+30 more)

### Community 18 - "Community 18"
Cohesion: 0.10
Nodes (19): Tests for the deterministic investigation service (Phase 5).  These exercise :fu, The scenario name alone is enough; it is auto-registered., Secrets are redacted everywhere, yet the report is still persisted., An ungrounded failure must escalate, not fabricate a confident diagnosis., If the repo cannot be read, no code evidence may be invented., The on-disk JSON re-validates straight through the IncidentReport schema., The Markdown report is written and never leaks a raw secret., A crafted scenario id cannot escape demo/incidents/. (+11 more)

### Community 19 - "Community 19"
Cohesion: 0.18
Nodes (13): _assign_incident_id(), get_incident(), IncidentState, In-memory incident store for the IncidentPilot control plane.  Phase 4 keeps all, Everything the control plane tracks for a single incident., Clear all in-memory state (used by tests)., Return a stable id for ``scenario`` (known map first, else sequential)., Create (or refresh) the incident for ``scenario`` and return its state.      Tri (+5 more)

### Community 20 - "Community 20"
Cohesion: 0.18
Nodes (10): Tests for the Phase 5 durable, JSON-first report storage.  Every test targets an, Return a minimal, schema-valid IncidentReport dict for tests., test_invalid_incident_id_cannot_escape(), test_list_reports_is_sorted_and_filtered(), test_no_raw_secret_in_saved_json(), test_overwrite_is_explicit(), test_save_and_load_report_json_round_trips(), test_save_report_json_accepts_model_and_dict() (+2 more)

### Community 21 - "Community 21"
Cohesion: 0.26
Nodes (8): Phase 2 demo fixture sanity tests.  These verify the demo incident fixtures exis, _read(), test_ambiguous_error_report_is_low_confidence(), test_broken_api_route_ci_log_has_attribute_error(), test_broken_api_route_report_mentions_root_cause_and_file(), test_json_files_parse(), test_secret_in_logs_ci_log_has_fake_secrets(), test_secret_in_logs_report_has_no_raw_secrets()

### Community 22 - "Community 22"
Cohesion: 0.14
Nodes (14): Report retrieval route., Return the stored, grounded incident report (after /investigate)., read_incident_report(), handle_incident_error(), IncidentPilot FastAPI application (Phase 4 control plane).  Registers the determ, Map control-plane domain errors to their HTTP status + detail., JSONResponse, Request (+6 more)

### Community 23 - "Community 23"
Cohesion: 0.33
Nodes (5): Tests for the demo payments service.  These are demo_repo FIXTURE tests, not par, Happy path: a known user can create a payment (HTTP 201)., Unknown user reproduces the production incident.      ``get_user`` returns ``Non, test_create_payment_succeeds_for_known_user(), test_create_payment_with_unknown_user_reproduces_incident()

### Community 26 - "Community 26"
Cohesion: 0.12
Nodes (21): AgentOutcome, Result of a single agent step — thin, inspectable, and not yet trusted.      ``s, FixPlannerAgent, Fix Planner agent: restate the grounded root cause and fix plan.  Runs after Cod, Thin wrapper around the deterministic root cause + fix plan., AgentInvestigationResult, _as_confidence(), _build_candidate() (+13 more)

### Community 27 - "Community 27"
Cohesion: 0.12
Nodes (26): Run the optional agent pipeline over a deterministic investigation.      The det, run_agent_investigation(), _deterministic(), Tests for the optional agent layer (Phase 6).  The agent layer wraps the determi, No agent-created evidence: every evidence id traces to deterministic mode., Importing/using the agent layer does not alter deterministic output., Every prompt-documented shape is accepted; broken_api_route parity holds., Every test starts and ends from a clean in-memory control plane. (+18 more)

### Community 28 - "Community 28"
Cohesion: 0.11
Nodes (16): LogInvestigatorAgent, Thin wrapper around the deterministic log finding., GroundedDeterministicClient, Default, offline model client: grounded by construction.      Returns ``payload[, CodeContextObjectShapeClient, DocumentedShapeClient, InvalidJSONClient, InventedPathClient (+8 more)

### Community 29 - "Community 29"
Cohesion: 0.13
Nodes (14): parse_agent_json(), Strictly parse an agent's raw output into a JSON object.      Returns ``None`` f, CodeContextAgent, Code Context agent: restate the deterministic, verified code finding.  Runs afte, Thin wrapper around the deterministic, path-verified code finding., ModelClient, The model boundary for the agent layer.  Every agent calls a :class:`ModelClient, Boundary between orchestration and whatever produces an agent's JSON. (+6 more)

### Community 30 - "Community 30"
Cohesion: 0.10
Nodes (27): approve_incident(), investigate_incident(), Incident control-plane routes: trigger, investigate, approve.  Handlers stay thi, Load the scenario's intake fixture and register a new incident., Run the deterministic investigation and return the grounded report., Record a human approval for ``create_github_issue`` (empty body = approve)., trigger_incident(), BaseModel (+19 more)

### Community 31 - "Community 31"
Cohesion: 0.25
Nodes (8): ApprovalRequired, Domain errors for the incident control plane.  Services raise these plain except, The safety review does not permit the requested external action., A required human approval is missing for the requested action., SafetyBlocked, _build_issue_preview(), create_github_issue(), Return a redacted preview of the GitHub issue for this incident.      Enforces e

### Community 32 - "Community 32"
Cohesion: 0.21
Nodes (7): EvidenceIndex, _norm_path(), Shared, dependency-light helpers for the optional agent layer.  The agent layer, True if every id is one the tools actually produced (empty is fine)., True if ``path`` names a file the tools actually verified.          Tolerates a, The closed set of facts an agent is allowed to cite.      Built only from the de, Optional, grounded agent layer for IncidentPilot.  This package adds an *optiona

### Community 33 - "Community 33"
Cohesion: 0.12
Nodes (25): assert_github_issue_allowed(), github_issue_block_reasons(), Re-derive, deterministically, why a GitHub issue is blocked for ``report``., Raise unless a GitHub issue may be created for ``report``.      The deterministi, _approved_record(), A misbehaving agent/LLM flipping the flat approval cannot authorize a block., secret_in_logs: secrets are redacted, never leaked, and never auto-shared., ambiguous_error: weak/vague evidence -> low confidence -> issue blocked. (+17 more)

### Community 34 - "Community 34"
Cohesion: 0.25
Nodes (8): _coerce_report(), Raised when a report exists and ``overwrite=False`` was requested., Validate ``report`` through the ``IncidentReport`` schema.      Accepts an alrea, Validate, redact, and persist ``report`` as ``{incident_id}.json``.      The rep, Redact and persist a Markdown report as ``{incident_id}.md``.      ``markdown``, ReportExistsError, save_report_json(), save_report_markdown()

### Community 35 - "Community 35"
Cohesion: 0.25
Nodes (8): load_report_json(), Return ``incident_id`` unchanged if it is a safe single path segment.      Treat, Resolve the on-disk path for an incident file, confined to the root.      Valida, Return the stored report for ``incident_id``, or ``None`` if absent.      Mirror, Return ``True`` if a JSON report is stored for ``incident_id``., report_exists(), _report_path(), _validate_incident_id()

### Community 36 - "Community 36"
Cohesion: 0.22
Nodes (3): load_prompt(), Return the text of ``prompts/{name}.md``.      Raises ``FileNotFoundError`` if t, Log Investigator agent: restate the deterministic log finding.  Runs after Triag

### Community 37 - "Community 37"
Cohesion: 0.17
Nodes (13): IncidentNotFound, The requested demo scenario has no intake fixture., No incident exists for the given id (it was never triggered)., ScenarioNotFound, investigate_incident(), _load_intake(), _persist_report(), Run the deterministic investigation for an incident or demo scenario.      ``sce (+5 more)

### Community 38 - "Community 38"
Cohesion: 0.18
Nodes (12): Exception, ApprovalRecord, A stored approval decision for one incident + action., get_approval(), InvalidIncidentIdError, Store a human approval decision, keyed by its action., Return the stored approval for ``incident_id``/``action`` if present., Base class for durable report-storage errors. (+4 more)

### Community 39 - "Community 39"
Cohesion: 0.15
Nodes (18): evaluate_safety(), Compute the authoritative :class:`SafetyReview` from grounded signals.      Para, Phase 7 — deterministic safety gate and action gating.  These tests pin the safe, Mirrors the Phase 7 required SafetyReview shape, including nested checks., The deterministic gate enforces the three-tier confidence policy exactly:      *, The structured ``checks`` object exposes exactly the six required fields., test_clean_grounded_high_confidence_is_eligible(), test_confidence_at_threshold_is_eligible() (+10 more)

### Community 40 - "Community 40"
Cohesion: 0.18
Nodes (11): GitHubIssueOptions, Body for ``POST /incidents/{id}/github/issue``.      The title and body are gene, An approved, eligible report still performs no real GitHub write., low_confidence_report: a clean report under 0.50 — display ok, writes not., When safety blocks, no issue payload is built and no external write runs.      T, test_create_github_issue_blocked_for_secret_scenario_even_after_approval(), test_create_github_issue_dry_run_preview_after_approval(), test_create_github_issue_never_writes_even_when_configured_and_not_dry_run() (+3 more)

### Community 41 - "Community 41"
Cohesion: 0.31
Nodes (8): The deterministic safety gate's structured pass/fail invariants.      Every fiel, SafetyChecks, checks_blocked_reasons(), _default_summary(), Deterministic, authoritative safety gate (Phase 7).  This module is the single s, Return the exact blocked-reason strings for every failing check.      Determinis, test_all_checks_pass_yields_no_blocked_reasons(), test_each_failing_check_maps_to_its_exact_reason()

### Community 42 - "Community 42"
Cohesion: 0.33
Nodes (6): ensure_storage_dirs(), list_reports(), Return the reports root to use (override for tests, else the default)., Create the reports directory if needed and return it. Idempotent., Return the sorted incident ids that have a stored JSON report.      Deterministi, _resolve_reports_dir()

## Knowledge Gaps
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `IncidentReport` connect `Community 26` to `Community 0`, `Community 1`, `Community 16`, `Community 18`, `Community 19`, `Community 20`, `Community 22`, `Community 27`, `Community 28`, `Community 29`, `Community 30`, `Community 31`, `Community 32`, `Community 33`, `Community 34`, `Community 35`, `Community 36`, `Community 37`, `Community 38`, `Community 39`, `Community 41`?**
  _High betweenness centrality (0.265) - this node is a cross-community bridge._
- **Why does `redact_secrets()` connect `Community 16` to `Community 1`, `Community 34`, `Community 3`, `Community 5`, `Community 39`, `Community 7`, `Community 41`, `Community 19`, `Community 26`?**
  _High betweenness centrality (0.100) - this node is a cross-community bridge._
- **Why does `read_ci_log()` connect `Community 3` to `Community 16`, `Community 5`, `Community 6`, `Community 7`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `IncidentReport` (e.g. with `AgentOutcome` and `EvidenceIndex`) actually correct?**
  _`IncidentReport` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `EvidenceIndex` (e.g. with `IncidentReport` and `CodeContextAgent`) actually correct?**
  _`EvidenceIndex` has 13 INFERRED edges - model-reasoned connections that need verification._
- **What connects `IncidentPilot backend package.`, `Optional, grounded agent layer for IncidentPilot.  This package adds an *optiona`, `Shared, dependency-light helpers for the optional agent layer.  The agent layer` to the rest of the system?**
  _234 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.11174242424242424 - nodes in this community are weakly interconnected._