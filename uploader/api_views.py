from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

from uploader.models import *
from uploader.serializers import *


@api_view(['GET'])
def api_root(request, format=None):
    """
    The entry endpoint of our API.
    """

    return Response({
        'files': reverse('uploadedfile-list', request=request),
    })


class UploadedFileList(generics.ListCreateAPIView):
    """
    API endpoint representing a list of files.
    """

    model = UploadedFile
    serializer_class = UploadedFileSerializer
    filter_fields = ('original_filename',)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UploadedFilePOSTSerializer

        return super(UploadedFileList, self).get_serializer_class()

    def post(self, request, *args, **kwargs):
        response = super(UploadedFileList, self).post(request, *args, **kwargs)
        # don't give back the sample_file field containing the file path on the server
        if 'uploaded_file' in response.data:
            del (response.data['uploaded_file'])
        return response


class UploadedFileDetail(generics.RetrieveAPIView):
    """
    API endpoint representing a single uploaded file.
    """

    model = UploadedFile
    serializer_class = UploadedFileSerializer
