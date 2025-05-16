from flask import Blueprint, jsonify
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from utils.schema.models import db
from utils.authentication.auth_helper import passwordHelper, AccessTokens
from uuid import UUID

helper = Blueprint('helper', __name__)

class Helper:

    def __init__(self, model):
        self.model = model

    def responseObject(self, Object):
        data = {}
        try:
            if Object.is_json:
                data = Object.get_json()
            else:
                data = Object.form.to_dict()
            return data
        except Exception as e:
            return jsonify({'message': f'Error processing request data: {str(e)}'}), 400
    
    def addRecordToDb(self, formObject):
        data = formObject
        model = self.model()
        password = passwordHelper()
        try:
            for key in dir(model):
                if key == 'password':
                    password = password.hash_password(data['password'])
                    setattr(model, key, password)
                else: 
                    if key in data:
                        setattr(model, key, data[key])
            
            db.session.add(model)
            db.session.commit()
            return jsonify({'message': 'Record added successfully'}), 200
    
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'SQLAlchemyError': f'Error adding record to database: {str(e)}'}), 400
        
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({'IntegrityError': f'Error adding record to database: {str(e)}'}), 400
 
        except AttributeError as e:
            db.session.rollback()
            return jsonify({'AttributeError': f'Error adding record to database: {str(e)}'}), 400
        
        except KeyError as e:
            db.session.rollback()
            return jsonify({'KeyError': f'Error adding record to database: {str(e)}'}), 400
        
        except ValueError as e:
            db.session.rollback()
            return jsonify({'ValueError': f'Error adding record to database: {str(e)}'}), 400
        
        except TypeError as e:
            db.session.rollback()
            return jsonify({'TypeError': f'Error adding record to database: {str(e)}'}), 400
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'Exception': f'Error adding record to database: {str(e)}'}), 400

        finally:
            db.session.close()

    def updateRecordToDb(self, formObject):
        data = formObject
        model = self.model()
        password = passwordHelper()

        model = self.model.query.get(data['id'])
        
        try:
            for key in dir(model):
                if key == 'password':
                    password = password.hash_password(data['password'])
                    setattr(model, key, password)
                else: 
                    if key in data:
                        setattr(model, key, data[key])
            
            db.session.commit()
            return jsonify({'message': 'Record updated successfully'}), 200
        
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'SQLAlchemyError': f'Error adding record to database: {str(e)}'}), 400
        
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({'IntegrityError': f'Error adding record to database: {str(e)}'}), 400
 
        except AttributeError as e:
            db.session.rollback()
            return jsonify({'AttributeError': f'Error adding record to database: {str(e)}'}), 400
        
        except KeyError as e:
            db.session.rollback()
            return jsonify({'KeyError': f'Error adding record to database: {str(e)}'}), 400
        
        except ValueError as e:
            db.session.rollback()
            return jsonify({'ValueError': f'Error adding record to database: {str(e)}'}), 400
        
        except TypeError as e:
            db.session.rollback()
            return jsonify({'TypeError': f'Error adding record to database: {str(e)}'}), 400
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'Exception': f'Error adding record to database: {str(e)}'}), 400

        finally:
            db.session.close()

    def deleteRecordFromDb(self, formObject):
        data = formObject
        model = self.model()

        model = self.model.query.get(data.id)

        try:
            db.session.delete(model)
            db.session.commit()
            return model
        
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'message': f'Error adding record to database: {str(e)}'}), 400
        
        except Exception as e:
            return jsonify({'message': f'Error adding record to database: {str(e)}'}), 400
        
        except AttributeError as e:
            return jsonify({'message': f'Error adding record to database: {str(e)}'}), 400
        
        except KeyError as e:
            return jsonify({'message': f'Error adding record to database: {str(e)}'}), 400
        
        except ValueError as e:
            return jsonify({'message': f'Error adding record to database: {str(e)}'}), 400
        
        except TypeError as e:
            return jsonify({'message': f'Error adding record to database: {str(e)}'}), 400
        
        finally:
            db.session.close()

