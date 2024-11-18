from mongoengine import Document, StringField, ReferenceField
from blog_app.users.models import User

class Post(Document):
    title = StringField(required=True)
    content = StringField(required=True)
    user_id = StringField(required=True)  # Store the user ID as a string
