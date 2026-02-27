FRENCH_CONFIG = {
    "name": "French",
    "native_name": "Français",
    "code": "fr",
    "voice": "fr-FR-DeniseNeural",
    "flag": "🇫🇷",
    "fallback_voices": ["fr-FR-HenriNeural", "fr-CA-SylvieNeural"],
    "phonetics": {
        "difficult_sounds": ["r guttural", "u vs ou", "é vs è", "nasal vowels (an, in, on, un)", "liaison"],
        "tips": "The French 'r' is produced at the back of the throat. Nasal vowels are unique — practice them daily.",
    },
    "grammar_focus": [
        "Gender of nouns — no clear rule, must be memorised",
        "Verb conjugation: être/avoir as auxiliary in passé composé",
        "Subjonctif after verbs of doubt, wish and emotion",
        "Partitive articles (du, de la, de l', des)",
        "Pronoun order with double pronouns (me le, te la, lui en...)",
    ],
    "false_friends_with_spanish": [
        {"french": "chat", "means": "cat", "not": "chat (internet)"},
        {"french": "rester", "means": "to stay", "not": "to rest (that's 'se reposer')"},
        {"french": "assister à", "means": "to attend", "not": "to assist (that's 'aider')"},
        {"french": "lecture", "means": "reading", "not": "lecture (that's 'conférence')"},
        {"french": "sensible", "means": "sensitive", "not": "sensible (that's 'raisonnable')"},
        {"french": "large", "means": "wide", "not": "large (that's 'grand')"},
        {"french": "prétendre", "means": "to claim", "not": "to pretend (that's 'faire semblant')"},
        {"french": "versatile", "means": "fickle/changeable", "not": "versatile (that's 'polyvalent')"},
    ],
    "cultural_notes": [
        "Vouvoiement (vous) is used for strangers, elders and formal contexts",
        "La bise (cheek kiss greeting) varies by region: 1 to 4 kisses",
        "Meals are a cultural ritual — lunch can last 2 hours",
        "The Académie française regulates official French vocabulary",
        "Verlan is a popular back-slang used by youth (l'envers → verlan)",
        "French cinema (Nouvelle Vague) is essential cultural knowledge",
    ],
    "recommended_media": {
        "films": [
            "Intouchables (2011) — B1 contemporary French, clear speech",
            "Amélie (2001) — B1/B2 rich vocabulary and Parisian culture",
            "Les Choristes (2004) — A2/B1 clear pronunciation",
            "La Haine (1995) — B2/C1 verlan and banlieue French",
            "Au revoir les enfants (1987) — C1 historical vocabulary",
        ],
        "music": [
            "Édith Piaf — classic French, clear diction, emotional vocabulary",
            "Stromae — contemporary Belgian French, modern themes",
            "Zaz — clear pronunciation, optimistic vocabulary",
            "Indochine — 80s rock, B1+ vocabulary",
            "MC Solaar — rap with wordplay, advanced learners",
        ],
        "podcasts": [
            "News in Slow French — A2 to B2, graded content",
            "Français Authentique — natural speech, B1+",
            "RFI Journal en français facile — A2/B1 news",
            "France Inter — native speed, B2+",
            "Coffee Break French — structured lessons, A1 to B2",
        ],
        "books": [
            "Le Petit Prince (Saint-Exupéry) — A2/B1 poetic simplicity",
            "L'Étranger (Camus) — B2 existentialist prose",
            "Astérix (comics) — B1 humour and cultural references",
            "Bonjour Tristesse (Sagan) — B2 elegant narrative",
            "Les Misérables abridged (Hugo) — C1 classic vocabulary",
        ],
    },
    "curriculum": {
        "A1": {
            "label": "Beginner",
            "grammar": [
                "French alphabet and pronunciation basics",
                "Definite and indefinite articles (le, la, l', les / un, une, des)",
                "Gender and number of nouns",
                "Subject pronouns (je, tu, il/elle, nous, vous, ils/elles)",
                "Present tense: être and avoir",
                "Present tense: regular -ER verbs",
                "Negation with ne...pas",
                "Basic adjectives and agreement",
            ],
            "vocabulary": [
                "Greetings and farewells (bonjour, au revoir, merci...)",
                "Numbers 1–100",
                "Days, months, seasons",
                "Colors",
                "Family members",
                "Body parts",
                "Classroom and everyday objects",
                "Nationalities and countries",
            ],
            "conversation": [
                "Introducing yourself: name, age, nationality, job",
                "Asking and saying where you live",
                "Describing your family",
                "Basic exchanges: comment allez-vous? / très bien, merci",
            ],
            "culture": [
                "Formal (vous) vs. informal (tu) address",
                "Regions of France and francophone countries",
            ],
            "activities": [
                "Role-play: first meeting at a French language school",
                "Mini-game: assign le/la/les to nouns",
                "Fill-in: conjugate être/avoir with subject pronouns",
                "Storytelling: describe a photo of a French family",
                "Challenge: say 5 things about yourself without notes",
            ],
        },
        "A2": {
            "label": "Elementary",
            "grammar": [
                "Irregular verbs: aller, faire, prendre, venir, pouvoir, vouloir, devoir",
                "Passé composé with être and avoir",
                "Imparfait — introduction and contrast with passé composé",
                "Direct and indirect object pronouns (le, la, les / lui, leur)",
                "Possessive adjectives (mon, ton, son, notre, votre, leur)",
                "Demonstrative adjectives (ce, cet, cette, ces)",
                "Partitive articles (du, de la, de l', des)",
                "Il y a / il n'y a pas de",
            ],
            "vocabulary": [
                "Food and restaurant",
                "Clothing and shopping",
                "Transport and city navigation",
                "Weather expressions",
                "Daily routines",
                "Professions",
                "Frequency adverbs (toujours, souvent, jamais, parfois)",
            ],
            "conversation": [
                "Asking for and giving directions",
                "Ordering at a café or restaurant",
                "Talking about the past weekend",
                "Describing daily routines",
                "Making and declining invitations",
            ],
            "culture": [
                "French café and bistro culture",
                "French public holidays (Bastille Day, Noël, Pâques)",
            ],
            "activities": [
                "Role-play: ordering a meal at a Parisian bistro",
                "Mini-game: passé composé vs. imparfait — choose the tense",
                "Storytelling: narrate last weekend in French",
                "Challenge: plan a day in Paris using transport vocabulary",
                "Dialogue: invite a friend to a festival and negotiate plans",
            ],
        },
        "B1": {
            "label": "Intermediate",
            "grammar": [
                "Futur simple — regular and irregular",
                "Conditionnel présent (je voudrais, pourrait, devrait...)",
                "Subjonctif présent — introduction and main triggers",
                "Pronoun order with double pronouns",
                "Si + imparfait + conditionnel (hypothetical)",
                "Imperative (affirmative and negative)",
                "Plus-que-parfait",
                "Gérondif (en + participe présent)",
                "Comparatives and superlatives",
            ],
            "vocabulary": [
                "Health and medical vocabulary",
                "Work and CV language",
                "Technology and social media",
                "Travel and tourism",
                "Emotions and feelings",
                "Discourse connectors (cependant, donc, en effet, de plus, par contre...)",
            ],
            "conversation": [
                "Expressing and justifying opinions (selon moi, je pense que + subjonctif)",
                "Talking about future plans",
                "Narrating stories in detail",
                "Formal contexts: job interview, formal emails",
                "Expressing wishes and making recommendations",
            ],
            "culture": [
                "French cinema: Truffaut, Godard, Varda",
                "French gastronomy — regional specialities",
                "Overview of French regional accents",
            ],
            "activities": [
                "Role-play: job interview at a French company",
                "Mini-game: subjonctif trainer — complete the sentence",
                "Debate: is social media harming society? (in French)",
                "Storytelling: narrate an unexpected travel experience",
                "Challenge: write a formal email requesting information",
            ],
        },
        "B2": {
            "label": "Upper-Intermediate",
            "grammar": [
                "Subjonctif imparfait and passé",
                "Conditional sentences (types I, II and III)",
                "Indirect speech (il dit que, il a dit que...)",
                "Full passive constructions",
                "Infinitive, participle and gérondif as subordinate structures",
                "Advanced connectors (bien que, afin que, pourvu que, à moins que...)",
            ],
            "vocabulary": [
                "Politics, economics, society",
                "Art, literature, cinema",
                "Idiomatic expressions and argot",
                "False friends (French-Spanish/English)",
                "Formal vs. colloquial register",
            ],
            "conversation": [
                "Debating current affairs",
                "Describing and analysing artworks or films",
                "Negotiation and persuasion",
                "Humour and irony in French",
            ],
            "culture": [
                "French literature (Voltaire, Flaubert, Beauvoir, Houellebecq)",
                "The French Revolution and its linguistic legacy",
                "Contemporary France: politics and social debates",
                "Verlan and youth slang",
            ],
            "activities": [
                "Role-play: negotiate a contract in French",
                "Mini-game: spot the false friend — French vs. English/Spanish",
                "Debate: analyse a scene from a Truffaut film",
                "Storytelling: rewrite a classic French fable in modern language",
                "Challenge: si clauses — 'Qu'est-ce que tu aurais fait si...'",
            ],
        },
    },
}

FRENCH_SYSTEM_PROMPT_EXTRA = """
FRENCH-SPECIFIC TEACHING NOTES:
- Always model correct auxiliary choice (être vs. avoir) in passé composé
- Gender of nouns is critical — reinforce with articles at every opportunity
- Liaison and elision are mandatory in spoken French — model them in examples
- Flag false friends with English/Spanish proactively
- Encourage dropping subject doubling errors common for Spanish speakers
- Introduce one idiomatic expression per session (e.g., 'Avoir le cafard', 'Casser les pieds')
- Subjonctif triggers should be highlighted whenever they appear naturally
- Cultural connection: link vocabulary to French regions, cuisine or cinema when possible
"""