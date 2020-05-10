#!/usr/bin/env python3

import os

from sqlalchemy.sql import func

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_restx import Api, Resource, fields


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'mysql+pymysql://root:rootpass@127.0.0.1:33306/todo')
db = SQLAlchemy(app)

app.config['CACHE_REDIS_HOST'] = os.getenv('CACHE_REDIS_HOST', '127.0.0.1')
app.config['CACHE_REDIS_PORT'] = os.getenv('CACHE_REDIS_PORT', 36379)
app.config['CACHE_TYPE'] = 'redis'
cache = Cache(app)

api = Api(app, version='1.0', title='Todo API', description='Todo API based on MySQL and Redis')

ns_todos = api.namespace('todos', description='TODO operations')
todo = api.model('Todo', {
    'id': fields.Integer(readOnly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details'),
    'created': fields.DateTime(readOnly=True, description='Date/time when the task was created')
})


class TodoModel(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task = db.Column(db.String(128), unique=True, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<TodoModel {self.task}>'


class TodoDao(object):
    @cache.cached(timeout=60, key_prefix='all_todos')
    def list(self):
        return TodoModel.query.all()

    @cache.memoize(timeout=60)
    def get(self, id):
        todo = TodoModel.query.filter_by(id=id).first()
        if not todo:
            api.abort(404, "Todo {} doesn't exist".format(id))
        return todo

    def create(self, data):
        todo = TodoModel(task=data['task'])
        db.session.add(todo)
        db.session.commit()
        cache.clear()
        return todo

    def update(self, id, data):
        todo = self.get(id)
        todo.task = data['task']
        db.session.commit()
        cache.clear()
        return todo

    def delete(self, id):
        TodoModel.query.filter_by(id=id).delete()
        db.session.commit()
        cache.clear()


todo_dao = TodoDao()

db.create_all()
if not list(filter(lambda t: t.task == 'Dummy task', todo_dao.list())):
    todo_dao.create({'task': 'Dummy task'})


@ns_todos.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns_todos.doc('list_todos')
    @ns_todos.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        return todo_dao.list()

    @ns_todos.doc('create_todo')
    @ns_todos.expect(todo)
    @ns_todos.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''
        return todo_dao.create(api.payload), 201


@ns_todos.route('/<int:id>')
@ns_todos.response(404, 'Todo not found')
@ns_todos.param('id', 'The task identifier')
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @ns_todos.doc('get_todo')
    @ns_todos.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resource'''
        return todo_dao.get(id)

    @ns_todos.doc('delete_todo')
    @ns_todos.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        todo_dao.delete(id)
        return '', 204

    @ns_todos.expect(todo)
    @ns_todos.marshal_with(todo)
    def put(self, id):
        '''Update a task given its identifier'''
        return todo_dao.update(id, api.payload)

