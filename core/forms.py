from django.forms import ModelForm
from .models import book, Topic, participant


class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = '__all__'
        labels = {
            'name': 'Topic name'
        }


class participantForm(ModelForm):
    class Meta:
        model = participant
        fields = '__all__'
        labels = {
            'name': 'Participant name'
        }


class bookForm(ModelForm):
    class Meta:
        model = book
        fields = '__all__'
        labels = {
            'host': 'Issuer',
            'name': 'book name',
            'desc': 'Description'
        }

    def __init__(self, *args, **kwargs):
        super(bookForm, self).__init__(*args, **kwargs)
        self.fields['host'].empty_label = "click here to select the Issuer"
