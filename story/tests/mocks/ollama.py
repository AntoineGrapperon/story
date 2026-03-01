import json

class ResponseError(Exception):
    pass

def generate(model, prompt):
    """
    Mocks the ollama.generate function.
    Returns a predefined response based on the prompt content.
    """
    # Mock for identify_characters_with_ollama in analyze_story.py
    if "identify all named characters and their frequency" in prompt:
        return {
            'response': json.dumps({
                "D'Artagnan": 10,
                "Athos": 5,
                "Porthos": 3,
                "Aramis": 2
            })
        }
    
    # Mock for identify_setups in analyze_narrative.py
    if "identify potential \"setups\"" in prompt:
        return {
            'response': json.dumps([
                {
                    "id": "S1",
                    "description": "Mock setup description",
                    "location": "Mock location"
                }
            ])
        }
    
    # Mock for analyze_payoffs in analyze_narrative.py
    if "determine if this specific setup has a \"payoff\"" in prompt:
        return {
            'response': json.dumps({
                "id": "S1",
                "status": "Paid Off",
                "payoff_description": "Mock payoff description",
                "payoff_location": "Mock payoff location"
            })
        }

    # Mock for character_profiler.py
    if "following fiction writing elements" in prompt or "Character Name:" in prompt:
        # Extract character name from prompt if possible
        import re
        match = re.search(r'Character Name: (.*)\n', prompt)
        character_name = match.group(1).strip() if match else "D'Artagnan"
        
        return {
            'response': f"""
# Character Profile: {character_name}

### Physical Appearance:
A young man from Gascony.

### Personality Traits:
Brave, hot-headed, and loyal.

### Backstory/History:
Son of a noble but poor family.

### Motivations & Goals:
To become a King's Musketeer.

### Strengths & Weaknesses:
Excellent swordsman but impulsive.

### Relationships:
Friends with the Three Musketeers.

### Dialogue & Speech Patterns:
Determined and polite.

### Actions & Behavior:
Fights for honor.

### Internal Thoughts & Feelings:
Wants to prove himself.

### Growth & Arc (Initial Impression):
Starting his journey.
"""
        }

    # Default fallback response
    return {
        'response': "This is a mock response from the fake Ollama."
    }
