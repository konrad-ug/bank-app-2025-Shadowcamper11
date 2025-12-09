from flask import Flask, request, jsonify
from src.account import AccountRegistry, Account

app = Flask(__name__)
registry = AccountRegistry()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    print(f"Create account request: {data}")
    
    if not data or 'name' not in data or 'surname' not in data or 'pesel' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    if registry.find_account_by_pesel(data["pesel"]) is not None:
        return jsonify({"error": "Account with this PESEL already exists"}), 409
    
    account = Account(data["name"], data["surname"], data["pesel"])
    registry.add_account(account)
    return jsonify({"message": "Account created"}), 201

@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    print("Get all accounts request received")
    accounts = registry.get_all_accounts()
    accounts_data = [{"name": acc.first_name, "surname": acc.last_name, "pesel": acc.pesel, "balance": acc.balance} for acc in accounts]
    return jsonify(accounts_data), 200

@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    print("Get account count request received")
    count = registry.get_accounts_count()
    return jsonify({"count": count}), 200

@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    print(f"Get account by pesel request: {pesel}")
    account = registry.find_account_by_pesel(pesel)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    
    return jsonify({
        "name": account.first_name, 
        "surname": account.last_name,
        "pesel": account.pesel,
        "balance": account.balance
    }), 200

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    print(f"Update account request: {pesel}")
    account = registry.find_account_by_pesel(pesel)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    if 'name' in data:
        account.first_name = data['name']
    if 'surname' in data:
        account.last_name = data['surname']
    
    return jsonify({"message": "Account updated"}), 200

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    print(f"Delete account request: {pesel}")
    account = registry.find_account_by_pesel(pesel)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    
    registry.accounts.remove(account)
    return jsonify({"message": "Account deleted"}), 200

@app.route("/api/accounts/<pesel>/transfer", methods=['POST'])
def transfer(pesel):
    print(f"Transfer request for pesel: {pesel}")
    account = registry.find_account_by_pesel(pesel)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    
    data = request.get_json()
    if not data or 'amount' not in data or 'type' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    transfer_type = data['type']
    amount = data['amount']
    
    if transfer_type not in ['incoming', 'outgoing', 'express']:
        return jsonify({"error": "Invalid transfer type"}), 400
    
    try:
        if transfer_type == 'incoming':
            account.incoming_transfer(amount)
            return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200
        elif transfer_type == 'outgoing':
            success = account.outgoing_transfer(amount)
            if not success:
                return jsonify({"error": "Insufficient funds"}), 422
            return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200
        elif transfer_type == 'express':
            success = account.express_outgoing_transfer(amount)
            if not success:
                return jsonify({"error": "Insufficient funds"}), 422
            return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 422





if __name__ == '__main__':
    app.run(debug=True)