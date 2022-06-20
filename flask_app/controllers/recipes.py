from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, recipe


#Create 
@app.route('/create/recipe', methods = ['POST', 'GET'])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if 'user_id' in session:
        if request.method == 'GET':
            return render_template('create_recipe.html')
        if recipe.Recipe.create_recipe(request.form):
            return redirect('/user/profile')
    return redirect('/create/recipe')

#Read 
@app.route('/view/recipe/<int:id>')
def view_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    this_recipe = recipe.Recipe.view_recipe_by_id(id)
    return render_template('view_recipe.html', this_recipe = this_recipe)


#Update 
@app.route('/edit/recipe/<int:id>', methods = ['POST', 'GET'])
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if 'user_id' in session:
        if request.method == 'GET':
            this_recipe = recipe.Recipe.view_recipe_by_id(id)
            return render_template('edit_recipe.html', this_recipe = this_recipe)
        if recipe.Recipe.edit_recipe_by_id(request.form) == False:
            return redirect(f'/edit/recipe/{id}')
        else:
            recipe.Recipe.edit_recipe_by_id(request.form)
            return redirect('/user/profile')
    return redirect('/user/profile')


#Delete 
@app.route('/delete/recipe/<int:id>')
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    recipe.Recipe.delete_recipe_by_id(id)
    return redirect('/user/profile')



#