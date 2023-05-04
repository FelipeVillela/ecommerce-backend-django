from django.shortcuts import render
from django.contrib.auth.hashers import check_password, make_password
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Users
from .serializers import UsersSerializer

# Create your views here.
class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    def create(self, request, *args, **kwargs):
        try:
            new_player = Users(
                email=request.data['email'].lower().strip(),
                name=request.data['name'],
                password=make_password(request.data['password']),
                birth_date=request.data['birth_date'],
            )
            new_player.save()

            return Response(data=UsersSerializer(new_player).data, status=status.HTTP_200_OK)

        except KeyError:
            response = {
                "message": "Parâmetros inválidos"
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            response = {
                "message": "Ocorreu um erro no servidor",
                "detail": f"{e}"
            }
            return Response(data=response, status=500)

    @action(detail=False, methods=['post'], name='Login', url_path='login')
    def login(self, request, *args, **kwargs):
        try:
            message_invalid_credentials = "Login ou senha inválidos. Revise as informações."

            player = Users.objects.get(email__exact=request.data['email'].lower().strip())

            if check_password(request.data['password'], player.password):

                player_data = UsersSerializer(player, context={'get_jwt': True}).data

                return Response(data=player_data, status=status.HTTP_200_OK)
            else:
                response = {
                    "message": message_invalid_credentials
                }
                return Response(data=response, status=status.HTTP_403_FORBIDDEN)
            
        except KeyError:
            response = {
                "message": "Parâmetros inválidos"
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        except Users.DoesNotExist:
            response = {
                "message": message_invalid_credentials
            }
            return Response(data=response, status=status.HTTP_403_FORBIDDEN)

        
        except Exception as e:
            print(e)
            response = {
                "message": "Erro ao realizar login.",
                "detail": f"{e}"
            }
            return Response(data=response, status=500)
