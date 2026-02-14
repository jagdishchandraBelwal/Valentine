from playwright.sync_api import sync_playwright
import time

# ==========================
# READY-TO-USE 92 SCENE PROMPTS
# ==========================
PROMPTS = [
    "Scene 1: Cinematic 2D animation, ancient Indian village at dusk, moonlight, fog, horror mood, बहुत पुराने समय की बात है, जब गाँवों में न कोई बिजली की रोशनी थी",
    "Scene 2: Moonlit night, flickering oil lamps, jungle whispers, eerie atmosphere, सिर्फ़ चाँदनी रातें, जलते दीये और जंगल की सिसकियाँ",
    "Scene 3: Village overview, Ramlaal walking through mud houses, traditional dhoti-kurta, suspense mood, उत्तर भारत के एक छोटे से गाँव कालाकाँकर में रहता था रामलाल",
    "Scene 4: Montage of fields, oxen plowing, treasure chest with gold, proud wealthy mood, वह गाँव का सबसे अमीर जमींदार था—बड़े-बड़े खेत, कई बैल, सोने-चाँदी से भरा तिजोरी",
    "Scene 5: Ramlaal hugging Sarita, soft light, affectionate yet mysterious, लेकिन उसकी सबसे बड़ी दौलत थी उसकी इकलौती बेटी, सरिता",
    "Scene 6: Close-up of Sarita's face, eyes hinting secrets, subtle fear mood, सरिता सुंदर थी, शांत थी, और गाँव वाले कहते थे कि उसकी आँखों में कोई पुराना राज़ छिपा है",
    "Scene 7: Dark new moon night, cracked old well, dread, एक अमावस्या की रात को रामलाल का पुराना कुआँ सूख गया",
    "Scene 8: Villagers worried at dry well, panic mood, पानी के लिए गाँव वाले परेशान थे",
    "Scene 9: Ramlaal pointing to distant jungle, abandoned well, determination mood, रामलाल ने फैसला किया कि वह पुराने जंगल के उस पार वाले कुएँ से पानी लाएगा, जो सदियों से बंद पड़ा था",
    "Scene 10: Villagers shaking heads, fearful mood, लोग डरते थे उस जगह से",
    "Scene 11: Flashback silhouette of woman in white saree pushed into well, horror mood, कहते थे वहाँ भूत रहता है—एक औरत का, जिसे सौ साल पहले जिंदा कुएँ में फेंक दिया गया था क्योंकि उसने जमींदार के बेटे से प्यार किया था",
    "Scene 12: Ramlaal laughing dismissively, uneasy shadow behind, रामलाल ने हँसकर बात टाल दी",
    "Scene 13: Ramlaal grabbing Sarita's hand, hesitant nod, hidden fear, उसने सरिता को साथ लिया—क्योंकि वह अकेले नहीं जाना चाहता था",
    "Scene 14: Torches igniting, entering dense jungle, tension building, दोनों ने मशालें जलाईं और जंगल में घुस गए",
    "Scene 15: Narrow path, branches animate like grasping hands, claustrophobic mood, रास्ता तंग था, पेड़ों की डालियाँ जैसे हाथ फैलाकर रोक रही हों",
    "Scene 16: Midnight reveal of ruined well through fog, arrival unease, आधी रात को वे उस पुराने कुएँ पर पहुँचे",
    "Scene 17: Broken well stones, cold mist rising, chilling mystery, कुआँ टूटा-फूटा था, लेकिन अंदर से पानी की ठंडी हवा आ रही थी",
    "Scene 18: Ramlaal tying rope, lowering bucket, focused tension, रामलाल ने रस्सी बाँधी और बाल्टी नीचे उतारी",
    "Scene 19: Bucket rising with water dripping, subtle bubble effect, anticipation, बाल्टी पानी से भरी हुई ऊपर आई",
    "Scene 20: Sarita lifting bucket, eyes widen in horror, shock mood, सरिता ने बाल्टी उठाई तो अचानक उसकी आँखें चौड़ी हो गईं",
    "Scene 21: Close-up of bucket with silver bangle, revelation dread, बाल्टी में पानी के साथ एक पुरानी चाँदी की चूड़ी थी—वही चूड़ी जो उसकी माँ की थी",
    "Scene 22: Sarita trembling, holding bangle, fearful whisper, “बापू... ये माँ की चूड़ी है,” सरिता की आवाज़ काँप रही थी",
    "Scene 23: Ramlaal pale face, close-up terror, रामलाल का चेहरा सफ़ेद पड़ गया",
    "Scene 24: Sudden grab of bucket, water splashing, panic motion, उसने झटके से बाल्टी छीन ली",
    "Scene 25: Ramlaal finger to lips, urgent secrecy, “चुप! कोई नहीं जानता ये बात।”",
    "Scene 26: Sarita questioning, fog thickens, confusion mood, सरिता ने पूछा, “माँ कहाँ गई थीं? ... लेकिन ये चूड़ी?”",
    "Scene 27: Ramlaal guilty silence, bowed head, रामलाल चुप रहा",
    "Scene 28: Soft eerie laughter from jungle, supernatural chill, तभी जंगल से एक औरत की हल्की-हलकी हँसी आई",
    "Scene 29: Ghost shadow in torchlight approaching well, slow advance, मशाल की रोशनी में एक सफ़ेद साड़ी वाली छाया दिखी—धीरे-धीरे कुएँ की तरफ़ बढ़ती हुई",
    "Scene 30: Ramlaal pushing Sarita back, protective fear, रामलाल ने सरिता को पीछे धकेला",
    "Scene 31: Ramlaal yelling, desperate command, “भाग यहाँ से!”",
    "Scene 32: Sarita frozen, defiant curiosity, लेकिन सरिता नहीं हिली",
    "Scene 33: Ghost shadow gliding closer, suspense intensifying, वह छाया करीब आई",
    "Scene 34: Ghost face blurry, eyes like Sarita's, uncanny recognition, चेहरा धुंधला था, लेकिन आँखें... आँखें सरिता जैसी ही थीं",
    "Scene 35: Sarita whispering, shocked, “तुम... माँ?” सरिता ने फुसफुसाया",
    "Scene 36: Ghost hand reaching, inviting menace, छाया ने हाथ बढ़ाया",
    "Scene 37: Ghost fingers icy visual effect, cold dread, उसकी उँगलियाँ ठंडी थीं",
    "Scene 38: Ghost morphing to Sarita's face, twisted revelation, “मैं तुम्हारी माँ नहीं हूँ... मैं तुम हूँ।”",
    "Scene 39: Ramlaal screaming in denial, dynamic rage, रामलाल चीखा, “नहीं! ये झूठ है!”",
    "Scene 40: Ghost laughing mockingly, medium shot, छाया हँसी",
    "Scene 41: Flashback overlay push into well, accusatory, “बीस साल पहले तूने मुझे कुएँ में धक्का दिया था, रामलाल।”",
    "Scene 42: Ghost pointing, bitter truth, “क्योंकि मैंने तुझे बताया था कि सरिता तेरी बेटी नहीं है।”",
    "Scene 43: Ghost ethereal glow, possessive reveal, “वो मेरी बेटी है... और तेरी पत्नी की नहीं।”",
    "Scene 44: Ramlaal stumbling backward, fearful, रामलाल पीछे हटा",
    "Scene 45: Extreme close-up on Ramlaal eyes, terror, उसकी आँखों में डर था",
    "Scene 46: Ramlaal stammering guilt, lips trembling, “मैंने... मैंने सिर्फ़ गुस्से में...”",
    "Scene 47: Sarita stunned, frozen expression, सरिता स्तब्ध थी",
    "Scene 48: Sarita questioning heartbreak, “तो मैं... आपकी बेटी नहीं हूँ?”",
    "Scene 49: Ghost maternal claim, soft smile, “तू मेरी बेटी है।”",
    "Scene 50: Ghost sacrificial flashback, “मैंने तुझे बचाने के लिए खुद को कुएँ में डाल दिया था।”",
    "Scene 51: Ghost finality, mist swirls, “लेकिन अब... अब तू जानती है सच्चाई।”",
    "Scene 52: Wind gusts, climactic tension, अचानक हवा तेज़ चली",
    "Scene 53: Torch extinguished, sudden darkness, मशाल बुझ गई",
    "Scene 54: Ramlaal silhouette breathing, isolated fear, अँधेरे में सिर्फ़ रामलाल की साँसें सुनाई दे रही थीं",
    "Scene 55: Sarita whisper in dark, faint glow, “बापू... सच बताओ।”",
    "Scene 56: Ramlaal breaking down, tears, रामलाल रो पड़ा",
    "Scene 57: Ramlaal confession, sobbing, “हाँ... मैंने किया था।”",
    "Scene 58: Ramlaal regret, gestures shadows mock, मैं डर गया था कि अगर लोग जान जाएँगे कि तू मेरी नहीं है...",
    "Scene 59: Water churning from well, ominous rise, तभी कुएँ से पानी की तेज़ आवाज़ आई",
    "Scene 60: Hands gripping well from below, impending doom, जैसे कोई नीचे से ऊपर चढ़ रहा हो",
    "Scene 61: Ramlaal clutching Sarita, desperate grasp, रामलाल ने सरिता को पकड़ लिया",
    "Scene 62: Urgent run, Ramlaal yelling, “चल, भागते हैं!”",
    "Scene 63: Sarita frees hand, stands firm, लेकिन सरिता ने हाथ छुड़ा लिया",
    "Scene 64: Sarita gazing into well, fearless, उसने कुएँ की तरफ़ देखा",
    "Scene 65: Bold stance, “मैं नहीं डरती।”",
    "Scene 66: Ghost reappears from darkness, slow fade, अँधेरे में छाया फिर प्रकट हुई",
    "Scene 67: Ghost aged Sarita face, weary similarity, इस बार उसका चेहरा साफ़ था—सरिता का ही चेहरा, लेकिन बूढ़ा, थका हुआ",
    "Scene 68: Ghost giving ultimatum, medium shot, “अब तू चुन,” छाया ने कहा",
    "Scene 69: Arms open ethereal chains visualize, “या तो मैं तुझे ले जाऊँगी... या तू मुझे आज़ाद कर देगी।”",
    "Scene 70: Ramlaal lunging, possessive scream, “नहीं! सरिता मेरी बेटी है!”",
    "Scene 71: Sarita conflicted eyes, torn, सरिता ने रामलाल की तरफ़ देखा",
    "Scene 72: Close-up on Sarita eyes, tears, उसकी आँखों में आँसू थे",
    "Scene 73: Sarita speaks softly, betrayed gratitude, “आपने मुझे पाला, प्यार किया... लेकिन सच छिपाया।”",
    "Scene 74: Sarita gaze shifts to ghost, acceptance, फिर उसने छाया की तरफ़ देखा",
    "Scene 75: Defining pose, “मैं तुम्हें आज़ाद करती हूँ।”",
    "Scene 76: Sarita pushes Ramlaal, cold resolve, उसने रामलाल को धक्का दिया",
    "Scene 77: Ramlaal falling into well, fatal, रामलाल कुएँ के किनारे पर लड़खड़ाया... और गिर गया",
    "Scene 78: Splash in water, horror impact, नीचे पानी में धड़ाम की आवाज़ आई",
    "Scene 79: Sunrise, resolution dawn, सुबह हुई",
    "Scene 80: Villagers gather, concerned, गाँव वाले कुएँ पर इकट्ठे हुए",
    "Scene 81: Floating corpse, grim discovery, रामलाल का शव पानी में तैर रहा था",
    "Scene 82: Sarita isolated, stoic, सरिता अकेली खड़ी थी, चुपचाप",
    "Scene 83: Villagers gesturing questions, inquiry, गाँव वालों ने पूछा, “क्या हुआ?”",
    "Scene 84: Sarita calm lie, “वो कुएँ में गिर गए। पानी निकालते वक्त।”",
    "Scene 85: Villagers accept, no suspicion, कोई शक नहीं किया",
    "Scene 86: Sarita wealth montage, shadows linger, रामलाल की मौत हो गई, और सरिता गाँव की सबसे अमीर औरत बन गई",
    "Scene 87: Night walk to well, secretive, लेकिन रात को, जब सब सो जाते, सरिता कुएँ पर जाती",
    "Scene 88: Sitting whisper, peaceful, वहाँ बैठकर फुसफुसाती, “माँ... अब हम दोनों आज़ाद हैं।”",
    "Scene 89: Haunting laughter from well, mist rises, और कुएँ से हल्की हँसी आती—जैसे कोई जवाब दे रहा हो",
    "Scene 90: Two women silhouettes near well, legendary fear, कभी-कभी गाँव वाले कहते हैं कि अमावस्या की रात को कुएँ के पास दो औरतें दिखती हैं... एक जवान, एक बूढ़ी",
    "Scene 91: Laughter sync, eerie joy, दोनों हँसती हैं",
    "Scene 92: Final zoom into dark well, eternal damnation, और रामलाल? वो अब भी कुएँ में है... हमेशा के लिए"
]

# ==========================
# PLAYWRIGHT AUTOMATION
# ==========================
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, args=["--start-maximized"])
    context = browser.new_context()
    page = context.new_page()

    # Go to Meta AI Media
    page.goto("https://www.meta.ai/media")
    input("✅ Make sure you are logged in in the browser. Press ENTER to continue...")

    for prompt in PROMPTS:
        # Fill prompt
        input_box = page.locator("textarea[data-testid='composer-input']")
        input_box.wait_for(state="visible", timeout=60000)  # wait until visible
        input_box.click()  # focus
        input_box.fill(prompt)

        page.keyboard.press("Enter")
        print(f"Generating video for: {prompt[:50]}...")

        # Wait for generation (adjust if needed)
        time.sleep(30)

        # Try to click download
        try:
            page.locator("button:has-text('Download')").click()
            print("✅ Download attempted")
            time.sleep(5)
        except:
            print("⚠️ Download button not found, download manually")

    browser.close()
