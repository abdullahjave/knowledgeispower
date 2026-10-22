# Prior-art check with Valency MCP Bond (Oct 22, 2026)

We used **Valency's MCP Bond** (`https://mcp.valency.io/`), connected as an MCP server in Claude Code, to check our
confirmed result (H14: transfer of protein co-regulation from public data improves single-cell proteomics imputation)
against the literature *before* submitting. Every DOI below was then checked on Crossref.

## Tool calls (verbatim queries)
1. `semantic_search_papers`: "imputation of missing values in single-cell proteomics using external reference datasets
   or transfer learning"
2. `semantic_search_papers`: "protein complex membership as prior knowledge to impute missing protein abundances in mass
   spectrometry proteomics"
3. `semantic_search_papers`: "benchmark of imputation methods for single-cell proteomics data kNN low-rank matrix completion"
4. `semantic_search_papers`: "protein co-regulation across proteomics experiments predicts protein abundance; reference
   panel style imputation analogous to genotype imputation"
5. `search_by_title` × 3, to read the abstracts of the closest hits.
6. `export_papers_bibtex` for 7 papers (below).

The searches covered PubMed, bioRxiv/medRxiv and arXiv in one call each.

## What it changed in our claims
| Paper | Overlap | Effect on our write-up |
|---|---|---|
| **Lupine**, Harris & Noble, *MCP* 2025 ([doi](https://doi.org/10.1016/j.mcpro.2025.101461)) | "First imputation method designed to learn jointly from many datasets" (bulk TMT, CPTAC) | We **no longer claim** that learning from many datasets is new. Our claim is narrowed to single-cell targets of 30 cells, curated vs empirical priors with nulls, and preregistered holdout confirmation |
| **GIRAFI**, Zhong et al., bioRxiv 2026 ([doi](https://doi.org/10.64898/2026.05.18.726081)) | Prior-knowledge-informed protein neighbourhoods for SCP imputation (our original thesis) | Cited as the closest prior work. Our results temper the "knowledge neighbourhoods help" story: they beat scrambled ones but add nothing over strong data-only + transfer baselines. No head-to-head yet |
| **Sonnett, Peshkin & Kirschner**, bioRxiv 2025 ([doi](https://doi.org/10.1101/2025.10.27.684979)) | Regularized regression on biological covariation for proteomics imputation | Cited. They show it in bulk; we find within-target covariation does *not* beat kNN at 30 single cells, while borrowed covariation does |
| **omicsGMF**, Segers et al., *Nat Commun* 2026 ([doi](https://doi.org/10.1038/s41467-026-73402-8)) | Matrix factorization imputation for bulk and SCP | A stronger low-rank baseline we have not yet benchmarked |
| Vanderaa & Gatto, *JPR* 2023; SoftHybrid (Shi et al., *JPR* 2026); Srivastava et al., *PLoS CB* 2022 | SCP missing-value practice; SCP imputation; protein abundance predicted from interacting partners | Context and citations |

All of these were added to `docs/prior-art.json` (class "Direct overlap" or "Adjacent", verified via Bond + Crossref).

## BibTeX (exported by Bond)
```bibtex
@article{harris2025proteomics, title={Proteomics Data Imputation With a Deep Model That Learns From Many Datasets}, author={Harris, Lincoln and Noble, William S}, year={2025}, journal={Molecular \& Cellular Proteomics 24(12):101461}, doi={10.1016/j.mcpro.2025.101461}}
@article{sonnett2025using, title={Using regularized regression and biological covariation to impute missing values in quantitative proteomics}, author={Sonnett, M. and Peshkin, L. and Kirschner, M. W.}, year={2025}, journal={bioRxiv}, doi={10.1101/2025.10.27.684979}}
@article{zhong2026recovering, title={Recovering biological structure in sparse single-cell proteomics with GIRAFI}, author={Zhong, H. and Chi, S. and Wong, R. and Rogalski, J. and Wang, Z. and others}, year={2026}, journal={bioRxiv}, doi={10.64898/2026.05.18.726081}}
@article{segers2026omicsgmf, title={omicsGMF: a multi-tool for dimensionality reduction, batch correction and imputation in bulk- and single-cell proteomics}, author={Segers, Alexandre and Castiglione, Cristian and Vanderaa, Christophe and Martens, Lennart and Risso, Davide and Clement, Lieven}, year={2026}, journal={Nature Communications 17}, doi={10.1038/s41467-026-73402-8}}
@article{vanderaa2023revisiting, title={Revisiting the Thorny Issue of Missing Values in Single-Cell Proteomics}, author={Vanderaa, Christophe and Gatto, Laurent}, year={2023}, journal={Journal of Proteome Research 22(9):2775-2784}, doi={10.1021/acs.jproteome.3c00227}}
@article{shi2026softhybrid, title={SoftHybrid: A Hybrid Imputation Algorithm Optimized for Single-Cell Proteomics Data}, author={Shi, Yixin and Davis, Simon and Charles, Philip D and others}, year={2026}, journal={Journal of Proteome Research 25(8):3893-3908}, doi={10.1021/acs.jproteome.5c01221}}
@article{srivastava2022protein, title={Protein prediction models support widespread post-transcriptional regulation of protein abundance by interacting partners}, author={Srivastava, Himangi and Lippincott, Michael J and Currie, Jordan and Canfield, Robert and Lam, Maggie P Y and Lau, Edward}, year={2022}, journal={PLoS Computational Biology 18(11):e1010702}, doi={10.1371/journal.pcbi.1010702}}
```
