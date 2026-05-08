import requests
import google.generativeai as genai
import schedule
import time
from urllib.parse import quote

# ============ CONFIG ============
GOOGLE_API_KEY = "AIzaSyA408W4MCaMVxz8y6XkyWb_Nv1RZ_j-JRE"
IG_USER_ID = "17841433559518798"
ACCESS_TOKEN = "EAAXUVOu2jfsBRcv2tOM7yxq5IOFhFZByjSaDhtREh4aIi1F7UZCxZCsrouYdZByFfTmpzXKLrZAi1UjlSDKlPCdZCtg9igv0B6gjZCDGZAjlrVO9536uPy0AKMgHbe2ICLGH7uarwVYZCG9jQPLWXlyjo7oweMhuviZBzOcASuq1nvKREppkkWUMjEzWab9Kt0ksEoya6gm1tFCPirxabuKjkdPrIXrTJZAuwx9l0kf1srzDnZAisB36KbJe44LsfjDnIwvMTre4o1pHKV9klZCs43L5E"

# Topics — har roz alag post
TOPICS = [
    "silence is the greatest weapon of the wise",
    "observe before you act",
    "patience builds empires",
    "the quietest person in the room is the most dangerous",
    "strike only when the time is right",
    "solitude is where strategies are born",
    "let your success make the noise",
]

# ============ SETUP ============
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-flash")

# ============ FUNCTIONS ============

def generate_caption(topic):
    print(f"✍️ Caption generate ho rahi hai: {topic}")
    response = model.generate_content(f"""
    You manage 'SilentAj' Instagram — tagline: 'Observe Silently. Strike Logically.'
    Dark, mysterious, motivational brand.
    Write an Instagram caption about: {topic}
    - 100-150 words, powerful and mysterious tone
    - End with 5-7 relevant hashtags
    """)
    return response.text

def generate_image_url(topic):
    print(f"🎨 Image generate ho rahi hai...")
    prompt = f"dark mysterious hooded figure, golden light, cinematic, motivational, {topic}, ultra realistic, 4k"
    encoded = quote(prompt)
    image_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1080&height=1080&nologo=true"
    return image_url

def post_to_instagram(image_url, caption):
    print(f"📸 Instagram pe post ho rahi hai...")
    create = requests.post(
        f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media",
        data={
            "image_url": image_url,
            "caption": caption,
            "access_token": ACCESS_TOKEN
        }
    ).json()
    
    container_id = create.get("id")
    if not container_id:
        print("❌ Error:", create)
        return False
    
    result = requests.post(
        f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish",
        data={
            "creation_id": container_id,
            "access_token": ACCESS_TOKEN
        }
    ).json()
    
    post_id = result.get("id")
    if post_id:
        print(f"✅ Posted! ID: {post_id}")
        return True
    else:
        print("❌ Publish Error:", result)
        return False

# ============ MAIN AGENT ============
import datetime

def run_agent():
    print(f"\n{'='*50}")
    print(f"🤖 SilentAj Agent — {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*50}")
    
    # Aaj ka topic select karo
    day = datetime.datetime.now().weekday()
    topic = TOPICS[day % len(TOPICS)]
    print(f"📌 Topic: {topic}")
    
    # Caption banao
    caption = generate_caption(topic)
    print(f"\n📝 Caption:\n{caption}\n")
    
    # Image URL banao
    image_url = generate_image_url(topic)
    print(f"🖼️ Image URL: {image_url[:60]}...")
    
    # Post karo
    post_to_instagram(image_url, caption)

# ============ RUN ============
if __name__ == "__main__":
    print("🚀 SilentAj Agent Starting...")
    
    # Abhi ek baar test karo
    # run_agent()
    
    # Phir roz subah 9 baje auto post
    schedule.every().day.at("09:00").do(run_agent)
    print("⏰ Scheduler active — roz 9 baje post hogi!")
    while True:
        schedule.run_pending()
        time.sleep(60)