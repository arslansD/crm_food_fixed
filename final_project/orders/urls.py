from django.urls import path

from . import views

urlpatterns = [
    path('tables/', views.TableView.as_view(), name="tables"),
    path('orders/', views.OrderView.as_view(), name="orders"),
    path("activeOrders/", views.GetAllActiveOrders.as_view(), name="active-orders"),
    path("checks/", views.CheckView.as_view(), name="checks"),
    path("mealsToOrder/", views.AddMealToOrder.as_view(), name="meals-to-orders"),
    path("statuses/<int:pk>/", views.StatusViews.as_view(), name="statuses"),
    path("servicePercentage/", views.PercentageCreate.as_view(), name="create_percentage"),
    path("servicePercentage/<int:pk>/", views.PercentageView.as_view(), name="percentage")

]
