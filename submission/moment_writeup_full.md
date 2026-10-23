Curated protein complexes are the most accurate knowledge prior for filling in missing single-cell proteomics data (#1 of 22 sources), but on their own they never beat plain kNN. What does work is an *empirical* biological prior: protein co-regulation learned from 16 public single-cell datasets plus two bulk proteomics atlases. Exposed to AI agents as MCP tools and preregistered end to end, it cut imputation error by **2.4–5.4% vs. the best data-only method** on an untouched holdout (6/6 tests). Curated complexes added nothing on top of it.

## Approach

**Problem.** Mass-spectrometry single-cell proteomics (SCP) quantifies only 20–60% of each cell's proteins, so every downstream analysis depends on imputation ([Vanderaa & Gatto 2023](https://doi.org/10.1021/acs.jproteome.3c00227)). Proteins are physical machines: subunits of a complex are assembled in fixed stoichiometry and should co-vary. We asked whether biological prior knowledge reconstructs missing values better than data-only methods.

**What we built.**
- **`scp-graphfs-mcp`**, an MCP server that gives any LLM agent tools to:
  - fetch curated complexes (CORUM, Complex Portal);
  - build provenance-tracked knowledge graphs with degree-preserving nulls;
  - propagate scores;
  - impute with a prior;
  - select measurement panels;
  - map a variant (e.g. `PSMB5:c.100A>G`) to the protein machines it hits and the partner subunits measured in a dataset.

  Real agent transcripts are included for Claude Code and GitHub Copilot CLI.
- **A preregistered benchmark (14 amendments).**
  - **Design:** development on three datasets ([Petrosius 2023](https://doi.org/10.14428/DVN/4DSPJM), Leduc 2022, SCoPE2/Specht 2021), with MCAR and MNAR masking at 30 and 200 cells and dev seeds only.
  - **Holdout rule:** every claim is confirmed **once** on an untouched dataset, with a 1% minimum effect size and paired-bootstrap CIs.
  - **Nulls:** every prior is tested against the same prior with protein labels scrambled.
- **22 protein representations:**
  - curated complexes (Complex Portal, CORUM, hu.MAP 3.0) and PDB co-structure (SIFTS);
  - networks (STRING, BioGRID, IntAct, Pathway Commons), Reactome, Monarch phenotypes, NCBI co-citation;
  - GO, HPA, UniProt, Pharos, ProtT5 sequence embeddings;
  - CCLE and ProteomeHD bulk proteomics.
- **A reference corpus:** 17 public SCP datasets (~10k cells) rebuilt from scpdata without R, every file SHA-256-checked.

**Estimators** (each borrowed from another field):
- **Reference-panel regression** (from genotype imputation). For protein $j$ with knowledge-neighbours $N_j$ and weights $w_{jk}$:
  $$s_{ij}=\frac{\sum_{k\in N_j} w_{jk}\, z_{ik}}{\sum_k |w_{jk}|},\qquad \hat z_{ij}=b_j\, s_{ij},\qquad b_j=\frac{\sum_{i\,\text{obs}} z_{ij}s_{ij}}{\sum_{i\,\text{obs}} s_{ij}^2+\lambda}$$
- **Reference projection** (from ancestry PCA and recommender cold-start).
  - Learn protein loadings $V$ on the external reference $Z_{\text{ref}}\approx UV^\top$ by masked ALS.
  - Each of the 30 target cells fits only its own scores, $u_i=(V_{o}^\top V_{o}+\lambda I)^{-1}V_{o}^\top z_{i,o}$, and predicts $\hat z_{i,m}=V_m u_i$.
  - Curated complexes can enter as a graph penalty on $V$ or as a cold-start for proteins the reference never saw.
- **Stacking.** The final imputer is $w_1\,\text{kNN}+w_2\,\text{low-rank}+w_3\,\text{projection}$, with weights chosen on an inner mask of *observed* entries only.

## Results

![Figure 1: knowledge-prior ranking](fig1_prior_ranking.png)

**1. Curated physical complexes are the best knowledge prior, but no prior alone beats kNN** (Fig. 1).
- Complex Portal, PDB co-structure and CORUM rank #1–3 of 22, and almost every source beats its own scrambled null.
- Broader knowledge (PPI networks, pathways, GO, sequence embeddings, drug-target annotations) helps less. Bulk co-regulation panels help least when used directly.
- **Gate:** 0/66 representation × estimator pairs passed the dev gate (≥ 1% better than kNN, low-rank and their stack, on ≥ 2/3 datasets under both masks).

**2. Transferring protein co-regulation from public data works.**
- **Dev (Petrosius):** projecting the 30 target cells onto loadings learned from the external reference cut error by 14% vs. kNN.
- **Holdout:** we preregistered H14 ([`PREREGISTRATION_v7.md`](https://github.com/xX-its-amit-Xx/knowledgeispower/blob/main/benchmarks/PREREGISTRATION_v7.md)) and tested it **once** on Brunner 2022 (434 HeLa cells, timsTOF DIA, a technology never used in development).

![Figure 2: holdout confirmation](fig2_holdout.png)

| In-complex RMSE, our stack vs. | MCAR | MNAR |
|---|---|---|
| kNN | **−6.0%** | **−8.9%** |
| kNN + low-rank (best data-only) | **−2.4%** | **−5.4%** |
| same pipeline, scrambled reference | **−2.5%** | **−4.3%** |

All six 95% paired-bootstrap CIs are below 0, and overall RMSE also improves on all six comparisons. Because the scrambled-reference control loses, the gain comes from the biology, not from extra model capacity.

**3. Curated complexes are correct but redundant once data is available.**
- Adding complex priors on top of transfer changed in-complex RMSE by only −0.06% to −0.54%, with CIs including 0.
- The stack gave the complex-regression component weight in only 1 of 36 dev subsamples.

**Honest limits:**
- On an earlier holdout (Khan 2023, MCF-10A EMT), a closely related stack beat kNN by 1.0–1.4% but the kNN + low-rank stack by only 0.2–0.6%. That is below our 1% bar, so the transfer effect replicates on **1 of 2** holdouts.
- H14 was refined after dev results. This is disclosed in its preregistration.

**Prior art, checked live with [Valency MCP Bond](https://www.valency.io/bond/).** Before submitting, a Bond literature sweep (PubMed, bioRxiv, arXiv) surfaced the closest work, and we narrowed our claims to match:
- [Lupine](https://doi.org/10.1016/j.mcpro.2025.101461) already learns imputation from many *bulk* datasets;
- [GIRAFI](https://doi.org/10.64898/2026.05.18.726081) already uses knowledge-informed protein neighbourhoods for SCP;
- see also [Sonnett et al. 2025](https://doi.org/10.1101/2025.10.27.684979) and [omicsGMF](https://doi.org/10.1038/s41467-026-73402-8).

Our contribution is the preregistered, null-controlled head-to-head of curated vs. empirical priors for 30-cell SCP targets, confirmed on an untouched holdout. The full trace is in [`docs/valency_bond_prior_art.md`](https://github.com/xX-its-amit-Xx/knowledgeispower/blob/main/docs/valency_bond_prior_art.md).

## Next steps

- **A third holdout to settle replication:** rebuild Derks 2022 from its unimputed precursors.
- **Head-to-head comparisons** with GIRAFI, Lupine and omicsGMF on our holdouts.
- **Peptide-level priors**, where complex stoichiometry constrains ratios directly.
- **Agent workflows** that chain variant → complex → measured partners → literature evidence (MCP Bond) into a single report.

**Team:** Amit Shenoy (lead); Eeshan Khan (variant bridge); Abdullah Javed (Copilot CLI recipe); Fatima Zahra and @aggravating08 (glossary, test hardening, which found and fixed a core bug); @imperorrp (NIFty panel baseline).

**Code (Apache-2.0):** [github.com/xX-its-amit-Xx/knowledgeispower](https://github.com/xX-its-amit-Xx/knowledgeispower). Built with Claude Code agents, the MCP Python SDK and Valency MCP Bond.
