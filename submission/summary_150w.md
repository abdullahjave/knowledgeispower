# Community-paper paragraph (≤150 words)

**scp-graphfs-mcp: which biological priors help reconstruct single-cell proteomes?**
We asked whether prior biological knowledge improves imputation of missing single-cell proteomics values beyond data-only
methods (kNN, low-rank). Every test was preregistered, developed on three datasets and confirmed on untouched holdouts.

**Results:**
- **Curated knowledge:** among 22 knowledge sources, curated physical complexes (Complex Portal, PDB co-structure, CORUM)
  are the most accurate prior, and every source beats its scrambled null. But none beats kNN meaningfully on its own.
- **Empirical priors:** protein co-regulation learned from 16 public single-cell datasets plus CCLE and ProteomeHD,
  stacked with kNN and low-rank, was **confirmed on an untouched holdout** (Brunner 2022, timsTOF DIA). It gave 2.4–5.4%
  lower RMSE than the best data-only method and 6–9% lower than kNN, 6/6 tests. On a second holdout the gain was below 1%.
- **Curated on top of empirical:** curated complexes add nothing once the empirical prior is used.

Benchmark, provenance and an MCP server for agents: github.com/xX-its-amit-Xx/knowledgeispower.
