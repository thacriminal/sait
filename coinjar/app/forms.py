from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, login
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
UserModel = get_user_model()
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label = _("email"))
    first_name = forms.CharField(required=True,)
    last_name = forms.CharField(required=True,)
    def __init__(self, *args, **kwargs):
        super(RegisterForm,self).__init__(*args, **kwargs)
    class Meta:
        abstract = False
        swappable = True
        model = get_user_model()
        fields = ('first_name','email','password1','password2','last_name')
    def clean_email(self):
        email = self.cleaned_data["email"]
        users = get_user_model().objects.filter(email=email)
        if users:
            raise forms.ValidationError("This email already exist")
        return email.lower()