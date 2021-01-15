# 160chars

160chars is a basic Twitter implementation, more like a blog with 160 characters limitation per post.

**Limitations**:

 - No check for brute-force login attemps.
 - No account activation system, users can register and then login immediately.
 - No check for repeated forgot password requests. This can be used as a way to SPAM users.
 - Probably many more that I am not aware of.

## Database

An SQLite database is configured for development purposes. As SQLAlchemy and Alembic are included via Flask-SQLALchemy and Flask-Migrate, using any other database supported by SQLAlchemy can be used immediately with small configuration edits.

## Other Required Software

**ElasticSearch**:
For search, ElasticSearch is implemented but as search code is generic, any other system can implemented instead of ElasticSearch.

**Redis**:
Redis is used for task queues. Currently, only implementation is backup of user posts.

## Installation

Clone the repo:

    git clone https://github.com/aliayar/160chars
  
After creating a virtual environment, install the requirements:

    pip install -r requirements.txt

Run the application:

    flask run

## Disclaimer

This attempt is nowhere near finished. It can only be used as a base and several shortcomings should be fixed before production. However if it should be used, I would recommend hide the auth pages due to spammable nature in the current implementation.
