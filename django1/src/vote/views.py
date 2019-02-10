from django.shortcuts import render, get_object_or_404
from .models import Question, Choice
from django.urls.base import reverse
from django.http.response import HttpResponseRedirect
from _ast import Pass
from test.test_set import TestBasicOpsString


#reverse(별칭문자열, args=(매개변수값)): 별칭기반으로 URL주소 반환
#HttpResponseRedirect(url주소문자열): 해당 URL 주소를 클라이언트에게 전달

#get_object-or_404: 특정한 모델클래스에 id값을 조건으로 검색해 객체 추출.
#단, 객체가 존재하지 않는 경우에 웹 클라이언트의 요청이 잘못된 것으로 판단해 더이상 뷰함수가 
#진행되지 않고 404 에러페이지를 클라이언트에게 전달

#질문 리스트(index)
def index(request):
    #모든 Question 객체 추출
    #슬라이싱:iterable 데이터의 특정 범위 만큼의 요소를 추출하는 방식
    #[시작인덱스:종료인덱스]->시작인덱스<=추출<종료인덱스
    #ex) a=[1,2,3,4,5]
    #a[1:4]=>[2,3,4]
    #시작인텍스가 빈칸인 경우->0번인덱스부터 추출
    #종료인덱스가 빈칸인 경우->마지막인텍스의 요소까지 추출
    #인덱스값이 음수인 경우->맨 뒤 요소부터 인덱스를 찾음
    qlist=Question.objects.all()
    #추출한 객체를 HTML에 전달 및 클라이언트에게 HTML 전달
    return render(request,'vote/index.html',
                        {'objs':qlist})

#질문 선택 시 답변항목 제공(detail)
def detail(request, q_id):
    #q_id 값을 이용해 Question 객체 한개 추출
    #get_object_or_404(모델클래스명, 조건)
    q=get_object_or_404(Question, id=q_id)
    #Question객체와 연결된 모든 Choice객체 추출
    #모델클래스A의객체.모델클래스B-set: A모델클래스와 B모델클래스가 1:n관계인 경우
    #해당 A객체와 연결된 B객체들을 대상으로 get(),all(),filter(),exclude()함수들을 사용할 수 있음
    #q.choice_set:해당 Question객체와 연결된 Choice객체들을 대상으로 선정
    c_list=q.choice_set.all()
    #결과로 HTML 파일 전달
    return render(request, 'vote/detail.html',
                      {'q':q, 'clist':c_list})
#웹 클라이언트가 선택한 답변항목의 투표수를 늘리는 처리(vote)
def vote(request):
     #POST방식으로 사용자가 요청했는지 확인
     #=>HTML의 form태그의 요청방식을 POST로 했기 때문에
     #request.method: 사용자의 요청방식이 문자열형태로 저장된 변수
    #대소문자 구분이 있으므로 비교연산자 사용시"GET","POST"로 비교
     if request.method =="POST":
         #request.POST:클라이언트가 POST 방식으로 요청할때 넘어온 데이터가 저장된 변수
         #request.GET:클라이언트가 GET 방식으로 요청할때 넘어온 데이터가 저장된 변수
         #사전형데이터.get(키값): 사전형 데이터에서 키값에 해당하는 값을 추출하는 함수
         c_id=request.POST.get('a')
         #c_id와 같은 id변수값을 가진 Choice객체를 추출
         c=get_object_or_404(Choice, id=c_id)
         #해당 Choice객체의 votes 변수값에 1을 누적
         c.votes +=1 #c.votes=c.votes+1
         c.save() #해당 객체의 변수값 변동을 데이터베이스에 반영
         #투표결과 화면을 보여줌
         return HttpResponseRedirect(reverse('vote:result', args=(c.q.id,)))        
#웹 클라이언트가 선택한 질문의 답변 투표결과(result)
def result(request, q_id):
    #Question객체를 찾기
    q=get_object_or_404(Question, id=q_id)
    #결과 HTML 클라이언트 전송
    return render(request, 'vote/result.html',
                  {'q':q})
    
