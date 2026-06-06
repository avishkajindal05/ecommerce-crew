import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from server.mcp_server import (
    get_open_complaints,
    get_document_list,
    search_documents,
    read_record,
    investigate_open_complaints,
    save_report,
)


def test_get_open_complaints():
    result = get_open_complaints()
    assert isinstance(result, list)
    assert len(result) > 0
    assert all(r["status"] == "Open" for r in result)


def test_get_document_list():
    docs = get_document_list()
    assert isinstance(docs, list)
    assert len(docs) > 0


def test_search_documents():
    result = search_documents("defect")
    assert isinstance(result, list)
    assert len(result) > 0


def test_read_record_document():
    result = read_record("returns_policy.txt")
    assert result["type"] == "document"
    assert "content" in result


def test_read_record_complaint():
    result = read_record("2001")
    assert result["type"] == "complaint"
    assert "data" in result


def test_investigate_open_complaints():
    result = investigate_open_complaints()
    assert "complaints" in result
    assert "evidence" in result
    assert len(result["complaints"]) > 0


def test_save_report(tmp_path, monkeypatch):
    import server.mcp_server as srv
    monkeypatch.setattr(srv, "REPORT_DIR", tmp_path)
    result = save_report("Test Report", "# Test\nSome content.")
    assert result["status"] == "saved"
