# Technology Comparison / Evaluation Template

> **Usage:** Copy this template, replace all `[PLACEHOLDER]` text, and delete this header block before publishing.
>
> **Best for:** Helping other teams make informed technology decisions by sharing the research, testing, and reasoning behind a choice your team made. Most useful when the decision was non-obvious or when teams keep facing the same question.
>
> **Ideal length:** 1,200–2,000 words

---

# [Tech A] vs [Tech B] for [Our Specific Use Case]

**Author:** [Your Name]
**Date:** [Publication Date]
**Decision date:** [When was the decision made? This helps readers assess how current the post is.]
**Tags:** [e.g., infrastructure, databases, messaging, frontend]
**Decision status:** ✅ Decided — we chose [Tech A/B]

---

## TL;DR

> What you evaluated, what you chose, and the one-sentence reason why.
>
> _Example: We evaluated PostgreSQL and MongoDB for storing user activity events (~50M/day). We chose PostgreSQL with table partitioning because our query patterns were relational and our team's Postgres expertise outweighed MongoDB's write throughput advantage for our scale._

---

## The Decision Context

### What We Were Trying to Do

[Describe the specific technical problem that required a technology choice. Be concrete — "we needed a database" is not enough.]

We needed to [specific task] in order to [business goal]. The key constraints were:

