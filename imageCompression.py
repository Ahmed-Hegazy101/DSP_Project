import cv2
import numpy as np 
from PIL import Image
import io

def rgb_to_yuv(img):
    
    #to convert we make it rgb not bgr
    rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    
    #spliting
    R = rgb[:,:,0].astype(np.float32)  
    G = rgb[:,:,1].astype(np.float32) 
    B = rgb[:,:,2].astype(np.float32)
    
    #converting formula
    Y = 0.299 * R + 0.587 * G + 0.114 * B #Luminance: light بنحاول منغيرش فيها 
    U = -0.147 * R - 0.289 * G + 0.436 * B + 128  #Chrominance :
    V = 0.615 * R - 0.515 * G - 0.100 * B + 128 #Chrominance : بنقلل المعلومت علشان تقلل حجم الصورة 
    
    #to make it safe 
    Y = np.clip(Y, 0, 255)
    U = np.clip(U, 0, 255)
    V = np.clip(V, 0, 255)
    
    #finished claculation
    return Y.astype(np.uint8), U.astype(np.uint8), V.astype(np.uint8) # تلات مصفوفات 8 بيت


def yuv_to_rgb(Y, U, V): # بنحول علشان نقدر نعرضها علي الشاشات
        
    Y = Y.astype(np.float32) # بيحول القيم لي ارقام عشرية علشان تكون دقيقة علشان الكسور الصغير بتفرق في الالوان
    U = U.astype(np.float32)
    V = V.astype(np.float32)
    
    R = Y + 1.140 * (V - 128)
    G = Y - 0.395 * (U - 128) - 0.581 * (V - 128) # معادلات علشان نحول لي rgb علشان كل بكسل له قية لي y u v 
    B = Y + 2.032 * (U - 128)

    R = np.clip(R, 0, 255) # بنستخدم دالة np.clip علشان نضمن ان قيم البكسل تكون في النطاق الصحيح
    G = np.clip(G, 0, 255)
    B = np.clip(B, 0, 255)
    
    rgb = np.stack([R, G, B], axis=2).astype(np.uint8) #نجمع كل قنوات الالوان #np.stack دي دالة بنجمع فيها القنوات
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR) # بنحول لي bgr
    
    return bgr

def chroma_subsample(U,V): # بنقلل حجم الصورة عن طريق الاستغناء عن بعض معلومات الالوان
    
    height,width = U.shape #بياخد ابعاد المصفوفة 
    
    U_small = U[:, ::2] # بتاخد عمود و تسيب عمود
    V_small = V[:, ::2] # v , u قنوات الالوان
    
    U_big = np.repeat(U_small,2,axis=1) # بيضعفوا بيانات بتاعت المصفوفة الصغير علشان ترجع لي ابعاده الاصلية 
    V_big = np.repeat(V_small,2,axis=1) #
    # بنستخدامه علشان اتاكد انا الابعاد متساوية تمام مع مصفوفة ال y علشان الالوان تظهر بشكل مظبوط  في الصورة النهائية
    if height % 2 == 1:
        U_big = U_big[:height,:] # بقص الزيادة
        V_big = V_big[:height,:]
        
    if width % 2 == 1:
        U_big = U_big[:, :width]
        V_big = V_big[:, :width]
        
    return U_big, V_big # برجع الابعاد المظبوطه

def quantize_channel(channel, bits=4): #هنستخدم 4 بيت لكل بيكسل # channel المصفوفة اللي شيالة البيانات بتاعت قناة واحدة من الصورة

    if bits >= 8: # بنستخدمه مع الصورة اللي جوده عالية علشان الضغط الزياة هياثر علي الجودة
        return channel
    
    levels = 2 ** bits
    step_size = 256 / levels
    
    # Quantize: round to nearest step
    quantized = (channel // step_size) * step_size #بنستخدمها علشان نقرب قيمة البكسل لي اقرب مستوي متح و ده بيساعده فتقليل الحجم
    
    return quantized.astype(np.uint8) #برجع المصفوفة المعدلة  بالارقام الصحيحية

def compress_image(img):
    '''
    pipeline:
    original(rgb) --> yuv --> chroma subsampling --> quantization --> rgb --> compressd
    '''
    Y,U,V = rgb_to_yuv(img) # بنتقسم الصورة علي التلات متغيرات # بستدع دلة ال rgb
    
    U,V = chroma_subsample(U,V) 
    
    Y = quantize_channel(Y,bits=6) 
    U = quantize_channel(U,bits=5)
    V = quantize_channel(V,bits=5)
    
    compressed = yuv_to_rgb(Y,U,V) # بجمع القنوات مع بعض 
    
    return compressed

def get_image_size_kb(img):
    
    rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    
    pil_img = Image.fromarray(rgb)
    buffer = io.BytesIO()
    pil_img.save(buffer,format='PNG')
    size_kb = len(buffer.getvalue())/1024
    
    return size_kb

def calculate_psnr(original, compressed):
    """
    > 40 dB: Excellent
    30-40 dB: Good
    20-30 dB: Acceptable
    < 20 dB: Poor
    """
    
    mse = np.mean((original.astype(float) - compressed.astype(float)) ** 2)
    
    if mse == 0:
        return 100
    
    max_pixel = 255.0
    psnr = 10 * np.log10(max_pixel ** 2 / mse)
    
    return psnr
#psnr : مقياس لي جودة الصورة المضغوة و بقارنة بالصورة الاصلية علشان اعرف مدي الدقة

# 3 step
# 1- بحولها yuv علشان نقدر نضغط الصورة 
# 2- chroma_subsample بتقلل معلومات اللون
# 3- quantize علشان اقلل عدد مستويات الالوان
# 4- compress بجمع كل الخطوات في خطوة واحدة 
    


