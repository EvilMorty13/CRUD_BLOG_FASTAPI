from fastapi import APIRouter, Depends, HTTPException, status
from bson.objectid import ObjectId
from pymongo.collection import Collection


from blog_app.users.dependencies import get_current_user  # Import the shared function
from database import db
from blog_app.posts.schemas import PostSchema,PostDetailSchema
from blog_app.users.models import User



# Access the "posts" collection
posts_collection: Collection = db["posts"]

post_router = APIRouter(prefix="/posts", tags=["Posts"])

# Route to create a post
@post_router.post("/", response_model=PostSchema)
async def create_post(post: PostSchema, current_user: User = Depends(get_current_user)):
    """
    Create a new post by the authenticated user.
    """
    # Ensure that the current user is authenticated before creating a post
    post_data = {
        "title": post.title,
        "content": post.content,
        "user_id": str(current_user.id),  # Save the user ID as a string
    }
    result = posts_collection.insert_one(post_data)  # Save post to the database
    created_post = posts_collection.find_one({"_id": result.inserted_id})

    # Return the created post
    return {
        "id": str(created_post["_id"]),
        "title": created_post["title"],
        "content": created_post["content"],
        "user_id": created_post["user_id"],
    }

# Route to update a post
@post_router.put("/{post_id}/", response_model=PostSchema)
async def update_post(post_id: str, post: PostSchema, current_user: User = Depends(get_current_user)):
    """
    Update an existing post by its ID if the current user is the creator.
    """
    post_obj = posts_collection.find_one({"_id": ObjectId(post_id)})

    if not post_obj:
        raise HTTPException(status_code=404, detail="Post not found")

    if post_obj["user_id"] != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to update this post")

    posts_collection.update_one(
        {"_id": ObjectId(post_id)},
        {"$set": {"title": post.title, "content": post.content}},
    )
    updated_post = posts_collection.find_one({"_id": ObjectId(post_id)})

    # Return the updated post
    return {
        "id": str(updated_post["_id"]),
        "title": updated_post["title"],
        "content": updated_post["content"],
        "user_id": updated_post["user_id"],
    }

# Route to delete a post
@post_router.delete("/{post_id}/")
async def delete_post(post_id: str, current_user: User = Depends(get_current_user)):
    """
    Delete a post by its ID if the current user is the creator.
    """
    post_obj = posts_collection.find_one({"_id": ObjectId(post_id)})

    if not post_obj:
        raise HTTPException(status_code=404, detail="Post not found")

    if post_obj["user_id"] != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")

    posts_collection.delete_one({"_id": ObjectId(post_id)})

    return {"message": "Post deleted successfully"}

@post_router.get("/", response_model=list[PostDetailSchema])
async def all_posts():
    """
    Fetch all posts from the database.
    """
    all_posts = posts_collection.find()
    return [
        {
            "id": str(post["_id"]),
            "title": post["title"],
            "content": post["content"],
            "user_id": post["user_id"],
        }
        for post in all_posts
    ]


# Route to get all posts of the logged-in user
@post_router.get("/my_posts", response_model=list[PostDetailSchema])
async def my_posts(current_user: User = Depends(get_current_user)):
    """
    Fetch all posts created by the authenticated user.
    """
    user_posts = posts_collection.find({"user_id": str(current_user.id)})
    return [
        {
            "id": str(post["_id"]),
            "title": post["title"],
            "content": post["content"],
            "user_id": post["user_id"],
        }
        for post in user_posts
    ]