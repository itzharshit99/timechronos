from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from utils.schema.models import User, Company
from utils.authentication.auth_helper import passwordHelper, AccessTokens
from utils.apis.helper import Helper

authentication = Blueprint('authentication', __name__)


### ✅ USER LOGIN
@authentication.route('/login/user', methods=['POST'])
def login_user():
    user_helper = Helper(User)
    data = user_helper.responseObject(request)

    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Email and password are required'}), 400

    user = user_helper.getRecordBy(email=data['email'])
    if not user:
        return jsonify({'message': 'Invalid credentials'}), 400

    if not passwordHelper().check_password(data['password'], user.password):
        return jsonify({'message': 'Invalid credentials'}), 400

    access_token = AccessTokens().create_access_token(user)
    refresh_token = AccessTokens().create_refresh_token(user)
    return jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 200


### ✅ COMPANY LOGIN
@authentication.route('/login/company', methods=['POST'])
def login_company():
    company_helper = Helper(Company)
    data = company_helper.responseObject(request)

    if not data or 'email_domain' not in data or 'password' not in data:
        return jsonify({'message': 'Email domain and password are required'}), 400

    company = company_helper.getRecordBy(email_domain=data['email_domain'])
    if not company:
        return jsonify({'message': 'Invalid credentials'}), 400

    if not passwordHelper().check_password(data['password'], company.password):
        return jsonify({'message': 'Invalid credentials'}), 400

    access_token = AccessTokens().create_access_token(company)
    refresh_token = AccessTokens().create_refresh_token(company)
    return jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 200


### ✅ LOGOUT (Common)
@authentication.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    AccessTokens.revoke_token(jti)
    return jsonify({'message': 'Logged out successfully'}), 200


### 🔄 REFRESH TOKENS (Common)
@authentication.route('/refreshtokens', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    
    # Determine if identity belongs to user or company
    user = Helper(User).getRecordBy(id=identity)
    if user:
        new_access_token = AccessTokens().create_access_token(user)
    else:
        company = Helper(Company).getRecordBy(id=identity)
        if not company:
            return jsonify({'message': 'Invalid identity'}), 400
        new_access_token = AccessTokens().create_access_token(company)
    
    return jsonify(access_token=new_access_token), 200
