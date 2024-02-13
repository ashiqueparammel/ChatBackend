from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class Google_Signup(APIView):
    def post(self, request):
        email = request.data.get("email")
        is_company = request.data.get("is_company")

        if not CustomUser.objects.filter(email=email).exists():
            if is_company == "":
                data = {
                    "Text": "Your not Signed Please signup !",
                    "status": 204,
                }
                return Response(data=data)
            serializer = User_Sign_Up(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                user.save()
                data = {
                    "Text": "Your google SignUp successfully!",
                    "signup": "signup",
                    "status": 200,
                }
                return Response(data=data)
        if CustomUser.objects.filter(email=email).exists():
            data = {
                "Text": "This Email alredy exist!",
                "status": 403,
            }
            return Response(data=data)

        else:
            data = {"Text": serializer.errors, "status": 404}
            return Response(data=data)


class Google_login(APIView):
    def post(self, request):
        email = request.data.get("email")

        if CustomUser.objects.filter(email=email).exists():
            access_token = request.data.get("access_token")
            Googleurl = config("GOOGLE_VERYFY")
            get_data = f"{Googleurl}access_token={access_token}"
            response = requests.get(get_data)

            if response.status_code == 200:
                user_data = response.json()
                check_email = user_data["email"]
                if check_email == email:
                    user = CustomUser.objects.get(email=email)
                    token = RefreshToken.for_user(user)
                    token["email"] = user.email
                    token["is_active"] = user.is_active
                    token["is_superuser"] = user.is_superuser
                    token["is_company"] = user.is_company
                    token["is_google"] = user.is_google
                    dataa = {
                        "refresh": str(token),
                        "access": str(token.access_token),
                    }

                    if user.is_active:
                        data = {
                            "message": "Your Login successfully! ",
                            "status": 201,
                            "token": dataa,
                        }
                    else:
                        data = {
                            "message": "Your Account has been blocked ! ",
                            "status": 202,
                            "token": dataa,
                        }

                    return Response(data=data)
            else:
                data = {
                    "message": response.text,
                    "status": 406,
                }
                return Response(data=data)
        else:
            data = {
                "message": "This Email have no account please Create new account! ",
                "status": 403,
            }
            return Response(data=data)
