from django.urls import path
from .views import *


urlpatterns = [
    # for staff only
    path('addcloth/', AddCloth.as_view(), name = 'add'),
    path('updatecloth/<int:pid>', UpdateCloth.as_view(), name= 'update'),

    path('', AdminLogIn.as_view(), name='admn'),
    path('admnlogout/', AdminLogOut.as_view(), name='admLO'),
    path('dash/', AdmView.as_view(), name= 'dash'),
    path('users/', AdmUsrView.as_view(), name= 'admU'),
    path('products/', AdmProView.as_view(), name= 'admP'),
    path('messages/', AdmMsgView.as_view(), name= 'admM'),
    path('feedbacks/', AdmFeedView.as_view(), name= 'admF'),
    # Admin Operations
    path('deleteMessage/<int:id>', admDeleteMessage, name='dltmsg'),
    path('feededit/<int:id>', AdmFeedEdit.as_view(), name='admfeededit'),
    path('feeddelete/<int:id>', admFeedDelete, name='admdltfeed'),
    path('deleteReport/<int:id>', admDeleteReport, name='d_reports'),
    path('createStaff/', CreateStaff.as_view(), name="cstaff"),
    path('makeStaff/<int:id>', makeStaff, name='mstaff'),
    path('deleteStaff/<int:id>', deleteStaff, name='dstaff'),
    path('activateUser/<int:id>', activateUser, name="activate"),
    path('deactivateUser/<int:id>', deactivateUser, name="deactivate"),
]