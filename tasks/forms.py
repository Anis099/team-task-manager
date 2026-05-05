from django import forms
from .models import Project, Task

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']

class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'placeholder': 'DD-MM-YYYY'}),
        input_formats=['%d-%m-%Y'],
        required=False
    )

    class Meta:
        model = Task
        fields = ['title', 'assigned_to', 'status', 'due_date']