import sqlalchemy as sa
from sqlalchemy import inspect, event
from sqlalchemy.orm import joinedload, selectinload, load_only
from sqlalchemy.orm.attributes import AttributeImpl, InstrumentedAttribute

from flask import request
from flask_restx import Mask

from app.models import db

class BaseService(object):
    def __init__(self, cls):
        self.cls = cls

    def insert(self, data, commit=True, **kwargs):
        if 'id' in data:
            del data['id']
        # we assume each relationship is an already instantiated object
        relationships = inspect(self.cls).relationships
        # loop over the relationships this class has
        for rel in relationships:
            # check if the supplied data has this relationship
            if rel.key in data:
                # map from int -> object
                if type(data[rel.key]) == int:
                    data[rel.key] = rel.mapper.class_.query.filter_by(id=data[rel.key]).first()
                # map from [int] -> [object]
                elif type(data[rel.key]) == list:
                    ret = []
                    for rel_elem in data[rel.key]:
                        if type(rel_elem) == int:
                            # this relationship is an integer, object already exists
                            ret.append(rel.mapper.class_.query.filter_by(id=rel_elem).first())
                        elif type(rel_elem) == dict:
                            # a dictionary was given, create a new element
                            ret.append(rel.mapper.class_(**rel_elem))
                    data[rel.key] = ret
                # other mappings not implemented yet
                # TODO: allow mapping objects/dicts, e.g. {"id": 8} -> Object
                else:
                    raise NotImplementedError('Only implemented mapping lists or ints to objects')
        # instantiate an object for the class with the given data
        obj = self.cls(**data)
        db.session.add(obj)
        if commit:
            db.session.commit()
        return obj

    def batch_insert(self, data):
        items = []
        for item in data:
            items.append(self.insert(item, commit=True, do_checks=True))
        return items

    def update(self, data, key='id'):
        if key not in data:
            raise KeyError('No "{}" key found in data object, cannot distinguish the object to update'.format(key))
        # remove the selection element from the update payload
        # del data[key]
        # update the object with the data supplied
        obj = self.cls.query.filter_by(**{key: data[key]}).first()
        for k, v in data.items():
            if key != k:
                setattr(obj, k, v) 
        db.session.commit()
        return obj
    
    def delete(self, data, key='id'):
        if key not in data:
            raise KeyError('No "{}" key found in data object, cannot distinguish the object to delete'.format(key))
        # fetch all objects to be deleted from the database
        to_be_deleted = self.get_all(filter_by={key: data[key]})
        # loop over each object, marking them as deleted
        for obj in to_be_deleted:
            db.session.delete(obj)
        # commit the session, flushing the changes in the database
        db.session.commit()

    def delete_all(self):
        """use with care"""
        self.cls.query.delete()

    def get_all(self, filter_by={}, order_by=None, default_mask=None):
        # sqlalchemy stopped supporting string arguments for sorting
        # this small hack makes sure our legacy code keeps working
        if type(order_by) == str:
            order_by = sa.text(order_by)

        # the x-fields header gives us the exact properies we want to fetch
        # preload relationships via a joined query if we find them in the mask
        preload_relationships = []
        load_columns = []
        if request.headers.has_key('X-FIELDS') or default_mask is not None:
            # get the relationships this class has
            relationships = inspect(self.cls).relationships
            relationships = [x.key for x in relationships]
            # parse the mask using the presupplied class from Flask-RestPlus
            mask = Mask(mask=request.headers.get('X-FIELDS') if request.headers.has_key('X-FIELDS') else default_mask)
            # add non-relationship columns to the column filter
            for col_name in mask:
                if col_name not in relationships:
                    if hasattr(self.cls, col_name):
                        prop = getattr(self.cls, col_name)
                        if type(prop) == InstrumentedAttribute:
                            load_columns.append(load_only(prop))
            # add relationship columns to the preloading list
            for relationship in relationships:
                if relationship in mask:
                    if hasattr(self.cls, relationship):
                        preload_relationships.append(selectinload(getattr(self.cls, relationship)))
        if len(load_columns) == 0:
            query = self.cls.query.options(*preload_relationships)
        else:
            query = self.cls.query.options(*load_columns, *preload_relationships)

        # run or filter query once
        or_run_once = False

        for attr,value in filter_by.items():
            attr_split = attr.split(" ")
            if len(attr_split) == 1:
                query = query.filter( getattr(self.cls,attr) == value )
            else:
                if attr_split[1] == 'not':
                    query = query.filter( getattr(self.cls,attr_split[0]) != value )
                if attr_split[1] == '>':
                    query = query.filter( getattr(self.cls,attr_split[0]) > value )
                if attr_split[1] == '<':
                    query = query.filter( getattr(self.cls,attr_split[0]) < value )
                if attr_split[1] == 'or':
                    if (or_run_once == False):
                        query = query.filter( sa.or_( v for v in self.split_or( filter_by )))
                    or_run_once = True
        return query.order_by(order_by).all()

    def get_first(self, filter_by={}):
        # the x-fields header gives us the exact properies we want to fetch
        # preload relationships via a joined query if we find them in the mask
        preload_relationships = []
        if request.headers.has_key('X-FIELDS'):
            mask = Mask(mask=request.headers.get('X-FIELDS'))
            # get the relationships this class has
            relationships = inspect(self.cls).relationships
            for relationship in relationships:
                if relationship.key in mask:
                    preload_relationships.append(joinedload(getattr(self.cls, relationship.key)))
        
        return self.cls.query.options(*preload_relationships).filter_by(**filter_by).first()

    def split_or(self, filter_by):
        statement = []
        for cattr,cvalue in filter_by.items():
            if cattr.split(" ")[1] == 'or':
                statement.append(getattr(self.cls,cattr.split(" ")[0]) == cvalue)
        return statement
