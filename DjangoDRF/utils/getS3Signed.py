import boto3

s3 = boto3.client( 's3',
                   aws_access_key_id='AKIATSF6SDROSKWO5XEE',
                   aws_secret_access_key='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' )

url = s3.generate_presigned_url(
    ClientMethod='get_object',
    Params={
        'Bucket': 'djangoapi',
        'Key': 'media/songs/Vishal_kumar.pdf'
    }
)
print( "url:", url )
