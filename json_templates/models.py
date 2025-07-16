from django.db import models
from django.contrib.auth.models import User
import json
import random
import string
from datetime import datetime, timedelta

class JsonTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='json_templates')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    template_structure = models.JSONField(help_text="JSON 템플릿 구조 정의")
    is_public = models.BooleanField(default=False, help_text="다른 사용자들이 볼 수 있는지 여부")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "JSON Templates"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} (by {self.user.username})"
    
    def generate_dummy_data(self, count=1):
        """템플릿 구조에 따라 더미 JSON 데이터 생성"""
        if count == 1:
            return self._generate_single_dummy()
        else:
            return [self._generate_single_dummy() for _ in range(count)]
    
    def _generate_single_dummy(self):
        """단일 더미 데이터 생성"""
        return self._process_template_structure(self.template_structure)
    
    def _process_template_structure(self, structure):
        """템플릿 구조를 처리하여 더미 데이터 생성"""
        if isinstance(structure, dict):
            result = {}
            for key, value in structure.items():
                result[key] = self._process_template_structure(value)
            return result
        elif isinstance(structure, list):
            if len(structure) > 0:
                # 리스트의 첫 번째 요소를 템플릿으로 사용
                return [self._process_template_structure(structure[0])]
            return []
        elif isinstance(structure, str):
            return self._generate_value_by_type(structure)
        else:
            return structure
    
    def _generate_value_by_type(self, type_definition):
        """타입 정의에 따라 더미 값 생성"""
        type_lower = type_definition.lower()
        
        if 'string' in type_lower:
            if 'name' in type_lower:
                return self._generate_name()
            elif 'email' in type_lower:
                return self._generate_email()
            elif 'phone' in type_lower:
                return self._generate_phone()
            elif 'address' in type_lower:
                return self._generate_address()
            elif 'url' in type_lower:
                return self._generate_url()
            else:
                return self._generate_random_string()
        
        elif 'number' in type_lower or 'int' in type_lower:
            if 'age' in type_lower:
                return random.randint(18, 80)
            elif 'price' in type_lower or 'cost' in type_lower:
                return round(random.uniform(10, 1000), 2)
            elif 'rating' in type_lower or 'score' in type_lower:
                return round(random.uniform(1, 5), 1)
            else:
                return random.randint(1, 1000)
        
        elif 'boolean' in type_lower or 'bool' in type_lower:
            return random.choice([True, False])
        
        elif 'date' in type_lower:
            if 'birth' in type_lower:
                # 생년월일 (20-60세)
                years_ago = random.randint(20, 60)
                return (datetime.now() - timedelta(days=years_ago*365)).strftime('%Y-%m-%d')
            else:
                # 최근 1년 내 날짜
                days_ago = random.randint(0, 365)
                return (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        
        elif 'datetime' in type_lower:
            # 최근 1년 내 날짜시간
            days_ago = random.randint(0, 365)
            hours_ago = random.randint(0, 24)
            return (datetime.now() - timedelta(days=days_ago, hours=hours_ago)).strftime('%Y-%m-%d %H:%M:%S')
        
        elif 'array' in type_lower or 'list' in type_lower:
            # 기본 문자열 배열
            return [self._generate_random_string() for _ in range(random.randint(1, 5))]
        
        else:
            # 기본값으로 랜덤 문자열 반환
            return self._generate_random_string()
    
    def _generate_name(self):
        """랜덤 이름 생성"""
        first_names = ['김', '이', '박', '최', '정', '강', '조', '윤', '장', '임']
        last_names = ['민준', '서준', '도윤', '예준', '시우', '주원', '하준', '지호', '지후', '준서']
        return random.choice(first_names) + random.choice(last_names)
    
    def _generate_email(self):
        """랜덤 이메일 생성"""
        domains = ['gmail.com', 'naver.com', 'daum.net', 'hotmail.com', 'yahoo.com']
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"{username}@{random.choice(domains)}"
    
    def _generate_phone(self):
        """랜덤 전화번호 생성"""
        return f"010-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    
    def _generate_address(self):
        """랜덤 주소 생성"""
        cities = ['서울시', '부산시', '대구시', '인천시', '광주시', '대전시', '울산시']
        districts = ['강남구', '서초구', '마포구', '종로구', '중구', '동대문구', '성동구']
        return f"{random.choice(cities)} {random.choice(districts)}"
    
    def _generate_url(self):
        """랜덤 URL 생성"""
        domains = ['example.com', 'test.com', 'demo.org', 'sample.net']
        paths = ['api', 'users', 'products', 'posts', 'comments']
        return f"https://{random.choice(domains)}/{random.choice(paths)}"
    
    def _generate_random_string(self):
        """랜덤 문자열 생성"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

class TemplateUsage(models.Model):
    """템플릿 사용 기록"""
    template = models.ForeignKey(JsonTemplate, on_delete=models.CASCADE, related_name='usages')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='template_usages')
    generated_count = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Template Usages"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.template.name} used by {self.user.username}"
