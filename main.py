from openai import OpenAI
import json
import os

# sample messages
MESSAGES = [
    "I love coffee in the morning",
    "I'm anxious about my interview",
    "I play guitar every evening",
    "I tend to procrastinate when stressed",
    "I'm a software engineer working on AI",
    "I prefer texts over calls",
    "I get excited learning new programming languages",
    "I've been feeling lonely in my new city",
    "I love spicy Thai food",
    "I'm not a morning person",
    "I struggle with imposter syndrome",
    "I enjoy hiking on weekends",
    "I get frustrated with slow replies",
    "Trying to go to gym regularly",
    "I love sci-fi movies",
    "I overthink social interactions",
    "I'm vegetarian for 3 years",
    "I get motivated by passion projects",
    "Having trouble sleeping due to stress",
    "I love reading tech blogs",
    "I'm anxious in large gatherings",
    "Learning Spanish on Duolingo daily",
    "I feel guilty taking breaks",
    "I love RPG video games",
    "I'm hard on myself for mistakes",
    "Planning to adopt a dog soon",
    "I get energized solving technical problems",
    "I journal to manage anxiety",
    "I listen to lo-fi while coding",
    "Trying to make friends in new city"
]

def extract_memories(messages, api_key):
    """Extract preferences, emotions, and facts from messages"""
    client = OpenAI(api_key=api_key)
    
    # PROMPT FOR MEMORY EXTRACTION
    prompt = f"""You are a memory extraction system for a companion AI. Analyze these messages and extract what's important to remember about this user.

Messages:
{chr(10).join(f"{i+1}. {msg}" for i, msg in enumerate(messages))}

Extract three categories:
1. PREFERENCES: Their likes, dislikes, habits, choices (what they enjoy/avoid)
2. EMOTIONAL_PATTERNS: Recurring feelings, triggers, mental health patterns, how they respond to stress
3. FACTS: Concrete life information - job, location, relationships, goals, background

Be specific and detailed. Extract 8-12 items per category. Use their own language when possible.

Return ONLY valid JSON:
{{"preferences": ["item1", "item2", ...], "emotional_patterns": ["item1", "item2", ...], "facts": ["item1", "item2", ...]}}"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Cheapest model, or use "gpt-4o" for better quality
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=2000
    )
    
    text = response.choices[0].message.content.replace("```json", "").replace("```", "").strip()
    return json.loads(text)

def transform_persona(text, persona, memory, api_key):
    """Transform text using persona style"""
    client = OpenAI(api_key=api_key)
    
    # PROMPT FOR PERSONALITY TRANSFORMATION
    prompt = f"""You are a {persona} responding to a user you know well.

USER CONTEXT:
Preferences: {', '.join(memory.get('preferences', [])[:5])}
Emotions: {', '.join(memory.get('emotional_patterns', [])[:5])}
Facts: {', '.join(memory.get('facts', [])[:5])}

ORIGINAL MESSAGE: "{text}"

Rewrite this completely in your {persona} voice:
- Reference specific user details naturally
- Transform tone, structure, and delivery entirely
- Be authentic to your persona style
- Make it feel personalized

Write ONLY your response:"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Cheapest model, or use "gpt-4o" for better quality
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=1000
    )
    
    return response.choices[0].message.content

def main():
    # PASTE YOUR OPENAI API KEY HERE
    api_key = os.environ.get("OPENAI_API_KEY", "PASTE_YOUR_OPENAI_API_KEY_HERE")
    
    if "PASTE_YOUR" in api_key:
        print("\n ERROR: Please add your OpenAI API key on line 103!")
        print("Get it from: https://platform.openai.com/api-keys\n")
        return
    
    print("\n=== MEMORY EXTRACTION ===\n")
    try:
        memories = extract_memories(MESSAGES, api_key)
        print(json.dumps(memories, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        return
    
    print("\n=== PERSONALITY ENGINE ===\n")
    base_text = "How are you feeling about your interview?"
    
    # DEFINE YOUR PERSONAS HERE - ADD OR MODIFY
    personas = ["Calm Mentor", "Witty Friend", "Therapist"]
    
    print(f"BASE: {base_text}\n")
    
    for persona in personas:
        print(f"\n{persona.upper()}:")
        try:
            result = transform_persona(base_text, persona, memories, api_key)
            print(result)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

