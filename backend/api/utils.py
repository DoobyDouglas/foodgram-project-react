from rest_framework.response import Response
from rest_framework import status


class AddAndDelMixin:

    def common_action(self, obj, relation, model):
        if self.request.method == 'POST':
            if relation.exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            field_names = [field.name for field in model._meta.fields]
            action_dict = {
                field_names[1]: obj,
                field_names[2]: self.request.user,
            }
            model.objects.create(**action_dict)
            return Response(status=status.HTTP_201_CREATED)
        if self.request.method == 'DELETE':
            if relation.exists():
                relation.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
