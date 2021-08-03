from django.forms import ModelForm
from ideas.models import *

class NewUser_ModelForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'phone',
            'birthdate',
            'password',
            'image'
        ]

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(NewUser_ModelForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UpdateUser_ModelForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name',
        'last_name',
        'username',
        'email',
        'phone',
        'birthdate',
        'image'
        ]

class NewRequest_ModelForm(ModelForm):
    class Meta:
        model = Request
        fields = [
            'title',
            'category',
            'definition',
            'something_else',
            'goal',
            'restrictions',
            'context',
            'offer_value',
            'requester'
        ]

class NewIdea_ModelForm(ModelForm):
    class Meta:
        model = Idea
        fields = [
            'idea_title',
            'idea_request',
            'idealist',
            'content',
            'attachments',
            'share_value'
        ]