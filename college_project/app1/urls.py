from django.urls import path, include
from .import views

urlpatterns = [
    path('',views.index, name='index'),
    path('add_course',views.add_course, name='add_course'),
    path('course',views.course, name='course'),
    path('student',views.student, name='student'),
    path('add_std_details',views.add_std_details, name='add_std_details'),
    path('show_details',views.show_details, name='show_details'),
    path('edit/<int:id>',views.edit, name='edit'),
    path('edit_details/<int:id>',views.edit_details, name='edit_details'),
    path('delete_student/<int:id>',views.delete_student, name='delete_student'),
    path('teacher_details',views.teacher_details, name='teacher_details'),
    path('login_page',views.login_page, name='login_page'),
    path('login_function',views.login_function, name='login_function'),
    path('signup_page',views.signup_page, name='signup_page'),
    path('signup_function',views.signup_function, name='signup_function'),
    path('logout_function',views.logout_function, name='logout_function'),
    path('admin_home',views.admin_home, name='admin_home'),
    path('teacher_home',views.teacher_home, name='teacher_home'),
    path('teacher_card',views.teacher_card, name='teacher_card'),
    path('teacher_update/<int:id>/',views.teacher_update, name='teacher_update'),
    path('teacher_update_function/<int:id>/',views.teacher_update_function, name='teacher_update_function'),
    path('delete_teacher/<int:id>',views.delete_teacher, name='delete_teacher'),
]