#데코레이터: URLConf를 통해 view함수가 호출 될때, 뷰가 실행되기 전 먼저 실행되는 함수.
#뷰함수에만 데코레이터를 적용할 수있음
#뷰클래스는 XXXMixin 클래스를 상속받아 데코레이터로 처리
#데코레터를 적용 방식
#@데코레이터 함수 이름
#def 뷰함수(request):

#클래스에 데코레이터 적용 방식
#class 뷰클래스(XXXMixin):

#login_required: 뷰함수 호출 전 요청을 한 크라이언트가 비로그인 상태인 경우, 웹프로젝트에 지정된 로그인 URL로 넘어가는 데코레이터 함수

#로그인 RUL 지정 방법
#setting.py  -> LOGIN_URL 변수에 URL저장

from django.contrib.auth.decorators import login_required
    
    
from .forms import QuestionForm, ChoiceForm
from _datetime import datetime #날짜/시간과 관련된 파이썬 클래스
#Question 객체를 사용자가 등록하는 뷰
#'질문추가' 링크를 타고온 클라이언트에게는 비어 있는 QuestionForm 기반의 입력양식을 제공
#폼을 제출한 경우, 클라이언트가 작성한 정보를 바탕으로 Question 객체를 생성 및 DB에 저장
#--> 완성된 객체에 대한 detail 뷰 호출
@login_required
def qregister(request):
    #사용자의 요청방식을 구분해 처리
     if request.method=="GET" :
        #QuestionForm 객체 생성
        #모델폼클래스 객체 생성 시 매개변수에 아무런 값도 전달하지 않는 경우, 입력방식에 값이 비어 있는 형태로 객체가 생성됨
        #값이 비어 있는 형태로 객체가 생성됨
        f=QuestionForm()
        #HTML 파일에 폼객체 전달
        return render(request, 'vote/qregister.html',{'f':f})
     #사용자 요청이 POST방식일 때   
     elif request.method =="POST" :
       #사용자가 보낸 데이터를 기반으로 QuestionForm 객체 생성
       #request.POST:POST 방식으로 요청했을 때 동봉된 데이터(사전형)
       f=QuestionForm(request.POST)
       #사용자가 보낸 데이터가 유효한 값인지 확인
       if f.is_valid():
            #폼객체.is_valid(): 사용자 입력이 유효한 값인 경우 True, 유효하지 않는 값이 입력되면 False 반환
            #폼객체.is_valid() 결과로 True가 반환된 경우, 폼객체에 들어 있는 값
            #데이터들을 추출할 수 있음->폼객체 .cleaned_data 변수 사용가능
            #ex) QuestionForm 객체.cleaned_data['name'] 사용 가능
            print('cleaned_data["name"]', f.cleaned_data['name'])
            #모델폼객체(QuestionForm) 기반으로 모델객체(Question)객체 생성
            #모델폼객체.save(): 연동된 모델클래스의 객체로 변환 및 반환, 데이터베이스에 저장
            #QuestionForm으로 Question 객체 저장 시, date 변수에 값이 없어 데이터베이스에 저장 시 에러가 발생
            #모델폼객체.save(commit=False): 연동된 모델클래스의 객체로 변환 및 반환
            q=f.save(commit=False) #Question 객체 생성 후 q변수에 저장
            #값이 비어 있는 date변수에 값 채우기
            q.date=datetime.now()#현재 컴퓨터의 날짜/시간정보를 date변수에 저장
            print('데이터베이스에 저장되기 전 Question 객체의 id값', q.id)
            #데이터베이스에 저장
            q.save()
            print('데이터베이스에 저장된 후 id 값', q.id)
            #새로 생성된 객체의 id값을 통해 detail 뷰 호출
            return HttpResponseRedirect(reverse('vote:detail', args=(q.id,)))         
            
            
   
