from django import forms
from apps.accounts.models import CustomUser, Skill

class UserSignupForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Create a password',
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm password',
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none'
        })
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'full_name', 'school', 'department', 'whatsapp']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Choose a username (e.g. john_doe)',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email address',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none'
            }),
            'full_name': forms.TextInput(attrs={
                'placeholder': 'Enter your full name',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none'
            }),
            'school': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg bg-white focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none'
            }),
            'department': forms.TextInput(attrs={
                'placeholder': 'e.g. Computer Science',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none'
            }),
            'whatsapp': forms.TextInput(attrs={
                'placeholder': 'e.g. 2348012345678',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none'
            }),
        }

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords don't match")
        if p1 and len(p1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ProfileEditForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = CustomUser
        fields = ['full_name', 'bio', 'school', 'department', 'whatsapp', 'profile_image', 'availability_status']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none'}),
            'bio': forms.Textarea(attrs={'rows': 3, 'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none'}),
            'school': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg bg-white'}),
            'department': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none'}),
            'whatsapp': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none'}),
            'availability_status': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg bg-white'}),
            'profile_image': forms.FileInput(attrs={'class': 'w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100'}),
        }