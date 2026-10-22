"""S7 regression checks: sparse evidence, graph boundaries, and Unicode inputs."""
import importlib.util
import json
from pathlib import Path

import anndata as ad
import networkx as nx
import numpy as np
import pytest

from scp_graphfs_mcp import methods, tools
from scp_graphfs_mcp.complexes import load_complexes
from scp_graphfs_mcp.datasets import from_log2_matrix
from scp_graphfs_mcp.ids import group_accessions
from scp_graphfs_mcp.priors import build_complex_graph, shuffled_null


@pytest.fixture
def sparse_data():
    # Synthetic intensities; final feature deliberately has no observations.
    values = np.array([[2., 3., np.nan], [4., np.nan, np.nan],
                       [6., 7., np.nan], [8., 9., np.nan], [10., 11., np.nan]])
    return from_log2_matrix(values, [f"cell{i}" for i in range(5)],
                            ["feature_a", "feature_b", "unobserved"])


@pytest.mark.parametrize("mode", ["none", "soft_weight"])
def test_panel_larger_than_candidates_never_selects_all_nan(sparse_data, mode):
    graph = nx.empty_graph(list(sparse_data.var_names))
    expected = set(sparse_data.var_names[(~np.isnan(sparse_data.X)).mean(0) >= .8])
    panel = methods.select_features(sparse_data, graph, k=10, mode=mode)
    assert set(panel) == expected
    assert len(panel) == len(expected)
    assert panel == methods.select_features(sparse_data, graph, k=10, mode=mode)


def test_random_panel_caps_at_candidates_and_is_seeded(sparse_data):
    expected = set(sparse_data.var_names[(~np.isnan(sparse_data.X)).mean(0) >= .8])
    panel = methods.select_random(sparse_data, 10, seed=42)
    assert set(panel) == expected and len(panel) == len(expected)
    assert panel == methods.select_random(sparse_data, 10, seed=42)


def test_edgeless_imputation_uses_fallback_without_mutating_input(sparse_data):
    original = sparse_data.X.copy()
    raw = sparse_data.layers["raw"].copy()
    # Explicit fallback isolates routing from the external kNN implementation.
    fallback = np.full(original.shape, 17.)
    missing = np.isnan(original)
    result = methods.impute_with_prior(sparse_data, nx.Graph(), fallback=fallback)
    np.testing.assert_array_equal(result.X, np.where(missing, fallback, original))
    np.testing.assert_array_equal(sparse_data.X, original)
    np.testing.assert_array_equal(result.layers["raw"], raw)
    np.testing.assert_array_equal(result.layers["was_imputed"], missing)
    assert not result.layers["imputed_by_prior"].any()
    assert result.uns["impute_with_prior"]["n_imputed_by_knn_fallback"] == missing.sum()


@pytest.mark.parametrize("scores", [{"a": 2., "b": 1.}, {}])
def test_edgeless_propagation_retains_normalized_seed_mass(scores):
    names = ["a", "b", "c"]
    actual = methods.propagate(nx.Graph(), scores, names)
    seed = np.array([scores.get(n, 0.) for n in names])
    expected = seed / seed.sum() if seed.sum() else np.ones(len(names)) / len(names)
    np.testing.assert_allclose(actual, expected)


@pytest.mark.parametrize("source", ["corum", "complexportal"])
def test_empty_prior_and_null_have_consistent_coverage(source):
    graph = build_complex_graph([], source)
    null = shuffled_null(graph, seed=42)
    assert len(graph) == len(null) == 0
    assert graph.number_of_edges() == null.number_of_edges() == 0
    assert graph.graph["coverage"]["unmapped_fraction"] == 0
    assert null.graph["provenance"]["n_swaps"] == 0
    assert graph.graph["provenance"].get("null_seed") is None


@pytest.mark.parametrize("source", ["corum", "complexportal"])
def test_isoform_group_membership_counts_each_complex_once(source):
    complexes = load_complexes((source,))
    members = next(sorted(m) for m in complexes["members"] if len(m) >= 2)
    a, b = members[:2]
    # Suffixes are parser fixtures, not assertions that these isoforms exist.
    group = f"{a}-2;{a};{a}-PRO_000001"
    partner = f"{b}-3"
    assert group_accessions(group) == [a]
    graph = build_complex_graph([group, partner], source)
    expected = sum(a in m and b in m for m in complexes["members"])
    assert graph.edges[group, partner]["weight"] == expected
    assert nx.number_of_selfloops(graph) == 0
    assert graph.graph["coverage"]["n_unmapped"] == 0


