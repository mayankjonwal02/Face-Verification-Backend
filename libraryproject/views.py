from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection
from rest_framework import status
from django.conf import settings
import os
from datetime import datetime
from deepface import DeepFace 
from django.http import JsonResponse
import shutil
from PIL import Image
import pyperclip
# from .function1 import is_face_front_center
from .function2 import recognize_face
import re


def developedby(request):
    return render(request, 'developedby.html')

class RegisterView(APIView):

    def get(self,request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            result = cursor.fetchall()
        
        data = [{'id': row[0], 'timestamp': row[1]} for row in result]
        return JsonResponse({'message': 'Hello, world!', 'data': data})

    def post(self, request):
        try:
            data = request.data
            user_id = data.get('id')
            image = request.FILES.get('image')

            if not user_id or not image:
                return JsonResponse({'error': 'ID and image are required'}, status=status.HTTP_400_BAD_REQUEST)
            
            user_id = user_id.strip()
            user_id = user_id.upper()

            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            image_name = user_id + '_' + timestamp + '.jpg'
            image_path = os.path.join(settings.MEDIA_ROOT, image_name)
            img = Image.open(image)
            img = img.resize((1200, 800), Image.LANCZOS)
            img.save(image_path)

            # if(is_face_front_center(img) == False):
            #     os.remove(image_path)
            #     return JsonResponse({'error': 'Look at Front '}, status=status.HTTP_400_BAD_REQUEST)

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE id = %s", [user_id])
                result = cursor.fetchone()
                if result:
                    return JsonResponse({'error': 'User already exists'}, status=status.HTTP_409_CONFLICT)


            # with open(image_path, 'wb') as destination:
            #     for chunk in image.chunks():
            #         destination.write(chunk)


            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO users (id) VALUES (%s)", [user_id])

            return JsonResponse({'message': 'Data inserted successfully'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def delete(self, request):
        data = request.data
        user_id = data.get('id')


        if not user_id:
            return JsonResponse({'error': 'ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_id = user_id.strip()
        user_id = user_id.upper()

        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE id = %s", [user_id])
            if cursor.rowcount == 0:
                return JsonResponse({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        files_deleted = []
        files = os.listdir(settings.MEDIA_ROOT)
        for file in files:
            name = remove_data_jpg(file)  # Assuming remove_data_jpg is defined elsewhere
            name = name.split('_')[0]
            
            if name == user_id:
                os.remove(os.path.join(settings.MEDIA_ROOT, file))
                files_deleted.append(file)

        return JsonResponse({'message': 'Data deleted successfully','files_deleted':files_deleted}, status=status.HTTP_204_NO_CONTENT)


class VerifyView(APIView):
    def post(self, request):
        try:
            data = request.data
            user_id = data.get('id')
            image = request.FILES.get('image')

            if not image or not user_id:
                return Response({'error': 'Image and ID is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            user_id = user_id.strip()
            user_id = user_id.upper()

            # Save the uploaded image to a temporary location
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            temp_image_name = 'temp_' + timestamp + '.jpg'
            temp_image_path = os.path.join(settings.TESTMEDIA_ROOT, temp_image_name)

            # with open(temp_image_path, 'wb') as destination:
            #     for chunk in image.chunks():
            #         destination.write(chunk)
            img = Image.open(image)
            img = img.resize((1200, 800), Image.LANCZOS)
            img.save(temp_image_path)

           
            # if( is_face_front_center(temp_image_path) == False):
            #     os.remove(temp_image_path)
            #     return JsonResponse({'error': 'Look in camera'}, status=status.HTTP_400_BAD_REQUEST)
            

            
            try:
                # Use DeepFace to recognize the face in the uploaded image.
               
                recognition = recognize_face(temp_image_path)
                
                print(recognition)
               
                
          
                
                # Handle recognition result
                if recognition:
                    try:
                        # Assuming 'remove_data_jpg' is a custom function you have defined elsewhere
                        
                        identity = remove_data_jpg(recognition[0]['identity'][0])
                        identity = identity.split('_')[0]
                        if identity == user_id:
                            keep_latest_two_images(user_id)
                            new_image_name = identity + '_' + timestamp + '.jpg'
                            new_image_path = os.path.join(settings.MEDIA_ROOT, new_image_name)
                        # Copy the image from the temporary path to the new path
                            shutil.copy(temp_image_path, new_image_path)
                            os.remove(temp_image_path)
                            
                            return JsonResponse({'message': 'Image received successfully!', 'recognition': identity })
                        else:
                            os.remove(temp_image_path)
                            return JsonResponse({'error': 'Invalid User'})
                    except KeyError as e:
                        os.remove(temp_image_path)
                        return JsonResponse({'message': 'Image received successfully!', 'error': str(e), 'recognition': 'Unknown'})
                else:
                    os.remove(temp_image_path)
                    return JsonResponse({'message': 'Image received successfully!', 'recognition': 'Unknown'})
            except ValueError as e:
                os.remove(temp_image_path)
                return JsonResponse({'message': 'Image received successfully!', 'error': str(e), 'recognition': 'Unknown'})

        except Exception as e:
            try:
                os.remove(temp_image_path)
            except Exception as en:
                pass
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




def remove_data_jpg(string):

  string = os.path.basename(string)
  start_index = string.find("\\") + 1  # Skip past leading "Data/"
  end_index = string.rfind(".")  # Find the last occurrence of "."
  if start_index != -1 and end_index != -1:
    return string[start_index:end_index]
  else:
    # Handle cases where "Data/" or ".jpg" is not present
    return string
  

def keep_latest_two_images( name):
    # Regular expression to match the filename pattern
    pattern = re.compile(rf'^{re.escape(name)}_(\d{{8}}\d{{6}})\.jpg$')
    
    # List to hold tuples of (timestamp, filepath)
    images = []

    folder_path = os.path.join(settings.MEDIA_ROOT)
    # Iterate over files in the folder
    for filename in os.listdir(folder_path):
        match = pattern.match(filename)
        if match:
            timestamp_str = match.group(1)
            timestamp = datetime.strptime(timestamp_str, '%Y%m%d%H%M%S')
            filepath = os.path.join(folder_path, filename)
            images.append((timestamp, filepath))
    
    # Sort images by timestamp in descending order
    images.sort(reverse=True, key=lambda x: x[0])
    
    # Keep only the latest two images and delete the rest
    for image in images[2:]:
        os.remove(image[1])



def registrationPage(request):
    return render(request, 'register.html')

def verifyPage(request):
    return render(request, 'verify.html')

def deregisterPage(request):
    pass


