from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContactForm
from .models import ContactMessage


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '문의가 접수되었습니다. 빠르게 답변드리겠습니다.')
            return redirect('contact:contact')
    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form})


@staff_member_required
def inbox_view(request):
    inbox_messages = ContactMessage.objects.all()
    return render(request, 'contact/inbox.html', {'inbox_messages': inbox_messages})


@staff_member_required
def inbox_detail_view(request, pk):
    contact_message = get_object_or_404(ContactMessage, pk=pk)
    if not contact_message.is_read:
        contact_message.is_read = True
        contact_message.save(update_fields=['is_read'])
    return render(request, 'contact/inbox_detail.html', {'contact_message': contact_message})
