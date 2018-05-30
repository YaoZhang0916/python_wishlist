from __future__ import unicode_literals
from django.db import models
import bcrypt, re
from datetime import datetime

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register(self, postData):
        errors={}
        if len(postData["first_name"])<2:
            errors["first_name"] = "First name should be more than 2 characters"
        if len(postData["last_name"])<2:
            errors["last_name"] = "Last name should be more than 2 characters"
        if not email_regex.match(postData['email']):
            errors["email"]='Not a valid email'

        if len(postData['email']) == 0:
            errors["noEmail"]='Please enter an email'

        if len(postData['password']) <7:
            errors["lengthPsw"]= 'Password at least 8 characters'

        if postData['password'] != postData['confirm']:
            errors["password"]='Passwords do not match'

        if postData["hire_date"]:
            if datetime.now() <= datetime.strptime(postData["hire_date"], '%Y-%m-%d'):
                errors["date"] = "Hired date must be past day"
        else:# len(postData["hire_date"])==0:
            errors["hire_date"]="Please enter hired data"

        checkemail = User.objects.filter(email=postData['email'])

        if checkemail:
            errors["checkemail"]="This email is used"

        if errors:
            return errors
        else:
            return errors
            # pwHash = bcrypt.hashpw(input['password'].encode(), bcrypt.gensalt().encode())
            # user = User.objects.create(first_name=postData['first_name'], last_name=postData['last_name'],
            #                            email=postData['email'], password=pwHash)

    def login(self, postData):
        errors = {}
        user = User.objects.filter(email=postData['email'])
        if user.exists():
            InputPw = postData['password'].encode()
            HashPw = user[0].password.encode()

            if bcrypt.checkpw(InputPw, HashPw):
                return errors
            else:
                errors["existEmail"]="Email or password doesn't exist!"
                return errors
        else:
            errors["noExistEmail"]="Email or password doesn't exist!"
        return errors

class JointManager(models.Manager):
    def join(self, user_id, wishlist_id):
        this_user = User.objects.get(id=user_id)
        this_wish = WishList.objects.get(id=wishlist_id)
        joint = Joint.jointManager.create(user=this_user, wishList=this_wish)
        return (joint)

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    hired_date = models.DateField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return self.first_name+" "+self.last_name

class WishList(models.Model):
    item = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.item


class Joint(models.Model):
    user = models.ForeignKey(User)
    wishlist = models.ForeignKey(WishList)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    jointManager = JointManager()
