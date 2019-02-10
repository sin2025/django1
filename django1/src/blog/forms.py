'''
Created on 2019. 2. 9.

@author: user
'''
from .models import Post
from django import forms
from pip._vendor.pkg_resources import require

#글쓰기에 사용할 폼클래스-모델폼클래스 상속
class PostForm(forms.ModelForm):
    #사용자가 첨부파일, 이미지를 업로드할 수 있도록 커스텀 입력양식 생성
    #required=False: 해당<input>을 사용자가 필수로 입력하지 않아도 되는 설정
    #첨부파일을 꼭 업로드하지 않아도 되는 설정
    #clearabelFileInput:<input type='file'> 형태의 입력공간에 파일관련 추가설정을 할 수 있는 위젯
    #multiple:하나의 입력공간에 여러개의 파일을 업로드할 수 있도록 허용
    files=forms.FileField(required=False,widget=forms.ClearableFileInput(attrs={'multiple':True}))
    
    images=forms.ImageField(required=False,widget=forms.ClearableFileInput(attrs={'multiple':True}))
    
    
    class Meta:
        model=Post
        fields=['category','headline','content']
        