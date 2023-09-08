from django import forms
from django.forms import FileInput,Textarea,NumberInput,TextInput
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
                                       PasswordChangeForm, User)
from froala_editor.widgets import FroalaEditor

from . import models
class PostForm(forms.ModelForm):
    description_rus = forms.CharField(widget=FroalaEditor,label='Описание (русский)')
    description_arm = forms.CharField(widget=FroalaEditor,label='Описание (армянский)')
    description_eng = forms.CharField(widget=FroalaEditor,label='Описание (английский)')
    avatar_p = forms.FileField(
        label='Добавите главное изоброжение',
        widget=forms.FileInput(attrs={'id': 'file_inp'})
    )
    
    
    


    class Meta:
        model = models.Blog
        fields = ('description_arm','description_rus','description_eng','avatar_p')

class aboutform(forms.ModelForm):
    description = forms.CharField(widget=FroalaEditor,label='Описание (русский)')
    description_am = forms.CharField(widget=FroalaEditor,label='Описание (армянский)')
    description_en = forms.CharField(widget=FroalaEditor,label='Описание (английский)')
    class Meta:
        model = models.about_us
        fields = ('description_am','description','description_en')
class delivery_infoform(forms.ModelForm):
    description = forms.CharField(widget=FroalaEditor,label='Описание (русский)')
    description_am = forms.CharField(widget=FroalaEditor,label='Описание (армянский)')
    description_en = forms.CharField(widget=FroalaEditor,label='Описание (английский)')
    class Meta:
        model = models.delivery_info
        fields = ('description_am','description','description_en')
class rulesform(forms.ModelForm):
    description = forms.CharField(widget=FroalaEditor,label='Описание (русский)')
    description_am = forms.CharField(widget=FroalaEditor,label='Описание (армянский)')
    description_en = forms.CharField(widget=FroalaEditor,label='Описание (английский)')
    class Meta:
        model = models.rules
        fields = ('description_am','description','description_en')
    


class UserRegistrationForm(UserCreationForm):
    

    class Meta:
        model = User
        fields = ('username', 'password1')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password2']    






         