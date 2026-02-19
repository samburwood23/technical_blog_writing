# Performance Optimization Story Template

> **Usage:** Copy this template, replace all `[PLACEHOLDER]` text, and delete this header block before publishing.
>
> **Best for:** Documenting a performance improvement project — from identifying the problem, through the investigation, to the measurable result. Works for any kind of performance: latency, throughput, build time, bundle size, memory usage.
>
> **Ideal length:** 1,200–2,000 words

---

# How We Improved [System/Feature] Performance by [X]%

**Author:** [Your Name]
**Date:** [Publication Date]
**Tags:** [e.g., performance, frontend, database, caching, profiling]
**Improvement type:** [Latency / Throughput / Memory / Build time / Bundle size / other]

---

## TL;DR

> Baseline, what you changed, end result. Two or three sentences.
>
> _Example: Our product listing page was taking 4.8 seconds to load on mobile. We identified three independent bottlenecks — an N+1 query, an uncompressed 1.2MB image payload, and a render-blocking third-party script — and resolved all three. Page load dropped to 1.1 seconds (77% improvement), and mobile conversion rate increased by 12%._

---

## The Performance Problem

### Baseline Metrics

[Always start with numbers. "It was slow" is not a baseline.]

| Metric | Baseline Value | Measurement Method |
|--------|---------------|-------------------|
| [e.g., Page load time P50] | [X]s | [e.g., WebPageTest, 4G throttled, Moto G4] |
| [e.g., Page load time P99] | [X]s | [same] |
| [e.g., Time to interactive] | [X]s | [e.g., Lighthouse in CI] |
| [e.g., API response time P50] | [X]ms | [e.g., Datadog APM] |
| [e.g., Memory usage (peak)] | [X]MB | [e.g., heap profiler] |

### Business Impact

