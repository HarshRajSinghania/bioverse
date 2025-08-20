import requests
import os
import json
import random

class BioVerseApp:
    def __init__(self):
        # API Configuration
        self.llm_base_url = os.getenv('LLM_BASE_URL', 'https://samuraiapi.in/v1')
        self.llm_api_key = os.getenv('LLM_API_KEY', '')
        self.llm_model = os.getenv('LLM_MODEL', 'groq/moonshotai/kimi-k2-instruct')
        
        self.image_base_url = os.getenv('IMAGE_BASE_URL', 'https://api.together.xyz/v1')
        self.image_api_key = os.getenv('IMAGE_API_KEY', '')
        self.image_model = os.getenv('IMAGE_MODEL', 'black-forest-labs/FLUX.1-schnell-Free')
        
        # IMGBB API Configuration for permanent image hosting
        self.imgbb_api_key = os.getenv('IMGBB_API_KEY', '')
    
    def analyze_planet(self, planet_name):
        """Analyze planet characteristics using LLM API with retry logic"""
        prompt = f"""Analyze the planet "{planet_name}" and provide detailed planetary characteristics in a compact JSON format.
Example: {{"name":"{planet_name}","gravity":0.38,"atmosphere":"Thin CO2","temperature":-63,"radiation":"High","water":"Polar Ice Caps","dayLength":24,"yearLength":687,"description":"A red, rocky planet with thin atmosphere and polar ice caps."}}
"""
        
        # Retry mechanism with exponential backoff
        max_retries = 5
        base_delay = 1000  # 1 second
        
        for i in range(max_retries):
            try:
                body = {
                    "model": self.llm_model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 300
                }
                
                headers = {
                    'Authorization': f'Bearer {self.llm_api_key}',
                    'Content-Type': 'application/json'
                }
                
                response = requests.post(
                    f'{self.llm_base_url}/chat/completions',
                    json=body,
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f'Planet analysis API response: {data}')
                    if data.get('choices') and len(data['choices']) > 0:
                        content = data['choices'][0]['message']['content']
                        print(f'Planet analysis content: {content}')
                        # Try to parse JSON from the response
                        json_start = content.find('{')
                        json_end = content.rfind('}')
                        
                        if json_start != -1 and json_end != -1 and json_end > json_start:
                            json_string = content[json_start:json_end + 1]
                            print(f'Planet analysis JSON string: {json_string}')
                            try:
                                return json.loads(json_string)
                            except json.JSONDecodeError as e:
                                print(f'JSON decode error: {e}')
                                print(f'JSON string length: {len(json_string)}')
                                raise Exception(f'Invalid JSON in response: {e}')
                        else:
                            print(f'No JSON found in content. Content length: {len(content)}')
                            raise Exception('No valid JSON found in response')
                    else:
                        raise Exception('Invalid API response format')
                else:
                    raise Exception(f'API request failed with status {response.status_code}')
                    
            except Exception as e:
                print(f'Planet analysis attempt {i + 1} failed: {e}')
                
                # If this is the last retry, re-raise the exception
                if i == max_retries - 1:
                    raise e
                
                # Exponential backoff: 1s, 2s, 4s, 8s, 16s
                delay = base_delay * (2 ** i)
                print(f'Retrying in {delay}ms...')
                
                # Wait before retrying
                import time
                time.sleep(delay / 1000.0)
    
    def generate_alien(self, planet_data):
        """Generate alien species based on planet data using LLM API with retry logic"""
        prompt = f"""Create a scientifically accurate alien species for planet {planet_data['name']} with these characteristics:
Gravity: {planet_data['gravity']}g
Atmosphere: {planet_data['atmosphere']}
Temperature: {planet_data['temperature']}°C
Radiation: {planet_data['radiation']}
Water: {planet_data['water']}

Provide the response in a compact JSON format with these exact keys:
Example: {{"name":"AlienName","description":"Detailed description","physicalTraits":["trait1","trait2","trait3"],"abilities":["ability1","ability2","ability3"],"scientificName":"Genus species"}}
"""
        
        # Retry mechanism with exponential backoff
        max_retries = 5
        base_delay = 1000  # 1 second
        
        for i in range(max_retries):
            try:
                body = {
                    "model": self.llm_model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 300
                }
                
                headers = {
                    'Authorization': f'Bearer {self.llm_api_key}',
                    'Content-Type': 'application/json'
                }
                
                response = requests.post(
                    f'{self.llm_base_url}/chat/completions',
                    json=body,
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f'Alien generation API response: {data}')
                    if data.get('choices') and len(data['choices']) > 0:
                        content = data['choices'][0]['message']['content']
                        print(f'Alien generation content: {content}')
                        # Try to parse JSON from the response
                        json_start = content.find('{')
                        json_end = content.rfind('}')
                        
                        if json_start != -1 and json_end != -1 and json_end > json_start:
                            json_string = content[json_start:json_end + 1]
                            print(f'Alien generation JSON string: {json_string}')
                            try:
                                return json.loads(json_string)
                            except json.JSONDecodeError as e:
                                print(f'JSON decode error: {e}')
                                print(f'JSON string length: {len(json_string)}')
                                raise Exception(f'Invalid JSON in response: {e}')
                        else:
                            print(f'No JSON found in content. Content length: {len(content)}')
                            raise Exception('No valid JSON found in response')
                    else:
                        raise Exception('Invalid API response format')
                else:
                    raise Exception(f'API request failed with status {response.status_code}')
                    
            except Exception as e:
                print(f'Alien generation attempt {i + 1} failed: {e}')
                
                # If this is the last retry, re-raise the exception
                if i == max_retries - 1:
                    raise e
                
                # Exponential backoff: 1s, 2s, 4s, 8s, 16s
                delay = base_delay * (2 ** i)
                print(f'Retrying in {delay}ms...')
                
                # Wait before retrying
                import time
                time.sleep(delay / 1000.0)
    
    def generate_image_prompt(self, planet_data, alien_data):
        """Generate optimized image prompt using LLM for better image generation"""
        prompt = f"""Create a detailed, scientifically accurate image prompt for an alien creature specifically evolved for {planet_data['name']} with these exact conditions:

PLANETARY CONDITIONS:
- Gravity: {planet_data['gravity']}g
- Temperature: {planet_data['temperature']}°C
- Atmosphere: {planet_data['atmosphere']}
- Radiation: {planet_data['radiation']}
- Water: {planet_data['water']}

ALIEN SPECIES:
- Name: {alien_data['name']}
- Description: {alien_data['description']}
- Physical Traits: {', '.join(alien_data['physicalTraits'])}
- Abilities: {', '.join(alien_data['abilities'])}

GENERATE IMAGE PROMPT:
Create a highly detailed, scientifically accurate image prompt for this alien creature. The prompt should:
1. Be optimized for AI image generation (FLUX.1 model)
2. Include specific visual details about morphology and adaptations
3. Emphasize non-humanoid, truly alien characteristics
4. Include lighting, texture, and environmental context
5. Be 2-3 sentences maximum, highly descriptive
6. Focus on unique biological adaptations for the specific planetary conditions
7. Avoid any humanoid features, bipedal stance, or human-like elements

Return ONLY the image prompt text, no JSON or additional formatting."""

        max_retries = 3
        base_delay = 1000
        
        for i in range(max_retries):
            try:
                body = {
                    "model": self.llm_model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.8,
                    "max_tokens": 200
                }
                
                headers = {
                    'Authorization': f'Bearer {self.llm_api_key}',
                    'Content-Type': 'application/json'
                }
                
                response = requests.post(
                    f'{self.llm_base_url}/chat/completions',
                    json=body,
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    content = data['choices'][0]['message']['content'].strip()
                    return content
                else:
                    raise Exception(f'API request failed with status {response.status_code}')
                    
            except Exception as e:
                print(f'Image prompt generation attempt {i + 1} failed: {e}')
                
                if i == max_retries - 1:
                    # Fallback to basic prompt if all retries fail
                    return f"Scientifically accurate non-humanoid alien creature specifically evolved for {planet_data['name']} with {planet_data['gravity']}g gravity, {planet_data['temperature']}°C, {planet_data['atmosphere']} atmosphere. Create a completely alien lifeform - no humanoid features, no bipedal stance, no human-like limbs or face. Instead, design a truly extraterrestrial organism with unique morphology adapted to these planetary conditions. Include visible adaptations for gravity, temperature, atmospheric composition, and radiation levels. The creature should be biologically plausible but utterly alien in appearance."
                
                delay = base_delay * (2 ** i)
                import time
                time.sleep(delay / 1000.0)

    def generate_image(self, prompt):
        """Generate alien image using image generation API with retry logic and fallback"""
        print(f"Starting image generation with prompt: {prompt[:50]}...")
        
        # Check if API keys are configured
        if not self.image_api_key or not self.imgbb_api_key:
            print("⚠️ Image generation API keys not configured, using fallback placeholder")
            return "https://via.placeholder.com/1024x1024/0a0a2e/00ffff?text=Alien+Creature"
        
        body = {
            "prompt": prompt,
            "model": self.image_model,
            "n": 1,
            "quality": "standard",
            "response_format": "url",
            "size": "1024x1024",
            "style": "vivid"
        }
        
        # Retry mechanism with shorter timeout
        max_retries = 3
        base_delay = 500  # 0.5 second
        
        for i in range(max_retries):
            try:
                print(f"Attempt {i+1} of {max_retries}...")
                headers = {
                    'Authorization': f'Bearer {self.image_api_key}',
                    'Content-Type': 'application/json'
                }
                
                # Add timeout to prevent hanging
                response = requests.post(
                    f'{self.image_base_url}/images/generations',
                    json=body,
                    headers=headers,
                    timeout=30  # 30 second timeout
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f'✅ Image generation successful')
                    
                    # Handle different API response formats
                    temp_image_url = None
                    if data.get('data') and len(data['data']) > 0 and data['data'][0].get('url'):
                        temp_image_url = data['data'][0]['url']
                    elif data.get('output') and len(data['output']) > 0:
                        temp_image_url = data['output'][0]
                    
                    if temp_image_url:
                        print(f'📸 Temporary image URL: {temp_image_url}')
                        
                        # Try IMGBB upload, but with fallback
                        try:
                            permanent_url = self.upload_image_to_imgbb(temp_image_url)
                            print(f'✅ Permanent image URL: {permanent_url}')
                            return permanent_url
                        except Exception as e:
                            print(f'⚠️ IMGBB upload failed: {e}, using temporary URL')
                            return temp_image_url
                    else:
                        raise Exception('No valid image URL found in response')
                else:
                    print(f'❌ Image API error: {response.status_code} - {response.text}')
                    if i == max_retries - 1:
                        break
                        
            except requests.exceptions.Timeout:
                print(f'⏰ Image generation timeout on attempt {i+1}')
                if i == max_retries - 1:
                    break
            except Exception as e:
                print(f'❌ Image generation error: {e}')
                if i == max_retries - 1:
                    break
        
        # Fallback to placeholder if all attempts fail
        print('🔄 Using fallback placeholder image')
        return "https://via.placeholder.com/1024x1024/0a0a2e/00ffff?text=Alien+Creature"
    
    def upload_image_to_imgbb(self, image_url):
        """Upload image to IMGBB to get a permanent link"""
        try:
            print(f'Attempting to upload image from URL: {image_url}')
            # First, download the image from the temporary URL
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            print(f'Image downloaded successfully. Content length: {len(image_response.content)}')
            
            # Convert image content to base64
            import base64
            image_base64 = base64.b64encode(image_response.content).decode('utf-8')
            print(f'Image encoded to base64. Length: {len(image_base64)}')
            
            # Upload to IMGBB
            imgbb_url = "https://api.imgbb.com/1/upload"
            payload = {
                "key": self.imgbb_api_key,
                "image": image_base64
            }
            
            print(f'Sending upload request to IMGBB with API key: {self.imgbb_api_key[:8]}...')
            upload_response = requests.post(imgbb_url, data=payload)
            print(f'IMGBB upload response status: {upload_response.status_code}')
            print(f'IMGBB upload response content: {upload_response.text}')
            upload_response.raise_for_status()
            
            upload_data = upload_response.json()
            if upload_data.get('data') and upload_data['data'].get('url'):
                permanent_url = upload_data['data']['url']
                print(f'Successfully uploaded to IMGBB. Permanent URL: {permanent_url}')
                return permanent_url
            else:
                raise Exception('No URL found in IMGBB response')
                
        except Exception as e:
            print(f'IMGBB upload failed: {e}')
            raise e

    def analyze_survival(self, alien_data, environment):
        """Analyze how an alien would survive in an extreme environment"""
        prompt = f"""Analyze the survival of this alien species in the extreme environment:

ALIEN SPECIES:
Name: {alien_data['name']}
Physical Traits: {', '.join(alien_data['physicalTraits'])}
Abilities: {', '.join(alien_data['abilities'])}
Description: {alien_data['description']}

EXTREME ENVIRONMENT:
Name: {environment.name}
Type: {environment.type}
Temperature: {environment.temperature}
Atmosphere: {environment.atmosphere}
Gravity: {environment.gravity}g
Description: {environment.description}
Challenges: {environment.challenges}

Provide a detailed survival analysis in JSON format with:
1. survival_score (0-100)
2. analysis (detailed scientific analysis)
3. narrative (engaging story of the alien's experience)

Example: {{"survival_score":75,"analysis":"The alien's crystalline exoskeleton provides excellent protection against volcanic heat...","narrative":"As the alien descended into the volcanic world, its heat-resistant scales shimmered like molten metal..."}}
"""
        
        max_retries = 3
        base_delay = 1000
        
        for i in range(max_retries):
            try:
                body = {
                    "model": self.llm_model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 500
                }
                
                headers = {
                    'Authorization': f'Bearer {self.llm_api_key}',
                    'Content-Type': 'application/json'
                }
                
                response = requests.post(
                    f'{self.llm_base_url}/chat/completions',
                    json=body,
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    content = data['choices'][0]['message']['content']
                    
                    # Parse JSON from response
                    json_start = content.find('{')
                    json_end = content.rfind('}')
                    
                    if json_start != -1 and json_end != -1:
                        json_string = content[json_start:json_end + 1]
                        result = json.loads(json_string)
                        
                        # Ensure all required fields are present
                        return {
                            'survival_score': result.get('survival_score', 50),
                            'analysis': result.get('analysis', 'Analysis not available'),
                            'narrative': result.get('narrative', 'Narrative not available')
                        }
                    else:
                        raise Exception('No valid JSON found in response')
                else:
                    raise Exception(f'API request failed with status {response.status_code}')
                    
            except Exception as e:
                print(f'Survival analysis attempt {i + 1} failed: {e}')
                
                if i == max_retries - 1:
                    # Return default analysis if all retries fail
                    return {
                        'survival_score': 50,
                        'analysis': f'Unable to analyze survival due to API limitations. Based on basic characteristics, this alien may face significant challenges in the {environment.name} environment.',
                        'narrative': f'The {alien_data["name"]} ventures into the {environment.name}, facing unknown challenges in this hostile world.'
                    }
                
                delay = base_delay * (2 ** i)
                import time
                time.sleep(delay / 1000.0)