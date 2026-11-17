def test_health_ok(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_home_page(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"Student Management System" in res.data
