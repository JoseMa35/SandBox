import sendgrid
from sendgrid.helpers.mail import (Mail, Email,Personalization)
from python_http_client import exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.settings.common import DEFAULT_FROM_EMAIL_DEV, SENDGRID_API_KEY_DEV, DEFAULT_TEMPLATE_ID

sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY_DEV)

class ConfirmationSendEmailApiView(APIView):
    def send_mail(self, template_id, sender, recipient, data_dict):
        mail = Mail()
        mail.template_id = template_id
        mail.from_email = Email(sender)
        personalization = Personalization()
        personalization.add_to(Email(recipient))
        personalization.dynamic_template_data = data_dict
        mail.add_personalization(personalization)

        try:
            response = sg.client.mail.send.post(request_body=mail.get())
        except exceptions.BadRequestsError as e:
            print("INSIDE")
            print(e.body)
            exit()
        print(response.status_code)
        print(response.body)
        print(response.headers)

    def post(self, request):
        recepient_email = request.data['recepient_email']
        subject = request.data['subject']
        fullname = request.data['fullname']
        body = request.data['body']

        # template_id = "d-1772e8ac6b5442e68975394ea71a4957"
        template_id = DEFAULT_TEMPLATE_ID
        sender = DEFAULT_FROM_EMAIL_DEV
        data_dict = {
            "subject": subject,
            "user_name": fullname, 
            "body": body
        }
        ConfirmationSendEmailApiView.send_mail(self, template_id, sender, recepient_email, data_dict)

        return Response(
            {
                "status_code": status.HTTP_200_OK,
                "message": "Mail sent successfully."
            }
        )