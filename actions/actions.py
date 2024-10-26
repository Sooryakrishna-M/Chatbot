from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Detailed dictionary for BNS clauses, including specific clause descriptions
BNS_CLAUSES = {
    "punishments": {
        "description": "BNS describes punishments for various crimes, including death, life imprisonment, fines, and community service. "
                       "Each punishment type varies in severity, based on the nature of the crime and the intent involved.",
        "keywords": ["punishment", "fine", "death penalty", "community service", "imprisonment"],
        "details": {
            "death": "Death penalty is prescribed for the most heinous crimes, such as murder with intent, treason, and other cases where "
                     "rehabilitation is deemed impossible or insufficient for justice.",
            "life_imprisonment": "Life imprisonment may be imposed for crimes of high severity, served as either rigorous or simple imprisonment, "
                                 "depending on the nature of the crime and judicial discretion.",
            "community_service": "Community service is considered a corrective measure for less severe crimes, aimed at rehabilitating the offender and giving back to society."
        }
    },
    "offences_against_women_and_children": {
        "description": "This category covers offenses against women and children, including rape, assault, and dowry-related violence. "
                       "The laws in this category are designed to protect the safety, dignity, and rights of women and children.",
        "keywords": ["rape", "dowry death", "assault", "women", "children"],
        "clauses": {
            "63": {
                "title": "Rape",
                "bns": "BNS Clause 63 defines rape as non-consensual sexual intercourse, raising the age of consent to 18. "
                       "It outlines severe penalties, with enhanced punishment if the crime involves violence or if the victim is a minor."
            },
            "74": {
                "title": "Assault with Intent to Outrage Modesty",
                "bns": "BNS Clause 74 criminalizes any form of assault aimed at outraging a woman's modesty, with severe penalties. "
                       "This includes verbal, physical, and non-verbal actions intended to cause humiliation."
            },
            "80": {
                "title": "Dowry Death",
                "bns": "BNS Clause 80 addresses dowry-related deaths, imposing strict punishment for those found guilty of causing or facilitating dowry-based violence "
                       "that results in the victim’s death. This clause aims to deter dowry-related abuse and protect women."
            }
        }
    },
    "criminal_force_and_assault": {
        "description": "These clauses address crimes involving the use of force or intent to harm, including definitions for assault, force, "
                       "and aggravated assault. The severity of punishment depends on the intent and harm caused.",
        "keywords": ["force", "assault", "criminal force"],
        "clauses": {
            "128": {
                "title": "Definition of Force",
                "bns": "BNS Clause 128 defines force as any physical action imposed on another person without their consent. This includes any act that "
                       "induces bodily movement, even without direct physical harm."
            },
            "130": {
                "title": "Definition of Assault",
                "bns": "BNS Clause 130 defines assault as an act intended to cause fear of harm without actual physical contact. The purpose of this clause "
                       "is to criminalize attempts to intimidate or threaten others through gestures or actions."
            },
            "131": {
                "title": "Punishment for Assault",
                "bns": "BNS Clause 131 prescribes punishments for assault, varying based on the intent and resulting harm. Penalties range from fines to "
                       "imprisonment, depending on the severity of the act and whether it caused physical harm."
            }
        }
    },
    "kidnapping_and_abduction": {
        "description": "BNS categorizes crimes related to kidnapping and abduction, including the unlawful removal of individuals from lawful guardianship or by force. "
                       "It also addresses kidnapping for ransom, with varying punishments depending on the intent and consequences of the act.",
        "keywords": ["kidnapping", "abduction", "ransom"],
        "clauses": {
            "137": {
                "title": "Kidnapping from Lawful Guardianship",
                "bns": "BNS Clause 137 criminalizes kidnapping a minor or a person of unsound mind from their lawful guardian without consent. "
                       "This clause aims to protect vulnerable individuals from being unlawfully taken from their guardians."
            },
            "138": {
                "title": "Abduction",
                "bns": "BNS Clause 138 defines abduction as forcibly or deceptively moving a person from one place to another against their will. "
                       "This includes cases where the abductor intends to harm or exploit the victim."
            },
            "140": {
                "title": "Kidnapping for Ransom",
                "bns": "BNS Clause 140 addresses kidnapping committed with the intent to demand ransom. This clause imposes severe punishments, "
                       "given the high level of threat and harm involved in such crimes."
            }
        }
    }
}

