from rest_framework import serializers
from .models import Segment, Brand, Vehicle
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    #決まり
    class Meta:
        model = User
        #serializerで取り扱う値を定義
        fields = ['id', 'username', 'password']
        #追加の設定(getでは渡さないようにする,入力が必須である,最小文字列)
        extra_kwargs = {'password': {'write_only': True, 'required': True, 'min_length': 5}}

        # createのserializerをカスタマイズ(ハッシュ化するなど)
        # createのメソッドをオーバーライドし、新しくユーザーを新規で作成するメソッドを作成する
        # validated_dataには、extra_kwargsで設定した条件を通ったusernameとpasswordのみが入る
        # extra_kwargsの条件を満たさなかった場合はvalidated_dataにからの辞書型が渡される
    def create(self, validated_data):
        # djangoのUserに準備してあるもので、パスワードのハッシュ化を行い新しいユーザーをuserに入れてくれる
        # 辞書型を関数の引数にはできないため、引数に入れれる形式に変換するために「**」がついている
        user = User.objects.create_user(**validated_data)
        return user


class SegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Segment
        fields = ['is', 'segment_name']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['is', 'brand_name']


class VehicleSerializer(serializers.ModelSerializer):
    # fields内で使うsegment_nameを定義
    # 紐付いているオブジェクトが持っている特定の属性にアクセスできるようにしている
    #引数のsourceのsegmentがmodelの名前、segment_nameが取得したい、segmentがもつ属性
    segment_name = serializers.ReadOnlyField(source='segment.segment_name', read_only=True)
    brand_name = serializers.ReadOnlyField(source='brand.brand_name', read_only=True)

    class Meta:
        model = Vehicle
        #getメソッドでデータを返す場合は、foreignKeyで紐付いているオブジェクトのidしか返らない。(segmentとbrand)
        #新しくsegmentとbrandのオブジェクト内の、segment_nameとbrand_nameを使って文字列を表示したいから、fieldに追加
        fields = ['is', 'vehicle_name', 'release_year', 'price', 'segment','brand', 'segment_name', 'brand_name']
        # viewsで、登録した人が誰なのかをログインしている情報から取得するため、readonlyに設定
        extra_kwargs = {'user': {'read_only': True}}