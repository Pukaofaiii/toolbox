from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django import forms
from .models import Member
from .models import *

class StaffRegistrationForm(forms.Form):
    username = forms.CharField(label='ชื่อผู้ใช้', max_length=150)
    first_name = forms.CharField(label='ชื่อจริง', max_length=150)
    last_name = forms.CharField(label='นามสกุล', max_length=150)
    email = forms.EmailField(label='อีเมล')
    phone_number = forms.CharField(label='เบอร์โทรศัพท์', max_length=15)
    password1 = forms.CharField(label='รหัสผ่าน', widget=forms.PasswordInput)
    password2 = forms.CharField(label='ยืนยันรหัสผ่าน', widget=forms.PasswordInput)
    is_admin = forms.BooleanField(label='เป็นผู้ดูแลระบบ', required=False)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('ชื่อผู้ใช้นี้ถูกใช้งานแล้ว')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('อีเมลนี้ถูกใช้งานแล้ว')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'รหัสผ่านไม่ตรงกัน')

        return cleaned_data


class MemberRegistrationForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'id_card', 'birth_date', 'gender', 'weight', 'height', 'phone_number']

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input mt-1 block w-full rounded-md border-yellow-500 p-3 shadow-md  focus:border-blue-500 focus:ring-blue-300 sm:text-sm',
            'placeholder': 'ชื่อ'
        }),
        label="ชื่อ",
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input mt-1 block w-full rounded-md border-orange-500 p-3 shadow-md  focus:border-blue-500 focus:ring-blue-300 sm:text-sm',
            'placeholder': 'นามสกุล'
        }),
        label="นามสกุล",
    )

    id_card = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^\d{13}$',
                message="รหัสบัตรประชาชนต้องเป็นตัวเลข 13 หลัก",
                code="invalid_id_card"
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-input mt-1 block w-full rounded-md border-orange-500 p-3 shadow-md  focus:border-blue-500 focus:ring-blue-300 sm:text-sm',
            'placeholder': 'รหัสบัตรประชาชน',
            'maxlength': '13'
        }),
        label="รหัสบัตรประชาชน",
    )

    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-input mt-1 block w-full rounded-md border-orange-500 p-3 shadow-md  focus:border-blue-500 focus:ring-blue-300 sm:text-sm',
            'type': 'date'
        }),
        label="วันเดือนปีเกิด",
    )

    gender = forms.ChoiceField(
        choices=Member.GENDER_CHOICES,  # Match model choices
        widget=forms.Select(attrs={
            'class': 'form-select mt-1 block w-full rounded-md border-orange-500 p-3 shadow-sm focus:border-blue-500 focus:ring-blue-300 sm:text-sm'
        }),
        label="เพศ",
    )

    weight = forms.FloatField(
        widget=forms.NumberInput(attrs={
            'class': 'form-input mt-1 block w-full rounded-md border-orange-500 p-3 shadow-md  focus:border-blue-500 focus:ring-blue-300 sm:text-sm',
            'placeholder': 'น้ำหนัก (กก.)'
        }),
        label="น้ำหนัก (กก.)",
    )

    height = forms.FloatField(
        widget=forms.NumberInput(attrs={
            'class': 'form-input mt-1 block w-full rounded-md border-orange-500 p-3 shadow-md  focus:border-blue-500 focus:ring-blue-300 sm:text-sm',
            'placeholder': 'ส่วนสูง (ซม.)'
        }),
        label="ส่วนสูง (ซม.)",
    )

    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input mt-1 block w-full rounded-md border-orange-500 p-3 shadow-md  focus:border-blue-500 focus:ring-blue-300 sm:text-sm',
            'placeholder': 'เบอร์โทรศัพท์',
            'maxlength': '15'
        }),
        label="เบอร์โทรศัพท์",
    )
