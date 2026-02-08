class AISimplifier:
    def __init__(self):
        # Removed heavy DL model (T5) to ensure instant response times (<1s).
        # We now rely primarily on the manually curated 'simple_desc' from the JSON data.
        pass

    def simplify(self, text: str) -> str:
        # Since we are prioritizing speed, we will not run runtime-AI simplification.
        # If the manual simplified description is missing, we return the original 
        # (or a message saying it's the original text).
        return text

    def generate_guidance_steps(self, problem_description: str) -> list:
        # This method is no longer used for generation as we switched to 
        # deterministic guidance in guidance.py. Keeping it for interface compatibility 
        # if needed, or we can just ignore it.
        return []

    def _get_fallback_guidance(self):
        return []

simplifier = AISimplifier()
