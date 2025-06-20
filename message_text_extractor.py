#!/usr/bin/env python3
"""
Message Text Extractor
LLM-based text extraction for message block images
"""

import cv2
import numpy as np
import base64
import requests
import json
from PIL import Image
from typing import Dict, Optional
import io

class MessageTextExtractor:
    """
    LLM-based text extractor for message blocks
    """
    
    def __init__(self, api_key: str = None, model: str = "gpt-4o"):
        """
        Initialize the LLM text extractor
        
        Args:
            api_key: OpenAI API key (can also be set via environment variable)
            model: Vision model to use for text extraction
        """
        self.api_key = api_key
        self.model = model
        self.api_url = "https://api.openai.com/v1/chat/completions"
        
        # If no API key provided, try to get from environment
        if not self.api_key:
            import os
            self.api_key = os.getenv('OPENAI_API_KEY')
        
        if not self.api_key:
            print("⚠️  Warning: No OpenAI API key provided. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
    
    def image_to_base64(self, image: np.ndarray) -> str:
        """
        Convert numpy image to base64 string for API
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Base64 encoded image string
        """
        # Convert BGR to RGB if needed
        if len(image.shape) == 3 and image.shape[2] == 3:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            image_rgb = image
        
        # Convert to PIL Image
        pil_image = Image.fromarray(image_rgb)
        
        # Convert to base64
        buffer = io.BytesIO()
        pil_image.save(buffer, format='PNG')
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return image_base64
    
    def extract_text(self, message_block_image: np.ndarray) -> Dict:
        """
        Extract text from a message block image using LLM
        
        Args:
            message_block_image: Input image containing the message block
            
        Returns:
            Dictionary with extracted text and metadata
        """
        if message_block_image is None or message_block_image.size == 0:
            return {
                'text': '',
                'confidence': 0,
                'error': 'Empty or invalid image'
            }
        
        if not self.api_key:
            return {
                'text': '',
                'confidence': 0,
                'error': 'No API key provided'
            }
        
        try:
            # Convert image to base64
            image_base64 = self.image_to_base64(message_block_image)
            
            # Prepare the prompt for Chinese game text extraction
            prompt = """
请分析这张中国手机游戏聊天界面的图像并提取文本内容。

重点关注：
1. 中文字符和文本
2. 用户名
3. 聊天消息
4. 游戏相关术语
5. 系统消息

只返回提取的文本内容，保持原始语言（中文字符）。如果有多行或多条消息，用换行符分隔。如果没有找到可读文本，返回"无文本"。

请准确保留原始中文字符的确切显示形式。
"""
            
            # Prepare API request
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 500
            }
            
            # Make API request
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                if 'choices' in result and len(result['choices']) > 0:
                    extracted_text = result['choices'][0]['message']['content'].strip()
                    
                    return {
                        'text': extracted_text,
                        'confidence': 95,
                        'method': 'llm_vision',
                        'model': self.model,
                        'success': True
                    }
                else:
                    return {
                        'text': '',
                        'confidence': 0,
                        'error': 'No response content from LLM'
                    }
            else:
                return {
                    'text': '',
                    'confidence': 0,
                    'error': f'API request failed: {response.status_code} - {response.text}'
                }
                
        except Exception as e:
            return {
                'text': '',
                'confidence': 0,
                'error': f'LLM extraction failed: {str(e)}'
            }

# Example usage functions
def extract_from_file(image_path: str, api_key: str = None) -> Dict:
    """
    Extract text from an image file using LLM
    
    Args:
        image_path: Path to image file
        api_key: OpenAI API key
        
    Returns:
        Text extraction results
    """
    extractor = MessageTextExtractor(api_key=api_key)
    
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        return {'text': '', 'confidence': 0, 'error': f'Could not load image: {image_path}'}
    
    return extractor.extract_text(image)

def extract_from_array(image_array: np.ndarray, api_key: str = None) -> Dict:
    """
    Extract text from a numpy image array using LLM
    
    Args:
        image_array: Image as numpy array
        api_key: OpenAI API key
        
    Returns:
        Text extraction results
    """
    extractor = MessageTextExtractor(api_key=api_key)
    return extractor.extract_text(image_array)

# Simple test function
def test_extractor():
    """Test the LLM extractor with available debug images"""
    import os
    
    debug_dir = "debug/avatar_template"
    if not os.path.exists(debug_dir):
        print("❌ No debug directory found")
        return
    
    # Find the most recent debug images
    files = [f for f in os.listdir(debug_dir) if f.startswith('full_chat_') and f.endswith('.png')]
    if not files:
        print("❌ No chat images found in debug directory")
        return
    
    # Use the most recent file
    latest_file = sorted(files)[-1]
    image_path = os.path.join(debug_dir, latest_file)
    
    print(f"🧪 Testing LLM text extraction on: {image_path}")
    
    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ No OPENAI_API_KEY environment variable found")
        print("💡 Set your OpenAI API key: export OPENAI_API_KEY='your-key-here'")
        return
    
    result = extract_from_file(image_path, api_key)
    
    print(f"📝 Extracted text: '{result['text']}'")
    print(f"🎯 Confidence: {result['confidence']}")
    print(f"🔧 Method: {result.get('method', 'unknown')}")
    if 'error' in result:
        print(f"❌ Error: {result['error']}")

if __name__ == "__main__":
    test_extractor() 