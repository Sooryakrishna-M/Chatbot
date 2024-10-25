from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Define a dictionary with keywords to help identify relevant topics and sections
BNS_SECTIONS = {
    "punishments": {
        "description": "BNS defines various forms of punishment such as death, life imprisonment, fines, and community service.",
        "keywords": ["punishment", "fine", "death penalty", "community service", "imprisonment"],
        "details": {
            "death": "Punishable by the state for the most severe crimes.",
            "life_imprisonment": "Can be imposed for crimes of high severity, served as rigorous or simple imprisonment.",
            "community_service": "Aimed at rehabilitation for less severe crimes."
        }
    },
    "offences_against_women_and_children": {
        "keywords": ["rape", "dowry death", "assault", "women", "children"],
        "sections": {
            "63": {
                "title": "Rape",
                "bns": "Defines and criminalizes rape with age of consent at 18, with enhanced punishment."
            },
            "74": {
                "title": "Assault with Intent to Outrage Modesty",
                "bns": "Defines assault with intent to harm modesty of a woman."
            },
            "80": {
                "title": "Dowry Death",
                "bns": "Defines dowry-related offences with strict punishment for resulting deaths."
            }
        }
    },
    "criminal_force_and_assault": {
        "keywords": ["force", "assault", "criminal force"],
        "sections": {
            "128": {
                "title": "Definition of Force",
                "bns": "Defines the use of force as any motion imposed on another person without consent."
            },
            "130": {
                "title": "Definition of Assault",
                "bns": "An action intended to cause apprehension of harm without physical contact."
            },
            "131": {
                "title": "Punishment for Assault",
                "bns": "Punishes assault with imprisonment or fine, varies with intent and harm caused."
            }
        }
    },
    "kidnapping_and_abduction": {
        "keywords": ["kidnapping", "abduction", "ransom"],
        "sections": {
            "137": {
                "title": "Kidnapping from Lawful Guardianship",
                "bns": "Kidnapping a minor or person of unsound mind from their lawful guardian without consent."
            },
            "138": {
                "title": "Abduction",
                "bns": "Forcing or deceiving a person to move from one place to another against their will."
            },
            "140": {
                "title": "Kidnapping for Ransom",
                "bns": "Kidnapping with intent to demand ransom or harm, with severe punishments."
            }
        }
    }
}

class ActionAnswerLegalQuestion(Action):
    def name(self):
        return "action_answer_legal_question"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        user_message = tracker.latest_message.get('text').lower()
        response = None

        # Match user message with topics and sections using keywords
        for topic, content in BNS_SECTIONS.items():
            # Check if any keyword matches the user message
            if any(keyword in user_message for keyword in content.get("keywords", [])):
                # Respond with general topic information if available
                response = f"Here's information on {topic.capitalize()}:\n{content['description']}\n"
                break
            
            # Check specific sections within each topic if keywords are found
            for section, details in content.get("sections", {}).items():
                if section in user_message or any(keyword in user_message for keyword in content["keywords"]):
                    response = (
                        f"Section {section} - {details['title']}:\nBNS: {details['bns']}"
                    )
                    break
            if response:
                break

        # Default response if no match is found
        if not response:
            response = "I'm sorry, I couldn't find specific legal information on that topic or section."

        dispatcher.utter_message(text=response)
        return []
