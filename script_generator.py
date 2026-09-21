import random
from config import TOPIC_LIST

FACT_BANK = {
    "space": [
        "A day on Venus is longer than its entire year.",
        "There is a planet made almost entirely of diamonds.",
        "Neutron stars are so dense one teaspoon weighs a billion tons.",
        "Footprints on the Moon will stay there for millions of years.",
    ],
    "human body": [
        "Your stomach lining replaces itself every few days.",
        "Humans glow in the dark, just too faint to see.",
        "Your bones are stronger than steel of the same weight.",
        "Babies have far more bones than adults.",
    ],
    "ocean": [
        "We have mapped less than a quarter of the ocean floor.",
        "The blue whale heart is the size of a small car.",
        "There are more shipwrecks than museums have artifacts.",
        "Some deep sea creatures never see sunlight.",
    ],
    "psychology": [
        "Your brain cannot fully separate imagination from reality.",
        "People remember the start and end more than the middle.",
        "Repeating a lie enough makes people believe it.",
        "Multitasking makes your brain slower, not faster.",
    ],
    "history": [
        "Cleopatra lived closer to the Moon landing than the pyramids.",
        "Oxford University predates the Aztec empire.",
        "The shortest war in history lasted 38 minutes.",
        "Ancient Romans used odd ingredients for hygiene.",
    ],
    "animal": [
        "Octopuses have three hearts and blue blood.",
        "A shrimp heart sits inside its head.",
        "Elephants cannot jump.",
        "Some turtles can breathe in unusual ways.",
    ],
    "money": [
        "Most self made millionaires read constantly.",
        "Rich people track every rupee they spend early on.",
        "Compound interest was called a wonder of the world.",
        "Average millionaires have many income streams.",
    ],
    "science": [
        "Lightning is hotter than the surface of the sun.",
        "Bananas are naturally radioactive but safe to eat.",
        "Hot water can sometimes freeze faster than cold.",
        "Your DNA stretched out would reach incredible lengths.",
    ],
}

HOOK_TEMPLATES = [
    "You wont believe this about {topic}",
    "99 percent of people dont know this {topic} fact",
    "This {topic} fact will blow your mind",
    "Stop scrolling, {topic} fact you need to know",
]

CTA_LINES = [
    "Follow for more facts like this!",
    "Comment WOW if this shocked you!",
    "Save this for later!",
    "Which fact surprised you most? Comment below!",
]


def match_bank(topic):
    topic_lower = topic.lower()
    for key in FACT_BANK:
        if key in topic_lower:
            return FACT_BANK[key]
    return random.choice(list(FACT_BANK.values()))


def generate_script(topic=None):
    topic = topic or random.choice(TOPIC_LIST)
    facts = match_bank(topic)
    chosen_facts = random.sample(facts, k=min(3, len(facts)))
    hook = random.choice(HOOK_TEMPLATES).format(topic=topic)
    cta = random.choice(CTA_LINES)
    script_lines = [hook] + chosen_facts + [cta]
    full_script = " ".join(script_lines)
    title = (hook + " shorts")[:100]
    description = chosen_facts[0] + " shorts facts viral " + topic
    return {
        "title": title,
        "description": description[:500],
        "script_lines": script_lines,
        "full_script": full_script,
        "topic": topic,
    }


if __name__ == "__main__":
    data = generate_script()
    print("TITLE:", data["title"])
    print("SCRIPT:", data["full_script"])
