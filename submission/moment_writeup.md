# Moment write-up (paste into "Write up what you built")

**KnowledgeIsPower: scp-graphfs-mcp, which physical priors help AI agents reconstruct single-cell proteomes?**

**The problem.** Mass-spectrometry single-cell proteomics measures only 20–60% of each cell's proteins. Every
downstream analysis depends on how the missing values are filled in. Proteins are physical machines: subunits of a
complex are built in fixed stoichiometry, so they should rise and fall together. We asked whether that physical and
biological prior knowledge, served to AI agents as tools, reconstructs missing measurements better than data-only methods.

**What we built.**
- **An MCP server** (`scp-graphfs-mcp`) that gives any LLM agent tools to:
  - fetch curated protein complexes;
  - build knowledge graphs, with provenance and degree-preserving nulls;
  - propagate scores;
  - impute with a prior;
  - select measurement panels;
  - map a genetic variant to the protein machines it hits and to the partner subunits measured in a dataset.

  Recipes and real transcripts are included for Claude Code and GitHub Copilot CLI.
- **A preregistered benchmark over 22 knowledge representations:**
  - curated complexes (CORUM, Complex Portal, hu.MAP);
  - PDB co-structure, interaction networks (STRING, BioGRID, IntAct);
  - Reactome, Monarch phenotypes, NCBI co-citation;
  - Pharos, Pathway Commons, ProtT5 sequence embeddings;
  - CCLE and ProteomeHD bulk proteomics.

  It covers three estimators and borrows cross-domain ideas: reference panels from genotype imputation, reference
  projection from ancestry PCA, and cold-start from recommender systems.
- **A reference corpus:** 17 public single-cell proteomics datasets (~10k cells) rebuilt without R from scpdata. Every
  file has a SHA-256 checksum.

**What we learned (all preregistered; negative results reported).**
1. **Curated physical complex membership is the most accurate knowledge prior** (#1 of 22), and every source beats its
   scrambled null. But no curated prior alone beats plain kNN by a meaningful margin at single-cell resolution.
2. **Empirical prior knowledge transfers.** Protein co-regulation learned from public data, stacked with kNN and low-rank
   completion, was **confirmed 6/6 on an untouched holdout** (Brunner 2022, HeLa, timsTOF DIA, 30-cell subsamples).
   - It gave 2.4–5.4% lower RMSE on complex-member proteins than the best data-only method, and 6–9% lower than kNN.
   - It gave 2.5–4.3% lower RMSE than the same pipeline with a scrambled reference, so the gain comes from the biology,
     not from extra model capacity.
3. **Honest limits:**
   - Curated complexes add nothing measurable on top of the empirical prior.
   - On a second holdout (Khan 2023) the gain was below our 1% bar, so the result replicates on 1 of 2 holdouts.

**Prior art (checked live with Valency MCP Bond).** A literature sweep through Valency's MCP Bond, run before
submitting, surfaced the closest work:
- **Lupine** (Harris & Noble, MCP 2025) already learns imputation from many *bulk* proteomics datasets.
- **GIRAFI** (bioRxiv 2026) already uses prior-knowledge protein neighbourhoods for single-cell proteomics.

We narrowed our claims accordingly. Our contribution is the **preregistered, null-controlled head-to-head of curated
vs empirical priors for 30-cell single-cell targets, confirmed on an untouched holdout**. The full trace is in
`docs/valency_bond_prior_art.md`.

**Why it matters.** Small single-cell experiments can borrow structure from public data, just as genotype imputation
borrows from reference panels, and agents can do this through standard MCP tools. The benchmark, the nulls and the
preregistration log give the field a reproducible bar any new "knowledge-guided" imputer has to clear.

**Built with** Claude Code agents, the MCP Python SDK and Valency MCP Bond (literature/prior-art agent); 14 preregistered amendments; 117 passing tests; contributions
from six people through scoped, test-gated slots. Code: https://github.com/xX-its-amit-Xx/knowledgeispower (Apache-2.0).
