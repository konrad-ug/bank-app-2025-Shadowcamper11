import time
import os
import requests

BASE_URL = os.getenv('BANK_APP_BASE_URL', 'http://127.0.0.1:5000')


def make_pesel(i: int) -> str:
    return f"{i:011d}"


def test_create_and_delete_account_100_times():
    for i in range(1, 101):
        pesel = make_pesel(i)
        payload = {"name": "Perf", "surname": "User", "pesel": pesel}

        start = time.perf_counter()
        resp = requests.post(f"{BASE_URL}/api/accounts", json=payload, timeout=1)
        duration = time.perf_counter() - start

        assert resp.status_code in (201, 409)
        assert duration < 0.5, f"Create request too slow: {duration}s (i={i})"

        if resp.status_code == 201:
            start = time.perf_counter()
            dresp = requests.delete(f"{BASE_URL}/api/accounts/{pesel}", timeout=1)
            d_dur = time.perf_counter() - start
            assert dresp.status_code == 200
            assert d_dur < 0.5, f"Delete request too slow: {d_dur}s (i={i})"


def test_create_account_and_100_incoming_transfers():
    pesel = make_pesel(99999)
    payload = {"name": "Perf", "surname": "Payer", "pesel": pesel}

    resp = requests.post(f"{BASE_URL}/api/accounts", json=payload, timeout=1)
    assert resp.status_code in (201, 409)

    for j in range(1, 101):
        transfer = {"amount": 1, "type": "incoming"}
        start = time.perf_counter()
        tresp = requests.post(f"{BASE_URL}/api/accounts/{pesel}/transfer", json=transfer, timeout=1)
        duration = time.perf_counter() - start
        assert tresp.status_code == 200
        assert duration < 0.5, f"Transfer request too slow: {duration}s (j={j})"

    gresp = requests.get(f"{BASE_URL}/api/accounts/{pesel}", timeout=1)
    assert gresp.status_code == 200
    data = gresp.json()
    assert data.get('balance', None) == 100
