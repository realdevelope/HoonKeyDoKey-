from django.urls import path
from . import views

urlpatterns = [
        path("register_test", views.register_test),
        path("registered_test", views.registered_test),
        path("login_test", views.login_test),
        path("logined_test", views.logined_test),
        path("update_test", views.update_test),
        path("delete_test", views.delete_test),
        path("logout_test", views.logout_test),
        path("my_page_test", views.my_page_test),
        path("password_save", views.password_save),


        path("upload", views.upload_file),
        path("checkbox", views.checkbox),
        path("checkbox_result", views.checkbox_result),
        path( 'ajax', views.ajax),
        path( 'ajax_test', views.ajax_test ),
        
        path('login', views.login),
        path('logged', views.logged),
        path('register', views.register),
        path('registered', views.registered), 
#       path('check_logged', views.check_logged),
        path('logout', views.logout),
        path('delete', views.delete),
        path('update', views.update),
        path('goShop', views.goShop),
        
        path('ok/no', views.hello),
        path('receive', views.rec),
        path('send', views.send),
        path('urltest', views.urltest),
        path('novel/<int:chapter>/<str:player1>/<str:player2>', views.novel),
        path('static', views.static)
]
