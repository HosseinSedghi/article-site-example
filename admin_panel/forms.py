from django import forms

from article_module.models import ArticleCategory


class ArticleCreateEditForm(forms.Form):
    title = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'عنوان مقاله'
        }),
        error_messages={
            'required': 'این فیلد الزامی است'
        }
    )
    slug = forms.SlugField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'اسلاگ مقاله'
        }),
        error_messages={
            'required': 'این فیلد الزامی است'
        }
    )
    image = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'placeholder': 'عنوان مقاله'
        }),
        error_messages={
            'required': 'این فیلد الزامی است'
        }
    )
    category = forms.ModelChoiceField(
        required=True,
        queryset=ArticleCategory.objects.all(),
        widget=forms.SelectMultiple(
            attrs={
            'class': 'form-control',
            'placeholder': 'عنوان مقاله'
        }),
        error_messages={
            'required': 'این فیلد الزامی است'
        }
    )
    is_special = forms.CharField(
        required=True,
        label='آیا این مقاله برای اعضای ویژه است؟',
        widget=forms.CheckboxInput(),
        error_messages={
            'required': 'این فیلد الزامی است'
        }
    )
    text = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'متن اصلی مقاله'
        }),
        error_messages={
            'required': 'این فیلد الزامی است'
        }
    )


class CategoryCreateEditForm(forms.ModelForm):
    class Meta:
        model = ArticleCategory
        fields = '__all__'
        widgets={
            'is_active': forms.CheckboxInput()
        }
        labels={
            'is_active': 'فعال یا غیر فعال'
        }
    title = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'عنوان دسته بندی'
        }),
        error_messages={
            'required': 'این فیلد الزامی است'
        }
    )
    slug = forms.SlugField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'اسلاگ دسته بندی'
        }),
        error_messages={
            'required': 'این فیلد الزامی است'
        }
    )
    parent = forms.ModelChoiceField(
        required=False,
        queryset=ArticleCategory.objects.all(),
        widget=forms.Select(
            attrs={
            'class': 'form-control',
            'placeholder': 'عنوان دسته بندی'
        }),
        error_messages={
            'required': 'این فیلد الزامی است'
        }
    )


class ChangePasswordForm(forms.Form):
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'گذرواژه'
        }),
        error_messages={
            'required': 'این فیلد الزامی است'
        }
    )
    new_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'گذرواژه جدید'
        }),
        error_messages={
            'required': 'این فیلد الزامی است'
        }
    )
    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'تکرار گذرواژه جدید'
        }),
        error_messages={
            'required': 'این فیلد الزامی است'
        }
    )

