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


#token認証が通っていないユーザーに対するテスト
class UnauthorizedUserApiTests(TestCase):
    #認証が必要ないためクライアントの設定のみ
    def setUp(self):
        self.client = APIClient()

    #ユーザーがきちんと作れるかどうかのテスト
    def test_1_4_should_create_new_user(self):
        payload = {
            'username': 'dummy',
            'password': 'dummy_pw',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        #createで作ったユーザーデータ(res.data)をgetで取得してuserに格納
        user = get_user_model().objects.get(**res.data)
        #新たに作成したユーザーのパスワードが一致しているかの確認
        #databaseではpwはハッシュ化されており直接は比較できないため、check_passwordメソッドを使って判定する。bool型で返る。
        #assertTrueは、Trueならpassするやつ
        self.assertTrue(
            user.check_password(payload['password'])
        )
        #返ってきたres.dataに'password'属性が入っていなければpassするやつ
        self.assertNotIn('password', res.data)

    #同じusernameでcreateしようとした場合にエラーを返すかのテスト
    def test_1_5_should_not_create_user_by_same_credentials(self):
        payload = {
            'username': 'dummy',
            'password': 'dummy_pw',
        }
        #**で辞書型を引数に変換
        get_user_model().objects.create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    #pwの文字数制限のテスト
    def test_1_6_should_not_create_user_with_short_pw(self):
        payload = {'username': 'dummy', 'password': 'pw'}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    #tokenが取得できるかのテスト
    def test_1_7_should_response_token(self):
        payload = {'username': 'dummy', 'password': 'dummy_pw'}
        get_user_model().objects.create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        #レスポンスの中(res.data)にtokenの属性が含まれているかのテスト
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    #間違ったユーザー情報でtokenを取得しようとした場合にエラーが出るかのテスト
    def test_1_8_should_not_response_token_with_invalid_credentials(self):
        get_user_model().objects.create_user(username='dummy', password='dummy_pw')
        #違うユーザーでtokenエンドポイントへアクセス
        payload = {'username': 'dummy', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        #レスポンスのデータにtokenの属性が含まれていないことを確認
        self.assertNotIn('token', res.data)
        #ステータスコードが400番であるかを確認
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    #存在しないユーザーでtokenを取得しようとした場合にエラーが出るかのテスト
    def test_1_9_should_not_response_token_with_non_exist_credentials(self):
        payload = {'username': 'dummy', 'password': 'dummy_pw'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    #passwordが空の場合にエラーが返るかのテスト
    def test_1__10_should_not_response_token_with_missing_field(self):
        get_user_model().objects.create_user(username='dummy', password='dummy_pw')
        payload = {'username': 'dummy', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    #usernameもpasswordも空の場合にエラーが返るか
    def test_1__11_should_not_response_token_with_missing_field(self):
        get_user_model().objects.create_user(username='dummy', password='dummy_pw')
        payload = {'username': '', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    #token認証をせずにprofileへアクセスした場合にエラーが出るか
    def test_1__12_should_not_get_user_profile_when_unauthorized(self):
        res = self.client.get(PROFILE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
