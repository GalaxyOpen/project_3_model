import torch
import numpy as np
import cv2
import io
import json
from PIL import Image
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import time
from loguru import logger

tokenizers = []

model = GPT2LMHeadModel.from_pretrained('models/gpt2_final_model/model/')
tokenizer = GPT2Tokenizer.from_pretrained('models/gpt2_final_model/model/tokenizer/')

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def gentext(input_text, max_new_tokens_=125):
    prompt = f"입력값: {input_text}\n출력값:"
    # 입력 텍스트를 토큰화
    text_input = tokenizer(prompt, return_tensors='pt', padding=True, truncation=True)

    # 입력 데이터와 attention mask를 GPU로 이동
    input_ids = text_input['input_ids'].to(device)
    attention_mask = text_input['attention_mask'].to(device)

    # 모델을 GPU로 이동
    model.to(device)
    # 모델과 토크나이저를 GPU로 이동
    model.to(device)
    input_ids = input_ids.to(device)

    # 모델 타입에 따라 다른 인자를 설정
    with torch.no_grad():
        # GPT-2의 텍스트 생성 설정
        outputs = model.generate(
            input_ids,
            attention_mask=attention_mask,
            max_new_tokens=max_new_tokens_,
            num_beams=1,
            no_repeat_ngram_size=30,
            top_k=50,
            top_p=0.95,
            temperature=1,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id)
        
    # 예측 결과 디코딩
    predicted_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
    logger.info(predicted_text)
    
    return predicted_text

# 테스트
if __name__ == "__main__":
    time_ = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))

    logger.add(f"result/gpt2/{time_}.log",format="{message}", level="INFO")

    print(gentext('공포, 모자, 빵', 125))