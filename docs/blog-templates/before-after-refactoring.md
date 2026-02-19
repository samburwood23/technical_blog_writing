# Before / After Refactoring Story Template

> **Usage:** Copy this template, replace all `[PLACEHOLDER]` text, and delete this header block before publishing.
>
> **Best for:** Documenting a significant code improvement — showing the messy reality of legacy code, the process of improving it, and the measurable outcome. Equally valuable for a 2-hour cleanup or a 3-month project.
>
> **Ideal length:** 1,000–1,800 words

---

# Refactoring [Component/System]: From [Problem Description] to [Solution Description]

**Author:** [Your Name]
**Date:** [Publication Date]
**Tags:** [e.g., refactoring, architecture, python, testing, technical-debt]

---

## TL;DR

> What was broken, what you did, what improved. Two or three sentences.
>
> _Example: Our order processing module had grown to 900 lines with no tests and 14 different callers passing subtly different argument shapes. We split it into three focused services, added a typed interface layer, and got test coverage from 0% to 87%. Deployments that used to require a 30-minute manual verification step now ship automatically._

---

## The "Before" State

### What It Looked Like

[Give context on the code. How old is it? How did it get this way? A few sentences of honest history helps readers see their own codebase in it.]

This code started as [origin story — e.g., a quick proof of concept in Q3 2021 that was "only temporary"]. Over [timeframe], it accumulated [description of what happened].

```python
# The original function — real complexity, not a strawman
def process_order(order_id, user=None, send_email=True, dry_run=False,
                  legacy_mode=False, retry_count=0, **kwargs):
    """Process an order. See JIRA-1234 for context."""
    if legacy_mode:
        # TODO: remove this after migration (added 2021-11-03)
        order_id = int(order_id)

    order = db.query(f"SELECT * FROM orders WHERE id = {order_id}")  # nosec
    if not order:
        if retry_count < 3:
            time.sleep(2 ** retry_count)
            return process_order(order_id, user, send_email, dry_run,
                                 legacy_mode, retry_count + 1, **kwargs)
        return None

    # 200 more lines...
```

### Pain Points

- **[Pain point 1]:** [e.g., The SQL string interpolation was a SQL injection risk that required a `# nosec` suppression comment to pass our scanner]
- **[Pain point 2]:** [e.g., The `**kwargs` signature made it impossible to know what callers were actually passing without reading all 14 call sites]
- **[Pain point 3]:** [e.g., The recursive retry logic made stack traces unreadable in Sentry]
- **[Pain point 4]:** [e.g., Zero test coverage — no one wanted to write tests for something this tangled]

### Metrics Showing the Problem

| Metric | Value |
|--------|-------|
| Lines of code | [e.g., 900] |
| Test coverage | [e.g., 0%] |
| Average time to add a feature | [e.g., 3 days] |
| Deployment verification time | [e.g., 30 minutes manual] |
| Sentry errors per week | [e.g., 12] |
| On-call escalations per month | [e.g., 4] |

---

## Why We Refactored

### The Triggering Event

