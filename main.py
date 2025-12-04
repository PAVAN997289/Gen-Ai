import anthropic
import json
import os

# sample messages
MESSAGES = [
    "I love coffee in the morning",
    "I'm anxious about my interview",
    "I play guitar every evening",
    # ADD MORE MESSAGES HERE 
]

def extract_memories(messages, api_key):
    """Extract preferences, emotions, and facts from messages"""
    client = anthropic.Anthropic(api_key=api_key)
    
    # PROMPT FOR MEMORY EXTRACTION - CUSTOMIZE THIS
    prompt = """Analyze these messages and extract user preferences, emotional patterns, and facts.

Messages:
{messages}

Return only JSON:
{{"preferences": [], "emotional_patterns": [], "facts": []}}"""
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt.format(messages="\n".join(messages))}]
    )
    
    return json.loads(response.content[0].text.replace("```json", "").replace("```", ""))

def transform_persona(text, persona, memory, api_key):
    """Transform text using persona style"""
    client = anthropic.Anthropic(api_key=api_key)
    
    # PROMPT FOR PERSONALITY TRANSFORMATION - CUSTOMIZE THIS
    prompt = f"""You are a {persona}. 
User context: {json.dumps(memory)}
Transform this: "{text}"
Make it match your persona style."""
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content[0].text

def main():
    #  SET YOUR API KEY HERE OR USE ENVIRONMENT VARIABLE
    api_key = os.environ.get("ANTHROPIC_API_KEY", "PASTE_YOUR_API_KEY_HERE")
    
    print("\n=== MEMORY EXTRACTION ===\n")
    memories = extract_memories(MESSAGES, api_key)
    print(json.dumps(memories, indent=2))
    
    print("\n=== PERSONALITY ENGINE ===\n")
    base_text = "How are you feeling about your interview?"
    
    # DEFINE YOUR PERSONAS HERE - ADD OR MODIFY
    personas = ["Calm Mentor", "Witty Friend", "Therapist"]
    
    print(f"BASE: {base_text}\n")
    
    for persona in personas:
        print(f"\n{persona.upper()}:")
        result = transform_persona(base_text, persona, memories, api_key)
        print(result)

if __name__ == "__main__":
    main()

