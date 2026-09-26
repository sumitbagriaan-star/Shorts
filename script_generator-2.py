import random
from config import TOPIC_LIST

QUOTES = [
    "The pain you feel today is the strength you feel tomorrow.",
    "Dont stop when you are tired, stop when you are done.",
    "Success is not for the lazy, it is for the relentless.",
    "Every champion was once someone who refused to give up.",
    "Discipline is choosing what you want most over what you want now.",
    "The comeback is always stronger than the setback.",
    "You dont find willpower, you create it through action.",
    "Small daily improvements lead to unstoppable results over time.",
    "Your only limit is the one you set in your own mind.",
    "Hard days build the person your future self will thank.",
    "Winners are not people who never fail, they are people who never quit.",
    "The moment you want to quit is the moment you should push harder.",
    "Growth begins at the end of your comfort zone.",
    "You are one decision away from a completely different life.",
    "Excuses will always be there for you, opportunity will not.",
    "The pain of discipline is nothing compared to the pain of regret.",
    "Doubt kills more dreams than failure ever will.",
    "Consistency turns average people into legends.",
    "Nobody is coming to save you, get up and save yourself.",
    "Your future is created by what you do today, not tomorrow.",
]

HOOK_TEMPLATES = [
    "Listen closely, this will change your mindset",
    "If you needed a sign, this is it",
    "Read this before you give up",
    "This is your motivation for today",
    "Save this for the day you want to quit",
]

CTA_LINES = [
    "Follow for daily motivation!",
    "Tag someone who needs to hear this!",
    "Save this and read it again tomorrow!",
    "Comment STRENGTH if this hit different!",
]


def generate_script(topic=None):
    background_topic = topic or random.choice(TOPIC_LIST)
    chosen_quotes = random.sample(QUOTES, k=3)
    hook = random.choice(HOOK_TEMPLATES)
    cta = random.choice(CTA_LINES)
    script_lines = [hook] + chosen_quotes + [cta]
    full_script = " ".join(script_lines)
    title = (hook + " - daily motivation shorts")[:100]
    description = chosen_quotes[0] + " motivation mindset shorts viral"
    return {
        "title": title,
        "description": description[:500],
        "script_lines": script_lines,
        "full_script": full_script,
        "topic": background_topic,
    }


if __name__ == "__main__":
    data = generate_script()
    print("TITLE:", data["title"])
    print("SCRIPT:", data["full_script"])
