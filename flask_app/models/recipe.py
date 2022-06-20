from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session

# make class, class methods with SQL, and logic
class Recipe:
    db = 'recipe_schema'

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date = data['date']
        self.time = data['time']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

#Create 
    @classmethod
    def create_recipe(cls, data):
        if not cls.validate_recipe(data):
            return False
        query = """
        INSERT INTO recipes(name, description, instructions, time, date, user_id)
        VALUES( %(name)s, %(description)s, %(instructions)s, %(time)s, %(date)s, %(user_id)s)
        ;"""

        recipe_id = connectToMySQL(cls.db).query_db(query, data)

        return recipe_id

#Read 
    @classmethod
    def view_recipe_by_id(cls, id):
        data = {'id' : id}
        query = """
        SELECT * FROM recipes
        WHERE id = %(id)s
        ;"""
        
        result = connectToMySQL(cls.db).query_db(query, data)

        return cls(result[0])

#Update 
    @classmethod
    def edit_recipe_by_id(cls, data,):
        if not cls.validate_recipe(data):
            return False
        query = """
        UPDATE recipes
        SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, time = %(time)s, date = %(date)s, updated_at = NOW()
        WHERE id = %(id)s
        ;"""

        return connectToMySQL(cls.db).query_db(query, data)


#Delete 
    @classmethod
    def delete_recipe_by_id(cls, id):
        data = {'id' : id}
        query = """
        DELETE FROM recipes
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)


#Validate
    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data['name']) < 2:
            flash('Your name must be at least 2 characters.')
            is_valid = False
        if len(data['description']) < 10:
            flash('Your description must be at least 10 characters.')
            is_valid = False
        if len(data['instructions']) < 10:
            flash('Your instructions must be at least 10 characters.')
            is_valid = False
        if not data['date']:
            flash('Please choose a date')
            is_valid = False
        if 'time' not in data:
            flash('Must select a time.')
            is_valid = False
        return is_valid