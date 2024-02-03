from django import forms

from blog.models import Article


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.ChoiceField):
                field.widget.attrs['class'] = 'form-select'
            elif isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ArticleForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'content', 'preview', 'is_published',)
