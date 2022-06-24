from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import user
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
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

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


    @classmethod
    def view_all_recipes(cls):
        query = """
        SELECT * FROM recipes
        JOIN users
        ON adventures.user_id = users.id
        ;"""

        result = connectToMySQL(cls.db).query_db(query)
        all_recipes = []
        if not result:
            return result
        for one_recipe in result:
            new_recipe = cls(one_recipe)
            this_recipe = {
                'id' : one_recipe['users.id'],
                'first_name' : one_recipe['first_name'],
                'last_name' : one_recipe['last_name'],
                'email' : one_recipe['email'],
                'password' : one_recipe['password'],
                'created_at' : one_recipe['users.created_at'],
                'updated_at' : one_recipe['users.updated_at']
            }
            new_recipe.creator = user.User(this_recipe)
            all_recipes.append(new_recipe)

            return all_recipes


#Update 
    @classmethod
    def edit_recipe_by_id(cls, data):
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