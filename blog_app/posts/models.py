from mongoengine import Document, StringField, ReferenceField, DateTimeField
from datetime import datetime, timezone

class Post(Document):
    title = StringField(required=True)
    content = StringField(required=True)
    user_id = StringField(required=True)  
    created_at = DateTimeField(default=datetime.now(timezone.utc))