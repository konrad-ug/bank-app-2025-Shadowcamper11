from behave import given, when, then, step
import requests

URL = "http://localhost:5000"


@step('I create an account using name: "{name}", last name: "{last_name}", pesel: "{pesel}"')
def create_account(context, name, last_name, pesel):
    json_body = {"name": f"{name}", "surname": f"{last_name}", "pesel": pesel}
    create_resp = requests.post(URL + "/api/accounts", json=json_body)
    assert create_resp.status_code == 201 or create_resp.status_code == 409, f"Create failed: {create_resp.status_code}"


@step('Account registry is empty')
@step('Acoount registry is empty')
def clear_account_registry(context):
    response = requests.get(URL + "/api/accounts")
    assert response.status_code == 200
    accounts = response.json()

    for account in accounts:
        pesel = account["pesel"]
        requests.delete(URL + f"/api/accounts/{pesel}")


@step('Number of accounts in registry equals: "{count}"')
def is_account_count_equal_to(context, count):
    response = requests.get(URL + "/api/accounts/count")
    assert response.status_code == 200
    data = response.json()
    assert int(data.get('count', -1)) == int(count), f"Expected {count}, got {data.get('count')}"


@step('Account with pesel "{pesel}" exists in registry')
def check_account_with_pesel_exists(context, pesel):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200, f"Account {pesel} not found (status {response.status_code})"


@step('Account with pesel "{pesel}" does not exist in registry')
def check_account_with_pesel_does_not_exist(context, pesel):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 404


@when('I delete account with pesel: "{pesel}"')
def delete_account(context, pesel):
    response = requests.delete(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200


@when('I update "{field}" of account with pesel: "{pesel}" to "{value}"')
def update_field(context, field, pesel, value):
    if field not in ["name", "surname"]:
        raise ValueError(f"Invalid field: {field}. Must be 'name' or 'surname'.")
    json_body = {f"{field}": f"{value}"}
    response = requests.patch(URL + f"/api/accounts/{pesel}", json=json_body)
    assert response.status_code == 200


@then('Account with pesel "{pesel}" has "{field}" equal to "{value}"')
def field_equals_to(context, pesel, field, value):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200
    data = response.json()
    if field == 'balance':
        assert str(data.get('balance', '')) == str(value), f"Expected balance {value}, got {data.get('balance')}"
    else:
        assert data.get(field, '') == value, f"Expected {field} {value}, got {data.get(field)}"


@when('I perform an incoming transfer of {amount} to account with pesel: "{pesel}"')
def perform_incoming_transfer(context, amount, pesel):
    json_body = {"amount": int(amount), "type": "incoming"}
    response = requests.post(URL + f"/api/accounts/{pesel}/transfer", json=json_body)
    assert response.status_code == 200
