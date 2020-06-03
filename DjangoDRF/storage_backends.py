from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public'  # for private access
    file_overwrite = False