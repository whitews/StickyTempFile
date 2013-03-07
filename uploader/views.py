from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from uploader.models import *
from uploader.forms import *


def view_files(request):

    files = UploadedFile.objects.all()

    return render_to_response(
        'view_files.html',
        {
            'files': files,
        },
        context_instance=RequestContext(request)
    )


def add_file(request):

    if request.method == 'POST':
        form = UploadedFileForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('view_files'))
    else:
        form = UploadedFileForm()

    return render_to_response(
        'add_file.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )
