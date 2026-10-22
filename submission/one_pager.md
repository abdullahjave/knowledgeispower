# scp-graphfs-mcp: biological priors for single-cell proteomics imputation (one page)

**Team:** Amit Shenoy (lead); Eeshan Khan (S1 variant bridge); Abdullah Javed (S5 Copilot CLI recipe);
Fatima Zahra (S6 glossary); @aggravating08 (S7 hardening, S6); @imperorrp (S4 NIFty baseline).
**Repo:** https://github.com/xX-its-amit-Xx/knowledgeispower (Apache-2.0).

**Question.** Single-cell proteomics measures only part of each cell's proteome, and imputation fills in the rest. Does
*prior biological knowledge* (curated protein complexes, interaction networks, pathways, structures, public proteomics)
reconstruct missing values better than data-only methods such as kNN and low-rank completion?

**How we tested it (agents + rigour).**
- **Agent tooling:** an MCP server exposes priors, propagation, imputation, panel selection and a variant → complex bridge
  as tools. Claude Code agents built the priors, benchmarks and data pipelines.
- **Preregistration:** every claim was preregistered (14 amendments), developed on dev seeds over three datasets, and
  confirmed **once** on untouched holdouts with a 1% minimum effect size, paired bootstrap CIs and scrambled-prior nulls.

**Results.**

| Finding | Evidence |
|---|---|
| Curated *physical* complexes are the best knowledge prior | #1 of 22 representations (Complex Portal > PDB co-structure > CORUM > … > PPI, pathways, sequence embeddings). Every source beats its scrambled null |
| No knowledge prior alone beats kNN meaningfully | 0/66 representation × estimator pairs pass the dev gate |
| **Empirical prior transfers (H14, confirmed 6/6)** | Brunner 2022 holdout (HeLa, timsTOF DIA). Co-regulation from 16 public SCP datasets + CCLE + ProteomeHD, stacked with kNN and low-rank: in-complex RMSE −2.4 / −5.4% vs kNN + low-rank (MCAR / MNAR), −6.0 / −8.9% vs kNN, −2.5 / −4.3% vs scrambled reference. All CIs < 0 |
| Curated complexes add nothing on top of the empirical prior | −0.06% to −0.54%, CIs include 0 |
| Replication is partial | On the Khan 2023 holdout the gain over kNN + low-rank was 0.2–0.6% (< 1%): **1 of 2 holdouts** |

**Takeaway.** Biological priors help single-cell proteomics, but the useful prior is *empirical* protein co-regulation
borrowed from large public datasets, analogous to genotype-imputation reference panels. Curated complexes are correct
but become redundant once that data is available. We release the negative results alongside the positive one.

**Platforms/tools:** Claude Code (Anthropic), the MCP Python SDK, GitHub, and public data from scpdata/ExperimentHub,
CORUM, Complex Portal, STRING, hu.MAP, UniProt, PDB/SIFTS, Reactome, BioGRID, IntAct, Monarch, NCBI, Pharos, Pathway
Commons, CCLE and ProteomeHD. All are listed with SHA-256 in `data/PROVENANCE.md`.
