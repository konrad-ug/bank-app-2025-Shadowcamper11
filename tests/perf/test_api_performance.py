import time
import pytest
from app.api import app, registry


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        registry.accounts.clear()
        yield client


def make_pesel(i: int) -> str:
    return f"{i:011d}"


def _post(client, url, json_payload):
    start = time.perf_counter()
    resp = client.post(url, json=json_payload)
    duration = time.perf_counter() - start
    data = None
    try:
        data = resp.get_json()
    except Exception:
        data = None
    return resp.status_code, data, duration


def _delete(client, url):
    start = time.perf_counter()
    resp = client.delete(url)
    duration = time.perf_counter() - start
    return resp.status_code, duration


def _get(client, url):
    start = time.perf_counter()
    resp = client.get(url)
    duration = time.perf_counter() - start
    return resp.status_code, resp.get_json(), duration


def test_create_and_delete_account_100_times(client):
    for i in range(1, 101):
        pesel = make_pesel(i)
        payload = {"name": "Perf", "surname": "User", "pesel": pesel}

        status, _, duration = _post(client, "/api/accounts", payload)

        assert status in (201, 409)
        assert duration < 0.5, f"Create request too slow: {duration}s (i={i})"

        if status == 201:
            d_status, d_dur = _delete(client, f"/api/accounts/{pesel}")
            assert d_status == 200
            assert d_dur < 0.5, f"Delete request too slow: {d_dur}s (i={i})"


def test_create_account_and_100_incoming_transfers(client):
    pesel = make_pesel(99999)
    payload = {"name": "Perf", "surname": "Payer", "pesel": pesel}

    status, _, _ = _post(client, "/api/accounts", payload)
    assert status in (201, 409)

    for j in range(1, 101):
        transfer = {"amount": 1, "type": "incoming"}
        t_status, _, duration = _post(client, f"/api/accounts/{pesel}/transfer", transfer)
        assert t_status == 200
        assert duration < 0.5, f"Transfer request too slow: {duration}s (j={j})"

    g_status, data, _ = _get(client, f"/api/accounts/{pesel}")
    assert g_status == 200
    assert data.get('balance', None) == 100
