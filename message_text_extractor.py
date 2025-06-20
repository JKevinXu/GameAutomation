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
    
    def contains_keyword(self, message_block_image: np.ndarray, keyword: str) -> Dict:
        """
        Use LLM to judge if the message block is related to a specific keyword or concept
        
        Args:
            message_block_image: Input image containing the message block
            keyword: Keyword or concept to check for (e.g., "320", "章鱼王")
            
        Returns:
            Dictionary with keyword detection results
        """
        if message_block_image is None or message_block_image.size == 0:
            return {
                'is_related': False,
                'keyword': keyword,
                'confidence': 0,
                'error': 'Empty or invalid image'
            }
        
        if not self.api_key:
            return {
                'is_related': False,
                'keyword': keyword,
                'confidence': 0,
                'error': 'No API key provided'
            }
        
        try:
            # Convert image to base64
            image_base64 = self.image_to_base64(message_block_image)
            
            # Prepare the prompt for keyword/concept analysis
            prompt = f"""
请分析这张中国手机游戏聊天界面的图像，判断其内容是否与关键词"{keyword}"相关。

请考虑以下方面：
1. 直接包含该关键词
2. 与该关键词相关的概念、活动或内容
3. 上下文和语义关联
4. 游戏术语和缩写

请用以下JSON格式回复：
{{
    "is_related": true/false,
    "confidence": 1-100,
    "explanation": "简短解释为什么相关或不相关",
    "extracted_content": "图像中提取的相关文本内容"
}}

只返回JSON格式，不要其他内容。
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
                "max_tokens": 300
            }
            
            # Make API request
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                if 'choices' in result and len(result['choices']) > 0:
                    response_text = result['choices'][0]['message']['content'].strip()
                    
                    try:
                        # Parse JSON response
                        import json
                        
                        # Remove markdown code block formatting if present
                        if response_text.startswith('```json'):
                            # Find the start and end of the JSON content
                            start_marker = '```json'
                            end_marker = '```'
                            start_index = response_text.find(start_marker) + len(start_marker)
                            end_index = response_text.rfind(end_marker)
                            if end_index > start_index:
                                response_text = response_text[start_index:end_index].strip()
                        elif response_text.startswith('```'):
                            # Handle generic code block
                            lines = response_text.split('\n')
                            if len(lines) > 2:
                                response_text = '\n'.join(lines[1:-1]).strip()
                        
                        analysis = json.loads(response_text)
                        
                        return {
                            'is_related': analysis.get('is_related', False),
                            'keyword': keyword,
                            'confidence': analysis.get('confidence', 0),
                            'explanation': analysis.get('explanation', ''),
                            'extracted_content': analysis.get('extracted_content', ''),
                            'method': 'llm_analysis',
                            'model': self.model,
                            'success': True
                        }
                    except json.JSONDecodeError:
                        # Fallback: try to interpret response as plain text
                        is_related = '是' in response_text or 'true' in response_text.lower() or '相关' in response_text
                        return {
                            'is_related': is_related,
                            'keyword': keyword,
                            'confidence': 80 if is_related else 20,
                            'explanation': response_text,
                            'extracted_content': '',
                            'method': 'llm_analysis_fallback',
                            'success': True
                        }
                else:
                    return {
                        'is_related': False,
                        'keyword': keyword,
                        'confidence': 0,
                        'error': 'No response content from LLM'
                    }
            else:
                return {
                    'is_related': False,
                    'keyword': keyword,
                    'confidence': 0,
                    'error': f'API request failed: {response.status_code} - {response.text}'
                }
                
        except Exception as e:
            return {
                'is_related': False,
                'keyword': keyword,
                'confidence': 0,
                'error': f'LLM analysis failed: {str(e)}'
            }
    
    def contains_any_keyword(self, message_block_image: np.ndarray, keywords: list) -> Dict:
        """
        Use LLM to judge if the message block is related to any of the specified keywords or concepts
        
        Args:
            message_block_image: Input image containing the message block
            keywords: List of keywords or concepts to check for (e.g., ["320", "章鱼王", "师门"])
            
        Returns:
            Dictionary with keyword detection results
        """
        if message_block_image is None or message_block_image.size == 0:
            return {
                'is_related_to_any': False,
                'keywords': keywords,
                'related_keywords': [],
                'confidence': 0,
                'error': 'Empty or invalid image'
            }
        
        if not self.api_key:
            return {
                'is_related_to_any': False,
                'keywords': keywords,
                'related_keywords': [],
                'confidence': 0,
                'error': 'No API key provided'
            }
        
        try:
            # Convert image to base64
            image_base64 = self.image_to_base64(message_block_image)
            
            # Create keywords string for prompt
            keywords_str = "、".join(keywords)
            
            # Prepare the prompt for multiple keyword/concept analysis
            prompt = f"""
请分析这张中国手机游戏聊天界面的图像，判断其内容是否与以下任何关键词相关：{keywords_str}

请考虑以下方面：
1. 直接包含这些关键词
2. 与这些关键词相关的概念、活动或内容
3. 上下文和语义关联
4. 游戏术语和缩写

请用以下JSON格式回复：
{{
    "is_related_to_any": true/false,
    "related_keywords": ["相关的关键词列表"],
    "confidence": 1-100,
    "explanation": "简短解释哪些关键词相关以及为什么",
    "extracted_content": "图像中提取的相关文本内容"
}}

