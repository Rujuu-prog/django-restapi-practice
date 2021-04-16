from rest_framework import genetics, permission, viewsets, status
from .serializers import UserSerializer, SegmentSerializer, BrandSerializer, VehicleSerializer
from .models import Segment, Brand, Vehicle
from rest_framework.response import Response


#ユーザーを新規で作成するview
#viewの継承元にはmodelのviewセットとgenericsのviewセットがある。
#modelのviewセットは、CRUDの機能をまるごと提供してくれるもの、Createの機能に特化したいものを作りたい場合は、genericsのviewセットからCreateAPIViewを継承する
class CreateUserView(generics.CreateAPIView):
    #このviewに適用したいシリアライザーを入れる
    serializer_class = UserSerializer
    #parmissionを上書きすることで誰でもCreateUserViewにアクセスできるように変更
    parmission_classes = (permissions.AllowAny,)


#ユーザーの情報を検索して表示
class ProfileUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    #ユーザー情報を取得
    def get_object(self):
        #self.request.userがログインしているユーザーを意味しており、これでログインしているユーザーのオブジェクトを返している
        return self.request.user

    #今回はgenericsのupdateは使わないので、putメソッドでアクセスされた際にエラーを出すようにする
    #updateのメソッドをオーバーライド
    def update(self, request, *args, **kwargs):
        response = {'message': 'PUT method is not allowed'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    #今回はgenericsのpartial_updateは使わないので、patchメソッドでアクセスされた際にエラーを出すようにする
    #partial_updateのメソッドをオーバーライド
    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'PATCH method is not allowed'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)


#segmentViewSetでは、CRUDのすべての機能を使いたいため、modelのviewセットを使用
#二行書くだけでCRUDの機能を使うことができる
class SegmentViewSet(viewsets.ModelViewSet):
    #modelviewsetを使う場合は、querysetにオブジェクトの一覧を格納する必要がある
    queryset = Segment.object.all()
    serializer_class = SegmentSerializer


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.object.all()
    serializer_class = BrandSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.object.all()
    serializer_class = VehicleSerializer

    #新しくvehicleのオブジェクトを作る際にログインしているユーザーの情報を割り当てる
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


