from rest_framework import serializers

from uploader.models import *


class UploadedFileSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='uploadedfile-detail')

    class Meta:
        model = UploadedFile
        fields = ('id', 'url', 'original_filename', 'sha1', 'date_uploaded')
        read_only_fields = ('original_filename', 'sha1', 'date_uploaded')


class UploadedFilePOSTSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='uploadedfile-detail')

    class Meta:
        model = UploadedFile
        fields = (
            'id', 'url', 'original_filename', 'sha1', 'uploaded_file', 'date_uploaded'
        )
        read_only_fields = ('original_filename', 'sha1', 'date_uploaded')
