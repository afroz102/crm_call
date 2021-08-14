import datetime
from django.utils import timezone
from django.conf import settings

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from .models import GmailCredential


# Improve order and space(In future)
def sortQueryObj(listObj, sortedIndexArr):
    # print(listObj)
    # print(sortedIndexArr)
    newListObj = []
    for index in sortedIndexArr:
        for obj in listObj:
            if int(index) == obj.id:
                newListObj.append(obj)

    # print(newListObj)
    return newListObj


# def save_credentials(user, credentials, valid=True):
#     try:
#         creds = GmailCredentials.objects.get(user=user)
#     except GmailCredentials.DoesNotExist:
#         creds = GmailCredentials.objects.create_credentials(
#             user,
#             credentials,
#             valid=valid
#         )
#
#     creds.save()
#     return creds


def load_credentials(user, ignore_valid=False):
    try:
        creds = GmailCredential.objects.get(user=user)
    except:
        # if something goes wrong here, we want to just raise the error
        # and pass it to the calling function.
        # yes, this is proper syntax! (don't want to lose the stack     trace)
        raise
    # is it valid? do we raise an error?
    if not ignore_valid and not creds.valid:
        raise ValueError('Credentials are not valid.')
    # ok, if we get to here we load/create the Credentials obj()
    # temp = json.loads(creds.json_string)
    credentials = Credentials(
        creds.token,
        refresh_token=creds.refresh_token,
        id_token=creds.id_token,
        token_uri=creds.token_uri,
        client_id=settings.GMAIL_CLIENT_ID,
        client_secret=settings.GMAIL_CLIENT_SECRET,
        scopes=creds.scopes.split(','),
    )
    expiry = creds.expiry.replace(tzinfo=None)
    # expiry_datetime = datetime.datetime.strptime(expiry,'%Y-%m-%d %H:%M:%S')
    print("expiry: ", expiry)
    credentials.expiry = expiry

    # And now we refresh the token
    # but not if we know that its not a valid token.

    if creds.valid:
        request = Request()
        if credentials.expired:
            credentials.refresh(request)
    # and finally, we return this whole deal

    if ignore_valid:
        return (credentials, creds.valid)
    else:
        return credentials