只返回JSON格式，不要其他内容。
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
                "max_tokens": 400
            }
            
            # Make API request
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                if 'choices' in result and len(result['choices']) > 0:
                    response_text = result['choices'][0]['message']['content'].strip()
                    
                    try:
                        # Parse JSON response
                        import json
                        
                        # Remove markdown code block formatting if present
                        if response_text.startswith('```json'):
                            # Find the start and end of the JSON content
                            start_marker = '```json'
                            end_marker = '```'
                            start_index = response_text.find(start_marker) + len(start_marker)
                            end_index = response_text.rfind(end_marker)
                            if end_index > start_index:
                                response_text = response_text[start_index:end_index].strip()
                        elif response_text.startswith('```'):
                            # Handle generic code block
                            lines = response_text.split('\n')
                            if len(lines) > 2:
                                response_text = '\n'.join(lines[1:-1]).strip()
                        
                        analysis = json.loads(response_text)
                        
                        return {
                            'is_related_to_any': analysis.get('is_related_to_any', False),
                            'keywords': keywords,
                            'related_keywords': analysis.get('related_keywords', []),
                            'confidence': analysis.get('confidence', 0),
                            'explanation': analysis.get('explanation', ''),
                            'extracted_content': analysis.get('extracted_content', ''),
                            'method': 'llm_analysis',
                            'model': self.model,
                            'success': True
                        }
                    except json.JSONDecodeError:
                        # Fallback: try to interpret response as plain text
                        is_related = '是' in response_text or 'true' in response_text.lower() or '相关' in response_text
                        return {
                            'is_related_to_any': is_related,
                            'keywords': keywords,
                            'related_keywords': [],
                            'confidence': 80 if is_related else 20,
                            'explanation': response_text,
                            'extracted_content': '',
                            'method': 'llm_analysis_fallback',
                            'success': True
                        }
                else:
                    return {
                        'is_related_to_any': False,
                        'keywords': keywords,
                        'related_keywords': [],
                        'confidence': 0,
                        'error': 'No response content from LLM'
                    }
            else:
                return {
                    'is_related_to_any': False,
                    'keywords': keywords,
                    'related_keywords': [],
                    'confidence': 0,
                    'error': f'API request failed: {response.status_code} - {response.text}'
                }
                
        except Exception as e:
            return {
                'is_related_to_any': False,
                'keywords': keywords,
                'related_keywords': [],
                'confidence': 0,
                'error': f'LLM analysis failed: {str(e)}'
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

# Helper functions for keyword detection
def check_keyword_in_file(image_path: str, keyword: str, api_key: str = None) -> Dict:
    """
    Check if an image file contains a specific keyword
    
    Args:
        image_path: Path to image file
        keyword: Keyword to search for
        api_key: OpenAI API key
        
    Returns:
        Keyword detection results
    """
    extractor = MessageTextExtractor(api_key=api_key)
    
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        return {'contains_keyword': False, 'error': f'Could not load image: {image_path}'}
    
    return extractor.contains_keyword(image, keyword)

def check_keywords_in_array(image_array: np.ndarray, keywords: list, api_key: str = None) -> Dict:
    """
    Check if an image array contains any of the specified keywords
    
    Args:
        image_array: Image as numpy array
        keywords: List of keywords to search for
        api_key: OpenAI API key
        
    Returns:
        Keyword detection results
    """
    extractor = MessageTextExtractor(api_key=api_key)
    return extractor.contains_any_keyword(image_array, keywords)

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
    
    # Test basic text extraction
    result = extract_from_file(image_path, api_key)
    
    print(f"📝 Extracted text: '{result['text']}'")
    print(f"🎯 Confidence: {result['confidence']}")
    print(f"🔧 Method: {result.get('method', 'unknown')}")
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
        return
    
    # Test LLM-based keyword analysis
    print("\n🔍 Testing LLM-based keyword analysis:")
    
    # Test individual keywords
    test_keywords = ["320", "章鱼王", "师门", "任务"]
    
    extractor = MessageTextExtractor(api_key=api_key)
    image = cv2.imread(image_path)
    
    for keyword in test_keywords:
        keyword_result = extractor.contains_keyword(image, keyword)
        if keyword_result.get('error'):
            print(f"   {keyword}: ❌ ERROR - {keyword_result['error']}")
        else:
            status = "✅ RELATED" if keyword_result['is_related'] else "❌ NOT RELATED"
            confidence = keyword_result['confidence']
            explanation = keyword_result.get('explanation', '')
            print(f"   {keyword}: {status} (信心度: {confidence}%)")
            if explanation:
                print(f"      解释: {explanation}")
    
    # Test multiple keywords at once
    print(f"\n🔍 Testing multiple keywords analysis: {test_keywords}")
    multi_result = extractor.contains_any_keyword(image, test_keywords)
    if multi_result.get('error'):
        print(f"❌ ERROR: {multi_result['error']}")
    else:
        if multi_result['is_related_to_any']:
            print(f"✅ Related keywords: {multi_result['related_keywords']}")
            print(f"   信心度: {multi_result['confidence']}%")
            print(f"   解释: {multi_result.get('explanation', '')}")
        else:
            print("❌ No related keywords found")

if __name__ == "__main__":
    test_extractor() 