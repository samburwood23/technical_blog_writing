# Tool / Technology Deep Dive Template

> **Usage:** Copy this template, replace all `[PLACEHOLDER]` text, and delete this header block before publishing.
>
> **Best for:** Teaching others about a specific tool, library, or technology — what it is, when to reach for it, and how to use it effectively in our stack.
>
> **Ideal length:** 1,200–2,000 words

---

# Complete Guide to [Tool Name] for [Specific Use Case]

**Author:** [Your Name]
**Date:** [Publication Date]
**Tags:** [e.g., tooling, infrastructure, testing, frontend]
**Version covered:** [Tool vX.Y — state the version so the post stays useful over time]

---

## TL;DR

> One paragraph: what the tool is, the single most important thing it does well, and who should read this post.
>
> _Example: Testcontainers is a library that spins up real Docker containers during your test suite — databases, message brokers, anything — so your integration tests hit the real thing, not a mock. If you're maintaining hand-rolled mock infrastructure for tests, this post will show you a better path._

---

## Why [Tool Name] Matters

### The Problem It Solves

[Describe the pain that existed before this tool. Be specific — generic "it makes things easier" isn't useful.]

- [Concrete pain point 1, e.g.: "We were maintaining three separate SQLite shims to fake Postgres behaviour in tests, and they diverged every time we upgraded Postgres."]
- [Concrete pain point 2]
- [Concrete pain point 3]

### Who Should Use It

**Good fit if you:**
- [Condition 1, e.g.: already use Docker in your dev environment]
- [Condition 2]
- [Condition 3]

**Not a good fit if you:**
- [Counter-condition 1, e.g.: your CI runners don't have Docker available]
- [Counter-condition 2]

### How It Fits Our Stack

[Explain where this tool sits in our existing architecture/workflow. A one-line diagram helps.]

```
[Our CI pipeline] → [Tool] → [Test results / Build artefact / Deployed service]
```

---

## Getting Started

### Prerequisites

- [Requirement 1, e.g.: Docker Desktop ≥ 4.x]
- [Requirement 2, e.g.: Python ≥ 3.11]
- [Requirement 3]

### Installation

```bash
# Package manager install
pip install testcontainers[postgres]

# Or via our internal package index
pip install testcontainers[postgres] --index-url https://pypi.internal.example.com/simple/
```

### Minimal Working Example

[Show the absolute simplest thing that works — 10-20 lines. Readers should be able to copy-paste this and see a result immediately.]

```python
from testcontainers.postgres import PostgresContainer

def test_database_connection():
    with PostgresContainer("postgres:15") as pg:
        connection_url = pg.get_connection_url()
        # Your test code here — the container is live and ready
        assert connection_url.startswith("postgresql+psycopg2://")
```

---

## Core Concepts

### Concept 1: [Name — e.g., Container Lifecycle]

[Explain the concept in plain language, then show code.]

[Tool name] manages [concept] by [brief explanation]. The key thing to understand is [key insight].

```python
# Annotated example demonstrating the concept
with PostgresContainer("postgres:15") as pg:
    # Container starts here — Docker pulls image if not cached
    url = pg.get_connection_url()
    run_migrations(url)           # your setup

    yield url                     # test runs

# Container is stopped and removed here — no manual cleanup
```

> **Gotcha:** [Common misunderstanding or trap related to this concept]

### Concept 2: [Name — e.g., Configuration]

```python
# Show configuration options with inline comments
pg = PostgresContainer("postgres:15") \
    .with_env("POSTGRES_DB", "testdb") \
    .with_env("POSTGRES_USER", "testuser") \
    .with_bind_ports(5432, 5433)   # expose on a fixed local port
```

### Concept 3: [Name — e.g., Waiting for Readiness]

[Some concepts need more prose — write as much as the topic needs.]

```python
# Example with wait strategy
from testcontainers.core.waiting_utils import wait_for_logs

container.with_wait_for(wait_for_logs("database system is ready"))
```

---

## Real-World Project

### The Scenario

[Describe a realistic project or task in our codebase that uses this tool. More concrete than a toy example.]

We used [tool name] to [specific task, e.g.: replace our pytest-postgres fixture with a container-backed one across the payments service]. Here's the full setup:

### Full Working Example

```python
# conftest.py — shared fixture for the payments service test suite
import pytest
from sqlalchemy import create_engine
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="session")
def postgres_container():
    """
    Starts a real Postgres container once per test session.
    Costs ~3s on first run (image pull), then reuses the running container.
    """
    with PostgresContainer("postgres:15-alpine") as pg:
        engine = create_engine(pg.get_connection_url())
        # Run Alembic migrations against the fresh container
        run_alembic_migrations(engine)
        yield engine

@pytest.fixture(autouse=True)
def rollback_after_test(postgres_container):
    """Wraps each test in a transaction that gets rolled back."""
    connection = postgres_container.connect()
    transaction = connection.begin()
    yield connection
    transaction.rollback()
    connection.close()
```

### Common Pitfalls and Solutions

| Pitfall | Why It Happens | Fix |
|---------|---------------|-----|
| `DockerException: Error while fetching server API version` | Docker not running | Start Docker Desktop; check `docker info` |
| Container takes 60+ seconds to start | Image not cached locally | Pre-pull in CI: `docker pull postgres:15-alpine` |
| Port conflict on `5432` | Local Postgres running | Use `.with_bind_ports(5432, 0)` to assign a random port |
| Tests pass locally, fail in CI | CI runner lacks Docker | Use a Docker-in-Docker CI executor |

---

## Best Practices

### Performance

- **Session-scope expensive containers** — starting a Postgres container takes 2-5 seconds. Use `scope="session"` in pytest fixtures and wrap tests in transactions that roll back rather than recreating the container per test.
- **Use Alpine images** — `postgres:15-alpine` is ~80MB vs ~370MB for the full image. Faster pulls in CI.
- **Pre-pull in CI** — add a `docker pull` step before your test step to separate network time from test time.

### Security

- [Security consideration relevant to the tool, e.g.: Never expose container ports on `0.0.0.0` in shared CI environments]
- [e.g.: Use short-lived credentials generated per container rather than hardcoded test passwords]

### Production Readiness

- [Note about what this tool is/isn't appropriate for in production]
- [Any monitoring or observability considerations]

---

## When to Use [Tool Name] vs. Alternatives

| Scenario | [Tool Name] | [Alternative A] | [Alternative B] |
|----------|------------|-----------------|-----------------|
| Integration tests against real DB | ✅ Best choice | ⚠️ Requires setup | ❌ Mocks behaviour |
| Unit tests with no I/O | ❌ Overkill | ❌ Overkill | ✅ Best choice |
| [Scenario 3] | [Assessment] | [Assessment] | [Assessment] |

**Our recommendation:** [When does our team reach for this tool vs. the alternatives?]

---

## Further Reading

- [Official documentation](link)
- [Link to internal ADR (Architecture Decision Record) if one exists]
- [Related internal blog posts]
- [Useful community resources]

---

*Questions? Leave a comment or ask in [#relevant-slack-channel].*

---

### Publishing Checklist

- [ ] Version number stated in the header
- [ ] All code examples are tested against the stated version
- [ ] "Not a good fit" section is honest and complete
- [ ] Pitfalls section covers the top 3 issues we actually encountered
- [ ] Technical review completed by [@reviewer]
