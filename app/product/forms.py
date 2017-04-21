from flask_wtf import Form
from wtforms import TextAreaField, StringField, SubmitField  # FileField
from wtforms.validators import DataRequired, Length
from app import product


class ProductForm(Form):
    """Add product form structure"""
    product_name = StringField("Name: ", validators=[DataRequired("Please enter the product name."), Length(min=3, max=70, message="Store name should be more than 3 characters long and less than 70")])
    product_desc = TextAreaField("Description: ", validators=[Length(min=1, message="Description is too short")])
    # product_img = FileField("Product Image: ")
    submit = SubmitField("Add Product")
