from django.urls import path
from .views import login_view,signup,home,dashboard,logout_view,upload_image

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    path('dashboard/', dashboard, name='dashboard'),
    path('upload_image/', upload_image, name='upload_image'),


]