# Graph Report - .  (2026-06-25)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 62 nodes · 88 edges · 16 communities (9 shown, 7 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 3 edges (avg confidence: 0.6)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a213ba0e`
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

## God Nodes (most connected - your core abstractions)
1. `IncidentReport` - 9 edges
2. `resolve_under_root()` - 9 edges
3. `create_placeholder_incident()` - 7 edges
4. `Finding` - 6 edges
5. `IncidentTriggerResponse` - 6 edges
6. `SafetySummary` - 6 edges
7. `Settings` - 5 edges
8. `create_incident()` - 5 edges
9. `get_report()` - 5 edges
10. `UnsafePathError` - 5 edges

## Surprising Connections (you probably didn't know these)
- `test_path_guard_blocks_traversal()` --calls--> `resolve_under_root()`  [EXTRACTED]
  tests/test_path_guard.py → app/tools/path_guard.py
- `test_redactor_removes_fake_secrets()` --calls--> `redact_secrets()`  [EXTRACTED]
  tests/test_redactor.py → app/tools/redactor.py
- `test_repo_search_finds_known_string_in_demo_repo()` --calls--> `search_repo()`  [EXTRACTED]
  tests/test_repo_search.py → app/tools/repo_search.py
- `IncidentReport` --uses--> `Finding`  [INFERRED]
  app/schemas/report.py → app/schemas/findings.py
- `IncidentReport` --uses--> `SafetySummary`  [INFERRED]
  app/schemas/report.py → app/schemas/safety.py

## Import Cycles
- None detected.

## Communities (16 total, 7 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.38
Nodes (7): read_incident_report(), BaseModel, Finding, IncidentReport, SafetySummary, create_placeholder_incident(), get_report()

### Community 1 - "Community 1"
Cohesion: 0.57
Nodes (4): trigger_incident(), IncidentTriggerRequest, IncidentTriggerResponse, create_incident()

### Community 2 - "Community 2"
Cohesion: 0.67
Nodes (4): get_settings(), Settings, settings_dependency(), BaseSettings

### Community 3 - "Community 3"
Cohesion: 0.53
Nodes (4): Path, test_path_guard_blocks_traversal(), read_ci_log(), resolve_under_root()

### Community 7 - "Community 7"
Cohesion: 0.50
Nodes (3): Raised when a requested path escapes the allowed root., UnsafePathError, ValueError

## Knowledge Gaps
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `resolve_under_root()` connect `Community 3` to `Community 6`, `Community 7`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Why does `redact_secrets()` connect `Community 5` to `Community 3`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `IncidentReport` (e.g. with `Finding` and `SafetySummary`) actually correct?**
  _`IncidentReport` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `IncidentPilot backend package.`, `Application services.`, `Local storage helpers.` to the rest of the system?**
  _5 weakly-connected nodes found - possible documentation gaps or missing edges._