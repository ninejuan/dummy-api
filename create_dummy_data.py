#!/usr/bin/env python
import os
import django
import yaml
import json

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dummy.settings')
django.setup()

from yaml_data.models import YamlCategory, YamlData
from code_samples.models import CodeCategory, CodeSample

def create_yaml_dummy_data():
    """YAML 더미 데이터 생성"""
    
    # YAML 카테고리 생성
    categories = [
        {
            'name': 'Docker 설정',
            'description': 'Docker 관련 YAML 설정 파일들'
        },
        {
            'name': 'Kubernetes 매니페스트',
            'description': 'Kubernetes 배포 및 서비스 설정'
        },
        {
            'name': 'CI/CD 파이프라인',
            'description': 'GitHub Actions, GitLab CI 등'
        }
    ]
    
    for cat_data in categories:
        category, created = YamlCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
        
        if created:
            print(f"YAML 카테고리 생성: {category.name}")
    
    # YAML 데이터 생성
    yaml_samples = [
        {
            'category_name': 'Docker 설정',
            'title': 'Docker Compose 기본 설정',
            'content': '''
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./html:/usr/share/nginx/html
    environment:
      - NGINX_HOST=localhost
      - NGINX_PORT=80
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
''',
            'tags': ['docker', 'compose', 'nginx', 'postgres']
        },
        {
            'category_name': 'Kubernetes 매니페스트',
            'title': 'Deployment와 Service',
            'content': '''
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: LoadBalancer
''',
            'tags': ['kubernetes', 'deployment', 'service']
        },
        {
            'category_name': 'CI/CD 파이프라인',
            'title': 'GitHub Actions 워크플로우',
            'content': '''
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m pytest
    
    - name: Build and push Docker image
      if: github.ref == 'refs/heads/main'
      run: |
        docker build -t myapp:${{ github.sha }} .
        docker push myapp:${{ github.sha }}
''',
            'tags': ['github-actions', 'ci-cd', 'docker']
        }
    ]
    
    for sample_data in yaml_samples:
        category = YamlCategory.objects.get(name=sample_data['category_name'])
        yaml_data, created = YamlData.objects.get_or_create(
            title=sample_data['title'],
            category=category,
            defaults={
                'content': sample_data['content'].strip(),
                'tags': sample_data['tags']
            }
        )
        
        if created:
            print(f"YAML 데이터 생성: {yaml_data.title}")

