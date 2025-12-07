from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField, SelectField, BooleanField, DateTimeLocalField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, URL

class RegisterForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired(), Length(max=120)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=180)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=128)])
    confirm = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Create account")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign in")

class FriendForm(FlaskForm):
    full_name = StringField("Full Name", validators=[DataRequired(), Length(max=120)])
    nickname = StringField("Nickname", validators=[Optional(), Length(max=80)])
    relationship = StringField("Relationship", validators=[Optional(), Length(max=80)])
    timezone = StringField("Timezone", validators=[Optional(), Length(max=64)])
    birth_date = DateField("Birth Date", validators=[DataRequired()], format="%Y-%m-%d")
    photo_url = StringField("Photo URL", validators=[Optional(), URL(), Length(max=500)])
    notes = TextAreaField("Notes / Memories", validators=[Optional(), Length(max=2000)])
    submit = SubmitField("Save")

class TemplateForm(FlaskForm):
    title = StringField("Template Title", validators=[DataRequired(), Length(max=120)])
    tone = SelectField("Tone", choices=[
        ("warm", "Warm"),
        ("funny", "Funny"),
        ("formal", "Formal"),
        ("emotional", "Emotional")
    ], validators=[DataRequired()])
    body = TextAreaField("Template Body", validators=[DataRequired(), Length(max=2000)])
    submit = SubmitField("Save Template")

class WishForm(FlaskForm):
    title = StringField("Wish Title", validators=[DataRequired(), Length(max=120)])
    tone = SelectField("Tone", choices=[
        ("warm", "Warm"),
        ("funny", "Funny"),
        ("formal", "Formal"),
        ("emotional", "Emotional")
    ], validators=[DataRequired()])
    body = TextAreaField("Wish Message", validators=[DataRequired(), Length(max=3000)])
    image_url = StringField("Image / GIF URL (optional)", validators=[Optional(), URL(), Length(max=500)])

    is_time_capsule = BooleanField("Time Capsule (unlock on birthday)")
    scheduled_for = DateTimeLocalField("Schedule for (optional)", validators=[Optional()], format="%Y-%m-%dT%H:%M")

    submit = SubmitField("Save Wish")

class GroupCardForm(FlaskForm):
    title = StringField("Card Title", validators=[DataRequired(), Length(max=140)])
    description = TextAreaField("Description", validators=[Optional(), Length(max=2000)])
    theme = SelectField("Theme", choices=[
        ("cloud", "Cloud"),
        ("minimal", "Minimal"),
        ("retro", "Retro"),
        ("party", "Party")
    ], validators=[DataRequired()])
    is_locked_until_bday = BooleanField("Lock until birthday")

    submit = SubmitField("Create Card")

class ContributionForm(FlaskForm):
    author_name = StringField("Your Name", validators=[DataRequired(), Length(max=120)])
    message = TextAreaField("Your Wish", validators=[DataRequired(), Length(max=2000)])
    reaction = SelectField("Reaction (optional)", choices=[
        ("", "No reaction"),
        ("❤️", "❤️ Love"),
        ("😂", "😂 Funny"),
        ("😭", "😭 Emotional"),
        ("🎉", "🎉 Party"),
        ("🌟", "🌟 Star")
    ], validators=[Optional()])
    submit = SubmitField("Add to Card")