INDIAN_LAW_KNOWLEDGE = {
    "constitutional_law": {
        "description": "Constitutional Law includes principles and rules within the Indian Constitution governing fundamental rights, directive principles, and government structure.",
        "keywords": ["constitutional"],
        "questions": {
            "fundamental rights under article 21": "Article 21 of the Indian Constitution protects the Right to Life and Personal Liberty. It includes the right to privacy, dignified life, and protection from arbitrary deprivation of life.",
            "right to privacy": "The Right to Privacy is safeguarded as a fundamental right under Article 21, reinforced by the Puttaswamy case. It covers privacy in personal data, bodily autonomy, and more.",
            "freedom of speech": "Article 19(1)(a) protects Freedom of Speech and Expression, allowing citizens to express opinions freely, subject to reasonable restrictions under Article 19(2) like security, public order, and decency."
        }
    },
    "civil_law": {
        "description": "Civil Law addresses non-criminal disputes involving individuals or entities, covering matters like marriage, contracts, and property rights.",
        "keywords": ["civil"],
        "questions": {
            "grounds for divorce under hindu marriage act": "Under the Hindu Marriage Act, 1955, grounds for divorce include adultery, cruelty, desertion, conversion, mental disorder, and incurable disease.",
            "filing a consumer complaint": "To file a consumer complaint, approach the District, State, or National Consumer Disputes Redressal Commission based on the claim amount. The complaint must state the grievance and desired resolution.",
            "limitation period for civil suit": "The Limitation Act, 1963, generally mandates filing civil suits within 3 years from when the cause of action arises. Specific cases may have different periods."
        }
    },
    "criminal_law": {
        "description": "Criminal Law governs offenses against the state and individuals, aiming to maintain public order and safety. It includes the Indian Penal Code (IPC) and Criminal Procedure Code (CrPC).",
        "keywords": ["criminal law"],
        "questions": {
            "ingredients of murder under ipc section 302": "Section 302 IPC defines murder, requiring intent to kill, knowledge of likely death, or intent to cause bodily harm likely to cause death.",
            "concept of bail": "Bail allows temporary release of an accused from custody. Types include regular, interim, and anticipatory bail, as governed by CrPC Sections 437-439.",
            "penalties for dui": "Driving under the influence is penalized under Section 185 of the Motor Vehicles Act, 1988, with fines up to ₹10,000 and/or imprisonment for repeat offenses."
        }
    },
    "corporate_law": {
        "description": "Corporate Law governs business operations, including company formation, compliance, and corporate governance in India.",
        "keywords": ["cooperative"],
        "questions": {
            "compliance requirements for a startup": "Compliance requirements for startups include registration, tax compliance (GST, TDS), labor laws, and intellectual property protection. Regular filings with regulatory bodies are mandatory.",
            "process for registering a company": "To register a company, apply through the Ministry of Corporate Affairs, file necessary documents, and obtain a Certificate of Incorporation under the Companies Act, 2013.",
            "insolvency and bankruptcy code": "The Insolvency and Bankruptcy Code, 2016, provides a time-bound process to resolve insolvency, aiming to protect creditors' interests and ensure business viability."
        }
    },
    "family_law": {
        "description": "Family Law addresses legal issues within family relationships, such as marriage, divorce, adoption, and child custody.",
        "keywords": ["family"],
        "questions": {
            "child custody in india": "Child custody in India is governed by laws including the Hindu Minority and Guardianship Act, and considers the child's welfare as paramount, with custody granted to one or both parents.",
            "maintenance under hindu adoption and maintenance act": "Under the Hindu Adoption and Maintenance Act, 1956, maintenance refers to support (financial or otherwise) that one family member is obligated to provide another, such as a spouse or parent.",
            "definition of domestic violence": "Domestic Violence in India is defined under the Protection of Women from Domestic Violence Act, 2005, and includes physical, emotional, sexual, and economic abuse within domestic relationships."
        }
    },
    "intellectual_property_law": {
        "description": "Intellectual Property Law covers legal rights associated with inventions, trademarks, copyright, and designs.",
        "keywords": ["intellectual property"],
        "questions": {
            "types of patents": "India grants three types of patents: ordinary patents, patents of addition, and convention patents. Each type serves different needs for inventors and businesses.",
            "process for registering a trademark": "To register a trademark, submit an application to the Trademark Registrar, conduct an examination, and await publication. If unopposed, the trademark is registered and protected for 10 years.",
            "penalties for copyright infringement": "Copyright infringement in India attracts civil and criminal penalties, including fines, injunctions, and imprisonment for severe violations."
        }
    },
    "labor_and_employment_law": {
        "description": "Labor and Employment Law regulates workplace conditions, wages, safety, and employee rights.",
        "keywords": ["labour","employment"],
        "questions": {
            "minimum wages in india": "Minimum wages are set by the respective state governments, ensuring fair remuneration. The Minimum Wages Act, 1948, governs this across various industries.",
            "retrenchment under industrial disputes act": "Retrenchment under the Industrial Disputes Act, 1947, refers to the termination of employees due to operational needs. It requires due notice and compensation based on tenure.",
            "sexual harassment at workplace": "Sexual harassment in the workplace is prohibited under the Sexual Harassment of Women at Workplace Act, 2013, mandating Internal Committees in organizations to handle complaints."
        }
    },
    "property_law": {
        "description": "Property Law governs the ownership, transfer, and rights associated with property, including inheritance and tenancy rights.",
        "keywords": ["property"],
        "questions": {
            "laws governing inheritance": "Inheritance laws in India vary by religion, with the Hindu Succession Act, 1956, governing Hindus, and the Indian Succession Act, 1925, for others, determining property rights after death.",
            "process for registering a property": "Property registration involves the execution of a sale deed, payment of stamp duty, and registration at the local sub-registrar's office to transfer legal ownership.",
            "rights of tenant under rent control act": "The Rent Control Act provides tenants with rights including protection against eviction, fair rent, and maintenance obligations by landlords."
        }
    },
    "taxation_law": {
        "description": "Taxation Law includes regulations on income, property, and corporate taxes, governing revenue generation by the government.",
        "keywords": ["taxation"],
        "questions": {
            "tax implications of selling property": "The sale of property in India is subject to capital gains tax. Short-term gains are taxed as per the individual's income slab, while long-term gains attract a 20% tax with indexation benefits.",
            "concept of gst": "Goods and Services Tax (GST) is a comprehensive, multi-stage tax applied at each stage of the supply chain, with credit available for taxes paid on inputs, aiming to unify indirect taxes in India.",
            "tax benefits for startups": "Startups registered under the Startup India scheme can access tax benefits including income tax exemption for three consecutive years and exemptions on capital gains."
        }
    },
    "miscellaneous": {
        "description": "This category covers various legal aspects such as public interest litigations, cybersecurity, and the judiciary.",
        "keywords": ["miscellaneous"],
        "questions": {
            "filing a public interest litigation": "To file a Public Interest Litigation (PIL), submit a writ petition directly to the High Court or Supreme Court, citing issues of public importance.",
            "indian judicial system hierarchy": "The Indian judiciary consists of the Supreme Court at the top, followed by High Courts in each state, and subordinate courts including district and session courts.",
            "cybersecurity laws": "India's cybersecurity framework includes the Information Technology Act, 2000, covering cybercrimes, data protection, and penalties for offenses like hacking and identity theft."
        }
    }
}


