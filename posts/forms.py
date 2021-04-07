from django.forms import ModelForm, Textarea
from django.utils.translation import gettext_lazy as _

from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            'text',
            'group'
        ]
        widgets = {
            'text': Textarea(attrs={'placeholder': _('Что нового?')})
        }
