from django.shortcuts import render
from django.contrib.auth.hashers import check_password, make_password
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Users
from .serializers import UsersSerializer
from application.utils import decode_jwt
import jwt


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    http_method_names = ['get', 'options', 'head', 'post', 'update', ]

    def create(self, request, *args, **kwargs):
        try:
            new_user = Users(
                email=request.data['email'].lower().strip(),
                name=request.data['name'],
                password=make_password(request.data['password']),
                birth_date=request.data['birth_date'],
            )
            new_user.save()

            return Response(data=UsersSerializer(new_user).data, status=status.HTTP_200_OK)

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

    def update(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            user = Users.objects.get(pk=pk)

            token_jwt = request.META.get('HTTP_AUTHORIZATION')
            jwt_data = decode_jwt(token_jwt, settings.APP_JWT_SECRET)

            if jwt_data['id'] != pk:
                response = {
                    "message": "Não autorizado"
                }
                return Response(data=response, status=401)
            

            serializer = UsersSerializer(
                instance=user,
                data=request.data,
                many=False,
                partial=False,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(data=UsersSerializer(user).data, status=status.HTTP_200_OK)
        
        except jwt.InvalidTokenError:
            response = {
                "message": "Não autorizado"
            }
            return Response(data=response, status=401)

        except Users.DoesNotExist:
            response = {
                "message": "Não econtrado"
            }
            return Response(data=response, status=status.HTTP_404_FORBIDDEN)

        except Exception as e:
            response = {
                "message": "Ocorreu um erro no servidor",
                "detail": f"{e}"
            }
            return Response(data=response, status=500)
        
    def partial_update(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            user = Users.objects.get(pk=pk)

            token_jwt = request.META.get('HTTP_AUTHORIZATION')
            jwt_data = decode_jwt(token_jwt, settings.APP_JWT_SECRET)

            if jwt_data['id'] != pk:
                response = {
                    "message": "Não autorizado"
                }
                return Response(data=response, status=401)
            

            serializer = UsersSerializer(
                instance=user,
                data=request.data,
                many=False,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(data=UsersSerializer(user).data, status=status.HTTP_200_OK)
        
        except jwt.InvalidTokenError:
            response = {
                "message": "Não autorizado"
            }
            return Response(data=response, status=401)

        except Users.DoesNotExist:
            response = {
                "message": "Não econtrado"
            }
            return Response(data=response, status=status.HTTP_404_FORBIDDEN)

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

            user = Users.objects.get(email__exact=request.data['email'].lower().strip())

            if check_password(request.data['password'], user.password):

                user_data = UsersSerializer(user, context={'get_jwt': True}).data

                return Response(data=user_data, status=status.HTTP_200_OK)
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
