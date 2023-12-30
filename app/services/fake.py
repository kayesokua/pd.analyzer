from sqlalchemy.exc import IntegrityError
from faker import Faker
from .. import db
from ..models.base import User, Post
from random import choice

def users(count=10):
    fake = Faker()
    i = 0
    while i < count:
        u = User(email=fake.email(),
                 username=fake.user_name(),
                 password='password',
                 confirmed=True,
                 name=fake.name(),
                 location=fake.city(),
                 about_me=fake.text(),
                 member_since=fake.past_date())
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()

def posts(count=30):
    fake = Faker()
    user_ids = [user.id for user in User.query.with_entities(User.id).all()]
    
    for _ in range(count):
        random_user_id = choice(user_ids)
        user = User.query.get(random_user_id)
        timestamp = fake.past_date(start_date="-30d", tzinfo=None)
        
        post = Post(
            title=fake.sentence(),
            body=fake.text(),
            body_html=fake.text(),
            video_url="default1.mp4",
            video_timestamp=timestamp,
            upload_timestamp=timestamp,
            last_updated_on=timestamp,
            author=user
        )
        db.session.add(post)
    db.session.commit()

    for post in Post.query.order_by(Post.id.desc()).limit(count).all():
        post.processed_data_dir = f"data/processed/{post.author.id}/{post.id}/"
        db.session.add(post)
    db.session.commit()