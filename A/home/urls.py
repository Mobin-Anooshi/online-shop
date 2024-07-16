from django.urls import path,include
from home import views


app_name = 'home'
bucket_urls = [
    path('',views.BucketHomeView.as_view(),name='bucket'),
    path('delete_obj/<str:key>',views.DeleteBucketObjects.as_view(),name='delete_obj_bucket'),
    path('download_obj/<str:key>',views.DownloadBucketObject.as_view(),name='download_obj_bucket'),
    # path('upload_obj/',views.UploadBucketObject.as_view(),name='upload_obj_bucket'),    
]
urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('category/<slug:category_slug>/',views.HomeView.as_view(),name='category_filter'),
    path('bucket/',include(bucket_urls)),
    path('<slug:slug>/',views.ProductDetailView.as_view(),name='product_detail'),
    
    
]
