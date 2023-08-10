from flask import Flask, request, jsonify
from  flask_restx import Namespace,Resource,fields
from models import*
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, \
jwt_required


recipe_ns = Namespace('receipe', description="A namespace for Recipes")

#model serializer, its helping to serialize our models
recipe_model = recipe_ns.model(
    "Recipe",
    {
        "id":fields.Integer(),
        "title":fields.String(),
        "description":fields.String()
    }
)




@recipe_ns.route('/hello')
class HelloResource(Resource):
    def get(self):
        return {"message":"Hello world"}








@recipe_ns.route('/recipes')
class RecipesResource(Resource):
    @recipe_ns.marshal_list_with(recipe_model)
    def get(self):
        """Get all recipes from the db
        
        Keyword arguments:
        argument -- description
        Return: return_description
        """
        recipes = Recipe.query.all()
        return recipes

    @recipe_ns.marshal_with(recipe_model)   #when returning one use marshal with, 
    @recipe_ns.expect(recipe_model)#tells the server what to expect from client
    #in otherwards the payload to expect to go to the server
    @jwt_required()
    def post(self):
        """Create a new recipe
        
        Keyword arguments:
        argument -- description
        Return: return_description
        """
        data = request.get_json() #helps us get data comig from any client
        new_recipe = Recipe(
            title = data.get('title'),
            description = data.get('description')
        )
        new_recipe.save() #==anabling us save to the db
        return new_recipe, 201

@recipe_ns.route('/recipe/<int:id>')
class RecipeResource(Resource):
    @recipe_ns.marshal_with(recipe_model)
    def get(self, id):
        """Get arecipe by id"""
        recipe = Recipe.query.get_or_404(id)
        return recipe
    
    @recipe_ns.marshal_with(recipe_model)
    @jwt_required()
    def put(self, id):
        """Update a recipe"""
        recipe_to_update=Recipe.query.get_or_404(id)
        data = request.get_json()
        recipe_to_update.update(data.get('title'), data.get('description'))
        return recipe_to_update
    
    @recipe_ns.marshal_with(recipe_model)
    @jwt_required()
    def delete(self, id):
        """delete a recipe by id"""
        recipe_to_delete=Recipe.query.get_or_404(id)
        recipe_to_delete.delete()
        return recipe_to_delete
