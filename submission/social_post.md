# Social post (LinkedIn / X / Bluesky). Post publicly, then paste the link into Moment.

**Long version (LinkedIn / Bluesky thread):**
At the #OSIHackathon we asked: can AI agents use biological knowledge to fill in the 40–80% of proteins that
single-cell mass spec misses?

We built scp-graphfs-mcp, an MCP server that gives LLM agents tools for protein complexes, knowledge graphs, imputation,
panel design and variant → complex mapping. We then ran a preregistered benchmark over 22 knowledge sources and
17 public single-cell datasets.

What we found:
✅ Curated physical complexes are the most accurate knowledge prior (#1 of 22).
✅ Protein co-regulation learned from public data cut imputation error by 2.4–5.4% vs the best data-only method on an
untouched holdout (6/6 preregistered tests), beating a scrambled-reference control.
⚠️ Curated complexes add nothing on top of that, and the effect replicated on 1 of 2 holdouts. We report it all.

Open source: https://github.com/xX-its-amit-Xx/knowledgeispower
Team: Amit Shenoy, Eeshan Khan, Abdullah Javed, Fatima Zahra, @aggravating08, @imperorrp

**Short version (X, ≤280 chars):**
Can AI agents use biology to fill gaps in single-cell proteomics? Our #OSIHackathon MCP server + preregistered benchmark:
public protein co-regulation cut error 2.4–5.4% vs the best data-only method on an untouched holdout (6/6 tests).
https://github.com/xX-its-amit-Xx/knowledgeispower
