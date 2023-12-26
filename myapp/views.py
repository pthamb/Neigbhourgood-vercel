from django.shortcuts import render
from .models import UserProfile
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
import logging
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
import json
import math
logger = logging.getLogger(__name__)


# Get an instance of a logger


# def front():
    
#     # return render(request, "index.html")
#     return JsonResponse({'Api is working'})

def user_profile_to_dict(user_profile):
    return {
        "id": user_profile.id,
        "name": user_profile.name,
        "age": user_profile.age,
        "email": user_profile.user.email,
        "zipCode": user_profile.zipCode,
        "mobile": user_profile.mobile,
        "walking":user_profile.walking,
        "running":user_profile.running,
        "swimming":user_profile.swimming,
        "coffeeTea":user_profile.coffeeTea,
        "foodGathering":user_profile.foodGathering,
        "televisionSports":user_profile.televisionSports,
        "movies":user_profile.movies,
        "shopping":user_profile.shopping,
        "happyHours":user_profile.happyHours,
        "errands":user_profile.errands,
        "rides":user_profile.rides,
        "childcare":user_profile.childcare,
        "eldercare":user_profile.eldercare,
        "petcare":user_profile.petcare,
        "tutoring":user_profile.tutoring,
        "repairAdvice":user_profile.repairAdvice,
        "otherAdvice":user_profile.otherAdvice,
        "latitude":user_profile.latitude,
        "longitude":user_profile.longitude,
        "sharePreference":user_profile.sharePreference,
        # Add other fields as necessary
    }

@csrf_exempt
@require_POST 
def register(request):
    
    if request.method == 'POST':
       
        try:
            data = json.loads(request.body)

            # data = request.POST
        except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON format or empty request body'}, status=400)
            
        required_fields = ["name", "age", "email"]
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            messages.error(request, "Please fill out the required fields: " + ', '.join(missing_fields))
            # return render(request, 'dashboard.html')
            return JsonResponse({'message': 'Fill the required filled'})
            
        print("no")

        # Assuming you have a model called 'User' to store this data
        # user = UserProfile()
        data = json.loads(request.body)
        name = data.get('name')
        age = data.get('age')
        email = data.get('email')
        password = data.get('password')
        zipCode = data.get('zipCode')
        mobile = data.get('mobile')
        walking = data.get('walking')
        running = data.get('running')
        gardening = data.get('gardening')
        swimming = data.get('swimming')
        coffeeTea = data.get('coffeeTea')
        foodGathering = data.get('foodGathering')
        televisionSports = data.get('televisionSports')
        movies = data.get('movies')
        shopping = data.get('shopping')
        happyHours = data.get('happyHours')
        errands = data.get('errands')
        rides = data.get('rides')
        childcare = data.get('childcare')
        eldercare = data.get('eldercare')
        petcare = data.get('petcare')
        tutoring = data.get('tutoring')
        repairAdvice = data.get('repairAdvice')
        otherAdvice = data.get('otherAdvice')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        sharePreference = data.get('sharePreference')

        # print(f"user: {user}")
        # # print(f"name{name}")
        # print(user.email)
        # print(user.zipCode)
        print(f"name:{name}")
        
        

        # Handle email and mobile based on sharePreference
        # if sharePreference == 'yes':
        #     email = request.POST.get('email', "")
        #     mobile = request.POST.get('mobile', "")
        # else:
        #     email = "*" * len(email)
        #     mobile = "*" * len(mobile)
           
        # Check if user with the same mobile already exists
        # existing_user = User.objects.filter(mobile=user.mobile).first()
        # if existing_user:
        #     messages.error(request, "User with the same mobile number already exists. Data not submitted.")
        if User.objects.filter(username=email).exists():
        #    return JsonResponse({'error': 'User with this email already exists.'}, status=400)
            return JsonResponse({'error': f'User with the email {email} already exists.'}, status=400)
           
        # user = User(username=email)
        # user.set_password(password)
        # user.save()
        user = User.objects.create_user(username=email, email=email, password=password)
        user.save()

        token, created = Token.objects.get_or_create(user=user)

        
        user_profile=UserProfile(user=user, name=name, age=age, email=email, zipCode=zipCode, mobile=mobile, walking=walking, running=running, gardening=gardening, swimming=swimming, coffeeTea= coffeeTea, foodGathering=foodGathering, televisionSports=televisionSports, movies=movies, shopping=shopping, happyHours=happyHours, errands=errands, rides=rides, childcare=childcare, eldercare=eldercare, petcare=petcare, tutoring=tutoring, repairAdvice=repairAdvice, otherAdvice=otherAdvice, latitude=latitude, longitude=longitude,sharePreference=sharePreference)
        user_profile.save()
        user_profile_data = user_profile_to_dict(user_profile)
        # login(request, user)
       
        messages.success(request, "Data submitted successfully!")
        # return JsonResponse({'message': 'User registered successfully'}, status=201)
        return JsonResponse({'message': 'User registered successfully', 'user':user_profile_data,'token': token.key}, status=201)
        

    return JsonResponse({'error': 'Invalid request'}, status=400)
       



