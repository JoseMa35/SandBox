

from checkOut.api.viewsets import ItemViewSet
from rest_framework import routers

router= routers.DefaultRouter()
router.register('Items',ItemViewSet, basename='Item')
#router.register('Items',itemViewSet, basename='Item')



# for url in router.urls:
#     print(url,'/n')