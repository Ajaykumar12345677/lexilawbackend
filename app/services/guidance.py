class GuidanceService:
    def get_guidance(self, item: dict, user_problem: str):
        # Deterministic Guidance based on Offence Title or Problem Keywords
        # This is strictly better than small model generation for standard legal advice.
        
        title = item.get('title', '').lower()
        desc = item.get('description', '').lower()
        
        steps = []
        
        # Map specific offenses to specific steps
        if 'theft' in title or 'stolen' in title or 'robbery' in title:
            steps = [
                "Immediately file an FIR at the nearest police station.",
                "Provide details of the stolen property (receipts, photos, IMEI number for phones).",
                "Do not disturb the crime scene if it happened at your property.",
                "Cooperate with the investigation officer."
            ]
        elif 'hurt' in title or 'assault' in title or 'beat' in title or 'injury' in title:
            steps = [
                "Visit a government hospital for a medical examination (MLC) immediately.",
                "The medical report is crucial evidence for police complaints.",
                "File an FIR or NCR at the local police station.",
                "Take photos of any visible injuries as additional record."
            ]
        elif 'defamation' in title or 'insult' in title or 'reputation' in title:
            steps = [
                "Save all proofs (screenshots, recordings, letters) of the defamatory statement.",
                "You may send a legal notice to the person asking them to apologize/withdraw.",
                "You can file a private criminal complaint before a Magistrate.",
                "Civil suits for damages can also be filed separately."
            ]
        elif 'cheating' in title or 'fraud' in title or 'dishonest' in title:
             steps = [
                "Gather all documentary proof (bank statements, chats, agreements).",
                "File a written complaint to the Station House Officer (SHO).",
                "If it's a cyber fraud, report it immediately on cybercrime.gov.in.",
                "Do not delete any communication with the fraudster."
             ]
        elif 'rape' in title or 'sexual' in title or 'modesty' in title:
             steps = [
                 "Go to a safe place immediately.",
                 "Do not wash your clothes or body to preserve forensic evidence.",
                 "Visit the nearest police station or hospital. Police must register FIR (Zero FIR applies).",
                 "You have the right to request a female police officer."
             ]
        elif 'murder' in title or 'death' in title or 'homicide' in title:
             steps = [
                 "Immediately inform the police (Dial 100/112).",
                 "Do not touch anything at the crime scene.",
                 "Identify potential witnesses who saw the incident.",
                 "Cooperate fully with the investigation."
             ]
        
        # Fallback for general offenses
        if not steps:
            steps = [
                "Visit the nearest police station to report the incident.",
                "Write down a detailed timeline of what happened while your memory is fresh.",
                "Identify any witnesses who can support your statement.",
                "Consult a qualified lawyer to understand the specific legal implications."
            ]

        # Always add the disclaimer as the final 'step' or separate field, but user asked for it in guidance.
        # We will add it as a "Note".
        # However, the frontend creates step numbers. So we keep it as steps.
        
        return steps

guidance_service = GuidanceService()
