from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from utils.apis.helper import Helper, RecordDML, AccessTokens
from utils.schema.models import Company, User

company_registration = Blueprint('company_registration', __name__)

@company_registration.route('/register-company', methods=['POST'])
def register_company():
    CompanyInstance = Helper(Company)
    responseObj = CompanyInstance.responseObject(request)

    if 'password' not in responseObj:
        return jsonify({'message': 'Password is required.'}), 400 

    # Check required fields
    companyParams = CompanyInstance.requiredParams(responseObj)
    if companyParams:
        return jsonify({'message': f'Required company parameters missing: {companyParams}'}), 400

    # Check if company already exists
    if CompanyInstance.getRecordBy(email_domain=responseObj.get('email_domain')):
        return jsonify({'message': f"Company with domain {responseObj['email_domain']} already exists. Registration failed."}), 400

    # Register company
    CompanyInstance.addRecordToDb(responseObj)
    return jsonify({'message': 'Company registration successful.'}), 200


@company_registration.route('/register-user', methods=['POST'])
def register_user():
    UserInstance = Helper(User)
    responseObj = UserInstance.responseObject(request)

    if 'password' not in responseObj:
        return jsonify({'message': 'Password is required.'}), 400 

    # Check required fields
    userParams = UserInstance.requiredParams(responseObj)
    if userParams:
        return jsonify({'message': f'Required user parameters missing: {userParams}'}), 400

    # Check if user exists
    if UserInstance.getRecordBy(email=responseObj.get('email')):
        return jsonify({'message': f"User with email {responseObj['email']} already exists. Registration failed."}), 400

    # Register user
    UserInstance.addRecordToDb(responseObj)
    return jsonify({'message': 'User registration successful.'}), 200


@company_registration.route('/update-company', methods=['POST'])
@jwt_required()
def update_company():
    claims = get_jwt()
    validate = AccessTokens.is_token_revoked(claims)
    if validate:
            return jsonify({'message': 'Token has been revoked, You logged out, please login again!'}), 401
    updateaccounts = RecordDML.updateRecord(claims, request, Company)
    return updateaccounts
