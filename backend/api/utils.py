from rest_framework.response import Response
from rest_framework import status


class AddAndDelMixin:

    def common_action(self, obj, relation, model):
        if not self.request.user.is_anonymous:
            if self.request.method == 'POST' and not relation.exists():
                field_names = [field.name for field in model._meta.fields]
                action_dict = {
                    field_names[1]: obj,
                    field_names[2]: self.request.user,
                }
                model(**action_dict).save()
                return Response(
                    data=self.request.data,
                    status=status.HTTP_201_CREATED
                )
            elif self.request.method == 'DELETE' and relation.exists():
                relation.delete()
                return Response(
                    data=self.request.data,
                    status=status.HTTP_204_NO_CONTENT
                )
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