@pytest.mark.parametrize("tool_name, kwargs, code", [
    ("get_complexes", {"id": "蛋白質🧬"}, "unresolved_identifier"),
    ("explain_protein", {"id": "蛋白質🧬"}, "unresolved_identifier"),
    ("build_prior", {"proteins": ["蛋白質🧬"], "sources": ["未知"]}, "invalid_input"),
    ("propagate_scores", {"handle": "未知🧬", "scores": {"蛋白質": 1.}}, "unknown_handle"),
    ("impute_with_prior", {}, "invalid_input"),
    ("select_panel", {}, "invalid_input"),
])
def test_each_core_tool_returns_json_error_for_unresolvable_unicode(tool_name, kwargs, code, tmp_path):
    kwargs = dict(kwargs)
    if tool_name in {"impute_with_prior", "select_panel"}:
        kwargs["h5ad_path"] = str(tmp_path / "不存在🧬.h5ad")
    response = getattr(tools, tool_name)(**kwargs)
    assert response["error"]["code"] == code
    assert response["error"]["message"]
    assert json.loads(json.dumps(response, ensure_ascii=False)) == response


def test_unicode_unmapped_protein_preserved_in_prior_and_propagation(monkeypatch):
    monkeypatch.setattr(tools, "_HANDLES", {})
    protein = "蛋白質🧬"
    result = tools.build_prior([protein], sources=["complexportal"])["priors"]["complexportal"]
    assert result["unmapped"] == [protein]
    assert result["n_proteins"] == 1 and result["n_edges"] == 0
    ranking = tools.propagate_scores(result["handle"], {protein: 1.})["top"]
    assert ranking[0]["protein"] == protein
    assert ranking[0]["propagated"] == pytest.approx(1.)


def test_unicode_h5ad_path_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(tools, "_HANDLES", {})
    members = next(sorted(m) for m in load_complexes(("complexportal",))["members"] if len(m) >= 2)
    names = members[:2]
    values = np.array([[2., 3.], [4., 5.], [6., 7.], [8., 9.], [10., np.nan]])
    data = from_log2_matrix(values, [f"cell{i}" for i in range(5)], names)
    path, output = tmp_path / "細胞🧬.h5ad", tmp_path / "推定🧬.h5ad"
    data.write_h5ad(path)
    report = tools.impute_with_prior(str(path), output_path=str(output))
    assert report["output_path"] == str(output)
    actual = ad.read_h5ad(output)
    np.testing.assert_array_equal(actual.X[~np.isnan(values)], values[~np.isnan(values)])
    assert np.isfinite(actual.X).all()
    panel = tools.select_panel(str(path), k=len(names), mode="none")
    assert {row["protein"] for row in panel["panel"]} == set(names)
    np.testing.assert_array_equal(ad.read_h5ad(path).X, values)


@pytest.mark.xfail(
    reason="Exposes core bug in methods.propagate(): ZeroDivisionError on 0-node graph when scores are empty. Flagged for Amit's core fix.",
    strict=True,
)
def test_zero_node_propagation_is_empty():
    result = methods.propagate(nx.Graph(), {})
    assert result.shape == (0,)


def test_default_knn_with_all_nan_column_retains_feature_shape(sparse_data):
    result = methods.impute_with_prior(sparse_data, nx.Graph())
    assert result.shape == sparse_data.shape
    assert np.isnan(result.X[:, -1]).all()  # no evidence must not become zero
    assert np.isfinite(result.X[:, :-1]).all()
    np.testing.assert_array_equal(result.X[~np.isnan(sparse_data.X)],
                                  sparse_data.X[~np.isnan(sparse_data.X)])


@pytest.fixture(scope="module")
def boot_rmse_diff():
    # benchmarks is not an installed package; load its helper without running main.
    path = Path(__file__).resolve().parents[2] / "benchmarks" / "run.py"
    spec = importlib.util.spec_from_file_location("s7_benchmark_run", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.boot_rmse_diff


@pytest.mark.parametrize("squared_errors", [np.array([4.]), np.array([0., 1., 9.])])
def test_paired_bootstrap_identical_predictions_have_zero_difference(squared_errors, boot_rmse_diff):

    report = boot_rmse_diff(squared_errors, [squared_errors.copy()], n_boot=32, seed=42)
    assert report["n_entries"] == len(squared_errors)
    assert report["delta_rmse"] == 0.
    assert report["ci95"] == [0., 0.]
    assert report["effect_size_dz_sqerr"] == 0.


def test_single_entry_bootstrap_matches_direct_rmse_difference(boot_rmse_diff):

    a, b = np.array([4.]), np.array([9.])
    expected = float(np.sqrt(a.mean()) - np.sqrt(b.mean()))
    report = boot_rmse_diff(a, [b], n_boot=32, seed=42)
    assert report["delta_rmse"] == expected
    assert report["ci95"] == [expected, expected]
    assert np.isfinite(report["effect_size_dz_sqerr"])


@pytest.mark.parametrize("n_cells", [5, 10, 29])
def test_data_graph_small_samples_keep_supported_positive_edge(n_cells):
    from scp_graphfs_mcp.phase2 import data_graph

    abundance = np.arange(n_cells, dtype=float)
    values = np.column_stack([abundance, 2 * abundance, -abundance])
    names = ["synthetic_a", "synthetic_b", "synthetic_c"]
    graph = data_graph(values, names, n_edges=1)
    assert set(graph.nodes) == set(names)
    assert {frozenset(edge) for edge in graph.edges} == {frozenset(names[:2])}
