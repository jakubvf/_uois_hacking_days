from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence
import datetime
from functools import cache

import sqlengine.sqlengine as SqlEngine

from . import BaseModel

@cache # funny thing, it makes from this function a singleton
def GetModels(BaseModel=BaseModel.getBaseModel(), unitedSequence=Sequence('all_id_seq')):
    #assert not(unitedSequence is None), "unitedSequence must be defined"
    print('Base models definition (UserModel, GroupModel, RoleModel, GroupTypeModel, RoleTypeModel)')
    class UserModel(BaseModel):
        __tablename__ = 'users'
        
        id = Column(BigInteger, unitedSequence, primary_key=True)
        name = Column(String)
        
        lastchange = Column(DateTime, default=datetime.datetime.now)
        externalId = Column(BigInteger, index=True)


    class GroupModel(BaseModel):
        __tablename__ = 'groups'
        
        id = Column(BigInteger, unitedSequence, primary_key=True)
        name = Column(String)
        
        lastchange = Column(DateTime, default=datetime.datetime.now)
        entryYearId = Column(Integer)

        externalId = Column(String, index=True)
        
    class RoleModel(BaseModel):
        __tablename__ = 'roles'

        id = Column(BigInteger, unitedSequence, primary_key=True)
        name = Column(String)
        
        lastchange = Column(DateTime, default=datetime.datetime.now)

    class GroupTypeModel(BaseModel):
        __tablename__ = 'grouptypes'
        
        id = Column(BigInteger, unitedSequence, primary_key=True)
        name = Column(String)
        
    class RoleTypeModel(BaseModel):
        __tablename__ = 'roletypes'

        id = Column(BigInteger, unitedSequence, primary_key=True)
        name = Column(String)

    return UserModel, GroupModel, RoleModel, GroupTypeModel, RoleTypeModel


from . import Relations 
@cache
def BuildRelations():
    UserModel, GroupModel, RoleModel, GroupTypeModel, RoleTypeModel = GetModels()
    print('building relations between base models')

    Relations.defineRelationNM(UserModel, GroupModel)
    Relations.defineRelation1N(GroupModel, GroupTypeModel)    
    Relations.defineRelation11(RoleModel, RoleTypeModel)
    Relations.defineRelation1N(RoleModel, GroupModel)
    Relations.defineRelation1N(RoleModel, UserModel)

    print('building relations between base models finished')
    #defineRelationNM(BaseModel, EventModel, UserModel, 'teachers', 'events')

    pass