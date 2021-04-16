from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

#テストするユーザー関連のエンドポイント
CREATE_USER_URL = '/api/create'
PROFILE_URL = '/api/profile/'
TOKEN_URL = '/api/auth/'


#TestCaseクラスからの継承
#class名自由
class AuthorizeUserApiTests(TestCase):
    #setupメソッドは各テストケースの最初に必ず実行される
    def setUp(self):
        #test用のユーザーを新規で作成
        self.user = get_user_model().objects.create_user(username='dummy', password='dummy_pw')
        #test用のクライアントを作成
        self.client = APIClient()
        #上のクライアントからの認証をテスト用に強制的に、self.userを使って通す
        self.client.force_authenticate(user=self.user)

    
    #プロフィールのエンドポイントで、ログインしているユーザー情報が取得できるかのテスト
    #test_1はファイル名の連番、次の１はこのあとのテストの連番
    def test_1_1_should_get_user_profile(self):
        #getメソッドでPROFILE_URLのエンドポイントにアクセスし、restに返ってきた値を格納
        res = self.client.get(PROFILE_URL)

        #レスポンスの内容を評価↓
        #レスポンスの中にあるstateが200番に一致するかどうかの評価
        #一致すればokでpassする
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        #レスポンスのデータがログインしているユーザーのidとユーザーネームに一致しているかどうかの評価
        self.assertEqual(res.data, {
            'id': self.user.id,
            'username': self.user.username,
        })
    
    #プロフィールのエンドポイントではPUTとPATCHをできないように設定したのでそれのテスト
    def test_1_2_should_not_allowed_by_PUT(self):
        #PUTメソッドで渡すjsonの内容を定義
        #任意の値でおけ
        payload = {
            'username': 'dummy',
            'password': 'dummy_pw'
        }
        #クライアントからPROFILE_URLのエンドポイントに、jsonのpayloadをPUTで渡してアクセス
        res = self.client.put(PROFILE_URL, payload)
        #status_codeが405番と一致するか
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_1_3_should_not_allowed_by_PATCH(self):
        payload = {
            'username': 'dummy',
            'password': 'dummy_pw'
        }
        res = self.client.patch(PROFILE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)