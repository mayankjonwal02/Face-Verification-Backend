# from rest_framework.decorators import api_view
# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# from rest_framework import status
# from PIL import Image
# import numpy as np
# import cv2
# from .functions.function1 import is_face_front_center

# @api_view(['POST'])
# @csrf_exempt
# def isFront(request):
#     if request.method == 'POST':
#         image = request.FILES.get('image')

#         if not image:
#             return JsonResponse({'error': 'Image is required'}, status=status.HTTP_400_BAD_REQUEST)
        
#         # Open the image using PIL
#         img = Image.open(image)

#         # Convert the PIL image to a NumPy array
#         img = np.array(img)

#         # Convert RGB to BGR for OpenCV if the image is in RGB format
#         if img.ndim == 3 and img.shape[2] == 3:
#             img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

#         # Check if the face is front and center
#         if is_face_front_center(img):
#             return JsonResponse({"front": True}, status=status.HTTP_200_OK)
#         else:
#             return JsonResponse({"front": False}, status=status.HTTP_200_OK)
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
