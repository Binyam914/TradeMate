from flask import render_template, redirect, request, session, flash,url_for
from flask_app import app
from flask_app.models.category import Category
from flask_app.models.business import Business
from flask_app.models.user import User

# dashboard

@app.route('/my_businesses')
def show_my_businesses():
    if 'user_id' not in session:
        flash('You must be logged into view the dashboard!', 'log_error')
        return redirect('/')
    data = {
        'user_id': session['user_id']
    }
    user_data = {
        'id': session['user_id']
    }
    businesses=Business.get_businesses_by_user(data)
    user = User.get_user_by_id(user_data)
    return render_template('my_businesses.html', businesses=businesses,user=user)

@app.route('/dashboard')
def show_all_businesses():
    if 'user_id' not in session:
        flash('You must be logged into view the dashboard!', 'log_error')
        return redirect('/')
    data = {
        'user_id': session['user_id']
    }
    user_data = {
        'id': session['user_id']
    }    
    user = User.get_user_by_id(user_data)
    businesses = Business.get_all(data)  
    return render_template('dashboard.html', businesses=businesses, user=user)


@app.route('/add_business')
def add_business():
    if 'user_id' not in session:
        flash('You must be logged in to add a business!', 'log_error')
        return redirect('/')

    categories = Category.get_categories()

    # Check if categories are not found
    if not categories:
        flash('No categories found. Please create a category first before adding a business.', 'category_error')
        return redirect('/categories') 
    return render_template('add_business.html', categories=categories)
   
# # Details

@app.route('/business/<int:id>', methods=['GET', 'POST'])
def show(id):
    if 'user_id' not in session:
        flash('You must be logged into to have this accesses!', 'log_error')
        return redirect('/')
    user_id = session.get('user_id')
  
    data = {
        "id": id,
        "user_id": user_id
    }
    business = Business.get_one_with_like(data)
    return render_template('show_Business.html',business=business ,user_id=user_id)

#   Stretch Purchase

@app.route('/like/<int:id>', methods=['GET', 'POST'])
def like(id):
        user_id = session.get('user_id')
        if 'user_id' not in session:
            flash('You must be logged in to have access!', 'log_error')
            return redirect('/')
        if not user_id:
            return redirect('/login')  
        data = {
            "id":id,
            "user_id":user_id
        }
        Business.like(data)
        business = Business.get_one_with_like(data)
        print(business)
        
        return render_template('show_Business.html', business=business)

@app.route('/like_in_dashboard/<int:id>', methods=['GET', 'POST'])
def like_in_dashboard(id):
        user_id = session.get('user_id')
        if 'user_id' not in session:
            flash('You must be logged in to have access!', 'log_error')
            return redirect('/')
        if not user_id:
            return redirect('/login')
        data = {
            "id":id,
            "user_id":user_id,
        }
        user_data = {
        'id': session['user_id']
        }
        Business.like(data)
        user = User.get_user_by_id(user_data)
        businesses = Business.get_all(data) 
        return render_template('dashboard.html', businesses=businesses, user=user)
    
@app.route('/remove_like/<int:id>', methods=['GET', 'POST'])
def remove_like(id):
    if request.method == 'POST':
        user_id = session.get('user_id')
        if 'user_id' not in session:
            flash('You must be logged in to have access!', 'log_error')
            return redirect('/')
        if not user_id:
            return redirect('/login')
        data = {
            "id":id,
            "user_id":user_id
        }
        Business.remove_like(data)
        business = Business.get_one_with_like(data)
        return render_template('show_business.html', business=business)
    
@app.route('/remove_like_in_dashboard/<int:id>', methods=['GET', 'POST'])
def remove_like_in_dashboard(id):
        user_id = session.get('user_id')
        if 'user_id' not in session:
            flash('You must be logged in to have access!', 'log_error')
            return redirect('/')
        if not user_id:
            return redirect('/login')
        
        data = {
            "id":id,
            "user_id":user_id
        }
        user_data = {
        'id': session['user_id']
        }
        Business.remove_like(data)        
        user = User.get_user_by_id(user_data)
        businesses = Business.get_all(data)  
        return render_template('dashboard.html', businesses=businesses, user=user)

@app.route('/business/save', methods=["POST"])
def create_business():
    if 'user_id' not in session:
        flash('You must be logged in to have access!', 'log_error')
        return redirect('/')    
    form_data = request.form
    print('form_data:', form_data)

    
    if not Business.validate_creation(form_data):
        return redirect('/add_business')
    
    # Initialize an empty dictionary to collect errors
    errors = {}
    fields_to_check = ['name', 'phone_number', 'link']
    for field in fields_to_check:
        # Check if each field is unique
        if not Business.is_field_unique(field, form_data.get(field)):
            errors[field] = f'{field.capitalize()} must be unique'
    
    # If any errors are found, inform the user and redirect to the form
    if errors:
        # Iterate over all collected errors and flash them
        for field, error in errors.items():
            flash(error, 'create_error')
        return redirect('/add_business')
    
    # If all checks pass, create the business
    Business.create(form_data)
    return redirect('/dashboard')



@app.route('/business/update/save', methods=["POST"])
def update_business():
    if 'user_id' not in session:
        flash('You must be logged in to have access!', 'log_error')
        return redirect('/')    
    form_data = request.form
    if not Business.validate_creation(form_data):
        flash('Validation error occurred. Please check your input.', 'update_error')
        return redirect(request.referrer) 
    
    business_id = form_data.get('id')
    
    # Check uniqueness of title, phone_number, and link for update
    errors = {}
    fields_to_check = ['name', 'phone_number', 'link']
    for field in fields_to_check:
        if not Business.is_field_unique_for_update(field, form_data.get(field), business_id):
            errors[field] = f'{field.capitalize()} must be unique'
    
    # If any errors are found, inform the user and redirect back to the form
    if errors:
        for field, error in errors.items():
            flash(error, 'update_error')
        return redirect(request.referrer)
    
    # If all checks pass, update the business
    Business.update_business(form_data)
    return redirect('/my_businesses')

@app.route('/business/delete/<int:id>', methods=['GET', 'POST'])
def delete_business(id):
    # Check if the user is logged in
    if 'user_id' not in session:
        flash('You must be logged in to delete a business.', 'error')
        return redirect('/login')

    # Fetch the business
    data={
        'id':id
    }
    business = Business.get_one(data)

    # Check if the business exists
    if not business:
        flash('Business not found.', 'error')
        return redirect('/dashboard')

    # Check if the logged-in user is the creator of the business
    if business['user_id'] != session['user_id']:
        flash('You are not authorized to delete this business.', 'business_error')
        return redirect('/my_businesses')

    # Delete the business
    Business.delete(data)

    flash('Business successfully deleted.', 'success')
    return redirect('/my_businesses')

@app.route('/business/edit/<int:id>',methods=['GET', 'POST'])
def lets_update_business(id):
    user_id = session.get('user_id')
    data = {
    "id": id,
    "user_id": user_id
    }
    business = Business.get_one_with_like(data)
    categories=Category.get_categories()
    return render_template("update_business.html", business=business,categories=categories)


