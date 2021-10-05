import mercadopago
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from payments.models import Payment

class MercadoPagoApiView(APIView):
    SDK_MERCADO = mercadopago.SDK("TEST-2734577806631487-052504-21c1748fdb47e0fd69b3399272c9f3dc-465550336")
  
    def post(self, request):
        print(" datos a recibir ", request.data) # paso1: imprimer request
        preference_data = { # paso2: crear arrays de datos
            "items": [
                {
                    "title": request.data["name"],
                    "quantity": 1,
                    "unit_price": request.data["price"],
                }
            ],
            "back_urls": {
                "success": "http://127.0.0.1:8888/success/",
                "failure": "http://127.0.0.1:8888/failure/",
                "pending": "http://127.0.0.1:8888/pendings/"
            },
            "auto_return": "approved"
        }
        preference_response = self.SDK_MERCADO.preference().create(preference_data) # paso 3 crear una preferencia
        preference = preference_response["response"]
        print("data preference", preference ) # paso 4 imprimer datos del response
        return Response(
            {
                "sandbox_init_point" : preference["sandbox_init_point"],
                "init_point": preference["init_point"]
            } # paso 4 devolvermos las url obtenedias en la creacion de preferencia
        )

class NotificationWebHookApiView(APIView):
    
    def post(self, request):
      print(request.data)

      SDK_MERCADO = mercadopago.SDK("TEST-2734577806631487-052504-21c1748fdb47e0fd69b3399272c9f3dc-465550336")
      
      mp_id = self.request.data['data']['id']
      
      data = SDK_MERCADO.payment().get(payment_id=mp_id)
      data = data['response']

  
      print("informacion del data", data)
      if data['status'] == 'approved':
        
        payment, _ = Payment.objects.get_or_create(
            #user = data.user,
            payment_id = data['id'],
            status_payment = data['status'],
            amount = data['transaction_amount'],
            currency = data['currency_id'],
            external_reference = data['external_reference'],
            
        )
        
        # payment.save()

        return Response({
            "status": "Ok"
        },
        status = status.HTTP_200_OK
        )

      return Response(
        {
            "status": "failed",
            "message": "No fue pagado"
        },
        status = status.HTTP_200_OK
      )

 #integracion de JoseMa para cancelaciones
class Refund(APIView):

    SDK_MERCADO_Jose = mercadopago.SDK("TEST-2734577806631487-052504-21c1748fdb47e0fd69b3399272c9f3dc-465550336")  

    def update(self, request):
        print(" datos a recibir ", request.data)
        payment_data  = {
            "status": "canceled" ,
            "id": "465550336-efa9c2ec-dd6b-4330-9d4f-149200d75c73"
        }
        
        payment_id = payment_data["id"]
        #payment_id = self.request.data['id']
        payment_response = self.SDK_MERCADO_Jose.payment().update(payment_id, payment_data)
        payment = payment_response["response"]
        print("Payment data", payment)
        return Response(payment_data)  

    def post(self, request):
        #print(" datos a recibir ", request.data)
        if 'id' in request.data:
            pay_id = self.request.data['id']

            refund_response = self.SDK_MERCADO_Jose.refund().create(payment_id=pay_id)
            refund = refund_response["response"]
        else:
            print("Payment_ID missing")    
        print("Refund data", refund)
        return Response({
            "status": "Ok"
        },
        status = status.HTTP_200_OK
        )          

    def get(self, request):

        print(" datos a recibir ", request.data)
        if 'id' in request.data:
            pay_id = self.request.data["id"]
        else:
            pay_id = "No PAYMENT_ID yet"      
        refunds_list = self.SDK_MERCADO_Jose.refund().list_all(payment_id=pay_id)
        refunds = refunds_list["response"]
        print("data preference", refunds)
        #return Response(refunds)
        return Response(pay_id)