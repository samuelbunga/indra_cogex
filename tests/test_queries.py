import pytest
from indra_cogex.client.queries import *
from indra.statements import *
from indra_cogex.representation import Node

from .test_neo4j_client import _get_client


@pytest.mark.nonpublic
def test_get_genes_in_tissue():
    # Single query
    client = _get_client()
    genes = get_genes_in_tissue(client, ("UBERON", "UBERON:0002349"))
    assert genes
    node0 = genes[0]
    assert isinstance(node0, Node)
    assert node0.db_ns == "HGNC"
    assert ("HGNC", "9891") in {g.grounding() for g in genes}


@pytest.mark.nonpublic
def test_get_tissues_for_gene():
    # Single query
    client = _get_client()
    tissues = get_tissues_for_gene(client, ("HGNC", "9896"))
    assert tissues
    node0 = tissues[0]
    assert isinstance(node0, Node)
    assert node0.db_ns in {"UBERON", "CL"}
    assert ("UBERON", "UBERON:0002349") in {g.grounding() for g in tissues}


@pytest.mark.nonpublic
def test_is_gene_in_tissue():
    client = _get_client()
    gene = ("HGNC", "9896")  # RBM10
    tissue = ("UBERON", "UBERON:0035841")  # esophagogastric junction muscularis propria
    assert is_gene_in_tissue(client, gene, tissue)


@pytest.mark.nonpublic
def test_get_go_terms_for_gene():
    client = _get_client()
    gene = ("HGNC", "2697")  # DBP
    go_terms = get_go_terms_for_gene(client, gene)
    assert go_terms
    node0 = go_terms[0]
    assert isinstance(node0, Node)
    assert node0.db_ns == "GO"
    assert ("GO", "GO:0000978") in {g.grounding() for g in go_terms}


@pytest.mark.nonpublic
def test_get_genes_for_go_term():
    # Single query
    client = _get_client()
    go_term = ("GO", "GO:0000978")
    genes = get_genes_for_go_term(client, go_term)
    assert genes
    node0 = genes[0]
    assert isinstance(node0, Node)
    assert node0.db_ns == "HGNC"
    assert ("HGNC", "2697") in {g.grounding() for g in genes}


@pytest.mark.nonpublic
def test_is_go_term_for_gene():
    # Single query
    client = _get_client()
    go_term = ("GO", "GO:0000978")
    gene = ("HGNC", "2697")  # DBP
    assert is_go_term_for_gene(client, gene, go_term)


@pytest.mark.nonpublic
def test_get_trials_for_drug():
    client = _get_client()
    drug = ("CHEBI", "CHEBI:27690")
    trials = get_trials_for_drug(client, drug)
    assert trials
    assert isinstance(trials[0], Node)
    assert trials[0].db_ns == "CLINICALTRIALS"
    assert ("CLINICALTRIALS", "NCT02703220") in {t.grounding() for t in trials}


@pytest.mark.nonpublic
def test_get_trials_for_disease():
    client = _get_client()
    disease = ("MESH", "D007855")
    trials = get_trials_for_disease(client, disease)
    assert trials
    assert isinstance(trials[0], Node)
    assert trials[0].db_ns == "CLINICALTRIALS"
    assert ("CLINICALTRIALS", "NCT00011661") in {t.grounding() for t in trials}


@pytest.mark.nonpublic
def test_get_drugs_for_trial():
    client = _get_client()
    trial = ("CLINICALTRIALS", "NCT00000114")
    drugs = get_drugs_for_trial(client, trial)
    assert drugs
    assert drugs[0].db_ns in ["CHEBI", "MESH"]
    assert ("MESH", "D014810") in {d.grounding() for d in drugs}


@pytest.mark.nonpublic
def test_get_diseases_for_trial():
    client = _get_client()
    trial = ("CLINICALTRIALS", "NCT00000114")
    diseases = get_diseases_for_trial(client, trial)
    assert diseases
    assert isinstance(diseases[0], Node)
    assert diseases[0].db_ns == "MESH"
    assert ("MESH", "D012174") in {d.grounding() for d in diseases}


@pytest.mark.nonpublic
def test_get_pathways_for_gene():
    client = _get_client()
    gene = ("HGNC", "16812")
    pathways = get_pathways_for_gene(client, gene)
    assert pathways
    assert isinstance(pathways[0], Node)
    assert pathways[0].db_ns in {"WIKIPATHWAYS", "REACTOME"}
    assert ("WIKIPATHWAYS", "WP5037") in {p.grounding() for p in pathways}


@pytest.mark.nonpublic
def test_get_genes_for_pathway():
    client = _get_client()
    pathway = ("WIKIPATHWAYS", "WP5037")
    genes = get_genes_for_pathway(client, pathway)
    assert genes
    assert isinstance(genes[0], Node)
    assert genes[0].db_ns == "HGNC"
    assert ("HGNC", "16812") in {g.grounding() for g in genes}


@pytest.mark.nonpublic
def test_is_gene_in_pathway():
    client = _get_client()
    gene = ("HGNC", "16812")
    pathway = ("WIKIPATHWAYS", "WP5037")
    assert is_gene_in_pathway(client, gene, pathway)


@pytest.mark.nonpublic
def test_get_side_effects_for_drug():
    client = _get_client()
    drug = ("CHEBI", "CHEBI:29108")
    side_effects = get_side_effects_for_drug(client, drug)
    assert side_effects
    assert isinstance(side_effects[0], Node)
    assert side_effects[0].db_ns in ["GO", "UMLS", "MESH", "HP"]
    assert ("UMLS", "C3267206") in {s.grounding() for s in side_effects}


