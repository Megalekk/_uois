from sqlalchemy import Table, Column, ForeignKey, BigInteger, Sequence
from sqlalchemy.orm import relationship, backref

def defineRelation11(TableA, TableB):
    tableAName = TableA.__tablename__
    tableBName = TableB.__tablename__
    tableBNameSingular = tableBName
    if tableBNameSingular[-1] == 's':
        tableBNameSingular = tableBNameSingular[:-1]

    tableANameSingular = tableAName
    if tableANameSingular[-1] == 's':
        tableANameSingular = tableANameSingular[:-1]
    
    setattr(TableA, f'{tableBNameSingular}_id', Column(ForeignKey(f'{tableBName}.id')))
    setattr(TableA, tableBNameSingular, relationship(TableB, back_populates=f'{tableANameSingular}', uselist=False))

    #setattr(TableB, f'{tableANameSingular}_id', Column(ForeignKey(f'{tableAName}.id')))
    setattr(TableB, tableANameSingular, relationship(TableA, back_populates=f'{tableBNameSingular}', uselist=False))

    return

def defineRelation1N(TableA, TableB):
    tableAName = TableA.__tablename__
    tableBName = TableB.__tablename__
    tableBNameSingular = TableB.__tablename__
    if tableBNameSingular[-1] == 's':
        tableBNameSingular = tableBNameSingular[:-1]
    
    setattr(TableA, f'{tableBNameSingular}_id', Column(ForeignKey(f'{tableBName}.id')))
    setattr(TableA, tableBNameSingular, relationship(TableB, back_populates=f'{tableAName}'))

    setattr(TableB, tableAName, relationship(TableA, back_populates=f'{tableBNameSingular}')) #relationship(lazy='dynamic')
    return

# inspired by and based on https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html
def defineRelationNM(TableA, TableB, sequence=Sequence('all_id_seq'), tableAItemName=None, tableBItemName=None):
    assert not(sequence is None), "sequence must be defined explicitly"

    tableAName = TableA.__tablename__ if tableAItemName is None else tableAItemName
    tableBName = TableB.__tablename__ if tableBItemName is None else tableBItemName
    
    interTable = Table(
        f'{tableAName}_{tableBName}', TableA.metadata,
        Column('id', BigInteger, sequence, primary_key=True),
        Column(f'{tableAName}_id', ForeignKey(f'{tableAName}.id'), primary_key=True),
        Column(f'{tableBName}_id', ForeignKey(f'{tableBName}.id'), primary_key=True)
    )

    setattr(TableA, tableBName, relationship(TableB, secondary=interTable)) #relationship(lazy='dynamic')
    setattr(TableB, tableAName, relationship(TableA, secondary=interTable))

    return
