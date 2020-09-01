from django.urls import path
from . import views
from .views import PlanRequestsListView, PostPaidListView, PlanCreateView, MyPlansListView, PlanActivateUpdateView, WaterTransactionCreateView, WaterTransactionListView
urlpatterns = [

    #for user
    path('postpaids', PostPaidListView.as_view(),name='post_paid_list'),
    path('new_plan/<int:product_id>/',PlanCreateView.as_view(),name='new_plan'),
    path('activate/<int:pk>/',PlanActivateUpdateView.as_view(),name='activate'),
    path('requests/<int:product_id>/',PlanRequestsListView.as_view(),name='requests'),
    path('my_plans/',MyPlansListView.as_view(),name='my_plans'),
    path('water_transaction/<int:plan_id>/',WaterTransactionCreateView.as_view(),name='water_transaction'),
    path('water_transaction/history/',WaterTransactionListView.as_view(),name='water_transaction_history'),
    path('dispense/<int:transaction_id>/',views.dispense,name='dispense'),
    #path('finish/<int:transaction_id>/',views.finish),


    # for product
    #path('sensor_value/',views.store_sensor_values),#not_currently
    path('txn/finish/',views.finish_txn),
    path('cash/',views.cash),
]