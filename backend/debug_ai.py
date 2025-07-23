#!/usr/bin/env python3
"""
Simple Debug Script - See what OpenAI returns
"""

import os
import openai
import json

def debug_openai():
    """Debug what OpenAI returns for your content"""
    
    print("🔍 DEBUGGING OPENAI RESPONSE")
    print("=" * 40)
    
    # Read your content
    try:
        with open('../module1_content.txt', 'r') as f:
            content = f.read()
        print(f"✅ Loaded content: {len(content)} characters")
    except:
        print("❌ Could not load ../module1_content.txt")
        return
    
    # Get API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ No OpenAI API key found")
        return
    
    print(f"✅ API key found: {api_key[:20]}...")
    
    # Create client
    client = openai.OpenAI(api_key=api_key)
    
    # Simple prompt
    prompt = f"""
    Extract key concepts from this educational content about communication theory.
    
    Content (first 2000 chars):
    {content[:2000]}
    
    Return ONLY valid JSON with this structure:
    {{
        "key_concepts": {{
            "concept1": "definition1"
        }},
        "real_world_examples": {{
            "example1": "description1"
        }}
    }}
    """
    
    try:
        print("🤖 Calling OpenAI...")
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=800
        )
        
        result = response.choices[0].message.content.strip()
        
        print("📝 RAW RESPONSE:")
        print("-" * 50)
        print(result)
        print("-" * 50)
        
        # Try to parse
        if result.startswith("```json"):
            result = result[7:]
        if result.endswith("```"):
            result = result[:-3]
        result = result.strip()
        
        print("🧹 CLEANED RESPONSE:")
        print("-" * 50)
        print(result)
        print("-" * 50)
        
        try:
            parsed = json.loads(result)
            print("✅ JSON PARSING SUCCESS!")
            print(f"📊 Found {len(parsed.get('key_concepts', {}))} concepts")
            print(f"📊 Found {len(parsed.get('real_world_examples', {}))} examples")
            
            # Show concepts
            for concept, definition in parsed.get('key_concepts', {}).items():
                print(f"  🎯 {concept}: {definition[:80]}...")
                
        except json.JSONDecodeError as e:
            print(f"❌ JSON PARSING FAILED: {e}")
            print("The AI didn't return valid JSON")
            
    except Exception as e:
        print(f"❌ OpenAI API call failed: {e}")

if __name__ == "__main__":
    debug_openai()