#Get Data from Models (Simple Queries)

    def getRecord(self, id):
        record = self.model.query.get(id)
        return record

    def getAllRecords(self):
        records = self.model.query.all()
        return records

    def getRecordBy(self, **kwargs):
        return self.model.query.filter_by(**kwargs).first()
       

    def getAllRecordsBy(self, **kwargs):
        records = self.model.query.filter_by(**kwargs).all()
        return records

    def getAllRecordsByIn(self, **kwargs):
        records = self.model.query.filter(self.model.in_(**kwargs)).all()
        return records

    def getAllRecordsByNotIn(self, **kwargs):
        records = self.model.query.filter(self.model.notin_(**kwargs)).all()
        return records

    def getAllRecordsByLike(self, **kwargs):
        records = self.model.query.filter(self.model.like(**kwargs)).all()
        return records

    def getAllRecordsByNotLike(self, **kwargs):
        records = self.model.query.filter(self.model.notlike(**kwargs)).all()
        return records

    def getAllRecordsByBetween(self, **kwargs):
        records = self.model.query.filter(self.model.between(**kwargs)).all()
        return records

    def getAllRecordsByNotBetween(self, **kwargs):
        records = self.model.query.filter(self.model.notbetween(**kwargs)).all()
        return records

    def getAllRecordsByGreaterThan(self, **kwargs):
        records = self.model.query.filter(self.model.gt(**kwargs)).all()
        return records

    def getAllRecordsByLessThan(self, **kwargs):
        records = self.model.query.filter(self.model.lt(**kwargs)).all()
        return records

    def getAllRecordsByGreaterThanOrEqual(self, **kwargs):
        records = self.model.query.filter(self.model.gte(**kwargs)).all()
        return records

    def getAllRecordsByLessThanOrEqual(self, **kwargs):
        records = self.model.query.filter(self.model.lte(**kwargs)).all()
        return records

    def getAllRecordsByNotEqual(self, **kwargs):
        records = self.model.query.filter(self.model.ne(**kwargs)).all()
        return records

    def getAllRecordsByIsNull(self, **kwargs):
        records = self.model.query.filter(self.model.isnull(**kwargs)).all()
        return records

    def getAllRecordsByIsNotNull(self, **kwargs):
        records = self.model.query.filter(self.model.isnotnull(**kwargs)).all()
        return records
    
    # required fields for each model

    model_required_fields = {
    "company": ["name", "email_domain", "contact_email", "contact_number", "address", "password"],
    "user": ["company_id", "first_name", "last_name", "email", "role", "password"],
    "client": ["company_id", "name", "code"],
    "project": ["client_id", "name", "code", "start_date", "end_date", "employee_rate"],
    "task": ["project_id", "name", "code", "start_date", "end_date"],
    "timesheet": ["user_id", "week_start"],
    "role": ["company_id", "name"],
    "tokenblacklist": ["jti", "token_type", "user_identity", "expires"]
}



    def requiredParams(self, responseObj):
        model_instance = self.model().__class__.__name__.lower()
        required_fields = self.model_required_fields[model_instance]
        not_available_fields = []
        for field in required_fields:
            if field not in responseObj:
                not_available_fields.append(field)
        
        return not_available_fields

class RecordDML:
    
    def addRecord(claims, request, model):
        claims = claims

        validate = AccessTokens.is_token_revoked(claims)
        if validate:
            return jsonify({'message': 'Token has been revoked, You logged out, please login again!'}), 401
               
        #Instantiating the Models with Helper Class
        objectInstance = Helper(model)

        #Getting the request object verified for the type of request and converting it to a dictionary
        responseObj = objectInstance.responseObject(request)
        try:
          responseObj['company_id'] = UUID(str(responseObj.get('company_id')))
        except Exception:
          return jsonify({'message': 'Invalid or missing company_id'}), 400


        #Checking if required Parameters are present in the request object
        UserParams = objectInstance.requiredParams(responseObj)
        if UserParams != []:
            return jsonify({'message': f'Missing required parameters: {UserParams}'}), 400

        #Check if user already exists
        if 'email' in responseObj:
          if objectInstance.getRecordBy(email=responseObj['email']):
              email = responseObj['email']
              return jsonify({'message': f'User already exists (email:{email}), the user registration failed.'}), 400

        if 'first_name' in claims and 'last_name' in claims:
            responseObj['created_by'] = str(claims.get('first_name') + ' ' +  claims.get('last_name'))
            responseObj['created_by_id'] = UUID(claims.get('id'))

        #Adding the User to the Database
        user = objectInstance.addRecordToDb(responseObj)
        return user
    
    
    def updateRecord(claims, request, model):
     claims = claims
     validate = AccessTokens.is_token_revoked(claims)
     if validate:
            return jsonify({'message': 'Token has been revoked, You logged out, please login again!'}), 401
    #Instantiate the User Model with Helper Class
     objectInstance = Helper(model)

     #Get the request object verified for the type of request and converting it to a dictionary
     responseObj = objectInstance.responseObject(request)
     requiredParams = objectInstance.requiredParams(responseObj)

     if requiredParams != []:
        return jsonify({'message': f'Missing required parameters: {requiredParams}'}), 400
     
     #See if the user exists
     user = objectInstance.getRecordBy(email=responseObj['email'])
     if not user:
         return jsonify({'message': 'User not found'}), 404
     else: #if exist then setup the information to be send for database update
          responseObj['accounts_id'] = UUID(claims['accounts_id'])
          responseObj['id'] = user.id
          responseObj['updated_by'] = str(claims.get('first_name') + ' ' +  claims.get('last_name'))
          responseObj['updated_by_id'] = UUID(claims.get('id'))
               
          #Send data to the database for update
          updateUser = objectInstance.updateRecordToDb(responseObj)
     return updateUser

    def deleteRecord(claims, request, model):
        claims = claims
        validate = AccessTokens.is_token_revoked(claims)
        if validate:
            return jsonify({'message': 'Token has been revoked, You logged out, please login again!'}), 401
        
        objectInstance = Helper(model)

    #Get the request object verified for the type of request and converting it to a dictionary
        responseObj = objectInstance.responseObject(request)

    #Checking if required Parameters are present in the request object
        UserParams = objectInstance.requiredParams(responseObj)
        if UserParams != []:
            return jsonify({'message': f'Missing required parameters: {UserParams}'}), 400

        #See if the user exists
        user = objectInstance.getRecordBy(email=responseObj['email'])
        if not user:
            email = responseObj['email']
            return jsonify({'message': f'User not found (email:{email}), the user registration failed.'}), 400
        else:
            #Send data to the database for update
            objectInstance.deleteRecordFromDb(user)
            return jsonify("User deleted successfully"), 200

class RecordView:
    pass