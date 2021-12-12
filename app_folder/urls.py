from django.urls import path
from . import views

urlpatterns = [
    path('',views.mainpage),
    path('success',views.success),
    path('register',views.register),
    path('login',views.login),
    path('logout',views.logout),
    path('add_favorite_book',views.add_favorite_book),
    path('view_book_information/<int:book_id>',views.view_book_information),
    path('edit_book_information/<int:book_id>',views.edit_book_information), 
    path('update_book_information/<int:book_id>',views.update_book_information),
    path('delete_book_information/<int:book_id>',views.delete_book_information),
    path('remove_book_from_favorites/<int:book_id>/<int:page_number>',views.remove_book_from_favorites),
    path('add_book_to_favorites/<int:book_id>/<int:page_number>',views.add_book_to_favorites), 
    path('display_user_info',views.display_user_info),
    path('edit_user_information',views.edit_user_information),
    path('update_user_information',views.update_user_information),
]