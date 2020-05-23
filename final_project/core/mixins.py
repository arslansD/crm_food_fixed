from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response


class CustomUpdateMixin:
    """
    Custom update mixin for my views
    """

    def custom_get_object(self):
        """
        Returns the object the view is displaying.
        Gets object by an id from request
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Getting object by an id of object
        obj = get_object_or_404(queryset, pk=self.request.data["id"])

        # May raise permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = get_object_or_404(self.model, pk=request.data["id"])
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class CustomDeleteMixin:
    """
    Custom delete mixin for my views
    """

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(self.model, pk=request.data["id"])
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
