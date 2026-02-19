# Problem-Solution Case Study Template

> **Usage:** Copy this template, replace all `[PLACEHOLDER]` text, and delete this header block before publishing.
>
> **Best for:** Sharing how you solved a specific technical challenge — outages, bottlenecks, tricky integrations, reliability issues.
>
> **Ideal length:** 1,000–1,500 words

---

# How We Solved [Specific Problem] at [Team/Project Name]

**Author:** [Your Name]
**Date:** [Publication Date]
**Tags:** [e.g., backend, performance, reliability, python]

---

## TL;DR

> One or two sentences summarising the problem and the fix. Readers who skim will start here.
>
> _Example: Our background job processor was silently dropping ~5% of tasks under load. We fixed it by replacing fire-and-forget celery calls with an explicit acknowledgement pattern, reducing task loss to zero._

---

## The Challenge

### Background

[Describe the system, service, or codebase involved. Give just enough context for someone unfamiliar with the team to understand the setting — 2-3 sentences.]

### What Was Going Wrong

[Describe the symptom from the user's or on-call engineer's perspective. Be concrete: error messages, metrics, user complaints.]

```
# Example: paste a real error message or log snippet here
TaskError: Worker lost while processing job_id=8a3f2c
Traceback (most recent call last):
  ...
```

### Why It Mattered

- **Business impact:** [e.g., X% of checkout confirmations were delayed by up to 30 seconds]
- **Engineering impact:** [e.g., on-call alerts firing 3× per week, 2-hour average investigation time]
- **Scope:** [How many users/systems were affected?]

### What We Tried First (and Why It Failed)

[Describe your first attempt. Don't skip this — it's the most useful part for readers debugging similar problems.]

- **Attempt 1:** [What you tried] — [Why it didn't work]
- **Attempt 2:** [What you tried] — [Why it didn't work]

---

## Root Cause

[Explain the actual cause once you found it. Use a diagram if it helps. Keep it technical but accessible.]

> **Key insight:** [Summarise the "aha" moment in one sentence.]

---

## Our Solution

### Approach

[Describe the strategy at a high level before showing code. Explain *why* you chose this approach over alternatives.]

We decided to [high-level approach] because:
- [Reason 1]
- [Reason 2]
- [Trade-off accepted: reason 3]

### Implementation

#### Step 1: [First Change]

[Explain what this step does and why it's necessary before showing the code.]

```python
# Before: fire-and-forget with no acknowledgement
def schedule_job(job_data: dict) -> None:
    process_job.delay(job_data)

# After: explicit result tracking with retry budget
def schedule_job(job_data: dict) -> AsyncResult:
    result = process_job.apply_async(
        args=[job_data],
        retry=True,
        retry_policy={
            "max_retries": 3,
            "interval_start": 0,
            "interval_step": 0.2,
            "interval_max": 0.5,
        },
    )
    JobTracker.record(result.id, job_data["type"])
    return result
```

#### Step 2: [Second Change]

[Continue the pattern — explain, then show code.]

```python
# Add explanation comments to non-obvious code
```

#### Step 3: [Configuration / Infrastructure Change]

[Not all solutions are code changes. Document config, infrastructure, or process changes too.]

```yaml
# Example: updated celery config
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
```

### Rollout

[Describe how you deployed safely: feature flags, canary, phased rollout, etc.]

- [x] Deployed to staging and ran load tests
- [x] Enabled for 10% of traffic on [date]
- [x] Rolled out to 100% after 48 hours of clean metrics

---

## Results

### Metrics

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Task loss rate | ~5% | 0% | -100% |
| On-call alerts / week | 3 | 0 | -100% |
| P99 processing latency | 8.2s | 1.4s | -83% |

### Qualitative Improvements

- [e.g., Engineers no longer need to manually reconcile dropped jobs on Monday mornings]
- [e.g., The fix also surfaced a second unrelated bug we hadn't noticed]

---

## Lessons Learned

- **[Lesson 1]:** [e.g., Silent failures are worse than noisy ones — add explicit acknowledgement wherever work is handed off between systems]
- **[Lesson 2]:** [e.g., Load testing in staging didn't reproduce the bug; we needed production traffic patterns]
- **[Lesson 3]:** [What you'd do differently if you were starting over]

---

## Takeaways

### When to Use This Approach

- [Scenario where this solution is a good fit]
- [Another appropriate scenario]

### When NOT to Use It

- [Trade-off or scenario where a different approach is better]

### Alternative Solutions We Considered

| Approach | Pros | Cons | Why We Didn't Choose It |
|----------|------|------|------------------------|
| [Option A] | [Pros] | [Cons] | [Reason] |
| [Option B] | [Pros] | [Cons] | [Reason] |

---

## Further Reading

- [Link to internal runbook or post-mortem]
- [Link to relevant library docs]
- [Link to a related post by another team member]

---

*Questions? Leave a comment or reach out in [#relevant-slack-channel].*

---

### Publishing Checklist

- [ ] Replaced all `[PLACEHOLDER]` text
- [ ] Code examples are tested and working
- [ ] Sensitive data (keys, internal hostnames, customer data) removed
- [ ] Technical review completed by [@reviewer]
- [ ] Metrics are accurate and approved to share
