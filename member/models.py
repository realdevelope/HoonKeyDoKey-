from django.db import models

# Create your models here.

#ORM의 역할 : SQL을 직접 작성하지 않아도
#             DB로 접근해서 CRUD가 가능하게 해준다.

class User(models.Model): # 여기서 모델의 이름은 User이다.

	# CharField는 문자열 필드
    # max_length 최대 길이, 길이제한

	#GENDERS = ( ('M','남성(Man)'),('W','여성(Woman)') )

    # DataTimeField auto_new_add=True
	# 0000-00-00 00:00:00 datetime

	userid=models.CharField(max_length=64, null = True, verbose_name='아이디')
	username=models.CharField(max_length=64, null = True, verbose_name='사용자명')
	password=models.CharField(max_length=64, null = True,  verbose_name='비밀번호')
	#gender=models.CharField(max_length=1, null = True,verbose_name='성별', choices=GENDERS)
	#registered=models.DateTimeField(auto_now_add=True, verbose_name='등록')

    #enum( 'M', 'W' )
	
	#TextField - 대용량 텍스트
	#IntegerField - 정수형
	# True ( 기본값은 False )


class Human(models.Model):

    human_id = models.CharField(max_length=64, verbose_name = "human_id")
    human_name = models.CharField(max_length=64, verbose_name = "human_name")
    human_password = models.CharField(max_length=64, verbose_name = "human_password")


class PasswordStorage(models.Model):

	human_id = models.CharField(max_length=64, verbose_name="human_id")
	site_name = models.CharField(max_length=64, verbose_name="site_name")
	site_password = models.CharField(max_length=15, verbose_name="site_password")