[Why did this matter to users or the business? Skip if it was a pure engineering quality concern — that's valid too.]

- [Impact 1, e.g.: Our mobile bounce rate was 68% — industry data suggests this is largely driven by load times above 3 seconds]
- [Impact 2, e.g.: The endpoint was in the critical path for our checkout flow; every 100ms of added latency was costing us ~0.5% in conversion]
- [Impact 3, e.g.: Our CI pipeline was taking 22 minutes — developer flow was broken]

### How We Discovered the Issue

[Describe the trigger: user complaint, alerting, a scheduled performance review, someone noticing it personally.]

The issue surfaced when [trigger]. We confirmed the problem was real (not a one-off) by [how you validated it — e.g., checking P99 over a 7-day window, running Lighthouse in three different network conditions].

---

## Investigation Process

### Tools Used

| Tool | What We Used It For |
|------|-------------------|
| [e.g., Chrome DevTools Performance tab] | [e.g., Identifying render-blocking resources] |
| [e.g., `EXPLAIN ANALYZE`] | [e.g., Query planning and execution cost] |
| [e.g., `py-spy`] | [e.g., CPU profiling of the API process] |
| [e.g., Datadog APM] | [e.g., Distributed trace to find slowest spans] |

### Investigation Steps

#### Step 1: [First Investigation — e.g., Profile the API]

[Describe what you did and what you found. Show the tool output.]

```bash
# CPU profile of the API process under load
py-spy record -o profile.svg --pid $(pgrep -f "uvicorn main:app")
# Run for 30 seconds under representative load
```

The flamegraph showed [what you found — e.g., 60% of CPU time in `serialize_product_list`].

#### Step 2: [Second Investigation — e.g., Check Database Queries]

```sql
-- Run EXPLAIN ANALYZE on the slow query
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT p.*, c.name as category_name, AVG(r.rating) as avg_rating
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
LEFT JOIN reviews r ON r.product_id = p.id
WHERE p.active = true
GROUP BY p.id, c.name
ORDER BY p.created_at DESC
LIMIT 50;
```

```
Seq Scan on products (cost=0.00..84231.45 rows=12847 width=842)
                     (actual time=0.042..2847.223 rows=12847 loops=1)
  Filter: active
  Rows Removed by Filter: 3
Buffers: shared hit=4 read=9821
Planning Time: 1.2 ms
Execution Time: 2891.4 ms          ← 2.9 seconds for this query alone
```

#### Step 3: [Third Investigation — e.g., Measure Frontend Bundle]

```bash
npm run build -- --analyze
# Or: npx webpack-bundle-analyzer dist/static/js/*.js
```

Key findings:
- [Finding 1, e.g.: `moment.js` (72KB gzipped) included for a single `formatDate` call]
- [Finding 2, e.g.: Full `lodash` bundle (24KB gzipped) instead of cherry-picked functions]

### What the Data Revealed

[Summarise the findings before jumping to solutions — what were the actual bottlenecks?]

We found three independent bottlenecks contributing roughly equally to the overall latency:

1. **[Bottleneck 1, e.g., N+1 query]** — [Impact: e.g., 2.9s per request]
2. **[Bottleneck 2, e.g., missing index]** — [Impact]
3. **[Bottleneck 3, e.g., 1.2MB uncompressed image]** — [Impact]

> **Surprising finding:** [e.g., We expected the rendering to be the bottleneck based on initial profiling, but 80% of the time was actually in serialization. Always profile before optimising.]

---

## Optimization Strategy

### Quick Wins (Week 1)

Changes that were low-effort and high-impact:

#### Fix 1: [Name — e.g., Add Composite Index]

**Effort:** [e.g., 1 hour] | **Impact:** [e.g., -2.4s per request]

```sql
-- Add covering index for the hot query
CREATE INDEX CONCURRENTLY idx_products_active_created
ON products (active, created_at DESC)
INCLUDE (id, name, price, category_id);
```

**Result:** Query time dropped from 2,891ms to 48ms.

#### Fix 2: [Name — e.g., Enable Response Compression]

**Effort:** [e.g., 30 minutes] | **Impact:** [e.g., -600ms on mobile]

```python
# Add gzip/brotli compression middleware
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

**Result:** [Measured improvement]

---

### Architectural Changes (Week 2–3)

Changes that required more design work or had more risk:

#### Fix 3: [Name — e.g., Resolve N+1 Query]

**Effort:** [e.g., 2 days] | **Impact:** [e.g., -800ms per request at 50 products]

```python
# Before: N+1 — one query per product to fetch its category
def get_products():
    products = Product.query.filter_by(active=True).all()
    for product in products:
        product.category  # triggers a separate SELECT for each product
    return products

# After: single query with JOIN
def get_products():
    return (
        Product.query
        .filter_by(active=True)
        .options(joinedload(Product.category))
        .options(
            selectinload(Product.reviews)
            .load_only(Review.rating)
        )
        .order_by(Product.created_at.desc())
        .limit(50)
        .all()
    )
```

**Result:** [Measured improvement]

---

### Code Optimizations (Week 4)

Fine-grained improvements after the big wins were in:

#### Fix 4: [Name — e.g., Replace moment.js]

**Effort:** [e.g., 4 hours] | **Impact:** [e.g., -72KB gzipped bundle size]

```javascript
// Before: full moment.js for one utility function
import moment from 'moment';
const formatted = moment(date).format('MMM D, YYYY');

// After: native Intl API — zero bundle cost
const formatted = new Intl.DateTimeFormat('en-US', {
  month: 'short', day: 'numeric', year: 'numeric'
}).format(new Date(date));
```

---

## Final Results

### Metrics

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| [Page load P50] | [X]s | [X]s | [X]% faster |
| [Page load P99] | [X]s | [X]s | [X]% faster |
| [API response P50] | [X]ms | [X]ms | [X]% faster |
| [Bundle size (gzipped)] | [X]KB | [X]KB | [X]% smaller |
| [Memory usage peak] | [X]MB | [X]MB | [X]% lower |

### Business Metrics (if applicable)

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| [e.g., Mobile bounce rate] | [X]% | [X]% | [+/-X]pp |
| [e.g., Checkout conversion] | [X]% | [X]% | [+/-X]pp |
| [e.g., CI pipeline time] | [X]min | [X]min | [X]% faster |

### Return on Investment

[Optional but powerful — how long did this take vs. what benefit did it deliver?]

Total engineering time: ~[X] days across [N] engineers.
Estimated annual value: [e.g., ~[X]% uplift in conversion × revenue = $X].

---

## General Principles

What we learned about performance optimization that applies beyond this specific case:

1. **Always measure before optimising.** [Brief elaboration on your specific experience — e.g., We were sure the frontend was the problem; the database was actually 80% of the issue.]
2. **Profile the production workload, not a toy example.** [e.g., Our local benchmarks didn't show the N+1 because we had 5 test products. Production had 12,000.]
3. **Fix the biggest bottleneck first.** [e.g., Fixing the index before the N+1 would have had 3× less impact, because the index optimises a query that runs N+1 times.]
4. **[Your own principle from this project]**

### Tools We'd Recommend

| Tool | Use Case | Getting Started |
|------|----------|----------------|
| [Tool 1] | [What it's good for] | [Link or note] |
| [Tool 2] | [What it's good for] | [Link or note] |

---

## Further Reading

- [Link to the PR or commit range]
- [Link to performance monitoring dashboard]
- [Relevant documentation or external resources]

---

*Questions? Leave a comment or reach out in [#relevant-slack-channel].*

---

### Publishing Checklist

- [ ] Baseline metrics table is filled in with real numbers and measurement methods
- [ ] "Surprising finding" callout is honest
- [ ] Each optimization lists effort, impact, and measured result
- [ ] "Always measure first" principle comes through clearly
- [ ] Final results table matches actual production measurements
- [ ] Technical review completed by [@reviewer]
