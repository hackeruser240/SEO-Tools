from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired,ValidationError, Length


class SearchResults(FlaskForm):
    keyword=StringField("Enter a keyword",validators=[DataRequired()])
    url=StringField("Enter a url",validators=[DataRequired()])
    enter=SubmitField("Submit")
class Broken_Link_Form(FlaskForm):
    url=StringField("Enter Url",validators=[DataRequired()])
    enter=SubmitField("Submit")


class Article_Rewriter(FlaskForm):
    paragraph=TextAreaField("Enter your Content Here",validators=[DataRequired()])

class SearchForm(FlaskForm):
    searchbar=StringField('Search Bar',validators=[DataRequired(),Length(min=2,max=50)])
    submit=SubmitField('Submit')

class Keyword_Density_Form(FlaskForm):
    url=StringField("Enter Url",render_kw={"placeholder": "https://seomasterz.com"})
    paragraph=TextAreaField("Enter your Content Here",render_kw={"placeholder": "Enter Your Content Here"})
    enter=SubmitField("Submit")


class Trends_Form(FlaskForm):
    keyword=StringField("Enter a Keyword",validators=[DataRequired()])
    enter=SubmitField("Submit")


class Ip_Address_Form(FlaskForm):
    url=StringField("Enter Url",validators=[DataRequired()])
    enter=SubmitField("Submit")

class Robots_Txt_Form(FlaskForm):
    xml=StringField("Enter A URL To Sitemap",render_kw={"placeholder": "If you do not have sitemap URL, create one"})
    disallow0=StringField("Enter a directory that you would not allow to be craweled",render_kw={"placeholder": "/admin"})
    disallow=StringField("Enter a directory that you would not allow to be craweled")
    disallow1=StringField("Enter a directory that you would not allow to be craweled")
    disallow2=StringField("Enter a directory that you would not allow to be craweled")