@pytest.mark.nonpublic
def test_get_drugs_for_side_effect():
    client = _get_client()
    side_effect = ("UMLS", "C3267206")
    drugs = get_drugs_for_side_effect(client, side_effect)
    assert drugs
    assert isinstance(drugs[0], Node)
    assert drugs[0].db_ns in ["CHEBI", "MESH"]
    assert ("CHEBI", "CHEBI:29108") in {d.grounding() for d in drugs}


@pytest.mark.nonpublic
def test_is_side_effect_for_drug():
    client = _get_client()
    drug = ("CHEBI", "CHEBI:29108")
    side_effect = ("UMLS", "C3267206")
    assert is_side_effect_for_drug(client, drug, side_effect)


@pytest.mark.nonpublic
def test_get_ontology_child_terms():
    client = _get_client()
    term = ("MESH", "D007855")
    children = get_ontology_child_terms(client, term)
    assert children
    assert isinstance(children[0], Node)
    assert children[0].db_ns == "MESH"
    assert ("MESH", "D020264") in {c.grounding() for c in children}


@pytest.mark.nonpublic
def test_get_ontology_parent_terms():
    client = _get_client()
    term = ("MESH", "D020263")
    parents = get_ontology_parent_terms(client, term)
    assert parents
    assert isinstance(parents[0], Node)
    assert parents[0].db_ns == "MESH"
    assert ("MESH", "D007855") in {p.grounding() for p in parents}


@pytest.mark.nonpublic
def test_isa_or_partof():
    client = _get_client()
    term = ("MESH", "D020263")
    parent = ("MESH", "D007855")
    assert isa_or_partof(client, term, parent)


@pytest.mark.nonpublic
def test_get_pmids_for_mesh():
    # Single query
    client = _get_client()
    pmids = get_pmids_for_mesh(client, ("MESH", "D015002"))
    assert pmids
    assert isinstance(pmids[0], Node)
    assert pmids[0].db_ns == "PUBMED"
    assert ("PUBMED", "14915949") in {p.grounding() for p in pmids}


@pytest.mark.nonpublic
def test_get_mesh_ids_for_pmid():
    # Single query
    client = _get_client()
    pmid = ("PUBMED", "27890007")
    mesh_ids = get_mesh_ids_for_pmid(client, pmid)
    assert mesh_ids
    assert isinstance(mesh_ids[0], Node)
    assert mesh_ids[0].db_ns == "MESH"
    assert ("MESH", "D000544") in {m.grounding() for m in mesh_ids}


@pytest.mark.nonpublic
def test_get_evidence_obj_for_mesh_id():
    client = _get_client()
    mesh_id = ("MESH", "D015002")
    evidence_dict = get_evidences_for_mesh(client, mesh_id)
    assert len(evidence_dict)
    assert isinstance(list(evidence_dict.values())[0][0], Evidence)


@pytest.mark.nonpublic
def test_get_evidence_obj_for_stmt_hash():
    # Note: This statement has 3 evidences
    # Single query
    stmt_hash = "12198579805553967"
    client = _get_client()
    ev_objs = get_evidences_for_stmt_hash(client, stmt_hash)
    assert ev_objs
    assert isinstance(ev_objs[0], Evidence)


@pytest.mark.nonpublic
def test_get_evidence_obj_for_stmt_hashes():
    # Note: These statements have 3+5 evidences
    # Single query
    stmt_hashes = ["12198579805553967", "30651649296901235"]
    client = _get_client()
    ev_dict = get_evidences_for_stmt_hashes(client, stmt_hashes)
    assert ev_dict
    assert set(ev_dict.keys()) == {"12198579805553967", "30651649296901235"}
    assert ev_dict["12198579805553967"]
    assert ev_dict["30651649296901235"]
    assert isinstance(ev_dict["12198579805553967"][0], Evidence)
    assert isinstance(ev_dict["30651649296901235"][0], Evidence)


@pytest.mark.nonpublic
def test_get_stmts_for_pmid():
    # Two queries: first evidences, then the statements
    client = _get_client()
    pmid = ("PUBMED", "14898026")
    stmts = get_stmts_for_pmid(client, pmid)
    assert stmts
    assert isinstance(stmts[0], Inhibition)


@pytest.mark.nonpublic
def test_get_stmts_for_mesh_id_w_children():
    # Two queries:
    # 1. evidences for publications with pmid having mesh annotation
    # 2. statements for the evidences in 2
    client = _get_client()
    mesh_id = ("MESH", "D000068236")
    stmts = get_stmts_for_mesh(client, mesh_id)
    assert stmts
    assert isinstance(stmts[0], Activation)


@pytest.mark.nonpublic
def test_get_stmts_for_mesh_id_wo_children():
    # Two queries:
    # 1. evidences for publications with pmid having mesh annotation
    # 2. statements for the evidences in 2
    client = _get_client()
    mesh_id = ("MESH", "D000068236")
    stmts = get_stmts_for_mesh(client, mesh_id, include_child_terms=False)
    assert stmts
    assert isinstance(stmts[0], Activation)


@pytest.mark.nonpublic
def test_get_stmts_by_hashes():
    # Note: This statement has a ~500 of evidences
    # Two queries: first statements, then all the evidence for the statements
    stmt_hashes = ["35279776755000170"]
    client = _get_client()
    stmts = get_stmts_for_stmt_hashes(client, stmt_hashes)
    assert stmts
    assert isinstance(stmts[0], Inhibition)
