# Debugging / Troubleshooting Guide Template

> **Usage:** Copy this template, replace all `[PLACEHOLDER]` text, and delete this header block before publishing.
>
> **Best for:** Documenting the investigation and fix for a tricky or recurring problem so the next engineer who faces it doesn't start from scratch. Write this *immediately after* resolving an incident or a difficult bug — the details are sharpest then.
>
> **Ideal length:** 800–1,500 words

---

# Debugging [Problem Name]: [Short Description of the Symptom]

**Author:** [Your Name]
**Date:** [Publication Date]
**Tags:** [e.g., debugging, kubernetes, postgres, networking]
**Affected systems:** [e.g., payments-service, checkout-api]
**Severity when this occurred:** [e.g., P2 — degraded service for ~15% of users]

---

## TL;DR

> What the symptom was, what caused it, and the one-line fix. Engineers at 2am will read this first.
>
> _Example: Intermittent 504s from the checkout API were caused by a connection pool exhaustion in the payments client — not a network issue as alerts suggested. Fix: increase `PAYMENTS_CLIENT_POOL_SIZE` from 5 to 20 and add a pool wait timeout._

---

## Problem Description

### How It Appears

[Describe what an engineer first sees when this problem occurs. Be precise about error messages, metrics, and user impact — this is how the post gets found via search.]

When this problem occurs, you will typically see:

- **Error message:** `[Exact error string — copy from logs, don't paraphrase]`
- **In logs:**

```
2024-03-15T14:32:01Z ERROR payments-client: connection pool exhausted after 30s
  pool_size=5 checked_out=5 overflow=0 timeout=30
  at checkout_api/clients/payments.py:142
```

- **In metrics:** [e.g., `payments_client_pool_wait_time_seconds` P99 spikes above 30s; `checkout_api_5xx_rate` rises from 0.01% to 8%]
- **User impact:** [e.g., Users see a "Payment service temporarily unavailable" error on the checkout confirmation page]

### When It Tends to Happen

- [Condition 1, e.g.: Under sustained traffic above ~200 requests/second to the checkout endpoint]
- [Condition 2, e.g.: When the payments service P99 latency rises above ~500ms (e.g., during a deployment)]
- [Condition 3, e.g.: After a connection pool was recently resized without restarting the service]

### What It Is Not

[Help engineers rule out other causes quickly — this saves time in the middle of an incident.]