class ActionAnswerLegalQuestion(Action):
    def name(self):
        return "action_answer_legal_question"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        user_message = tracker.latest_message.get('text').lower()
        response = None

        # 1. First, check for specific BNS clauses
        for topic, content in BNS_CLAUSES.items():
            # Check specific clauses within each topic for a match
            for clause, details in content.get("clauses", {}).items():
                if clause in user_message or details["title"].lower() in user_message:
                    response = (
                        f"Clause {clause} - {details['title']}:\nBNS: {details.get('bns', 'No BNS information available.')}"
                    )
                    break
            if response:
                break
            
            # Check if any keyword in general BNS topics match
            if any(keyword in user_message for keyword in content.get("keywords", [])):
                response = f"Here's information on {topic.replace('_', ' ').capitalize()}:\n{content.get('description', 'No detailed description available.')}\n"
                break

        # 2. If no specific clause found, check for general Indian law questions
        if not response:
            for topic, content in INDIAN_LAW_KNOWLEDGE.items():
                # Check if specific questions within each law topic match
                for question, answer in content.get("questions", {}).items():
                    if question in user_message:
                        response = answer
                        break
                if response:
                    break

                # Check if general law topic keywords match
                if topic in user_message:
                    response = f"Here's information on {topic.replace('_', ' ').capitalize()}:\n{content.get('description', 'No detailed description available.')}\n"
                    break

        # Default response if no specific information is found
        if not response:
            response = "I'm sorry, I couldn't find specific legal information about that topic."

        dispatcher.utter_message(text=response)
        return []
