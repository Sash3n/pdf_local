from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_dashboard_links_into_real_tools():
    response = client.get("/")
    assert response.status_code == 200
    assert "Merge Files" in response.text
    assert "/tools/merge" in response.text
    assert "ship in the next phase" not in response.text


def test_tools_index_lists_categories_and_tools():
    response = client.get("/tools")
    assert response.status_code == 200
    assert "Organize" in response.text
    assert "Merge PDF" in response.text
    assert "/tools/compress" in response.text
    assert "/security/sign" in response.text


def test_tool_workspace_page_renders_merge():
    response = client.get("/tools/merge")
    assert response.status_code == 200
    assert "Merge PDF" in response.text
    assert "Merge Files" in response.text


def test_tool_workspace_page_renders_extra_fields():
    response = client.get("/tools/compress")
    assert response.status_code == 200
    assert 'name="quality"' in response.text
    assert 'type="range"' in response.text


def test_tool_workspace_page_404_for_unknown_slug():
    response = client.get("/tools/not-a-real-tool")
    assert response.status_code == 404


def test_sign_page_renders():
    response = client.get("/security/sign")
    assert response.status_code == 200
    assert "Sign PDF" in response.text
    assert "sign-canvas" in response.text


def test_privacy_page_renders():
    response = client.get("/privacy")
    assert response.status_code == 200
    assert "Privacy" in response.text
    assert "pikepdf" in response.text
    assert "Local User" in response.text
