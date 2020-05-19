from .extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

topics_results_m2m_table = db.Table(
'topics_results_m2m_table',
db.Column('topic_id', db.Integer, db.ForeignKey('topic.id')),
db.Column('results_id', db.Integer, db.ForeignKey('results.id'))
)

'''  
    Set up the user database. 
    The database will store the students id, username, password. 

'''
#set up user database 

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    admin = db.Column(db.Boolean)
    student = db.Column(db.Boolean)
    enabled = db.Column(db.Boolean)

    results = db.relationship('Results', backref='user_results')

    def is_admin(self):
        return self.admin

    @property
    def unhashed_password(self):
        raise AttributeError('Cannot view unhashed password')

    @unhashed_password.setter
    def unhashed_password(self, unhashed_password):
        self.password = generate_password_hash(unhashed_password)



#Set up database for the subject 

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    questions = db.Column(db.Text(30))
    enabled = db.Column(db.Boolean)

    results = db.relationship(
    'Results',
    secondary = topics_results_m2m_table,
    backref = 'topicResults'
    )

#Set up Database to store the results 

class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    result_of_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    result_for_topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))