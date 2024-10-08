import torch
import numpy as np
import cv2
import io
import json
from PIL import Image

from ultralytics import YOLO
from ultralytics.models import YOLOv10
from transformers import T5TokenizerFast, T5ForConditionalGeneration

import time
from loguru import logger

model = T5ForConditionalGeneration.from_pretrained('models/t5_base_final/model/')
tokenizer = T5TokenizerFast.from_pretrained('models/t5_base_final/model/tokenizer')

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def gentext(input_text, max_new_tokens_=64):
    prompt = input_text
    # 입력 텍스트를 토큰화
    text_input = tokenizer(prompt, return_tensors='pt', padding=True)

    # 입력 데이터와 attention mask를 GPU로 이동
    input_ids = text_input['input_ids'].to(device)
    attention_mask = text_input['attention_mask'].to(device)

    # 모델을 GPU로 이동
    model.to(device)
    # 모델과 토크나이저를 GPU로 이동
    model.to(device)
    input_ids = input_ids.to(device)

    with torch.no_grad():
        outputs = model.generate(
            input_ids,
            attention_mask=attention_mask,
            max_new_tokens=max_new_tokens_,
            num_beams=1,
            pad_token_id=tokenizer.eos_token_id
        )
        
    # 예측 결과 디코딩
    predicted_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
    logger.info(f'입력 : {input_text} \n출력: {predicted_text}')
    
    return predicted_text

# 테스트
if __name__ == "__main__":
    time_ = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))

    logger.add(f"result/t5_base/{time_}.log",format="{message}", level="INFO")
    gentext('공포, 모자, 빵', 64)