[What finally made the team decide to tackle this? Be honest — "we always meant to" isn't a trigger. Good examples: a production incident, a new hire who couldn't understand the code, a performance requirement that couldn't be met with the existing structure.]

The decision was triggered by [specific event]. This made it clear that [what the event revealed about the code's limits].

### Business Drivers

- [Driver 1, e.g.: We needed to support a new payment provider by Q2, which required changes to the core order flow]
- [Driver 2, e.g.: A recent incident cost us 2 hours of investigation because no one understood the retry logic]

### What We Decided Not to Rewrite

[Scope decisions are as important as the work itself. What did you deliberately leave alone?]

We kept [specific parts] unchanged because [reasons — e.g., they worked correctly, touched too many other systems, or were out of scope for this quarter].

---

## The Refactoring Process

### Our Approach

[Describe the strategy: did you use the strangler fig pattern, add tests before changing code, split into parallel tracks, etc.?]

We followed this sequence:
1. **Add characterisation tests** — write tests that describe existing behaviour (even the wrong bits) so we'd know if we broke anything
2. **Extract and isolate** — move logic into focused functions before changing it
3. **Improve** — make the actual improvements once the code had clear boundaries

### Step 1: [First Concrete Change]

[Explain what this step accomplishes and why you did it before the next one.]

```python
# Before: raw SQL string with injection risk
order = db.query(f"SELECT * FROM orders WHERE id = {order_id}")

# After: parameterised query
order = db.query(
    "SELECT * FROM orders WHERE id = :order_id",
    {"order_id": order_id}
)
```

### Step 2: [Second Change — Extract Retry Logic]

```python
# Before: recursive retry buried in the business logic function
def process_order(..., retry_count=0, ...):
    if not order:
        if retry_count < 3:
            time.sleep(2 ** retry_count)
            return process_order(..., retry_count + 1, ...)

# After: explicit retry decorator — behaviour is the same, but visible
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
def fetch_order(order_id: int) -> Order:
    order = OrderRepository.get(order_id)
    if order is None:
        raise OrderNotFoundError(order_id)
    return order
```

### Step 3: [Third Change — Type the Interface]

```python
# Before: any caller could pass anything
def process_order(order_id, user=None, send_email=True, dry_run=False,
                  legacy_mode=False, retry_count=0, **kwargs):

# After: explicit typed dataclass — IDE completion works, callers are obvious
from dataclasses import dataclass, field

@dataclass
class OrderProcessingRequest:
    order_id: int
    user_id: int
    notify: bool = True
    dry_run: bool = False

def process_order(request: OrderProcessingRequest) -> OrderResult:
    ...
```

### Step 4: [Remove Legacy Code]

[Sometimes a refactor's most impactful step is a deletion.]

After confirming no callers were using `legacy_mode=True` (verified via [grep / feature flag telemetry / migration tracker]), we deleted the branch entirely — [N] lines of code removed.

---

## Results

### Code Metrics

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Lines of code | 900 | 310 | -66% |
| Test coverage | 0% | 87% | +87pp |
| Cyclomatic complexity (main fn) | 24 | 4 | -83% |
| Number of public call signatures | 1 (with **kwargs) | 3 (typed) | — |

### Operational Metrics

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Sentry errors / week | 12 | 1 | -92% |
| Deployment verification time | 30 min manual | Automated | -100% |
| Average time to add a feature | 3 days | 4 hours | -83% |

### Developer Experience

- [Qualitative improvement 1, e.g.: New team members can now understand the order flow in under an hour — previously it took a full day with a guided walkthrough]
- [Qualitative improvement 2, e.g.: The typed interface caught 2 bugs during the refactor that had been silently failing in production]

---

## Lessons Learned

- **[Lesson 1]:** [e.g., Adding characterisation tests before changing anything was the single most valuable step. It took a day but saved us from three separate regressions.]
- **[Lesson 2]:** [e.g., The `**kwargs` pattern was a signal that the function was doing too many things. We'll flag this in code review going forward.]
- **[Lesson 3]:** [e.g., We should have deleted the `legacy_mode` branch 6 months ago when the migration completed. Keeping dead code "just in case" has a real cost.]
- **[What we'd do differently]:** [e.g., Next time we'd involve QA earlier — they caught an edge case in the notification logic that we'd missed in our characterisation tests.]

---

## Further Reading

- [Link to the PR or commit range]
- [Link to ADR documenting the new architecture]
- [Link to relevant internal runbook]

---

*Questions? Leave a comment or reach out in [#relevant-slack-channel].*

---

### Publishing Checklist

- [ ] "Before" code is honest — don't sanitise it into a strawman
- [ ] Metrics table is filled in with real numbers
- [ ] Lessons section includes what you'd do *differently*
- [ ] Code examples reflect the actual PR (not a cleaned-up idealisation)
- [ ] Technical review completed by [@reviewer]
- [ ] Legacy/old code has been confirmed deleted or scheduled for deletion
