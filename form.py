from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, ValidationError
import re

class Form(FlaskForm):
    username = StringField('ユーザ名')
    password = PasswordField('パスワード')
    
    def validate_username(self, username):
        '''
        - 未入力 禁止
        - 文字数9文字以上 禁止
        - 「-」 禁止
        '''
        input_string = username.data
        
        if input_string is None:
            raise ValidationError('入力してください')
        
        input_string = input_string.strip()
        
        if input_string == '':
            raise ValidationError('入力してください')
        
        if len(input_string) > 8:
            raise ValidationError('値を8文字以内で入力してください')
        
        if '-' in username.data:
            raise ValidationError('「-」の入力は禁止されています')
    
    def validate_password(self, password):
        
        input_password = password.data
        pw_pat = re.compile("^[0-9a-zA-Z]+$")
        
        if input_password is None:
            raise ValidationError('入力してください')
        
        input_string = input_password.strip()
        
        if input_password == "":
            raise ValidationError('入力してください')

        if len(input_password) < 4 or len(input_password) > 10:
            raise ValidationError('4文字以上10文字以下で入力してください')

        if not pw_pat.match(input_password):
            raise ValidationError('使用できない文字が含まれています')