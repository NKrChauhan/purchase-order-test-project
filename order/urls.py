from django.urls import path

from .views.purchase_order import PurchaseOrderAPIView

urlpatterns = [
    # For GET PUT DELETE API calls with purchase_order_id
    path('<int:purchase_order_id>/', PurchaseOrderAPIView.as_view(), name='purchase_order_view'),
    # For GET POST API calls since GET might have no purchase_order_id & POST will be without purchase_order_id
    path('', PurchaseOrderAPIView.as_view(), name='purchase_order_creation'),
]
