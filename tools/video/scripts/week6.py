"""Week 6 explainer in Hinglish: generative AI project lifecycle."""
from vidkit import title, cards, split, traps, end, video

S = [
  title(6, "Generative AI<br>project lifecycle", ["Scope → deploy", "Instruction fine-tuning", "PEFT · LoRA", "RLHF", "RAG · LangChain"]),

  {"html": split("The lifecycle", 6, 0, [
     (1, "<b>Scope</b> narrow rakho · <b>Select</b>: existing model, rarely pre-train"),
     (2, "<b>Adapt</b>: pehle prompting, phir fine-tuning, phir RLHF"),
     (3, "<b>Evaluate</b>: ROUGE, BLEU, MMLU, human review"),
     (4, "<b>Deploy</b>: quantise, distil, prune · <b>Integrate</b>: RAG, agents")], max_h=400)},

  {"html": cards("Fine-tuning", [
     (1, "Instruction FT", "prompt–completion pairs", "full FT → catastrophic forgetting"),
     (2, "PEFT", "base frozen, few params train", "small checkpoints"),
     (3, "LoRA", "ΔW = BA, params r(d + k)", "QLoRA: 4-bit base"),
     (4, "Prompt tuning", "soft prompt embeddings", "model unchanged")], cols=2)},

  {"html": cards("RLHF &amp; evaluation", [
     (1, "RLHF", "SFT → reward model → PPO", "humans rank outputs"),
     (2, "KL penalty", "reference model ke paas raho", "reward hacking rokta hai"),
     (3, "DPO · RLAIF", "DPO: no reward model", "Constitutional AI: AI feedback"),
     (4, "Metrics", "ROUGE: summary · BLEU: translation", "MMLU: 57 subjects")], cols=2)},

  {"html": cards("Building the app", [
     (1, "RAG", "chunks → embeddings → vector DB → retrieve → prompt", "fresh knowledge, no retraining"),
     (2, "LangChain", "chain = fixed steps<br>agent = LLM chooses tools", "memory, retrievers, templates"),
     (3, "Optimise", "quantise: low precision<br>distil: student ← teacher", "prune: weights hatao")], cols=3)},

  {"html": traps([
     (1, "RLHF order", "SFT → reward → PPO"),
     (1, "KL penalty", "stops reward hacking"),
     (2, "LoRA params", "r(d + k), base frozen"),
     (2, "Full FT risk", "catastrophic forgetting"),
     (3, "Weekly-updated docs", "RAG, not fine-tuning"),
     (3, "Chinchilla", "~20 tokens per parameter")])},

  end(6, "Week 7 · Responsible AI"),
]