def create_code_dummy_data():
    """코드 샘플 더미 데이터 생성"""
    
    # 코드 카테고리 생성
    categories = [
        {
            'name': 'Python 기초',
            'description': 'Python 기본 문법과 예제',
            'language': 'python'
        },
        {
            'name': 'JavaScript ES6+',
            'description': '모던 JavaScript 문법',
            'language': 'javascript'
        },
        {
            'name': 'React 컴포넌트',
            'description': 'React 함수형 컴포넌트 예제',
            'language': 'jsx'
        }
    ]
    
    for cat_data in categories:
        category, created = CodeCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
        
        if created:
            print(f"코드 카테고리 생성: {category.name}")
    
    # 코드 샘플 생성
    code_samples = [
        {
            'category_name': 'Python 기초',
            'title': '리스트 컴프리헨션',
            'description': 'Python의 강력한 리스트 컴프리헨션 예제',
            'code': '''
# 기본 리스트 컴프리헨션
numbers = [1, 2, 3, 4, 5]
squares = [x**2 for x in numbers]
print(squares)  # [1, 4, 9, 16, 25]

# 조건부 리스트 컴프리헨션
even_squares = [x**2 for x in numbers if x % 2 == 0]
print(even_squares)  # [4, 16]

# 중첩 리스트 컴프리헨션
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [item for row in matrix for item in row]
print(flattened)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
''',
            'language': 'python',
            'difficulty': 'intermediate',
            'tags': ['python', 'list-comprehension', 'functional-programming']
        },
        {
            'category_name': 'JavaScript ES6+',
            'title': 'Async/Await 패턴',
            'description': '비동기 처리를 위한 async/await 사용법',
            'code': '''
// 기본 async/await 사용법
async function fetchUserData(userId) {
    try {
        const response = await fetch(`/api/users/${userId}`);
        const userData = await response.json();
        return userData;
    } catch (error) {
        console.error('사용자 데이터 가져오기 실패:', error);
        throw error;
    }
}

// Promise.all을 사용한 병렬 처리
async function fetchMultipleUsers(userIds) {
    const promises = userIds.map(id => fetchUserData(id));
    const users = await Promise.all(promises);
    return users;
}

// 실제 사용 예제
async function main() {
    try {
        const user = await fetchUserData(123);
        console.log('사용자 정보:', user);
        
        const users = await fetchMultipleUsers([1, 2, 3]);
        console.log('여러 사용자:', users);
    } catch (error) {
        console.error('오류 발생:', error);
    }
}

main();
''',
            'language': 'javascript',
            'difficulty': 'advanced',
            'tags': ['javascript', 'async-await', 'promises', 'es6']
        },
        {
            'category_name': 'React 컴포넌트',
            'title': 'Custom Hook 만들기',
            'description': 'React Custom Hook을 사용한 상태 관리',
            'code': '''
import { useState, useEffect } from 'react';

// Custom Hook: 로컬 스토리지 사용
function useLocalStorage(key, initialValue) {
    const [storedValue, setStoredValue] = useState(() => {
        try {
            const item = window.localStorage.getItem(key);
            return item ? JSON.parse(item) : initialValue;
        } catch (error) {
            console.error('로컬 스토리지 읽기 오류:', error);
            return initialValue;
        }
    });

    const setValue = (value) => {
        try {
            const valueToStore = value instanceof Function ? value(storedValue) : value;
            setStoredValue(valueToStore);
            window.localStorage.setItem(key, JSON.stringify(valueToStore));
        } catch (error) {
            console.error('로컬 스토리지 저장 오류:', error);
        }
    };

    return [storedValue, setValue];
}

// Custom Hook: API 호출
function useApi(url) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const response = await fetch(url);
                const result = await response.json();
                setData(result);
            } catch (err) {
                setError(err);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [url]);

    return { data, loading, error };
}

// 사용 예제
function TodoApp() {
    const [todos, setTodos] = useLocalStorage('todos', []);
    const { data: userData, loading, error } = useApi('/api/user');

    const addTodo = (text) => {
        setTodos([...todos, { id: Date.now(), text, completed: false }]);
    };

    if (loading) return <div>로딩 중...</div>;
    if (error) return <div>오류 발생: {error.message}</div>;

    return (
        <div>
            <h1>할 일 목록</h1>
            <p>사용자: {userData?.name}</p>
            {/* Todo 컴포넌트들 */}
        </div>
    );
}
''',
            'language': 'jsx',
            'difficulty': 'advanced',
            'tags': ['react', 'custom-hooks', 'localstorage', 'api']
        }
    ]
    
    for sample_data in code_samples:
        category = CodeCategory.objects.get(name=sample_data['category_name'])
        code_sample, created = CodeSample.objects.get_or_create(
            title=sample_data['title'],
            category=category,
            defaults={
                'description': sample_data['description'],
                'code': sample_data['code'].strip(),
                'language': sample_data['language'],
                'difficulty': sample_data['difficulty'],
                'tags': sample_data['tags']
            }
        )
        
        if created:
            print(f"코드 샘플 생성: {code_sample.title}")

if __name__ == '__main__':
    print("더미 데이터 생성을 시작합니다...")
    
    print("\n1. YAML 더미 데이터 생성 중...")
    create_yaml_dummy_data()
    
    print("\n2. 코드 샘플 더미 데이터 생성 중...")
    create_code_dummy_data()
    
    print("\n더미 데이터 생성이 완료되었습니다!")
    print("\n사용 가능한 API 엔드포인트:")
    print("- YAML 데이터: /yaml/")
    print("- 코드 샘플: /code/")
    print("- Swagger 문서: /swagger/") 