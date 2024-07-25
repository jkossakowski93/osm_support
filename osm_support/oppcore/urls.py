from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [


    path('login/', auth_views.LoginView.as_view(template_name='oppcore/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='oppcore/logout.html'), name='logout'),
    path('home/', views.home, name='home'),
    path('', views.home, name='home'),
    path('home_global_coordinator/', views.home_global_coordinator, name='home_global_coordinator'),
    path('home_local_coordinator/', views.home_local_coordinator, name='home_local_coordinator'),
    path('<int:opp_id>/', views.opp_details, name='opp_details'),
    path('add_opp/', views.add_opp, name='add_opp'),
    path('<int:opp_id>/edit_opp/', views.edit_opp, name='edit_opp'),
    path('<int:opp_id>/add_opp_spot/', views.add_opp_spot, name='add_opp_spot'),
    path('add_opp_spot_category/', views.add_opp_spot_category, name='add_opp_spot_category'),
    path('<int:opp_id>/<int:oppspot_id>/', views.opp_spot_details, name='opp_spot_details'),
    path('<int:opp_id>/<int:oppspot_id>/edit_opp_spot', views.edit_opp_spot, name='edit_opp_spot'),
    path('register_global_coordinator/', views.register_global_coordinator, name='register_global_coordinator'),
    path('register_global_admin/', views.register_global_admin, name='register_global_admin'),
    path('<int:opp_id>/register_local_coordinator/', views.register_local_coordinator, name='register_local_coordinator'),
    path('<int:opp_id>/register_local_admin/', views.register_local_admin, name='register_local_admin'),
    path('<int:opp_id>/json_for_opp_points/', views.json_for_opp_points, name='json_for_opp_points'),
    path('json_for_global_coordinator/', views.json_for_global_coordinator, name='json_for_global_coordinator'),
    path('json_for_local_coordinator/', views.json_for_local_coordinator, name='json_for_local_coordinator'),

]