This is **not** caused by:
- A network partition between checkout-api and payments-service (check `payments_client_http_error_rate` — if it's 0, the network is fine)
- A Postgres slow query (payments-service itself is healthy; the bottleneck is the client pool in checkout-api)
- A memory leak (RSS stays flat)

---

## Diagnostic Checklist

Work through these in order. Each step takes 1-2 minutes.

- [ ] **Check the raw error message** — grep for the exact string `connection pool exhausted` in the last 15 minutes:

```bash
kubectl logs -l app=checkout-api --since=15m | grep "pool exhausted"
```

- [ ] **Check the pool metrics dashboard** — open [Grafana link] and look at the `checkout_api / payments_client / pool` panel

- [ ] **Confirm payments-service is healthy** — it should be returning 200s; if it's not, that's a separate incident:

```bash
kubectl exec -it checkout-api-pod -- curl -s payments-service/health | jq .
```

- [ ] **Check current pool configuration:**

```bash
kubectl exec -it checkout-api-pod -- printenv | grep PAYMENTS_CLIENT
# Expected: PAYMENTS_CLIENT_POOL_SIZE=5
# If it shows 20, the fix is already applied — something else is wrong
```

- [ ] **Check for slow payments responses** — if P99 > 500ms, the pool drains faster under normal traffic:

```bash
kubectl logs -l app=payments-service --since=15m | grep "slow_query"
```

---

## Common Scenarios and Fixes

### Scenario 1: Normal Traffic Spike (Most Common)

**Cause:** Traffic exceeded the pool's capacity. The default pool size of 5 is too small for peak load.

**Fix:**

```bash
# Immediate mitigation: increase pool size via environment variable
kubectl set env deployment/checkout-api PAYMENTS_CLIENT_POOL_SIZE=20

# Verify the change took effect (new pods will start rolling)
kubectl rollout status deployment/checkout-api

# Confirm pool size in running pod
kubectl exec -it $(kubectl get pod -l app=checkout-api -o name | head -1) \
  -- printenv PAYMENTS_CLIENT_POOL_SIZE
```

**Permanent fix:** Update the value in `infrastructure/helm/checkout-api/values.yaml` and raise a PR.

**Time to resolve:** ~3 minutes for mitigation, ~30 minutes for the PR.

---

### Scenario 2: Slow Payments Service

**Cause:** The payments service is responding slowly (P99 > 500ms), so connections are held for longer, exhausting the pool at lower traffic levels.

**Signs:**
- `payments_client_http_duration_seconds` P99 > 500ms in Grafana
- `kubectl logs -l app=payments-service` shows slow queries

**Fix:** Address the payments service slowness first (this is a separate issue — see [payments-service runbook](link)). The pool exhaustion will resolve on its own once payments responses are fast.

If you need to keep checkout-api running while payments is slow, temporarily increase the pool size (Scenario 1 fix) to buy time.

---

### Scenario 3: Post-Deployment Stale Configuration

**Cause:** A recent deployment changed the pool size in config but the old pods are still running with the old value.

**Signs:**
- `kubectl rollout history deployment/checkout-api` shows a recent deployment
- `PAYMENTS_CLIENT_POOL_SIZE` in the running pod doesn't match `values.yaml`

**Fix:**

```bash
# Force a fresh rollout to pick up the new config
kubectl rollout restart deployment/checkout-api
kubectl rollout status deployment/checkout-api
```

---

### Scenario 4: [Additional Scenario]

[Continue the pattern for each distinct root cause.]

---

## Prevention

### Monitoring Improvements

Add these alerts if they don't already exist:

```yaml
# Example Prometheus alert rule
- alert: PaymentsClientPoolNearExhaustion
  expr: |
    checkout_api_payments_client_pool_checked_out
    / checkout_api_payments_client_pool_size > 0.8
  for: 2m
  labels:
    severity: warning
  annotations:
    summary: "Payments client connection pool is >80% utilised"
    runbook: "https://internal.example.com/runbooks/checkout-api-pool"
```

### Code Patterns That Help

```python
# Add an explicit pool wait timeout so requests fail fast
# rather than queuing indefinitely
payments_client = PaymentsClient(
    pool_size=int(os.environ["PAYMENTS_CLIENT_POOL_SIZE"]),
    pool_timeout=5,      # raise after 5s waiting for a connection
    pool_pre_ping=True,  # verify connections before use
)
```

### Configuration Best Practices

- **Set `pool_timeout`** — without it, requests queue indefinitely and the user sees a 60-second timeout instead of a fast failure
- **Size the pool to your traffic model** — a good starting point is `(peak_rps × avg_response_time_seconds) × 1.5` (Little's Law + headroom)
- **Revisit pool sizes after significant traffic growth** — add it to your quarterly infrastructure review

---

## Escalation

If none of the scenarios above resolve the issue:

| Condition | Who to Contact | How |
|-----------|---------------|-----|
| Payments service is unhealthy | Payments team on-call | PagerDuty policy `payments-oncall` |
| Kubernetes cluster issues | Platform team | #platform-support + PagerDuty `platform-oncall` |
| Unexplained pool exhaustion after applying fixes | Team lead + SRE | #incidents channel |

**Information to include when escalating:**
- Output of `kubectl logs -l app=checkout-api --since=30m | grep pool`
- Screenshot of the pool metrics dashboard
- Current value of `PAYMENTS_CLIENT_POOL_SIZE`

---

## Incident History

| Date | Duration | Root Cause | Resolution |
|------|----------|-----------|------------|
| [Date] | [X min] | [Brief cause] | [Brief fix] |
| [Date] | [X min] | [Brief cause] | [Brief fix] |

---

*Questions? Leave a comment or reach out in [#relevant-slack-channel].*

---

### Publishing Checklist

- [ ] TL;DR is useful to someone at 2am with no context
- [ ] Error messages and log snippets are copied verbatim (not paraphrased)
- [ ] "What it is not" section covers the top 2-3 red herrings
- [ ] All `kubectl` / CLI commands are tested and correct
- [ ] Escalation contacts are current
- [ ] Technical review completed by [@reviewer who knows this system]
