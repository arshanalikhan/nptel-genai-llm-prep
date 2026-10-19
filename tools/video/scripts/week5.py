"""Week 5 explainer in Hinglish: introduction to large language models."""
from vidkit import title, cards, split, traps, end, video

S = [
  title(5, "Introduction to<br>Large Language Models", ["Self-supervised", "Causal vs masked LM", "In-context learning", "Prompting", "Temperature · top-k · top-p"]),

  {"html": split("How an LLM generates", 5, 0, [
     (1, "<b>Self-supervised</b> pre-training: label text khud deta hai"),
     (2, "<b>Causal LM</b> (GPT): next token · <b>Masked LM</b> (BERT): hidden token"),
     (3, "Loop: score every token → pick one → append → repeat"),
     (4, "<b>Context window</b> = prompt + output ki token limit")])},

  {"html": cards("Prompting", [
     (1, "In-context learning", "zero-shot · one-shot · few-shot", "weights change nahi hote"),
     (2, "Chain of thought", "“Let's think step by step”", "reasoning better"),
     (3, "Good prompts", "role, clear instruction, delimiters, format, examples", "self-consistency: majority vote"),
     (4, "Limits", "hallucination, knowledge cutoff, context limit", "arithmetic weak")], cols=2)},

  {"html": cards("Decoding settings", [
     (1, "Greedy", "highest token every step", "repetitive, deterministic"),
     (2, "Temperature", "p ∝ e^(z/T)", "T↓ focused · T↑ creative"),
     (3, "Top-k", "fixed k tokens", "k = 2 → top 2"),
     (4, "Top-p", "smallest set with sum ≥ p", "size changes with confidence")], cols=2)},

  {"html": traps([
     (1, "Few-shot prompting", "no weight change"),
     (1, "GPT objective", "next token"),
     (2, "T → 0", "greedy"),
     (2, "Top-p", "variable number of tokens"),
     (3, "Perplexity", "lower is better"),
     (3, "GPT-3 size", "175B")])},

  end(5, "Week 6 · Generative AI project lifecycle"),
]

STEPS = [
  [[0, "Week five: large language models, यानी LLMs।",
       "Week five: large language models, yaani LLMs."]],
  [[0, "LLM असल में एक बहुत बड़ा next token predictor है।",
       "LLM asal mein ek bahut bada next token predictor hai."],
   [1, "Pre-training self-supervised होती है: label text ख़ुद देता है, किसी human labelling की ज़रूरत नहीं।",
       "Pre-training self-supervised hoti hai: label text khud deta hai, kisi human labelling ki zaroorat nahi."],
   [2, "GPT causal language modelling करता है, यानी next token। BERT masked language modelling करता है, यानी छिपे हुए token को दोनों तरफ़ से predict करना।",
       "GPT causal language modelling karta hai, yaani next token. BERT masked language modelling karta hai, yaani chhipe hue token ko dono taraf se predict karna."],
   [3, "Generation एक loop है: हर token का score, एक token चुनो, जोड़ो, और repeat।",
       "Generation ek loop hai: har token ka score, ek token chuno, jodo, aur repeat."],
   [4, "Context window prompt और output मिलाकर tokens की limit है।",
       "Context window prompt aur output milaakar tokens ki limit hai."]],
  [[0, "अब prompting।",
       "Ab prompting."],
   [1, "In-context learning: zero-shot, one-shot, few-shot। Prompt में examples देते हैं, model के weights नहीं बदलते।",
       "In-context learning: zero-shot, one-shot, few-shot. Prompt mein examples dete hain, model ke weights nahi badalte."],
   [2, "Chain of thought: let's think step by step लिखने से reasoning बेहतर होती है।",
       "Chain of thought: let's think step by step likhne se reasoning behtar hoti hai."],
   [3, "अच्छे prompt में role, साफ़ instruction, delimiters, output format और examples। Self-consistency कई answers का majority लेता है।",
       "Achhe prompt mein role, saaf instruction, delimiters, output format aur examples. Self-consistency kai answers ka majority leta hai."],
   [4, "Limits: hallucination, knowledge cutoff, context limit, और arithmetic में कमज़ोरी।",
       "Limits: hallucination, knowledge cutoff, context limit, aur arithmetic mein kamzori."]],
  [[0, "Decoding settings, जो numericals में भी आती हैं।",
       "Decoding settings, jo numericals mein bhi aati hain."],
   [1, "Greedy हर step पर सबसे ऊँचा token लेता है: deterministic, पर अक्सर repetitive।",
       "Greedy har step par sabse ooncha token leta hai: deterministic, par aksar repetitive."],
   [2, "Temperature logits को T से divide करता है। कम T focused, ज़्यादा T creative।",
       "Temperature logits ko T se divide karta hai. Kam T focused, zyada T creative."],
   [3, "Top-k fixed k tokens रखता है।",
       "Top-k fixed k tokens rakhta hai."],
   [4, "Top-p सबसे छोटा set रखता है जिसका probability sum p या ज़्यादा हो, इसलिए size बदलता रहता है।",
       "Top-p sabse chhota set rakhta hai jiska probability sum p ya zyada ho, isliye size badalta rehta hai."]],
  [[1, "Recap। Few-shot में weights नहीं बदलते, और GPT का objective next token।",
       "Recap. Few-shot mein weights nahi badalte, aur GPT ka objective next token."],
   [2, "Temperature zero की तरफ़ मतलब greedy, और top-p variable tokens रखता है।",
       "Temperature zero ki taraf matlab greedy, aur top-p variable tokens rakhta hai."],
   [3, "Perplexity जितनी कम उतना अच्छा, और GPT-3 में 175 billion parameters।",
       "Perplexity jitni kam utna achha, aur GPT-3 mein 175 billion parameters."]],
  [[0, "Week five ख़त्म। Next video, week six: generative AI project lifecycle।",
       "Week five khatam. Next video, week six: generative AI project lifecycle."]],
]

VIDEO = video(5, "Week 5 · Large Language Models", S, STEPS)