#Question 객체를 사용자가 수정하는 뷰
def qupdate(request, q_id):
     #수정하고자 하는 객체를 추출
     q=get_object_or_404(Question, id=q_id)
     #GET, POST 방식 분류
     #GET 방식
     if request.method=='GET':
        #데이터베이스에 저장된 객체를 기반으로 QuestionForm 객체를 생성
        #HTML 코드로 변환 시 빈칸이 아닌 해당 객체에 저장된 값으로 채워진 형태로 변환됨
        f=QuestionForm(instance=q)
        #생성된 QuestionForm 객체를 HTML에 전달 및 전송
        #qregister.html과 유사하게 HTML코드가 구현되기 때문에 기존에 만들어진 HTML 파일을 재사용. form태그의 action속성을 빈칸으로 처리했기 때문에,
        #qregister 뷰에서 qregister.html를 쓴 것과, qupdate 뷰에서 qregister.html를 쓴 결과가 각자의 뷰함수로 POST 요청을 함
        return render(request, 'vote/qregister.html',{'f':f})
     #POST 방식
     elif request.method=='POST':
        #데이터베이스에 저장된 객체+사용자의 입력데이터를 기반으로 QuestionForm객체생성
        f=QuestionForm(request.POST, instance=q)
        #유효한 값이 들어 있는지 확인
        if f.is_valid():
                #데이터베이스에 저장
                qu=f.save()
                print('사용자 요청으로 찾은 객체:', q)
                print('값이 수정된 객체:', qu)
                #이동할 URL주소 클라이언트에게 전달
                return HttpResponseRedirect(reverse('vote:detail', args=(q.id,)))
                
                           
#Question 객체 삭제
@login_required
def qdelete(request, q_id):
    #삭제할 Question 객체 추출
    q=get_object_or_404(Question, id=q_id)
    #삭제함수 호출
    print('데이터베이스에 삭제되기전 id변수:', q.id)
    #해당 객체를 데이터베이스에서 삭제함. 삭제한 객체에 저장된 변수값은 사용할 수 있음
    q.delete()
    print('삭제된 후 id변수값:', q.id)
    #다른 URL or HTML 파일 전달
    return HttpResponseRedirect(reverse('vote:index'))

#Choice 객체 등록
@login_required
def cregister(request):
    if request.method == 'GET':
        f=ChoiceForm()
        #->HTML
        print('f.as_table()에서 반환하는 값: ',f.as_table())
        return render(request, 'vote/cform.html',{'i':f.as_table()})
    elif request.method=="POST":
        #사용자 입력기반 ChoiceForm객체 생성, 유효값 확인, Choce객체 변환 및 저장
        f=ChoiceForm(data=request.POST)#ChoiceForm(request.POST)
        if f.is_valid():#사용자 입력이 유효한 값일때의 처리
            #사용자 입력으로 Choice 객체에 변수들의 값이 채워진 상태이므로 바로 데이터베이스에 저장해도 됨
            c=f.save()#c: 사용자 입력기반의 새로운 Choce 객체
            #c.q.id:Choice 객체가 연결한 Question객체의 id값
            return HttpResponseRedirect(reverse('vote:detail',args=(c.q.id,)))    
        else:# 사용자 입력이 유효하지 않는 값일때의 처리
            #f: 사용자가 입력한 데이터를 바탕으로 생성된 form객체.
            #=>입력공간이 빈칸이 아니라 사용자 입력으로 채워져있음
            return render(request, 'vote/cform.html', {'i':f.as_table(), 'error':'잘못된 입력입니다'})
            pass
#Choice 객체 수정
@login_required
def cupdate(request, c_id):
     #수정할 Choice 객체 추출
     c=get_object_or_404(Choice, id=c_id)
     #GET, POST 분리
     if request.method=="GET":
        
            #ChoiceForm 객체 생성 - Choice 객체 기반
            f=ChoiceForm(instance=c)
            #HTML 전달
            return render(request, 'vote/cform.html', {'i':f.as_table()})
     #POST
     elif request.method == "POST":
            
            #ChoiceForm 객체 생성- Choice객체 + 사용자 입력
            f=ChoiceForm(request.POST, instance=c)
            #유효한 값인지 확인
            if f.is_valid():
                    #데이터베이스에 수정사항 반영
                    #c변수와 f.save()함수에서 주는 Choice객체가 동일하기 때문에 변수에 저장하지 않음
                    f.save()
                    #다른 URL을 사용자에게 전송
                    return HttpResponseRedirect(reverse('vote:detail', args=(c.q.id,)))
                    
                    
#Choice 객체 삭제
@login_required
def cdelete(request, c_id):
    c=get_object_or_404(Choice, id=c_id)
    c.delete()
    return HttpResponseRedirect(reverse('vote:detail', args=(c.q.id,) ) )