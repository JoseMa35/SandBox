import mercadopago
from rest_framework.views import APIView
from rest_framework.response import Response
    
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

