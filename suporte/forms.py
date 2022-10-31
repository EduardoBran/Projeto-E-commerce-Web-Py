from django import forms
from django.core.mail import EmailMessage


class ContatoForm(forms.Form):
    nome = forms.CharField(label="Nome", max_length=100)
    email = forms.EmailField(label="E-mail", max_length=100)
    assunto = forms.CharField(label="Assunto", max_length=100)
    mensagem = forms.CharField(label="Mensagem", widget=forms.Textarea())

    def send_email(self):
        nome = self.cleaned_data['nome']
        email = self.cleaned_data['email']
        assunto = self.cleaned_data['assunto']
        mensagem = self.cleaned_data['mensagem']

        corpo = f'Nome: {nome}\nEmail: {email}\nMensagem:{mensagem}'

        mail = EmailMessage(
            subject=assunto,
            from_email=email,
            to=['uniquestore.online2022@gmail.com', ],
            body=corpo,
            headers={
                'Replay-To': 'uniquestore.online2022@gmail.com'
            }
        )
        mail.send()
