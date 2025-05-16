import uuid
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates
from marshmallow import Schema, fields, validates as ma_validates, ValidationError
from flask import Blueprint
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
ma = Marshmallow()

models = Blueprint('models', __name__)
def generate_uuid():
    return str(uuid.uuid4())

# Models with UUID primary keys

class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(50))
    email_domain = db.Column(db.String(50), unique=True, nullable=False)
    contact_email = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(20))
    address = db.Column(db.Text)
    password = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class User(db.Model):
    __tablename__ = 'users1'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    company_id = db.Column(UUID(as_uuid=True), db.ForeignKey('companies.id'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    password = db.Column(db.String(255))
    role = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    company = db.relationship('Company', backref='users')

    ALLOWED_ROLES = {'admin', 'manager', 'employee', 'contractor'}

    @validates('role')
    def validate_role(self, key, value):
        if value not in self.ALLOWED_ROLES:
            raise ValueError(f"Invalid role: {value}. Allowed roles: {self.ALLOWED_ROLES}")
        return value


class Client(db.Model):
    __tablename__ = 'clients1'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    company_id = db.Column(UUID(as_uuid=True), db.ForeignKey('companies.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    company = db.relationship('Company', backref=db.backref('clients', lazy=True))


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    client_id = db.Column(UUID(as_uuid=True), db.ForeignKey('clients1.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    default_billable = db.Column(db.Boolean, default=True)
    employee_rate = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='planned')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    client = db.relationship('Client', backref='projects', lazy=True)

    ALLOWED_STATUSES = {'planned', 'active', 'completed'}

    @validates('status')
    def validate_status(self, key, value):
        if value not in self.ALLOWED_STATUSES:
            raise ValueError(f"Invalid project status: {value}. Allowed: {self.ALLOWED_STATUSES}")
        return value


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    project_id = db.Column(UUID(as_uuid=True), db.ForeignKey('projects.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)
    billable = db.Column(db.Boolean, default=True, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    project = db.relationship('Project', backref='tasks')


class Timesheet(db.Model):
    __tablename__ = 'timesheets'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users1.id'), nullable=False)
    week_start = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='draft')
    submitted_at = db.Column(db.DateTime)
    approved_at = db.Column(db.DateTime)
    rejected_at = db.Column(db.DateTime)
    rejection_reason = db.Column(db.Text)
    recalled_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = db.relationship('User', backref='timesheets')

    ALLOWED_STATUSES = {'draft', 'submitted', 'approved', 'rejected', 'recalled'}

    @validates('status')
    def validate_status(self, key, value):
        if value not in self.ALLOWED_STATUSES:
            raise ValueError(f"Invalid timesheet status: {value}. Allowed: {self.ALLOWED_STATUSES}")
        return value


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    company_id = db.Column(UUID(as_uuid=True), db.ForeignKey('companies.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    permissions = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    company = db.relationship('Company', backref=db.backref('roles', lazy=True))


class Country(db.Model):
    __tablename__ = 'country'

    name = db.Column(db.String(100), primary_key=True)
    nicename = db.Column(db.String(100))
    iso3 = db.Column(db.String(3))
    iso = db.Column(db.String(2))
    numcode = db.Column(db.Integer)
    phonecode = db.Column(db.String(10))


class TokenBlacklist(db.Model):
    __tablename__ = 'token_blacklist'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    jti = db.Column(db.String(36), nullable=False, index=True)
    token_type = db.Column(db.String(20), nullable=False)
    user_identity = db.Column(db.String(120), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False, default=False)
    expires = db.Column(db.DateTime, nullable=False)
    epoch_expires = db.Column(db.BigInteger, nullable=True)
    client_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


# Marshmallow Schemas

class CompanySchema(Schema):
    id = fields.UUID()
    name = fields.Str(required=True)
    industry = fields.Str()
    email_domain = fields.Str(required=True)
    contact_email = fields.Email(required=True)
    contact_number = fields.Str()
    address = fields.Str()
    password = fields.Str(load_only=True)
    created_at = fields.DateTime()


class UserSchema(Schema):
    id = fields.UUID()
    company_id = fields.UUID(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str()
    password = fields.Str(load_only=True)
    role = fields.Str(required=True)
    created_at = fields.DateTime()

    @ma_validates('role')
    def validate_role(self, value):
        allowed = {'admin', 'manager', 'employee', 'contractor'}
        if value not in allowed:
            raise ValidationError(f"Invalid role: {value}. Allowed roles: {allowed}")


class ClientSchema(Schema):
    id = fields.UUID()
    company_id = fields.UUID(required=True)
    name = fields.Str(required=True)
    code = fields.Str(required=True)
    description = fields.Str()
    created_at = fields.DateTime()


class ProjectSchema(Schema):
    id = fields.UUID()
    client_id = fields.UUID(required=True)
    name = fields.Str(required=True)
    code = fields.Str(required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    default_billable = fields.Bool()
    employee_rate = fields.Float(required=True)
    status = fields.Str()
    created_at = fields.DateTime()

    @ma_validates('status')
    def validate_status(self, value):
        allowed = {'planned', 'active', 'completed'}
        if value not in allowed:
            raise ValidationError(f"Invalid project status: {value}. Allowed: {allowed}")


class TaskSchema(Schema):
    id = fields.UUID()
    project_id = fields.UUID(required=True)
    name = fields.Str(required=True)
    code = fields.Str(required=True)
    billable = fields.Bool()
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    description = fields.Str()
    created_at = fields.DateTime()


class TimesheetSchema(Schema):
    id = fields.UUID()
    user_id = fields.UUID(required=True)
    week_start = fields.Date(required=True)
    status = fields.Str()
    submitted_at = fields.DateTime()
    approved_at = fields.DateTime()
    rejected_at = fields.DateTime()
    rejection_reason = fields.Str()
    recalled_at = fields.DateTime()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @ma_validates('status')
    def validate_status(self, value):
        allowed = {'draft', 'submitted', 'approved', 'rejected', 'recalled'}
        if value not in allowed:
            raise ValidationError(f"Invalid timesheet status: {value}. Allowed: {allowed}")


class RoleSchema(Schema):
    id = fields.UUID()
    company_id = fields.UUID(required=True)
    name = fields.Str(required=True)
    description = fields.Str()
    permissions = fields.Str()
    created_at = fields.DateTime()


class CountrySchema(Schema):
    name = fields.Str()
    nicename = fields.Str()
    iso3 = fields.Str()
    iso = fields.Str()
    numcode = fields.Int()
    phonecode = fields.Str()


class TokenBlacklistSchema(Schema):
    id = fields.UUID()
    jti = fields.Str(required=True)
    token_type = fields.Str(required=True)
    user_identity = fields.Str(required=True)
    revoked = fields.Bool()
    expires = fields.DateTime()
    epoch_expires = fields.Int()
    client_id = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
