from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session
from flask_app.models import recipe
import re
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

# make class, class methods with SQL, and logic
class User:
    db = 'recipe_schema'

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []

#Create 
    @classmethod
    def create_user(cls, data):
        if not cls.validate_user_reg(data):
            return False
        parsed_data = cls.parse_reg_data(data)
        query = """
        INSERT INTO users(first_name, last_name, email, password, created_at, updated_at)
        VALUES( %(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW())
        ;"""

        user_id = connectToMySQL(cls.db).query_db(query, parsed_data)

        session['user_id'] = user_id

        return True

#Read 
    @classmethod
    def get_user_by_email(cls, email):
        data = {'email' : email}
        query = """
        SELECT * FROM users
        WHERE email = %(email)s
        ;"""

        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            result = cls(result[0])

        return result


    @classmethod
    def get_user_by_id(cls, id):
        data = {'id' : id}
        query = """
        SELECT * FROM users
        LEFT JOIN recipes 
        ON users.id = recipes.user_id
        WHERE users.id = %(id)s
        ;"""

        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            this_result = cls(result[0])
            for one_recipe in result:
                info = {
                    'id' : one_recipe['recipes.id'],
                    'name' : one_recipe['name'],
                    'description' : one_recipe['description'],
                    'instructions' : one_recipe['instructions'],
                    'date' : one_recipe['date'],
                    'time' : one_recipe['time'],
                    'user_id' : one_recipe['user_id'],
                    'created_at' : one_recipe['recipes.created_at'],
                    'updated_at' : one_recipe['recipes.updated_at']
                }
                this_result.recipes.append(recipe.Recipe(info))

        return this_result

#Update 


#Delete 


#Validate 
    @staticmethod
    def validate_user_reg(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(data['first_name']) < 2:
            flash('Your name must be at least 2 characters.')
            is_valid = False
        if len(data['last_name']) < 2:
            flash('Your name must be at least 2 characters.')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid email address!')
            is_valid = False
        if User.get_user_by_email(data['email'].lower()):
            flash('Email already exits')
            is_valid = False
        if len(data['password']) < 8:
            flash('Your password must contain at least 8 characters.')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash('Your password does not match')
            is_valid = False
        return is_valid

    @staticmethod
    def parse_reg_data(data):
        parsed_data = {}
        parsed_data['first_name'] = data['first_name']
        parsed_data['last_name'] = data['last_name']
        parsed_data['email'] = data['email'].lower()
        parsed_data['password'] = bcrypt.generate_password_hash(data['password'])
        return parsed_data

    @staticmethod
    def login(data):
        this_user = User.get_user_by_email(data['email'].lower())
        if this_user:
            if bcrypt.check_password_hash(this_user.password, data['password']):
                session['user_id'] = this_user.id
                return True
        flash('Your login info is incorrect')
        return False