- **Scale:** [e.g., ~50M write events per day, ~500 complex reads per day]
- **Latency requirements:** [e.g., writes < 50ms P99, reads < 200ms P99]
- **Team:** [e.g., 4 engineers, strong Postgres familiarity, no prior MongoDB experience]
- **Timeline:** [e.g., production-ready in 6 weeks]
- **Operational constraints:** [e.g., must run on our existing AWS RDS setup; we can't introduce a new managed service]

### Our Success Criteria

[List the criteria you used to evaluate options. Being explicit here lets readers apply your analysis to their own (different) constraints.]

| Criterion | Weight | Why It Matters |
|-----------|--------|---------------|
| Write throughput | High | [Justification] |
| Query flexibility | High | [Justification] |
| Operational complexity | Medium | [Justification] |
| Team familiarity | Medium | [Justification] |
| Ecosystem maturity | Low | [Justification] |
| Licensing / cost | Low | [Justification] |

### What We Did Not Evaluate

[Scope boundaries are important. What did you deliberately exclude and why?]

We excluded [Option C] because [reason, e.g.: it requires a separate SLA agreement and would take 3+ months to procure]. We excluded [Option D] because [reason].

---

## Technologies Evaluated

### [Technology A]

**What it is:** [One sentence description]

**Version evaluated:** [vX.Y]

**Core strengths in our context:**
- [Strength 1 specific to your use case]
- [Strength 2]
- [Strength 3]

**Weaknesses in our context:**
- [Weakness 1 — be honest and specific]
- [Weakness 2]

**Pricing / licensing:** [Relevant cost model, especially if cost was a factor]

### [Technology B]

**What it is:** [One sentence description]

**Version evaluated:** [vX.Y]

**Core strengths in our context:**
- [Strength 1]
- [Strength 2]
- [Strength 3]

**Weaknesses in our context:**
- [Weakness 1]
- [Weakness 2]

**Pricing / licensing:** [Relevant cost model]

---

## Hands-On Testing

### Test Setup

[Describe how you tested. Synthetic benchmarks are useful but not the whole story — explain what you did beyond running `pgbench`.]

We built a [test harness / proof of concept] that:
- Generated realistic data matching our production schema and access patterns
- Ran for [duration] against [hardware spec / RDS instance type]
- Measured [specific metrics]

**Test data:** [e.g., 10M synthetic event records matching our production distribution]

### Test: Write Throughput

```python
# Tech A — PostgreSQL bulk insert via COPY
import psycopg2

def bulk_insert_events(events: list[dict]) -> None:
    with psycopg2.connect(PG_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("COPY events (user_id, event_type, payload) FROM STDIN", ...)
```

```javascript
// Tech B — MongoDB bulk write
const result = await db.collection('events').bulkWrite(
  events.map(event => ({
    insertOne: { document: event }
  })),
  { ordered: false }  // unordered for maximum throughput
);
```

### Test Results

| Test | Tech A | Tech B | Notes |
|------|--------|--------|-------|
| Single-row insert P50 | [X]ms | [X]ms | [Context] |
| Single-row insert P99 | [X]ms | [X]ms | [Context] |
| Bulk insert (1k rows) | [X]ms | [X]ms | [Context] |
| Complex join query P50 | [X]ms | [X]ms | [Context] |
| Aggregation query P50 | [X]ms | [X]ms | [Context] |
| Storage per 1M records | [X]MB | [X]MB | [Context] |

> **Important caveat:** [e.g., These results reflect our specific access patterns and hardware. Your results will differ. The benchmark is a data point, not a verdict.]

---

## Evaluation Summary

| Criterion | Tech A | Tech B | Winner |
|-----------|--------|--------|--------|
| Write throughput | [score/10] | [score/10] | [A/B/Tie] |
| Query flexibility | [score/10] | [score/10] | [A/B/Tie] |
| Operational complexity | [score/10] | [score/10] | [A/B/Tie] |
| Team familiarity | [score/10] | [score/10] | [A/B/Tie] |
| Ecosystem maturity | [score/10] | [score/10] | [A/B/Tie] |
| Licensing / cost | [score/10] | [score/10] | [A/B/Tie] |
| **Weighted total** | **[X/60]** | **[X/60]** | **[A/B]** |

---

## Our Decision

**We chose [Technology A/B].**

### Key Deciding Factors

1. **[Factor 1]:** [Explain why this tipped the balance. Be specific — "it was faster" is less useful than "its P99 write latency was 28ms vs 67ms, which kept us within our 50ms SLA under our peak load"]
2. **[Factor 2]:** [Explanation]
3. **[Factor 3]:** [Explanation]

### Trade-offs We Accepted

- We accepted [trade-off 1, e.g.: 40% higher storage costs] because [reason, e.g.: the query flexibility savings outweigh it at our scale]
- We accepted [trade-off 2] because [reason]

### What Would Change Our Decision

[This is one of the most useful things you can include — under what circumstances would you revisit?]

We would reconsider this decision if:
- Our write volume grew beyond [X writes/second]
- [Condition 2]
- [Condition 3]

---

## Implementation Notes

[Brief notes on how you integrated the chosen technology. Link to the ADR and/or implementation PR.]

Key implementation decisions:
- [e.g., We used table partitioning by `created_at` month from day one, even though we don't need it yet — adding it retrospectively is painful]
- [e.g., We wrapped the client in an internal repository class so we can swap the underlying technology later if needed]
- [Link to ADR / RFC / implementation PR]

---

## Recommendations for Other Teams

[Under what circumstances should a different team make a different choice? This is the most transferable part of the post.]

**Choose [Tech A] if:**
- [Condition 1]
- [Condition 2]

**Choose [Tech B] if:**
- [Condition 1]
- [Condition 2]

**Revisit the decision entirely if:**
- [Condition that makes both options wrong]

---

## Further Reading

- [Official documentation for Tech A](link)
- [Official documentation for Tech B](link)
- [Internal ADR](link)
- [Any prior evaluations by other teams](link)

---

*Questions? Leave a comment or reach out in [#relevant-slack-channel].*

---

### Publishing Checklist

- [ ] Decision date is stated (so readers know how current this is)
- [ ] Success criteria are listed explicitly before the results
- [ ] Benchmark caveats are honest and prominent
- [ ] "What would change our decision" section is filled in
- [ ] Technical review completed by [@reviewer]
- [ ] Both technologies reviewed for factual accuracy