# def dashboard(request):
#     # Your logic here
#  return render(request, 'dashboard.html')

@csrf_exempt
def user_login(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are accepted'}, status=405)
 
    try:
    
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        print(f"Received email: {email}, password: {password}")

        if not email or not password:
                return JsonResponse({'error': 'Email and password are required fields.'}, status=400)
        
        user = authenticate(request, username=email, password=password)

       
        print("today")

        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            try:
                user_profile = UserProfile.objects.get(user=user)
                user_profile_data = user_profile_to_dict(user_profile)
            except UserProfile.DoesNotExist:
                user_profile_data = {}
            return JsonResponse({'message': 'Login successful', 'token': token.key, 'user': user_profile_data})
        else:
           
            return JsonResponse({'error': 'Invalid login credentials'}, status=401)
   
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'An error occurred during login'}, status=500)

        
#  return HttpResponseBadRequest("Bad Request: Invalid login request")

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def restricted_page(request):
    
    for header, value in request.headers.items():
        # print(f"{header}: {value}")
     try:
        # Get the user from the request
        user = request.user
        
        # Retrieve the user profile
        user_profile = UserProfile.objects.get(user=user)
        user_profile_data = user_profile_to_dict(user_profile)

        return Response({
            'message': 'Access granted',
            'user': user_profile_data
        })
        
        

     except UserProfile.DoesNotExist:
        return Response({'message': 'Request unauthorized, please login'}, status=404)
     except Exception as e:
        return Response({'message': f'An error occurred: {str(e)}'}, status=500)


def user_logout(request):
    logout(request)





def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in km

    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    a = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    return distance


# def calculate_similarity(user1, user2):
#     fields = ['walking', 'running', 'swimming', 'coffeeTea', 'foodGathering', 'televisionSports', 'movies', 'shopping', 'happyHours', 'errands', 'rides', 'childcare', 'eldercare', 'petcare', 'tutoring', 'repairAdvice', 'otherAdvice']
#     total_fields = len(fields)
#     matches = 0

#     for field in fields:
#         if getattr(user1, field) == getattr(user2, field):
#             matches += 1

#     similarity = (matches / total_fields) * 100
#     return similarity   # Returns True if similarity is 50% or more

def calculate_similarity(user1, user2):
    fields = ['walking', 'running', 'swimming', 'coffeeTea', 'foodGathering', 'televisionSports', 'movies', 'shopping', 'happyHours', 'errands', 'rides', 'childcare', 'eldercare', 'petcare', 'tutoring', 'repairAdvice', 'otherAdvice']
    matches = 0
    valid_fields = 0  # Count of fields that are not null in both user profiles
    matching_fields = []
    

    for field in fields:
        user1_value = getattr(user1, field)
        user2_value = getattr(user2, field)

        # Check if both user1 and user2 have non-null values for this field
        if user1_value is not None and user2_value is not None:
            valid_fields += 1
            if user1_value == user2_value:
                matches += 1
                matching_fields.append(field)

    # To avoid division by zero if all fields are null
    if valid_fields == 0:
        return 0

    similarity = (matches / valid_fields) * 100
    return similarity, matching_fields




@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def find_similar_users(request):
    try:
        # data = request.data
        current_user = request.user
        current_user_profile = UserProfile.objects.get(user=current_user)
        print(f"current:{current_user}")

        # Check if the current user is within a 5km radius and has a 50% data match
        similar_users = []
        for user in UserProfile.objects.exclude(user=current_user):
            distance = haversine(current_user_profile.latitude, current_user_profile.longitude, user.latitude, user.longitude)
            # if distance <= 5 and calculate_similarity(current_user_profile, user) >= 50:
            #     similar_users.append(user_profile_to_dict(user))
            print(f"Checking user: {user}, Distance: {distance} km")
            # if distance <= 5:
            similarity, matching_fields = calculate_similarity(current_user_profile, user)
            print(f"Distance: {distance}, Similarity: {similarity}%, User: {user}, Matching Fields: {matching_fields}")
            # if calculate_similarity(current_user_profile, user):
            if distance <= 5 and similarity> 50:
                    similar_users.append(user_profile_to_dict(user))
                    

        if similar_users:
            return Response({'users': similar_users})
        else:
            return Response({'message': 'No similar users found'}, status=404)

    except UserProfile.DoesNotExist:
        return Response({'message': 'Current user profile not found'}, status=404)
    except Exception as e:
        return Response({'message': f'An error occurred: {str(e)}'}, status=500)
    




@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_similar_user_profile(request):   # type: ignore
    try:
        logger.info(f"Received query parameters: {request.GET}")

        # Fetching the 'id' parameter from the query string
        user_id = request.GET.get('id', None)  # Replace 'None' with your default value or handling for missing 'id'
        print(f"id{user_id}")
        if not user_id:
            return JsonResponse({'error': 'User ID is required'}, status=400)

        # Fetch the user profile based on the user ID
        user_profile = UserProfile.objects.get(id=user_id)
        user_profile_data = user_profile_to_dict(user_profile)
        return JsonResponse({'user': user_profile_data})
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User profile not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
