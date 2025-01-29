from openai import OpenAI
import json
from abc import ABC, abstractmethod


class SizeChooser(ABC):
    client = None

    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    @abstractmethod
    def get_size_info(self, url):
        """Extract size information from the given URL."""
        pass

    def choose_size(self, user_info, size_info):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """당신은 고객에게 가장 적합한 사이즈를 추천하는 패션 전문가입니다.

응답 형식:
추천 사이즈: [사이즈]
설명: [150자 이내의 추천 이유 설명]

- 고객 정보와 사이즈 측정값을 분석하여 정확한 사이즈를 추천해주세요
- 설명은 한국어로 작성하고, 150자를 넘지 않도록 해주세요
"""
                },
                {
                    "role": "user",
                    "content": f"""Customer Information:
{user_info}

Size Information:
{json.dumps(size_info, ensure_ascii=False, indent=2)}"""
                },
            ],
        )
        return response.choices[0].message.content
    

class TopSizeChooser(SizeChooser):
    def get_size_info(self, url):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert in extracting size information for tops (shirts, jackets, etc.) from fashion product URLs.
                    Extract size measurements in a structured format. 
                    - If a measurement is not available, use "-" as the value
                    - Only include available sizes
                    - All measurements should be in centimeters
                    - Do not include any explanatory text, only return the JSON data"""
                },
                {
                    "role": "user",
                    "content": f"Extract size information from this URL: {url}. Return the data in this format:" + """
                    {
                        "sizes": [
                            {
                                "size": "M",
                                "measurements": {
                                    "총장": "68",
                                    "가슴단면": "58",
                                    "어깨너비": "54",
                                    "소매길이": "61"
                                }
                            }
                        ]
                    }
                    Note: Use "-" for any missing measurements."""
                }
            ],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        
        sizes_data = {
            '사이즈': [],
            '총장 (cm)': [],
            '가슴단면 (cm)': [],
            '어깨너비 (cm)': [],
            '소매길이 (cm)': []
        }
        
        for size_info in result['sizes']:
            sizes_data['사이즈'].append(size_info['size'])
            sizes_data['총장 (cm)'].append(size_info['measurements'].get('총장', '-'))
            sizes_data['가슴단면 (cm)'].append(size_info['measurements'].get('가슴단면', '-'))
            sizes_data['어깨너비 (cm)'].append(size_info['measurements'].get('어깨너비', '-'))
            sizes_data['소매길이 (cm)'].append(size_info['measurements'].get('소매길이', '-'))
        
        return sizes_data


class LowerSizeChooser(SizeChooser):
    def get_size_info(self, url):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert in extracting size information for bottoms (pants, skirts, etc.) from fashion product URLs.
                    Extract size measurements in a structured format. 
                    - If a measurement is not available, use "-" as the value
                    - Only include available sizes
                    - All measurements should be in centimeters
                    - Do not include any explanatory text, only return the JSON data"""
                },
                {
                    "role": "user",
                    "content": f"Extract size information from this URL: {url}. Return the data in this format:" + """
                    {
                        "sizes": [
                            {
                                "size": "M",
                                "measurements": {
                                    "총장": "98",
                                    "허리단면": "36",
                                    "엉덩이단면": "52",
                                    "허벅지단면": "31",
                                    "밑위": "28",
                                    "밑단단면": "17"
                                }
                            }
                        ]
                    }
                    Note: Use "-" for any missing measurements."""
                }
            ],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        
        sizes_data = {
            '사이즈': [],
            '총장 (cm)': [],
            '허리단면 (cm)': [],
            '엉덩이단면 (cm)': [],
            '허벅지단면 (cm)': [],
            '밑위 (cm)': [],
            '밑단단면 (cm)': []
        }
        
        for size_info in result['sizes']:
            sizes_data['사이즈'].append(size_info['size'])
            sizes_data['총장 (cm)'].append(size_info['measurements'].get('총장', '-'))
            sizes_data['허리단면 (cm)'].append(size_info['measurements'].get('허리단면', '-'))
            sizes_data['엉덩이단면 (cm)'].append(size_info['measurements'].get('엉덩이단면', '-'))
            sizes_data['허벅지단면 (cm)'].append(size_info['measurements'].get('허벅지단면', '-'))
            sizes_data['밑위 (cm)'].append(size_info['measurements'].get('밑위', '-'))
            sizes_data['밑단단면 (cm)'].append(size_info['measurements'].get('밑단단면', '-'))
        
        return sizes_data