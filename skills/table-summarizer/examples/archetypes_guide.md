# Markdown Table Summarizer Archetypes & Patterns

This guide details the five standard archetypes defined in `table-summarizer` to transform unstructured discussions, reports, benchmarks, and data dumps into high-signal Markdown matrices.

---

## 1. Action Items & Meeting Decisions

**When to use:** Post-meeting debriefs, standup notes, sprint planning, and incident post-mortems.

### Column Structure
| Topic | Decision / Task | Owner | Due Date / Status |
| :--- | :--- | :--- | :--- |
| **API Auth Migration** | Deprecate legacy API keys in favor of short-lived JWT tokens | `@dev-lead` | `2026-11-01` (In Progress) |
| **Rate Limit Guard** | Implement Leaky Bucket middleware with Redis backend | `@infra-team` | `2026-10-25` (Blocked on Redis cluster) |
| **SDK Documentation** | Publish interactive quickstarts for Python and TypeScript | `@tech-writer` | `2026-10-20` (Review Ready) |

*Key takeaway:* Auth migration remains the primary critical path item before v2.0 GA release.

---

## 2. Comparative Matrix (Options & Architectures)

**When to use:** Tool selection, library bake-offs, architecture choices, model evaluations.

### Column Structure
| Dimension / Criterion | Option A: REST + Polling | Option B: WebSocket / SSE | Recommendation / Verdict |
| :--- | :--- | :--- | :--- |
| **Latency** | 200ms - 2s | < 25ms | **SSE / WebSocket** for real-time tickers |
| **Server Overhead** | High (frequent connection setup) | Low sustained connection cost | **Option B** scales better for high concurrency |
| **Client Complexity** | Minimal (`fetch` / interval) | Medium (reconnect & backoff logic) | **Option A** simpler for low frequency needs |
| **Verdict** | Best for hourly syncs | Best for live trading UI | **Choose Option B** for dynamic agent streams |

---

## 3. Executive & Research Synthesis

**When to use:** Synthesizing research papers, quarterly market reports, or complex technical whitepapers.

### Column Structure
| Key Finding | Supporting Evidence & Details | Impact & Strategic Significance |
| :--- | :--- | :--- |
| **Token Reduction** | ReportLab unclipped PDF output saves 85% chat token context | Drastically extends context window longevity for agents |
| **Prompt Reliability** | Strict file delimiters eliminate regex parser hallucinations | 100% deterministic code extraction across runs |
| **Multi-File Packaging** | Single document encapsulates multi-tier file hierarchy | Zero file truncation across conversational roundtrips |

---

## 4. Chronological & Milestone Tracking

**When to use:** Project roadmaps, release timelines, deprecation phases.

### Column Structure
| Phase / Target | Milestone | Key Deliverables | Status |
| :--- | :--- | :--- | :--- |
| **Phase 1 (Q3)** | Core Architecture Freeze | Schema specs, delimiter conventions | **Complete** |
| **Phase 2 (Q4)** | Skill Registry & Tooling | ReportLab PDF script, CLI runner | **In Progress** |
| **Phase 3 (Q1)** | Automated Agent Testing | Benchmarks across Antigravity & Gemini CLI | **Planned** |

---

## 5. Trade-offs / Pros & Cons Matrix

**When to use:** Evaluating technical debt, architectural compromises, or migration strategies.

### Column Structure
| Strategy / Area | Advantage | Disadvantage | Mitigation |
| :--- | :--- | :--- | :--- |
| **Monorepo for Skills** | Single source of truth, synchronized versioning | Larger initial clone footprint | Use sparse checkout or subpath references |
| **Pure SVG Visuals** | Infinite scalability, zero pixel blur on retina | Cannot render complex realistic textures | Use geometric accents and high-contrast typography |
