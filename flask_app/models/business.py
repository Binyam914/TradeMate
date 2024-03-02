from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

class Business: 
    db = "businesses_ad_schema"  # change it your DB name

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.link = data['link']
        self.state = data['state']
        self.city = data['city']
        self.phone_number = data['phone_number']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['id']
        self.category_id = data['category_id']

    @classmethod
    def get_businesses_by_user(cls, data):
        query = '''
            SELECT * FROM businesses
            WHERE user_id = %(user_id)s
        '''
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def create(cls, data):
        query = "INSERT INTO businesses(name, description, link, state, city, phone_number, updated_at, created_at, user_id, category_id) VALUES (%(name)s, %(description)s, %(link)s, %(state)s, %(city)s, %(phone_number)s, NULL, NOW(), %(user_id)s, %(category_id)s);"

        business = connectToMySQL(cls.db).query_db(query, data)
        return business

    @classmethod
    def get_all(cls, data):
        query = '''
            SELECT b.*, COUNT(l.business_id) AS like_count,
            MAX(CASE WHEN l.user_id = %(user_id)s THEN 1 ELSE 0 END) AS user_voted
            FROM businesses b
            LEFT JOIN likes l ON b.id = l.business_id
            GROUP BY b.id
        '''
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def get_one(cls, data):
        query = """
            SELECT businesses.*, users.first_name AS creator_name
            FROM businesses
            JOIN users ON businesses.user_id = users.id
            WHERE businesses.id = %(id)s
        """

        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            return result[0] 
        else:
            return None

    @classmethod
    def get_one_with_like(cls, data):
        print(data,'some place to be')
        query = """
            SELECT businesses.*, users.first_name AS creator_name,
            (SELECT COUNT(*) FROM likes WHERE likes.user_id = %(user_id)s AND likes.business_id = businesses.id) AS user_voted
            FROM businesses
            JOIN users ON businesses.user_id = users.id
            WHERE businesses.id = %(id)s
        """
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            business_data = result[0]
            business_data['user_voted'] = business_data['user_voted'] > 0
            return business_data
        else:
            return None

    @classmethod
    def delete(cls, data):
        delete_likes_query = "DELETE FROM likes WHERE business_id = %(id)s"
        connectToMySQL(cls.db).query_db(delete_likes_query, data)

        delete_business_query = "DELETE FROM businesses WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(delete_business_query, data)
        
        return results

    @classmethod
    def like(cls, data):
        vote = "INSERT INTO likes (user_id, business_id, created_at) VALUES (%(user_id)s, %(id)s, NOW())"
        connectToMySQL(cls.db).query_db(vote, data)
        return vote

    @classmethod
    def remove_like(cls, data):
        query = "DELETE FROM likes WHERE user_id = %(user_id)s AND business_id = %(id)s"
        connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update_business(cls, data):
        print('dance:',data)
        query = "UPDATE businesses SET name = %(name)s, description = %(description)s, link = %(link)s, state = %(state)s, city = %(city)s,  phone_number = %(phone_number)s, updated_at = NOW() WHERE id = %(id)s;"
        business = connectToMySQL(cls.db).query_db(query, data)
        return business

    @staticmethod
    def validate_creation(business):
        is_valid = True
        if len(business['name']) < 2:
            flash('Name must be at least 2 characters', 'create_error')
            is_valid = False
        if len(business['description']) < 3:
            flash('Description must be at least 3 characters', 'create_error')
            is_valid = False
        if len(business['link']) < 3:
            flash('Link must be at least 3 characters', 'create_error')
        if len(business['state']) < 3:
            flash('State must be at least 3 characters', 'create_error')
        if len(business['city']) < 3:
            flash('City must be at least 3 characters', 'create_error')
        if len(business['phone_number']) < 10:
            flash('Phone number must be at least 10 characters', 'create_error')
            is_valid = False
        return is_valid
     


    @classmethod
    def is_field_unique(cls, field_name, field_value):
        query = f"SELECT id FROM businesses WHERE {field_name} = %({field_name})s"
        data = {field_name: field_value}
        result = connectToMySQL(cls.db).query_db(query, data)
        return not result
    @classmethod
    def is_field_unique_for_update(cls, field_name, field_value, business_id):
        query = f"SELECT id FROM businesses WHERE {field_name} = %({field_name})s AND id != %(id)s"
        data = {field_name: field_value, 'id': business_id}
        result = connectToMySQL(cls.db).query_db(query, data)
        return not result
    @classmethod
    def is_field_unique_for_update(cls, field_name, field_value, business_id):
        query = f"SELECT id FROM businesses WHERE {field_name} = %({field_name})s AND id != %(id)s"
        data = {field_name: field_value, 'id': business_id}
        result = connectToMySQL(cls.db).query_db(query, data)
        return not result