STEPS = [
  [[0, "Week six: generative AI project lifecycle। Exam के लिए यह सबसे heavy week है।",
       "Week six: generative AI project lifecycle. Exam ke liye yeh sabse heavy week hai."]],
  [[0, "Lifecycle के stages।",
       "Lifecycle ke stages."],
   [1, "पहले scope narrow रखिए। फिर model select कीजिए। Existing foundation model लेना आम है, नया pre-train करना rare।",
       "Pehle scope narrow rakhiye. Phir model select kijiye. Existing foundation model lena aam hai, naya pre-train karna rare."],
   [2, "Adapt करने का order: पहले prompting, काफ़ी नहीं तो fine-tuning, फिर alignment के लिए RLHF।",
       "Adapt karne ka order: pehle prompting, kaafi nahi toh fine-tuning, phir alignment ke liye RLHF."],
   [3, "Evaluate कीजिए ROUGE, BLEU, MMLU जैसे benchmarks और human review से।",
       "Evaluate kijiye ROUGE, BLEU, MMLU jaise benchmarks aur human review se."],
   [4, "फिर deploy: quantisation, distillation, pruning। और app में RAG और agents से integrate।",
       "Phir deploy: quantisation, distillation, pruning. Aur app mein RAG aur agents se integrate."]],
  [[0, "Fine-tuning।",
       "Fine-tuning."],
   [1, "Instruction fine-tuning prompt और completion pairs पर होता है। Full fine-tuning से catastrophic forgetting हो सकता है, यानी बाकी tasks भूल जाना।",
       "Instruction fine-tuning prompt aur completion pairs par hota hai. Full fine-tuning se catastrophic forgetting ho sakta hai, yaani baaki tasks bhool jaana."],
   [2, "PEFT में base model frozen रहता है, सिर्फ थोड़े parameters train होते हैं। Checkpoints छोटे।",
       "PEFT mein base model frozen rehta hai, sirf thode parameters train hote hain. Checkpoints chhote."],
   [3, "LoRA दो low rank matrices जोड़ता है। Trainable parameters r गुणा d plus k। QLoRA में base model four bit का होता है।",
       "LoRA do low rank matrices jodta hai. Trainable parameters r guna d plus k. QLoRA mein base model four bit ka hota hai."],
   [4, "Prompt tuning soft prompt embeddings train करता है, model वही रहता है।",
       "Prompt tuning soft prompt embeddings train karta hai, model wahi rehta hai."]],
  [[0, "RLHF और evaluation।",
       "RLHF aur evaluation."],
   [1, "RLHF का order: supervised fine-tuning, फिर human rankings से reward model, फिर PPO से optimisation।",
       "RLHF ka order: supervised fine-tuning, phir human rankings se reward model, phir PPO se optimisation."],
   [2, "KL penalty model को reference model के पास रखता है, ताकि reward hacking न हो।",
       "KL penalty model ko reference model ke paas rakhta hai, taaki reward hacking na ho."],
   [3, "DPO में अलग reward model नहीं चाहिए। Constitutional AI written principles से AI feedback देता है।",
       "DPO mein alag reward model nahi chahiye. Constitutional AI written principles se AI feedback deta hai."],
   [4, "ROUGE summary के लिए, BLEU translation के लिए, और MMLU 57 subjects का knowledge test है।",
       "ROUGE summary ke liye, BLEU translation ke liye, aur MMLU 57 subjects ka knowledge test hai."]],
  [[0, "अब app बनाना।",
       "Ab app banana."],
   [1, "RAG: documents को chunks में तोड़ो, embeddings बनाओ, vector database में रखो, query पर relevant chunks retrieve करके prompt में डालो। बिना retraining fresh knowledge।",
       "RAG: documents ko chunks mein todo, embeddings banao, vector database mein rakho, query par relevant chunks retrieve karke prompt mein daalo. Bina retraining fresh knowledge."],
   [2, "LangChain में chain fixed steps चलाती है, agent ख़ुद तय करता है कौन सा tool call करना है।",
       "LangChain mein chain fixed steps chalaati hai, agent khud tay karta hai kaun sa tool call karna hai."],
   [3, "Optimise: quantisation precision कम करता है, distillation में छोटा student बड़े teacher से सीखता है, pruning weights हटाता है।",
       "Optimise: quantisation precision kam karta hai, distillation mein chhota student bade teacher se seekhta hai, pruning weights hataata hai."]],
  [[1, "Recap। RLHF का order SFT, reward, PPO, और KL penalty reward hacking रोकता है।",
       "Recap. RLHF ka order SFT, reward, PPO, aur KL penalty reward hacking rokta hai."],
   [2, "LoRA parameters r गुणा d plus k, और full fine-tuning का risk catastrophic forgetting।",
       "LoRA parameters r guna d plus k, aur full fine-tuning ka risk catastrophic forgetting."],
   [3, "हर हफ़्ते बदलते documents के लिए RAG। और Chinchilla rule: लगभग 20 tokens per parameter।",
       "Har hafte badalte documents ke liye RAG. Aur Chinchilla rule: lagbhag 20 tokens per parameter."]],
  [[0, "Week six ख़त्म। Next video, week seven: responsible AI।",
       "Week six khatam. Next video, week seven: responsible AI."]],
]

VIDEO = video(6, "Week 6 · Generative AI project lifecycle", S, STEPS)
