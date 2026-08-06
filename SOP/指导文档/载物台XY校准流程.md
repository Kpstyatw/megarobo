# 载物台XY校准流程

**校准步骤**

1.  将校准块按照图示方向放入载物台
    
    ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/meonarb98AywjqXx/img/39416924-f663-495d-9dac-f600b6ecef5c.png)
    
2.  打开NUC，设备ID输入CellVue，登录
    
    ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/meonarb98AywjqXx/img/d13fa271-2e2b-4cf3-989b-0ff8a2d657d9.png)
    
3.  调试界面点击打开，设备进行初始化。初始化完成后，实况界面可以看到设备状态为Idle
    
    ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/jP2lRYjypXwymO8g/img/d40f8c35-a3f4-4879-bd25-d2796aafb53f.png)
    
4.  安全起见，在示教界面，Z轴导轨坐标输入1200，点击滑动到，使Z轴运动到1200
    
    ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/jP2lRYjypXwymO8g/img/95cd29a7-b93f-4635-b1cf-c1c1935d2a53.png)
    
5.  调试界面找到相机，修改视频前的ROI长宽和偏移，如下
    
    ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/meonarb98AywjqXx/img/440e78ba-d95e-4e76-b0a2-4680a4567db5.png)
    
6.  W索引选择20xAPO或40x物镜所在位置，注意1号位置索引为0，点击切换镜头，切换到高倍镜
    
    ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/jP2lRYjypXwymO8g/img/00c638e8-1d10-40aa-80e8-ef5b119a3965.png)
    
7.  调试界面，X输入20，Y输入56，点击运动XY，去找P1点
    
    ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/jP2lRYjypXwymO8g/img/2da23256-a891-4825-b9f4-26b7d9162292.png)
    
8.  点击视频按钮，弹窗显示实时图像，
    
    ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/jP2lRYjypXwymO8g/img/b03fbd7e-942e-445b-91c4-8e323eebc4c9.png)
    
9.  如果曝光参数不合适，修改曝光参数后，点击设置视频参数
    
    ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/jP2lRYjypXwymO8g/img/d3429bab-c768-4e75-84fe-bc7a6eafbfbc.png)
    
10.  按下箱体上的开仓按钮，通过手柄调整P1孔接近物镜中心，调整接近后，按下箱体的关仓按钮
    
11.  点击示教，调整Z的坐标为2500，此时查看视频窗口，勾选上中心线，基本能看到P1角，通过手柄调整Z找到焦面使图片清晰
    
    ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/jP2lRYjypXwymO8g/img/a1b75563-4fce-4226-9bed-e6b6eab3756e.png)
    
12.  观察相机视频中的图像情况，通过示教界面调整XYZ的步长点击加、减，同时观察实时图像，直到找到焦面，且P1点位于视野中心
    
    ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/jP2lRYjypXwymO8g/img/1aba183f-21d5-400c-bfad-75e2cb1ecd33.png)
    
    P1孔实例![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/jP2lRYjypXwymO8g/img/53b99644-1cfe-443b-8483-a8faf785d7fb.png)
    
13.  点击示教界面最下方，“校准XY”按钮，弹出校准弹窗,在校准XY界面点击P1点的获取坐标
    
    ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/jP2lRYjypXwymO8g/img/6897bf07-e716-4137-8da7-98096e702607.png)
    
14.  同理，在调试界面，X输入72，Y输入18，点击运动XY，去找P2点
    
    ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/jP2lRYjypXwymO8g/img/b2fc8630-0395-4afc-a5f6-d0f7a31bd402.png)
    
15.  通过示教界面调整XY的步长点击加、减，同时观察实时图像，直到P2点位于视野中心
    
    P2孔![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/jP2lRYjypXwymO8g/img/65bcf754-ba12-45b1-a127-2e9f4ad39e65.png)
    
16.  在校准XY界面点击P2点的获取坐标
    
    ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/jP2lRYjypXwymO8g/img/830e239b-1878-4e75-9fa9-ee80b0d544d2.png)
    
17.  在校准XY界面，点击P1孔的移动至，回到P1
    
    ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/jP2lRYjypXwymO8g/img/2ac2bb25-b682-4022-b87f-4736bd386024.png)
    
18.  通过调整X Y的步进，移动P1点，使P1是在十字的横线上
    
    R角
    
    ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/jP2lRYjypXwymO8g/img/b2274891-a815-4c7f-aed9-7ccb6a091421.png)
    
    ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/jP2lRYjypXwymO8g/img/7af4fd72-f69d-4ecd-9cf1-d163ff7517eb.png)
    
19.  点击校准，保存对应的数据，关闭校准XY弹窗
    
    ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/jP2lRYjypXwymO8g/img/3118149f-cd92-475a-8855-72d345d5ba5d.png)
    
    ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/jP2lRYjypXwymO8g/img/ac86f4a6-f2ef-464c-a050-571d6d4ef884.png)
    
20.  在调试界面X输入102，Y输入56，查看实时图像，如P3点大概位于视野中心，则校准成功。如偏差过大，则需要重新校准。
    
    ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/jP2lRYjypXwymO8g/img/7b978b0a-b43e-4c73-829b-92a32b7089a8.png)
    
21.  返回实况点击终止，
    
    ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/jP2lRYjypXwymO8g/img/6e55ea38-0385-46af-98c0-dc0b46f3312e.png)
    
22.  返回调试点击关闭，退出NUC![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/jP2lRYjypXwymO8g/img/e6d293d9-7989-4739-af3a-c0eb9f52dfe5.png)