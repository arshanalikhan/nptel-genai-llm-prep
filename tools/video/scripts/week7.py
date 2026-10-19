"""Week 7 explainer in Hinglish: responsible AI."""
from vidkit import title, cards, split, traps, end, video

S = [
  title(7, "Responsible AI", ["Principles", "Bias", "Hallucination", "Privacy · IP", "Guardrails · regulation"]),

  {"html": split("Risks and controls", 7, 0, [
     (1, "<b>Bias</b> → diverse data, audits, fairness metrics"),
     (2, "<b>Hallucination</b> → RAG, citations, human review"),
     (3, "<b>Toxicity, jailbreaks</b> → RLHF, guardrails, red-teaming"),
     (4, "<b>Privacy, IP, deepfakes</b> → PII masking, licensed data, watermarking")], max_h=400)},

  {"html": cards("Principles &amp; governance", [
     (1, "Six principles", "fairness, reliability &amp; safety, privacy &amp; security, inclusiveness, transparency, accountability", "Microsoft"),
     (2, "Transparency", "model cards, datasheets", "AI content disclose karo"),
     (3, "Regulation", "EU AI Act: risk-based tiers", "India: DPDP Act 2023"),
     (4, "Humans", "human-in-the-loop, accountability", "log hi responsible")], cols=2)},

  {"html": traps([
     (1, "Hallucination with RAG", "reduced, not eliminated"),
     (1, "Red-teaming", "deliberate attacks"),
     (2, "Prompt injection", "hidden instructions in input"),
     (2, "Biased hiring model", "historical data bias"),
     (3, "EU AI Act", "risk-based"),
     (3, "Change only religion, output changes", "counterfactual fairness test")])},

  end(7, "Mock exams · 50 questions, 3 hours"),
]

STEPS = [
  [[0, "Week seven: responsible AI। Last week, और exam में scenario questions यहीं से आते हैं।",
       "Week seven: responsible AI. Last week, aur exam mein scenario questions yahin se aate hain."]],
  [[0, "हर risk का एक control है।",
       "Har risk ka ek control hai."],
   [1, "Bias training data से आता है, जैसे पुराना hiring data। Fix: diverse data, audits और fairness metrics।",
       "Bias training data se aata hai, jaise purana hiring data. Fix: diverse data, audits aur fairness metrics."],
   [2, "Hallucination यानी confident पर गलत answer। RAG, citations और human review से कम होता है, पूरी तरह ख़त्म नहीं।",
       "Hallucination yaani confident par galat answer. RAG, citations aur human review se kam hota hai, poori tarah khatam nahi."],
   [3, "Toxic output और jailbreaks के लिए RLHF, guardrails और red-teaming, यानी जानबूझकर model पर attack करके कमियाँ ढूँढना।",
       "Toxic output aur jailbreaks ke liye RLHF, guardrails aur red-teaming, yaani jaanboojhkar model par attack karke kamiyaan dhoondhna."],
   [4, "Privacy के लिए PII masking, IP के लिए licensed data, और deepfakes के लिए watermarking।",
       "Privacy ke liye PII masking, IP ke liye licensed data, aur deepfakes ke liye watermarking."]],
  [[0, "Principles और governance।",
       "Principles aur governance."],
   [1, "Microsoft के छह principles: fairness, reliability and safety, privacy and security, inclusiveness, transparency और accountability।",
       "Microsoft ke chhah principles: fairness, reliability and safety, privacy and security, inclusiveness, transparency aur accountability."],
   [2, "Transparency के लिए model cards और datasheets, और AI generated content disclose करना।",
       "Transparency ke liye model cards aur datasheets, aur AI generated content disclose karna."],
   [3, "EU AI Act risk-based है: unacceptable, high, limited, minimal। India में DPDP Act 2023।",
       "EU AI Act risk-based hai: unacceptable, high, limited, minimal. India mein DPDP Act 2023."],
   [4, "और human in the loop: ज़िम्मेदारी हमेशा लोगों की रहती है, AI की नहीं।",
       "Aur human in the loop: zimmedaari hamesha logon ki rehti hai, AI ki nahi."]],
  [[1, "Recap। RAG hallucination कम करता है, ख़त्म नहीं। Red-teaming जानबूझकर attack है।",
       "Recap. RAG hallucination kam karta hai, khatam nahi. Red-teaming jaanboojhkar attack hai."],
   [2, "Input में छिपे instructions prompt injection हैं, और biased hiring model historical data bias है।",
       "Input mein chhipe instructions prompt injection hain, aur biased hiring model historical data bias hai."],
   [3, "EU AI Act risk-based है, और सिर्फ religion बदलने से output बदले, तो वह counterfactual fairness test है।",
       "EU AI Act risk-based hai, aur sirf religion badalne se output badle, toh woh counterfactual fairness test hai."]],
  [[0, "सारे weeks ख़त्म। अब mock exams दीजिए: पचास questions, तीन घंटे। All the best!",
       "Saare weeks khatam. Ab mock exams dijiye: pachaas questions, teen ghante. All the best!"]],
]

VIDEO = video(7, "Week 7 · Responsible AI", S, STEPS)
