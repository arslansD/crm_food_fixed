from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveDestroyAPIView, get_object_or_404, \
    CreateAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response

from core.mixins import CustomDeleteMixin
from . import serializers
from .models import Check, Order, Status, Table, ServicePercentage


class TableView(ListCreateAPIView, CustomDeleteMixin):
    """
    Responsible for endpoints/views of Table model
    """

    queryset = Table.objects.all()
    model = Table
    serializer_class = serializers.TableSerializer

    def delete(self, request, *args, **kwargs):
        """
        Needed  for 'DELETE' method, which accepts the id from request and delete corresponding model
        """
        return self.destroy(request, *args, **kwargs)


class OrderView(ListCreateAPIView, CustomDeleteMixin):
    """
    Responsible for endpoints/views of Order model
    """

    queryset = Order.objects.all()
    model = Order
    serializer_class = serializers.OrderSerializer

    def delete(self, request, *args, **kwargs):
        """
        Needed  for 'DELETE' method, which accepts the id from request and delete corresponding model
        """
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Create a new order"""
        serializer.save(waiter_id=self.request.user)


class GetAllActiveOrders(ListAPIView):
    """
    Responsible for listing orders that are active
    """
    queryset = Order.objects.filter(is_open=True)
    model = Order
    serializer_class = serializers.OrderSerializer


class AddMealToOrder(ListCreateAPIView, UpdateModelMixin, RetrieveModelMixin):
    """
    Responsible for listing meals of an order and adding additional meals to order
    """

    model = Order
    queryset = Order.objects.all()
    serializer_class = serializers.MealToOrderSerializer

    def delete(self, request, *args, **kwargs):
        """
        Needed  for 'DELETE' method, which accepts the order_id, meal_id, amount
        """
        instance = self.get_object()
        instance.remove_meal(request)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        Needed for 'POST' method that accepts order_id and meals and updates them
        """
        instance = self.get_object()
        instance.add_meals(request)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        """
        Needed for 'GET' method that accepts order_id and return all related meals
        """
        return self.retrieve(request, *args, **kwargs)

    def get_object(self):
        """
        Returns the object the view is displaying.
        Gets object by an id from request
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Getting object by an id of object
        obj = get_object_or_404(queryset, pk=self.request.data["order_id"])

        # May raise permission denied
        self.check_object_permissions(self.request, obj)

        return obj


class CheckView(ListCreateAPIView, CustomDeleteMixin):
    """
    Responsible for endpoints/views of departments model
    """

    queryset = Check.objects.all()
    model = Check
    serializer_class = serializers.CheckSerializer

    def delete(self, request, *args, **kwargs):
        """
        Needed for 'DELETE' method, which accepts an id from request and delete corresponding model
        """
        return self.destroy(request, *args, **kwargs)


class StatusViews(RetrieveDestroyAPIView, CreateModelMixin):
    """
    View responsible for status endpoints
    """

    queryset = Order.objects.all()
    model = Order
    lookup_field = "pk"
    serializer_class = serializers.StatusesOfOrder

    def get_serializer_class(self):
        """
        Returning serializer depending on request method
        """
        method = self.request.method

        if method == "POST":
            return serializers.StatusSerializer

        return serializers.StatusesOfOrder

    def delete(self, request, *args, **kwargs):
        """
        Function responsible for 'DELETE' method, which accepts an id of status and performs delete
        """
        instance = get_object_or_404(Status, pk=request.data["id"])
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, *args, **kwargs):
        """
        Needed for 'POST' method, which accepts a status and adds it to order
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(order_id=self.get_object())


class PercentageCreate(CreateAPIView):
    """
    View responsible for Service PERCENTAGE Creation
    """
    model = ServicePercentage
    queryset = ServicePercentage.objects.all()
    serializer_class = serializers.SpSerializer


class PercentageView(RetrieveDestroyAPIView):
    """
    View responsible for Service PERCENTAGE
    """

    queryset = ServicePercentage.objects.all()
    model = ServicePercentage
    lookup_field = "pk"
    serializer_class = serializers.SpSerializer

