from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Segment
from .serializers import SegmentSerializer

SEGMENTS_URL = '/api/segments/'

#segmentのobjectを新しく作成
def create_segment(segment_name):
    return Segment.objects.create(segment_name=segment_name)

#reverseはurlのpathの生成
#引数にmodel名と-detailを指定するとdjangoが自動で、末尾にidを追加してくれる。127.0.0.1:8000/api/segment/segment_id
def detail_url(segment_id):
    return reverse('api:segment-detail', args=[segment_id])

#tokenの認証が通ったuserに対するテスト
class AuthorizedSegmentApiTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='dummy', password='dummy_pw')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    #getメソッドでsegmentの一覧が取得できるかのテスト
    def test_2_1_should_get_all_segments(self):
        #セグメントを2つ作成
        create_segment(segment_name="SUV")
        create_segment(segment_name="Sedan")
        #segmentをgetメソッドで、api経由で取得
        res = self.client.get(SEGMENTS_URL)
        #databaseのobjectの一覧を取得
        #Segment.objects.all()でobjectをすべて取得。.order_by('id')でid順で並び替え
        segments = Segment.objects.all().order_by('id')
        #serializerを通して辞書型に変換
        #segmentが複数ある場合は、manyをTrueに。
        serializer = SegmentSerializer(segments, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    #getメソッドでidを指定して一つのメソッドを取得できるかのテスト
    def test_2_2_should_get_single_segment(self):
        segment = create_segment(segment_name="SUV")
        #上で作成したdetail_urlを呼び出して、引数にidを渡す。
        url = detail_url(segment.id)
        print(url)
        #生成したurl(127.0.0.1:8000/api/segment/segment_id)にアクセスしレスポンスを取得
        res = self.client.get(url)
        #辞書型に変換
        serializer = SegmentSerializer(segment)
        self.assertEqual(res.data, serializer.data)
    
    #新規でsegmentを作成できるかのテスト
    def test_2_3_should_create_new_segment_successfully(self):
        #作成できるか
        payload = {'segment_name': 'K-Car'}
        res = self.client.post(SEGMENTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        #databaseに存在するか
        #存在すればexistsにTrueが返る
        exists = Segment.objects.filter(
            segment_name=payload['segment_name']
        ).exists()
        self.assertTrue(exists)

    #segmentの名前を空にした場合にエラーが返るかのテスト
    def test_2_4_should_not_create_new_segment_with_invalid(self):
        payload = {'segment_name': ''}
        res = self.client.post(SEGMENTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    #データがたくさんある場合はPATCHを使うと効率的に更新することができる
    #segmentをPATCHで変更できるか
    def test_2_5_should_partial_update_segment(self):
        #segment作成
        segment = create_segment(segment_name="SUV")
        #変更したいsegmentの名前
        payload = {'segment_name': 'Compact SUV'}
        #SUVのsegmentへのurlを作成
        url = detail_url(segment.id)
        #パーシャルアップデートを実行
        self.client.patch(url, payload)
        #最新のsegmentの情報にupload
        segment.refresh_from_db()
        #segmentの名前がCompact SUVと一致するか
        self.assertEqual(segment.segment_name, payload['segment_name'])

    #segmentをPUTで変更できるか
    def test_2_6_should_update_segment(self):
        segment = create_segment(segment_name="SUV")
        payload = {'segment_name': 'Compact SUV'}
        url = detail_url(segment.id)
        self.client.put(url, payload)
        segment.refresh_from_db()
        self.assertEqual(segment.segment_name, payload['segment_name'])

    #deleteのテスト
    def test_2_7_should_delete_segment(self):
        segment = create_segment(segment_name="SUV")
        #databaseにあるsegmentの数をカウントし、1に一致するか
        self.assertEqual(1, Segment.objects.count())
        url = detail_url(segment.id)
        #消したいsegmentのエンドポイントにdeleteのメソッドでアクセス
        self.client.delete(url)
        self.assertEqual(0, Segment.objects.count())

#ログイン認証が通っていないユーザーに対するテスト
class UnauthorizedSegmentApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_2_8_should_not_get_segments_when_unauthorized(self):
        res = self.client.get(SEGMENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)