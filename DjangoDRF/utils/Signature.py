import hashlib

import requests
from aws_request_signer import AwsRequestSigner

AWS_REGION = "eu-west-1"
AWS_ACCESS_KEY_ID = "AKIAVPFRGEIV3NFYX55C"
AWS_SECRET_ACCESS_KEY = "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"

URL = "https://api-gw-staging.telkomsdp.com/billing/ad-hoc"

# Demo content for our target file.
content = '{"svc_id":"43","billing_rate":"200","channel":"WAP","doi_channel":"SMS","msisdn":"27614047726","ext_ref":"123455667"}'

content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()

# Create a request signer instance.
request_signer = AwsRequestSigner(
    AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, "execute-api"
)

# The headers we'll provide and want to sign.
headers = {
            "accept": "application/vnd.sdp+json;version=1.*",
            # "Content-Length": str(len(content)),
          }

# Add the authentication headers.
headers.update(
    request_signer.sign_with_headers("POST", URL, headers, content_hash)
)

print("Authorization:", headers.get('Authorization'))
print("x-amz-date:", headers.get('x-amz-date'))
# Make the request.

# resp = requests.post(URL, headers=headers, data=content)
# print("resp:", resp.status_code)
# print("resp:", resp.text)
#r.raise_for_status()

