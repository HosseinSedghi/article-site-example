from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input100',
        }),
        error_messages={
            'required': 'this field is required'
        }
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'input100',
        }),
        error_messages={
            'required': 'this field is required'
        }
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'input100',
        }),
        error_messages={
            'required': 'این فیلد الزامی است'
        }
    )
    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'input100',
        }),
        error_messages={
            'required': 'این فیلد الزامی است'
        }
    )


class LoginForm(forms.Form):
    username = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input100',
        }),
        error_messages={
            'required': 'this field is required'
        }
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'input100',
        }),
        error_messages={
            'required': 'این فیلد الزامی است'
        }
    )


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'input100',
        }),
        error_messages={
            'required': 'این فیلد الزامی است'
        }
    )


class ChangePasswordForm(forms.Form):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'input100',
        }),
        error_messages={
            'required': 'این فیلد الزامی است'
        }
    )
    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'input100',
        }),
        error_messages={
            'required': 'این فیلد الزامی است'
        }
    )