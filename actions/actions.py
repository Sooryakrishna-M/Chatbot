from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Example dictionary for BNS and IPC comparison
BNS_IPC_COMPARISON = {
    "375": {
        "bns": "BNS 63 (Rape) - Age of consent raised to 18.",
        "ipc": "IPC 375 (Rape) - Earlier allowed consent for minors in some cases."
    },
    "302": {
        "bns": "BNS 103 (Murder) - No major changes.",
        "ipc": "IPC 302 (Murder) - Life imprisonment or death penalty."
    },
    "376": {
        "bns": "BNS 66 (Rape in special cases) - Enhanced punishment.",
        "ipc": "IPC 376 (Rape) - Standard punishment."
    }
}

class ActionReportCrime(Action):
    def name(self):
        return "action_report_crime"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        crime_type = tracker.get_slot('crime_type').lower()

        crime_suggestions = {
            "abuse": ("BNS Section 63", "IPC Section 375"),
            "theft": ("BNS Section 96", "IPC Section 378"),
            "assault": ("BNS Section 115", "IPC Section 351")
        }

        if crime_type in crime_suggestions:
            bns_section, ipc_section = crime_suggestions[crime_type]
            dispatcher.utter_message(
                text=f"For {crime_type}, under BNS, you can file a case under Section {bns_section} and under IPC under Section {ipc_section}."
            )
        else:
            dispatcher.utter_message(text=f"No legal suggestions available for {crime_type}.")
        
        return []

class ActionCompareLaw(Action):
    def name(self):
        return "action_compare_law"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        section_number = tracker.get_slot('section_number')
        if section_number in BNS_IPC_COMPARISON:
            comparison = BNS_IPC_COMPARISON[section_number]
            dispatcher.utter_message(
                text=f"The comparison for section {section_number} is:\nBNS: {comparison['bns']}\nIPC: {comparison['ipc']}"
            )
        else:
            dispatcher.utter_message(text="No comparison available for this section.")
        
        return []
