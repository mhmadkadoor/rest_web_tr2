from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.home, name='home'),
    path('admin/', views.admin, name='admin'),
    path("login",views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('proSettings/', views.proSettings, name='proSettings'),
    path("product/view/<int:product_id>/", views.viewProduct, name='viewProduct'),
    path("product/viewAdmin/<int:product_id>/", views.viewProductAdmin, name='viewProductAdmin'),
    path("product/edit/<int:product_id>/", views.editProduct, name='editProduct'),
    path("product/viewAdmin/", views.viewProductsAdmin, name='viewProductsAdmin'),
    path("product/delete/<int:product_id>/", views.deleteProduct, name='deleteProduct'),
    path("hotdeal/edit/<int:hotdeal_id>/", views.editHotdeal, name='editHotdeal'),
    path("hotdeal/view/<int:hotdeal_id>/", views.viewHotdeal, name='viewHotdeal'),
    path("hotdeal/viewAdmin/", views.viewHotdealsAdmin, name='viewHotdealsAdmin'),
    path("hotdeal/delete/<int:hotdeal_id>/", views.deleteHotdeal, name='deleteHotdeal'),
    path("hotdeal/viewAdmin/<int:hotdeal_id>/", views.viewHotdealAdmin, name='viewHotdealAdmin'),
    path("search/", views.search, name='search'),
    path("all/", views.all, name='all'),
    
]
  




handler404 = 'pages.views.custom_page_not_found_view'
handler500 = 'pages.views.custom_error_view'