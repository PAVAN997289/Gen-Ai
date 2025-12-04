import anthropic
import json
import os

# sample messages
MESSAGES = [
    "I love coffee in the morning",
    "I'm anxious about my interview",
    "I play guitar every evening",
    # ADD MORE MESSAGES HERE (need 30 total)
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
    client = anthropic.Anthropic(api_key=api_key)
    
    # PROMPT FOR MEMORY EXTRACTION - CUSTOMIZE THIS
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
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    text = response.content[0].text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)

def transform_persona(text, persona, memory, api_key):
    """Transform text using persona style"""
    client = anthropic.Anthropic(api_key=api_key)
    
    # PROMPT FOR PERSONALITY TRANSFORMATION - CUSTOMIZE THIS
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
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content[0].text

def main():
    # SET YOUR API KEY HERE OR USE ENVIRONMENT VARIABLE
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
