from flask import render_template, redirect,request, session, flash,url_for
from flask_app import app
from flask_app.models.category import Category
from flask_app.models.user import User


@app.route('/categories')
def categories():
    if 'user_id' not in session:
        flash('You must be logged in to add business!', 'log_error')
        return redirect('/')
    user_id = session.get('user_id')
    categories=Category.get_categories()
    return render_template('categories.html',categories=categories,user_id=user_id)

@app.route('/category/save', methods=["POST"])
def create_category():
    if 'user_id' not in session:
        flash('You must be logged into to have this accesses!', 'log_error')
        return redirect('/')    
    form_data = request.form
    if not Category.validate_creation(form_data):
        return redirect('/categories')

    if not Category.is_title_unique(form_data):
        flash('This category already exists!', 'category_error')
        return redirect('/categories')
    Category.create(form_data)
    return redirect('/categories')
@app.route('/category/update/save', methods=["POST"])
def update_category():
    if 'user_id' not in session:
        flash('You must be logged into to have this accesses!', 'log_error')
        return redirect('/')    
    form_data = request.form
    if not Category.validate_creation(form_data):
        return redirect(request.referrer) 
    if not Category.is_title_unique_for_update(form_data):
        form_data
        flash('This category already exists!', 'category_error')
        return redirect(request.referrer) 
    Category.update_category(form_data)
    return redirect('/categories')

@app.route('/category/edit/<int:id>', methods=['GET', 'POST'])
def lets_update_category(id):
    data = {
        'id':id
    }
    category = Category.get_one(data)  
    return render_template("update_category.html", category=category)

# @app.route('/category/delete/<int:id>', methods=['GET', 'POST'])
# def delete_category(id):
#     data = {"id": id}
#     if Category.is_category_listed_for_business(data):
#         flash('Cannot delete category.because other user used this category to list business!.', 'delete_error')
#     else:

#         Category.delete(data)
#         flash('Category successfully deleted.', 'success')
#     return redirect('/categories')
@app.route('/category/delete/<int:id>', methods=['GET', 'POST'])
def delete_category(id):
    data = {"id": id}
    
    # Assuming you have a user ID stored in the session
    if 'user_id' not in session:
        # User is not logged in, handle accordingly
        return redirect('/login')  # Redirect to login page or handle unauthorized access
        
    # Fetch the category by ID
    category_data = Category.get_one(data)
    
    # Assuming 'user_id' is a key in the dictionary returned by get_one
    if category_data['user_id'] != session['user_id']:
        # Current user is not the owner of the category
        flash('You are not authorized to delete this category.', 'category_error')
        return redirect('/categories')  # Redirect to categories page or handle unauthorized access
    
    if Category.is_category_listed_for_business(data):
        flash('Cannot delete category because other users used this category to list businesses!', 'category_error')
    else:
        Category.delete(data)
        flash('Category successfully deleted.', 'success')
        
    return redirect('/categories')

