from allauth.socialaccount.adapter import DefaultSocialAccountAdapter



class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        extra_data = sociallogin.account.extra_data
        # [추가] 터미널에서 네이버가 뭘 보내주는지 직접 확인하기
        print("======== 네이버 데이터 확인 ========")
        print(extra_data)
        print("==================================")
        if sociallogin.account.provider == 'kakao':
            kakao_nickname = extra_data.get('properties', {}).get('nickname')
            if kakao_nickname:
                user.nickname = kakao_nickname
            user.username = f"kakao_{sociallogin.account.uid}"
            
        elif sociallogin.account.provider == 'naver':
            naver_nickname = extra_data.get('nickname') 
            if naver_nickname:
                user.nickname = naver_nickname
                
            naver_mobile = extra_data.get('mobile')
            if naver_mobile:
                user.phone_number = naver_mobile

            user.username = f"naver_{sociallogin.account.uid}"
        
        user.save()
        return user