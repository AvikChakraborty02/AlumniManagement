"""alumniproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    # Common URls

    path("",views.home,name="home"),
    path("register/",views.register,name="register"),
    path("otp_modal/",views.otp_modal,name="otp_modal"),
    path("error_page/",views.error_page,name="error_page"),
    path("registration_form/",views.registration_form,name="registration_form"),
    path("something_went_wrong/",views.something_went_wrong,name="something_went_wrong"),
    path("logout/",views.logout,name="logout"),

    # Alumni Admin URLs

    path("admin_home/",views.admin_home,name="admin_home"),
    path("add_admin/",views.add_admin,name="add_admin"),
    path("coordinator_details/",views.coordinator_details,name="coordinator_details"),
    path("edit_admin_otp/<id>",views.edit_admin_otp,name="edit_admin_otp"),
    path("edit_credentials/<id>",views.edit_credentials,name="edit_credentials"),
    path("delete_credentials/<id>",views.delete_credentials,name="delete_credentials"),
    path("view_application/",views.view_application,name="view_application"),
    path("view_details/<application_id>",views.view_details,name="view_details"),
    path("accept_application/<application_id>",views.accept_application,name="accept_application"),
    path("delete_application/<application_id>",views.delete_application,name="delete_application"),
    path("search_alumni/",views.search_alumni,name="search_alumni"),
    path("search_view_details/<alumni_id>",views.search_view_details,name="search_view_details"), 
    path("delete_alumni/<alumni_id>",views.delete_alumni,name="delete_alumni"), 
    path("change_password_otp/",views.change_password_otp,name="change_password_otp"),
    path("change_password/",views.change_password,name="change_password"),
    path("search_alumni_values/",views.search_alumni_values,name="search_alumni_values"),
    path("search_view_application/",views.search_view_application,name="search_view_application"),
    path("admin_news/",views.admin_news,name="admin_news"),
    path("add_events/",views.add_events,name="add_events"),
    path("delete_post_by_admin/<post_id>",views.delete_post_by_admin,name="delete_post_by_admin"),
    path("manage_events/",views.manage_events,name="manage_events"),
    path("delete_events/<event_id>",views.delete_events,name="delete_events"),

    # Alumni User URLs

    path("alumni_home/",views.alumni_home,name="alumni_home"),
    path("create_post/",views.create_post,name="create_post"),
    path("my_profile/",views.my_profile,name="my_profile"),
    path("edit_posts/<post_id>",views.edit_posts,name="edit_posts"),
    path("delete_post/<post_id>",views.delete_post,name="delete_post"),
    path("batchmates/",views.batchmates,name="batchmates"),
    path("edit_profile/",views.edit_profile,name="edit_profile"),
    path("alumni_change_password/",views.alumni_change_password,name="alumni_chnage_password"),
    path("alumni_change_password_otp/",views.alumni_change_password_otp,name="alumni_chnage_password_otp"),
    path("alumni_search_alumni/",views.alumni_search_alumni,name="alumni_search_alumni"),
    path("search_people/",views.search_people,name="search_people"),

    #Rest APIs URls(Admin and Common Only)

    path("get_otp/",views.get_otp,name="get otp"),
    path("verify_otp/",views.verify_otp,name="verify_otp"),
    path("admin_login_verification/",views.admin_login_verification,name="admin_login_verification"),
    path("add_alumni_coordinator/",views.add_alumni_coordinator,name="add_alumni_coordinator"),
    path("search_admin/",views.search_admin,name="search_admin"),
    path("edit_admin_verify_otp/",views.edit_admin_verify_otp,name="edit_admin_verify_otp"),
    path("update_admin_credentials/",views.update_admin_credentials,name="update_admin_credentials"),
    path("save/",views.save,name="save"),
    path("search_by_id/",views.search_by_id,name="search_by_id"),
    path("search_details/",views.search_details,name="search_details"),
    path("change_password_otp_verify/",views.change_password_otp_verify,name="change_password_otp_verify"),
    path("update_password/",views.update_password,name="update_password"),
    path("create_event/",views.create_event,name="create_event"),

    #Rest APIs URLs(Alumni Only)

    path("alumni_login_verification/",views.alumni_login_verification,name="alumni_login_verification"),
    path("insert_post/",views.insert_post,name="insert_post"),
    path("edit_post/",views.edit_post,name="edit_post"),
    path("update_profile/",views.update_profile,name="update_profile"),
    path("update_profile_picture/",views.update_profile_picture,name="update_profile_picture"),
    path("alumni_change_password_otp_verify/",views.alumni_change_password_otp_verify,name="alumni_change_password_otp_verify"),
    path("alumni_update_password/",views.alumni_update_password,name="alumni_update_password"),
    path("alumni_search_people/",views.alumni_search_people,name="alumni_search_people"),

    #Load More URL
    path("load/",views.load_more,name="load"),
    path("my_profile_load_more",views.my_profile_load_more,name="my_profile_load_more"),

    #Donate and Payment URL
    path("donate/",views.donate,name="donate"),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('get_amount/',views.get_amount,name="get_amount"),
]   
