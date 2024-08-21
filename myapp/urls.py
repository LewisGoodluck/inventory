from django.urls import path
from . import views

urlpatterns = [
    # login and logout
    path('login/',views.login_view,name="login"),
    path('logout/',views.logout_view,name='logout'),

    # homepage
    path('',views.home,name="home"),

    # crud on products
    path("registerProducts/",views.register_products,name="registerProducts"),
    path("viewProducts/",views.view_products,name="viewProducts"),
    path("updateProducts/<int:id>",views.update_products,name="updateProducts"),
    path("deleteProducts/<int:id>",views.delete_products,name="deleteProducts"),
]
