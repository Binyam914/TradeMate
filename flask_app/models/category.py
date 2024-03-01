from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL

class Category: 
    db = "businesses_ad_schema" # change it your DB name
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['id']
    @classmethod
    def get_categories(cls):
        query = '''
            SELECT c.*, COUNT(b.id) AS business_count, u.first_name, u.last_name
            FROM categories c
            LEFT JOIN businesses b ON c.id = b.category_id
            LEFT JOIN users u ON c.user_id = u.id
            GROUP BY c.id, c.name
        '''
        results = connectToMySQL(cls.db).query_db(query)
        return results

    # ADD NEW
    @classmethod
    def create(cls, data):
        query = "INSERT INTO categories(name,updated_at, created_at, user_id) VALUES (%(name)s, NULL, NOW(), %(user_id)s);"
        business = connectToMySQL(cls.db).query_db(query, data)
        return business

    @classmethod
    def get_all(cls, data):
        query = '''
            SELECT businesses.*, users.id, users.first_name, users.last_name, COUNT(likes.business_id) AS like_count
            FROM businesses
            JOIN users ON businesses.user_id = users.id 
            LEFT JOIN likes ON businesses.id = likes.business_id
            GROUP BY businesses.id
            ORDER BY like_count DESC
        '''
        results = connectToMySQL(cls.db).query_db(query, data)
        return results


    def get_my_businesses(cls,data):
        query = '''
            SELECT * FROM businesses
            WHERE user_id =  %(user_id)s
        '''
        results = connectToMySQL('businesses_ad_schema').query_db(query,data)
        return results

    @classmethod
    def get_one(cls, data):
        query = """
            SELECT * FROM categories 
            WHERE id = %(id)s
        """

        result = connectToMySQL('businesses_ad_schema').query_db(query, data)
        if result:
            return result[0] 
        else:
            return None

    
    @staticmethod
    def delete(data):
        query = "DELETE FROM categories WHERE id = %(id)s"
        connectToMySQL('businesses_ad_schema').query_db(query, data)

    @classmethod
    def update_category(cls, data):
        query = "UPDATE categories SET name = %(name)s, updated_at = NOW() WHERE id = %(id)s;"
        connectToMySQL(cls.db).query_db(query, data)

    # Validations
    @staticmethod
    def validate_creation(category):
            is_valid = True
            if len(category['name']) < 3:
                flash('Name of category hast be at least 3 characters!', 'category_error')
                is_valid = False
            return is_valid
    @classmethod
    def is_title_unique(cls,data):
        query = "SELECT id FROM categories WHERE name = %(name)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        return not result 
    
    @classmethod
    def is_title_unique_for_update(cls,data):
        query = "SELECT id FROM categories WHERE name = %(name)s AND id != %(id)s"
        result = connectToMySQL(cls.db).query_db(query,data)
        return not result 
    @classmethod
    def is_category_listed_for_business(cls,data):
        query = "SELECT id FROM businesses WHERE category_id = %(id)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        print('result')
        return bool(result)  


