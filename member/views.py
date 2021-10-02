from django.shortcuts import render
from .models import User
import os
from .forms import UploadFileForm
#from django.contrib import messages
from .models import Human
from .models import PasswordStorage
from django.http import JsonResponse
from django.core.mail import send_mail
import json

###################################################################################################
#체크박스 실습 예제
def checkbox_result(req) :
    list = req.POST.getlist('my_id[]')
    return render(req, 'checkbox_result.html', {'result': req.POST.getlist('my_id[]')})

def checkbox(req) :
    return render(req, 'checkbox.html')

###################################################################################################
#파일업로드 실습 예제
def upload_file( req ):

    if req.method == 'POST':
        form = UploadFileForm(req.POST, req.FILES)

        if form.is_valid():
            ssac_upload(req.FILES['file'])
            return render(req, 'uploadend.html')
    else:
        form = UploadFileForm()
        return render(req, 'upload.html', {'form': form})

def ssac_upload( f ):
    with open( os.path.abspath( './member/static/'+ str( f ) ), 'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)

###################################################################################################
#ajax 실습예제
def ajax_test( req ) :
    return render( req, 'a.html', {'parameter1' : req.POST.get('userid'),
                                'parameter2' : req.POST.get('password')})

def ajax( req ) :
    return render ( req, 'ajax.html')


###################################################################################################
# 새로 제작 (두번째)
def register_test( req ):   # 회원가입 페이지
    return render( req, 'register_test.html')

def registered_test ( req ):    # 회원가입 완료 페이지
    registered_test_member = Human(human_id = req.POST.get('human_id'),
                            human_name = req.POST.get('human_name'),
                            human_password = req.POST.get('human_password'))
    
    is_Human = Human.objects.filter ( userid = req.POST.get('human_id'))

    if is_Human :   # 아이디 중복시 회원가입 실패로 처리
        return render(req, "registerFail.html")

    registered_test_member.save()

    return render (req, 'registered_test.html', {'human_id': req.POST.get('human_id'),
                                                'human_name': req.POST.get('human_name'),
                                                'human_password': req.POST.get('human_password')})

def logined_test( req ):    # 메인페이지
    logged_human = Human.objects.filter ( human_id = req.POST.get('human_id'),
                                        human_password = req.POST.get('human_password') )
    print("logged_human")
    print(logged_human)
    if logged_human:
        req.session['human_id'] = logged_human[0].human_id

        if req.session.get('human_id'):
            return render( req, 'main_test.html', {'human_id': req.POST.get('human_id'),
                                                'human_name': logged_human[0].human_name})
        else:
            return render( req, 'nosession_test.html')

    return render(req, 'loginfail_test.html')

def my_page_test ( req ) :    # 마이페이지
    if req.session.get('human_id'):
        global getHuman
        getHuman = Human.objects.get(human_id = req.session.get('human_id'))
        return render( req, 'myPage.html', {'human_id' : getHuman.human_id, 
                                            'human_name' : getHuman.human_name, 
                                            'human_password' : getHuman.human_password})
    else:
        return render( req, 'nosession_test.html')

def login_test ( req ):     # 로그인 페이지
    return render( req, 'login_test.html' )

def update_test ( req ):    #
    human = getHuman
    if not req.POST.get('editPassword_test'):  # password 공백일 때 유저정보가 변경되지 않고 메인페이지로 이동
        print("password 공백이므로 유저정보가 변경되지 않고 메인페이지로 이동")
        return render( req, 'main_test.html')

    if not req.POST.get('editHumanName_test'):   # humanName 공백일 때 유저정보가 변경되지 않고 메인페이지로 이동
        print("humanName 공백이므로 유저정보가 변경되지 않고 메인페이지로 이동")
        return render( req, 'main_test.html')

    human.human_name = req.POST.get('editHumanName_test')
    human.human_password = req.POST.get('editPassword_test')
    human.save()

    return render( req, 'login_test.html')

def delete_test ( req ):
    human = getHuman
    human.delete()

    return render( req, 'register_test.html')

def logout_test ( req ):
    req.session.pop('human_id')

    return render(req, 'login_test.html')

###################################################################################################
# 메인페이지 유저가 등록한 패스워드를 처리하는 부분

def password_save( req ):
    setPassword = PasswordStorage(human_id = req.session['human_id'],
                                site_name = req.POST.get('siteName'),
                                site_password = req.POST.get('userPassword'))

    print(setPassword.site_password)
    if setPassword == None or setPassword.site_password == None:
        return render(req, 'main_test.html')

    setPassword.save()
    return render(req, 'main_test.html')

def password_show( req ):
    thatPassword = PasswordStorage.objects.filter( human_id = req.session.get('human_id'),
                                                    site_name = req.POST.get('siteName'))

    return JsonResponse({'showPassword' : thatPassword[0].site_password}, status=200)

def password_get( req ):
    thatUser = PasswordStorage.objects.filter ( human_id = req.session.get('human_id'),
                                                site_name = req.POST.get('siteName'))
    isIt = 0
    if not thatUser:
        isIt = 0
        print("해당 사이트에 유저가 등록한 비밀번호가 없습니다.")
        return JsonResponse({'isIt': isIt}, status=200)
    else:
        isIt = 1
        print("유저가 패스워드를 등록한 사이트를 불러옵니다.")
        return JsonResponse({'isIt': isIt}, status=200)


def password_edit( req ):
    print("password_edit")
    userFilter = PasswordStorage.objects.filter ( human_id = req.session.get('human_id'),
                                                site_name = req.POST.get('siteName'))

    changePassword = req.POST.get('changePassword')

    getUserPassword = PasswordStorage.objects.get(human_id = req.session.get('human_id'),
                                                site_name = req.POST.get('siteName'))
    
    getUserPassword.site_password = changePassword
    getUserPassword.save()

    return render( req, 'main_test.html')

def contact( req ):
    contact_human = Human.objects.filter ( human_id = req.POST.get('human_id'),
                                        human_name = req.POST.get('human_name'),
                                        phone = req.POST.get('phone') )
    
    content = req.POST.get('content')

    send_mail(
    'Subject here',
    phone,
    human_id,
    content, 
    ['adasddasd12@naver.com'],
    fail_silently=False,)

    return JsonResponse({'isIt': "mailSended"}, status=200)

###################################################################################################
#회원가입, 로그인 세션까지 실습예제
def register ( req ) :      # 회원가입
    return render( req, 'register.html')

def registered ( req ) :    # 회원가입 완료
    registered_member = User(userid = req.POST.get('userid'), 
                            username = req.POST.get('username'), 
                            password = req.POST.get('password')
                            )

    is_member = User.objects.filter ( userid = req.POST.get('userid'))

    if is_member :
        return render(req, "registerFail.html")

    registered_member.save()    # 회원가입할때 작성했던 회원정보 저장(DB에)
    print("저장됨?")
    print(registered_member)

    return render ( req, 'registered.html', {'userid': req.POST.get('userid'), 
                                            'username': req.POST.get('username'), 
                                            'password': req.POST.get('password')} )

def login ( req ) :     # 로그인
    return render( req, 'login.html' )

def goShop(req) :   # 쇼핑몰 페이지(main.html)
    logged_member = User.objects.filter ( userid = req.POST.get('userid'),
                                        password = req.POST.get('password') )
    print("무엇?")
    print(logged_member)
    if logged_member:   # 해당하는 유저가 있다면
        global isLogged     # 유저정보를 저장할 전역 변수

        req.session['userid'] = logged_member[0].userid

        if not req.session.get('userid'):      # 세션을 못받아왔을 때 이동하는 페이지
            return render( req, 'nosession.html')

        isLogged = User.objects.get(userid=logged_member[0].userid) # 로그인한 유저를 전역변수 "isLogged"에 저장

        return render(req, 'main.html')

    else :  # 로그인 실패 시(해당하는 유저정보가 없을 때)
        return render(req, 'fail.html')

    
def logged ( req ) :    # 마이페이지
    if req.session.get('userid'):      # 세션을 못받아왔으때 이동하는 페이지
            return render( req, 'logged.html', {'username' : isLogged.username} )
    else :
            return render( req, 'nosession.html')

def update( req ) :     # 비밀번호 변경
    user = isLogged
    user.password = req.POST.get('editPassword')    # input name 으로 받아옴
    user.save()     # 변경된 비밀번호로 유저 저장
    print("호출")

    return render(req, "login.html")
    
def delete ( req ) :    # 유저 삭제
    user = isLogged
    user.delete()

    return render(req, "register.html")

def logout(req) :   # 로그아웃
    req.session.pop('userid')   # 세션 삭제
    #req.session.clear()   # 세션 다날라감(admin페이지도)

    return render(req, 'login.html')

###########################################################################################################################
def search ( req ) :
    all_member = User.objects.filter( username = "이상훈", 
                                    password="0000" )

    return render( req, 'g.html', { 'total_member' : all_member } )


def rec ( req ) :
    new_member = User (userid = req.POST.get('userid'), 
                        username = req.POST.get('username'), 
                        password = req.POST.get('password'), 
                        gender = req.POST.get('gender') )

    new_member.save()
    return render( req, 'registered.html' )


def hello( req ) : 
    return render(req, 'a.html')

def send( req ) :
    return render( req, 'b.html')

# def rec( req ) :
#   #print( req.GET.get('hahahah') )   #get방식
#
#    return render ( req, 'd.html', { 
#                                    'info_1' : req.POST.get('name'),
#                                    'info_2' : req.POST.get('id'),
#                                    'info_3' : req.POST.get('pw'),
#                                    'info_4' : req.POST.get('pwCheck')
#                                    })     #post방식

def novel ( req, chapter, player1, player2 ) :
    return render(req, 'c.html', { 
                                    'c' : chapter,
                                    'p1': player1, 
                                    'p2' : player2
                                })

def urltest( req ) : 
    return render( req, 'e.html')

def static ( req ) :
    return render( req, 'f.html')
    
