# 高内涵成像（HCS）图像分析常用算法与 Python 实现

高内涵成像（High Content Screening, HCS）典型的图像分析流程包括：

1. **图像拼接与投影**（多视野/多层图像的预处理）
2. **图像处理**（去噪、背景校正、增强）
3. **目标识别**（细胞/细胞核分割）
4. **目标测量**（形态、强度、纹理、共定位等特征提取）

主要依赖库：`scikit-image`、`opencv-python`、`scipy`、`numpy`、`pandas`，深度学习分割用 `cellpose`。

---

## 目录

- [一、图像拼接（Stitching）](#一图像拼接stitching)
- [二、图像投影（Projection）](#二图像投影projection)
- [三、图像预处理](#三图像预处理)
- [四、目标识别（分割）](#四目标识别分割)
- [五、目标测量（特征提取）](#五目标测量特征提取)
- [总结对照表](#总结对照表)

---

## 一、图像拼接（Stitching）

高内涵成像单次拍摄视野（FOV）有限，全孔或全片扫描需要将多个视野（tile）按网格排列拼接成一张大图。常见方法有基于相位相关的网格拼接、基于特征点匹配的拼接，以及专用显微镜拼接工具。

### 1. 基于相位相关（Phase Correlation）的两图拼接

适用于已知大致重叠区域、平移为主（无旋转缩放）的显微镜相邻视野拼接，精度可达亚像素级。

```python
import numpy as np
from skimage.registration import phase_cross_correlation

def stitch_two_tiles(img_left, img_right, overlap_guess=0.15):
    """基于相位相关的两张有重叠区域图像拼接（估算平移量）"""
    h, w = img_left.shape
    overlap_w = int(w * overlap_guess)

    region_left = img_left[:, -overlap_w:]
    region_right = img_right[:, :overlap_w]

    shift, error, diffphase = phase_cross_correlation(
        region_left, region_right, upsample_factor=10
    )
    dy, dx = shift

    canvas_w = w + (w - overlap_w) - int(dx)
    canvas = np.zeros((h, canvas_w), dtype=img_left.dtype)
    canvas[:, :w] = img_left
    x_offset = w - overlap_w - int(dx)
    canvas[:, x_offset:x_offset + w] = img_right
    return canvas
```

### 2. 网格拼接（多视野，按孔板扫描常见排布方式）

按已知的行列网格和重叠比例，将多个 tile 拼成完整大图（简化版，实际生产环境建议在此基础上加入互相关精配准）。

```python
import numpy as np

def stitch_grid(tiles, grid_shape, overlap=0.1):
    """
    tiles: dict {(row, col): image}
    grid_shape: (n_rows, n_cols)
    overlap: 相邻tile之间的重叠比例
    """
    n_rows, n_cols = grid_shape
    tile_h, tile_w = next(iter(tiles.values())).shape
    step_y = int(tile_h * (1 - overlap))
    step_x = int(tile_w * (1 - overlap))

    canvas_h = tile_h + step_y * (n_rows - 1)
    canvas_w = tile_w + step_x * (n_cols - 1)
    canvas = np.zeros((canvas_h, canvas_w), dtype=np.float32)
    weight = np.zeros((canvas_h, canvas_w), dtype=np.float32)

    for (r, c), tile in tiles.items():
        y0, x0 = r * step_y, c * step_x
        canvas[y0:y0 + tile_h, x0:x0 + tile_w] += tile
        weight[y0:y0 + tile_h, x0:x0 + tile_w] += 1

    weight[weight == 0] = 1
    return (canvas / weight).astype(next(iter(tiles.values())).dtype)
```

### 3. 基于特征点匹配的拼接（OpenCV，适合明场/不规则重叠图像）

```python
import cv2

def stitch_with_opencv(image_list):
    """基于SIFT/ORB特征匹配+单应性变换的通用拼接，适合非规则网格或明场图像"""
    stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)
    status, pano = stitcher.stitch(image_list)
    if status == cv2.Stitcher_OK:
        return pano
    else:
        raise RuntimeError(f"拼接失败，错误码: {status}")
```

### 4. 专用显微镜拼接工具（ASHLAR）

对于多孔板全片扫描（尤其带已知载物台坐标的场景），推荐使用专为显微镜设计的 `ASHLAR`，支持亚像素配准和多通道对齐。

```bash
# pip install ashlar
# 命令行使用，输入为一系列已知网格坐标的tile文件（如OME-TIFF）
ashlar input_files.ome.tiff -o stitched_output.ome.tiff --flip-y
```

---

## 二、图像投影（Projection）

荧光显微镜常拍摄 Z 轴堆栈（Z-stack），需要将三维体数据投影为二维图像用于后续分割与测量。常见投影方式如下。

### 1. 基础强度投影（MIP / MinIP / Mean / Sum / STD）

```python
import numpy as np
from skimage import io

z_stack = io.imread('z_stack.tif')  # shape: (Z, H, W)

mip = np.max(z_stack, axis=0)                        # 最大强度投影(MIP)：最常用，突出高亮结构（如点状信号）
min_ip = np.min(z_stack, axis=0)                      # 最小强度投影：用于观察暗区/阴影结构
mean_ip = np.mean(z_stack, axis=0)                    # 平均强度投影：降噪但会模糊细节
sum_ip = np.sum(z_stack, axis=0, dtype=np.float32)    # 总和投影：常用于定量总荧光强度（如总mRNA信号）
std_ip = np.std(z_stack, axis=0)                      # 标准差投影：突出Z轴方向强度变化剧烈的区域
```

### 2. 扩展景深投影（EDF / Focus Stacking）

当样本较厚、单一层面无法覆盖全部聚焦结构时，采用逐像素选取"最清晰Z层"的方式合成全聚焦图像，常用拉普拉斯算子局部方差作为清晰度衡量指标。

```python
import numpy as np
import cv2
from scipy.ndimage import gaussian_filter

def extended_focus_projection(z_stack, kernel_size=5):
    """
    扩展景深投影（EDF）：对每个像素选取Z轴上聚焦最清晰的切片强度值
    使用拉普拉斯算子的局部方差作为清晰度衡量指标
    """
    z, h, w = z_stack.shape
    focus_measure = np.zeros_like(z_stack, dtype=np.float32)

    for i in range(z):
        lap = cv2.Laplacian(z_stack[i].astype(np.float32), cv2.CV_32F, ksize=kernel_size)
        focus_measure[i] = gaussian_filter(lap ** 2, sigma=2)  # 局部方差近似，衡量清晰度

    best_z = np.argmax(focus_measure, axis=0)
    rows, cols = np.indices((h, w))
    edf_image = z_stack[best_z, rows, cols]
    return edf_image, best_z  # best_z 可用于生成焦平面高度图（深度图）
```

### 3. 多通道 Z-stack 投影（读取多维显微镜文件）

```python
import tifffile
import numpy as np

# 读取形如 (C, Z, H, W) 的多通道多层图像
stack = tifffile.imread('multichannel_zstack.tif')

projections = {}
for c in range(stack.shape[0]):
    projections[f'channel_{c}_MIP'] = np.max(stack[c], axis=0)
```

---

## 三、图像预处理

### 1. 光照不均校正 / 背景扣除

细胞图像常有背景荧光不均匀问题，常用滚球（rolling ball）或形态学开运算估计背景。

```python
import numpy as np
from skimage import io, restoration

img = io.imread('cell_image.tif').astype(np.float32)

background = restoration.rolling_ball(img, radius=50)
corrected = np.clip(img - background, 0, None)
```

### 2. 去噪

```python
from skimage import filters, restoration
from skimage.morphology import disk

denoised_gaussian = filters.gaussian(corrected, sigma=1)          # 高斯滤波
denoised_median = filters.median(corrected, disk(3))              # 中值滤波，抗椒盐噪声
denoised_nlm = restoration.denoise_nl_means(corrected, patch_size=5, patch_distance=6)  # 非局部均值，保边缘
```

### 3. 对比度增强 / 强度归一化

```python
from skimage import exposure

img_clahe = exposure.equalize_adapthist(denoised_gaussian, clip_limit=0.01)  # CLAHE

p2, p98 = np.percentile(denoised_gaussian, (2, 98))                          # 百分位拉伸（常用于批量归一化）
img_norm = exposure.rescale_intensity(denoised_gaussian, in_range=(p2, p98))
```

---

## 四、目标识别（分割）

### 1. Otsu 全局阈值分割

最基础的细胞/细胞核前景分割方法。

```python
from skimage import filters
from skimage.measure import label

thresh = filters.threshold_otsu(img_norm)
binary = img_norm > thresh
labeled_mask = label(binary)
```

### 2. 分水岭分割（分离粘连细胞/细胞核）

高内涵图像中细胞常密集粘连，需要基于距离变换+分水岭分离。

```python
from scipy import ndimage as ndi
from skimage.feature import peak_local_max
from skimage.segmentation import watershed

distance = ndi.distance_transform_edt(binary)
coords = peak_local_max(distance, min_distance=10, labels=binary)
mask = np.zeros(distance.shape, dtype=bool)
mask[tuple(coords.T)] = True
markers, _ = ndi.label(mask)

labels_ws = watershed(-distance, markers, mask=binary)
```

### 3. Cellpose 深度学习分割（目前HCS中最常用的细胞/细胞核分割工具）

比传统阈值+分水岭更鲁棒，尤其适合密集、不规则形态的细胞。

```python
# pip install cellpose
from cellpose import models

model = models.Cellpose(model_type='cyto')  # 'nuclei' 用于细胞核
masks, flows, styles, diams = model.eval(img_norm, diameter=None, channels=[0, 0])
```

### 4. 连通域标记与计数

```python
from skimage.measure import label

labeled_array, num_objects = label(binary, connectivity=2, return_num=True)
print(f"检测到 {num_objects} 个目标")
```

---

## 五、目标测量（特征提取）

### 1. 形态学特征

```python
from skimage.measure import regionprops_table
import pandas as pd

props = regionprops_table(
    labeled_array, intensity_image=img_norm,
    properties=['label', 'area', 'perimeter', 'eccentricity',
                'solidity', 'major_axis_length', 'minor_axis_length',
                'mean_intensity', 'centroid']
)
df = pd.DataFrame(props)
```

### 2. 多通道荧光强度测量（每个细胞对应通道的表达量）

```python
# channel2 为另一荧光通道（如GFP标记蛋白）
intensity_props = regionprops_table(
    labeled_array, intensity_image=channel2,
    properties=['label', 'mean_intensity', 'max_intensity', 'min_intensity']
)
df_intensity = pd.DataFrame(intensity_props)
```

### 3. 纹理特征（GLCM，用于表征细胞质/细胞核纹理异质性）

```python
from skimage.feature import graycomatrix, graycoprops

img_uint8 = exposure.rescale_intensity(img_norm, out_range=(0, 255)).astype('uint8')
glcm = graycomatrix(img_uint8, distances=[1], angles=[0], levels=256,
                     symmetric=True, normed=True)

contrast = graycoprops(glcm, 'contrast')[0, 0]
homogeneity = graycoprops(glcm, 'homogeneity')[0, 0]
energy = graycoprops(glcm, 'energy')[0, 0]
```

### 4. 共定位分析（两通道荧光信号共定位程度）

```python
def pearson_colocalization(ch1, ch2, mask):
    return np.corrcoef(ch1[mask], ch2[mask])[0, 1]

def manders_coefficients(ch1, ch2, mask, thresh1, thresh2):
    ch1_m, ch2_m = ch1[mask], ch2[mask]
    M1 = np.sum(ch1_m[ch2_m > thresh2]) / np.sum(ch1_m)
    M2 = np.sum(ch2_m[ch1_m > thresh1]) / np.sum(ch2_m)
    return M1, M2
```

---

## 总结对照表

| 阶段 | 常用算法 | 主要库 |
|---|---|---|
| 图像拼接 | 相位相关网格拼接、特征点匹配拼接、ASHLAR专用拼接 | skimage.registration, opencv-python, ashlar |
| 图像投影 | MIP/MinIP/Mean/Sum/STD投影、扩展景深投影(EDF) | numpy, opencv-python, scipy.ndimage, tifffile |
| 图像处理 | 背景扣除、去噪、CLAHE/归一化 | skimage.restoration, skimage.filters, skimage.exposure |
| 目标识别 | Otsu阈值、分水岭、Cellpose/StarDist深度学习分割、连通域标记 | skimage.filters, skimage.segmentation, cellpose, scipy.ndimage |
| 目标测量 | regionprops形态学特征、多通道强度、GLCM纹理、共定位系数 | skimage.measure, skimage.feature |

---

*说明：以上代码为示例性质，实际生产环境中建议根据具体显微镜元数据（如OME-XML、载物台坐标）、通道数量及样本厚度对参数进行调整，并对分割结果做质控（如面积/圆度过滤，去除边缘不完整目标等）。*

这个问题不能简单地用"先后"二分——因为"预处理"其实包含两类性质不同的操作，需要拆开看：

## 核心结论:分析顺序

**部分预处理必须在拼接/投影之前做，另一部分则应该放在之后。**

| 处理类型 | 该放在哪 | 原因 |
|---|---|---|
| 光照不均校正（flat-field/shading correction）、暗场/偏置扣除 | **拼接投影之前**，且要按单个视野（tile）逐个做 | 每个FOV的渐晕（vignetting）模式是光学系统固有的，只对单个tile有效；如果先拼接再校正，校正模型和图像已经不对齐了 |
| Z轴投影（MIP/EDF等） | 通常在**拼接之前**，按每个tile单独做 | 每个视野各自采集了完整Z-stack，先在tile层面投影成2D，能大幅减少后续拼接要处理的数据量（3D直接拼接代价很高） |
| 图像拼接（Stitching） | 在上述两步**之后** | 拼接的输入应该是已经过光照校正、且已经压成2D的干净图像，这样配准算法（相位相关/特征匹配）才不会被渐晕伪影或Z轴离焦干扰 |
| 背景扣除（rolling ball）、去噪、CLAHE/对比度增强 | 拼接完成**之后**，在最终的大图上做 | 这类操作通常需要较大的空间统计信息（比如背景估计半径），在拼接后的完整视野上做效果更准确；而且只需处理一次，比对每个tile重复处理更省算力，也能避免拼接缝处理不一致造成的接缝伪影 |

## 推荐流程顺序