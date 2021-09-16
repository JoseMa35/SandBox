# Medios de pago disponibles
from django.http import HttpResponse
import mercadopago
import json

PUBLIC_KEY = 'TEST-5a7a86f5-398a-4076-9438-789a698e8de9'
ACCESS_TOKEN = 'TEST-8789921003899809-091602-ff2978a2a48fc8b2ed3decc078e12d75-260357063'

PAGOEFECTIVO_ID = 'pagoefectivo_atm'
PAGOEFECTIVO_PAYMENT_TYPE = 'atm'

DOCUMENT_TYPE = {
    "id": "DNI",
    "name": "DNI",
    "type": "number",
    "min_length": 7,
    "max_length": 8
}


def available_payment_list(request):
    sdk = mercadopago.SDK(ACCESS_TOKEN)

    payment_methods_response = sdk.payment_methods().list_all()
    payment_methods = payment_methods_response["response"]

    return HttpResponse(json.dumps(payment_methods, sort_keys=True))


def available_payment(request):
    sdk = mercadopago.SDK(ACCESS_TOKEN)

    if 'payment_type' in request.GET != None:
        payment_type = request.GET['payment_type']
    else:
        return HttpResponse({'PAYMENT_TYPE param is required'}, status=400, )

    payment_methods_response = sdk.payment_methods().list_all()
    payment_methods = payment_methods_response["response"]

    method = []
    for payment in payment_methods:
        if payment_type == payment['id']:
            method = payment

    if len(method) > 0:
        return HttpResponse(json.dumps(method, sort_keys=True))
    else:
        return HttpResponse({'type doenst exist'}, status=400, )


def transaction_payment(request):
    sdk = mercadopago.SDK(ACCESS_TOKEN)

    name = 'yahyr'
    last_name = 'paredes'
    email = 'yahyr97@gmail.com'
    document_type = 'DNI'
    document = '73884071'
    amount_value = 100
    product_description = 'Una empanada'

    payment_data = {
        "transaction_amount": amount_value,
        "description": product_description,
        "payment_method_id": PAGOEFECTIVO_ID,
        "payer": {
            "email": email,
            "first_name": name,
            "last_name": last_name,
            "identification": {
                "number": document,
                "type": document_type,
            }

        }
    }

    payment_response = sdk.payment().create(payment_data)
    payment = payment_response["response"]
    # print(payment['id'])
    # print(payment['transaction_details'] )
    return HttpResponse(json.dumps(payment, sort_keys=True))
