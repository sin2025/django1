'''
Created on 2019. 1. 20.

@author: user
'''
#하위 URLConf.
#app_name: 하위 URLConf 파일의 등록된 URL들의 그룹명
#urlpatterns: URL과 뷰함수를 리스트형태로 등록하는 변수
from django.urls import path
from .views import *
#바로 위 원래 명령을 from .views import index, detail, result, vote, qregister, qupdate, qdelete->*로 변경함
app_name='vote'
#기본 주소: 127.0.0.1:8000/vote/
urlpatterns=[
    #웹 클라이언트가 127.0.0.1:8000/vote/ 요청시 index 뷰함수 호출
    #name:해당 URL, 뷰함수 등록에 대해서 별칭을 지정
    path('',index, name='index'),
    #127.0.0.1:8000/vote/숫자/
    path('<int:q_id>/', detail, name='detail'),
    path('vote/', vote, name='vote'),
    path('result/<int:q_id>/', result, name='result'),
    #127.0.0.1:8000/vote/qr
    path('qr/', qregister, name='qr'),
    path('qu/<int:q_id>/', qupdate, name='qu'),
    #127.0.0.1:8000/vote/qd/Question객체의id값
    path('qd/<int:q_id>/',qdelete, name='qd'),
    #127.0.0.1:8000/vote/cr/
    path('cr/',cregister,name='cr'),
    #127.0.0.1:8000/vote/cu/Choice 객체 id 값
    path('cu/<int:c_id>/', cupdate, name='cu'),
    path('cd/<int:c_id>/', cdelete, name='cd'),
    ]