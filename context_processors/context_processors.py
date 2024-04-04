from contact.models import Contact


def context_processors(request):
    contact = Contact.objects.last()
    return {'contact': contact}
