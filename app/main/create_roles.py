from app import db
from app.main.models import Role
from app.main.forms import EditProfileForm


def create_roles():
    choices = EditProfileForm.choices
    for i in range(len(choices)):
        role = Role(name=choices[i][1])
        db.session.add(role)

    db.session.commit()
