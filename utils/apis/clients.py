from flask import jsonify, Blueprint, request
from utils.apis.helper import RecordDML
from utils.schema.models import Client
from flask_jwt_extended import jwt_required, get_jwt

clients = Blueprint('clients', __name__)

@clients.route('/addclients', methods=['POST'])
@jwt_required()
def addClients():
    claims = get_jwt()
    addClients = RecordDML.addRecord(claims, request, Client)
    return addClients

@clients.route('/updateclients', methods=['POST'])
@jwt_required()
def updateClients():
    claims = get_jwt()
    updateClients = RecordDML.updateRecord(claims, request, Client)
    return updateClients

@clients.route('/deleteclients', methods=['POST'])
@jwt_required()
def deleteClients():
    claims = get_jwt()
    deleteClients = RecordDML.deleteRecord(claims, request, Client)
    return deleteClients