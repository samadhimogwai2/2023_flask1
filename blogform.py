from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, ValidationError

class BlogForm(FlaskForm):
    title = StringField('タイトル')
    containt = TextAreaField('内容')
    
    def validate_title(self, title):

        input_string = input_string.strip()
        
        if input_string == '':
            raise ValidationError('タイトルを入力してください')
    
           
    def validate_containt(self, containt):

        if containt.data == '':
            raise ValidationError('内容が未入力です')
        