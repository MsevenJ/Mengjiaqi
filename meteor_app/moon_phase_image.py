import requests
from PIL import Image, ImageDraw, ImageFont
import os
import datetime
import logging

def get_moon_phase_image(date):
    """
    根据日期从 NASA 下载月球相位图像
    """
    year = date.year
    month = date.month
    day = date.day
    url = f"https://svs.gsfc.nasa.gov/vis/a000000/a005100/a005187/frames/5760x3240_16x9_30p/moon.{year:04d}{month:02d}{day:02d}.tif"
    response = requests.get(url)
    if response.status_code == 200:
        image_path = f"moon_{year}{month:02d}{day:02d}.tif"
        with open(image_path, 'wb') as f:
            f.write(response.content)
        return image_path
    return None

def process_image(moon_image_path, background_path):
    """
    处理图像，将月球图像叠加到背景上，并标注信息
    """
    if not os.path.exists(background_path):
        logger.error(f"Background image file {background_path} not found.")
        return None
    moon_image = Image.open(moon_image_path)
    background = Image.open(background_path)
    # 调整月球图像大小
    moon_image = moon_image.resize((background.width // 4, background.height // 4))
    # 叠加图像
    position = (background.width - moon_image.width - 20, 20)
    background.paste(moon_image, position, moon_image)
    # 标注信息
    draw = ImageDraw.Draw(background)
    font = ImageFont.load_default()
    # 这里简单示例标注日期
    draw.text((20, 20), f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}", fill=(255, 255, 255), font=font)
    processed_image_path = "processed_image.jpg"
    background.save(processed_image_path)
    return processed_image_path

def get_date_image(date):
    """
    获取指定日期的处理后图像
    """
    moon_image_path = get_moon_phase_image(date)
    if moon_image_path:
        background_path = "best_small.tif"  # 背景图像路径
        processed_image_path = process_image(moon_image_path, background_path)
        # 删除临时月球图像
        os.remove(moon_image_path)
        return processed_image_path
    return None