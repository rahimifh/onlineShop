from contact.models import Contact


def context_processors(request):
    contacts = Contact.objects.last()
    return {'contacts': contacts}