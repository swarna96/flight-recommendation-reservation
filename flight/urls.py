from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
app_name = "flight"
urlpatterns = [path("", views.homepage, name="homepage"),
             path("login/", views.login, name="login"),
             path("signup/", views.signup, name="signup"),
             path("logout/", views.logout_request, name="logout"),
             path("cpanel/",views.cpanel,name="cpanel"),
             path("cpanel1/",views.cpanel1,name="cpanel1"),
             path("contact/", views.Contact.as_view(), name="contact"),
             path("show_flight/",views.show_flight,name="show_flight"),
             path("book_flight/",views.book_flight,name="book_flight"),
             path('book_flight/<int:pk>/book/',views.Book.as_view(),name="book"),
             path("create_flight/",views.Create_flight.as_view(),name="create_flight"),
             path('manage/<int:pk>/update/', views.Update_flight.as_view(), name='update_flight'),
             path('manage/<int:pk>/delete/',views.Delete_flight.as_view(),name='delete_flight'),
             path('manage/',views.Manage_flight.as_view(),name='manage_flight'),
             path("profile/", views.Profile.as_view(), name="profile"),
             path('profile/<int:pk>/profile_update/', views.Profile_update.as_view(), name='profile_update'),
             path('rating/', views.View_Ratings, name='view_ratings'),
             path('add_rating/', views.Add_Ratings.as_view(), name='add_ratings'),
]

