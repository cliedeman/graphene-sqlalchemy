import sqlalchemy_enum34

import graphene
from graphene.types import Enum, String
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from models import Department as DepartmentModel
from models import Employee as EmployeeModel
from models import Role as RoleModel

from graphene_sqlalchemy.converter import convert_sqlalchemy_type


@convert_sqlalchemy_type.register(sqlalchemy_enum34.Enum)
def convert_column_to_string(type, column, registry=None):
    name = '{}_{}'.format(column.table.name, column.name).upper()
    choices = [e.value for e in type.python_type]
    return Enum(name, choices, description=column.doc)


class Department(SQLAlchemyObjectType):

    class Meta:
        model = DepartmentModel
        interfaces = (relay.Node, )


class Employee(SQLAlchemyObjectType):
    gender = graphene.Field(String)

    class Meta:
        model = EmployeeModel
        interfaces = (relay.Node, )

    def resolve_gender(self, args, context, info):
        return self.gender.value

class Role(SQLAlchemyObjectType):

    class Meta:
        model = RoleModel
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_employees = SQLAlchemyConnectionField(Employee)
    all_roles = SQLAlchemyConnectionField(Role)
    role = graphene.Field(Role)


schema = graphene.Schema(query=Query, types=[Department, Employee, Role])
