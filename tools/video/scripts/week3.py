"""Week 3 explainer in Hinglish: attention and transformers."""
from vidkit import title, cards, split, traps, end, video

S = [
  title(3, "Attention mechanism<br>&amp; transformers", ["Q · K · V", "÷ √d_k", "Multi-head", "Positional encoding", "BERT · GPT · T5"]),

  {"html": split("Scaled dot-product attention", 3, 0, [
     (1, "<b>Query</b> poochta hai, <b>Key</b> se match, <b>Value</b> se answer"),
     (2, "softmax(QKᵀ / √d_k) V · weights ka sum = 1"),
     (3, "<b>√d_k</b> se divide: bade dot products softmax ko saturate na karein"),
     (4, "Self-attention: Q, K, V ek hi sequence se · cross: Q decoder se")])},

  {"html": cards("The transformer", [
     (1, "No recurrence", "Attention Is All You Need, 2017", "saare tokens parallel"),
     (2, "Multi-head", "h heads, d_k = d_model / h", "512 / 8 = 64"),
     (3, "Positional encoding", "attention order-blind hai", "position info add karo"),
     (4, "Masking &amp; cost", "decoder future tokens nahi dekhta", "self-attention O(n²)")], cols=2)},

  {"html": cards("Three families", [
     (1, "Encoder-only", "BERT · masked LM · bidirectional", "classification, NER"),
     (2, "Decoder-only", "GPT · next-token", "generation, chat"),
     (3, "Encoder–decoder", "T5, BART", "translation, summarization")], cols=3)},

  {"html": traps([
     (1, "Scaling factor", "√d_k, not d_k"),
     (1, "Attention weights", "non-negative, sum 1"),
     (2, "Order information", "positional encoding"),
     (2, "Self-attention cost", "O(n²)"),
     (3, "BERT", "encoder, masked LM"),
     (3, "GPT", "decoder, next token")])},

  end(3, "Week 4 · Introduction to Generative AI"),
]

STEPS = [
  [[0, "Week three: attention mechanism और transformers। यह पूरे course का सबसे ज़रूरी week है।",
       "Week three: attention mechanism aur transformers. Yeh poore course ka sabse zaroori week hai."]],
  [[0, "Attention का idea: decoder हर step पर सारे input tokens देख सकता है, सिर्फ एक context vector नहीं।",
       "Attention ka idea: decoder har step par saare input tokens dekh sakta hai, sirf ek context vector nahi."],
   [1, "हर token एक query बनाता है, उसे सबकी keys से match करता है, और values का weighted average लेता है।",
       "Har token ek query banata hai, use sabki keys se match karta hai, aur values ka weighted average leta hai."],
   [2, "Formula: softmax of Q K transpose बटा root d k, गुणा V। Softmax के बाद weights का sum one होता है।",
       "Formula: softmax of Q K transpose bata root d k, guna V. Softmax ke baad weights ka sum one hota hai."],
   [3, "Root d k से divide क्यों? बड़े dimensions में dot products बड़े हो जाते हैं, softmax saturate होकर gradients छोटे कर देता है।",
       "Root d k se divide kyon? Bade dimensions mein dot products bade ho jaate hain, softmax saturate hokar gradients chhote kar deta hai."],
   [4, "Self-attention में Q, K, V एक ही sequence से आते हैं। Cross-attention में query decoder से, key और value encoder से।",
       "Self-attention mein Q, K, V ek hi sequence se aate hain. Cross-attention mein query decoder se, key aur value encoder se."]],
  [[0, "अब transformer architecture।",
       "Ab transformer architecture."],
   [1, "Attention Is All You Need, 2017। इसमें recurrence नहीं, इसलिए सारे tokens parallel में process होते हैं।",
       "Attention Is All You Need, 2017. Ismein recurrence nahi, isliye saare tokens parallel mein process hote hain."],
   [2, "Multi-head attention में h heads अलग-अलग relations सीखते हैं। d k बराबर d model बटा h, जैसे 512 बटा 8 बराबर 64।",
       "Multi-head attention mein h heads alag-alag relations seekhte hain. d k barabar d model bata h, jaise 512 bata 8 barabar 64."],
   [3, "Attention को order पता नहीं, इसलिए positional encoding embeddings में add की जाती है।",
       "Attention ko order pata nahi, isliye positional encoding embeddings mein add ki jaati hai."],
   [4, "Decoder में masking future tokens छिपाती है। और self-attention का cost sequence length का square है, इसलिए context window limited है।",
       "Decoder mein masking future tokens chhipaati hai. Aur self-attention ka cost sequence length ka square hai, isliye context window limited hai."]],
  [[0, "Transformers की तीन families।",
       "Transformers ki teen families."],
   [1, "Encoder only, जैसे BERT: masked language modelling, दोनों तरफ़ का context। Classification और NER के लिए।",
       "Encoder only, jaise BERT: masked language modelling, dono taraf ka context. Classification aur NER ke liye."],
   [2, "Decoder only, जैसे GPT: next token prediction, generation और chat के लिए।",
       "Decoder only, jaise GPT: next token prediction, generation aur chat ke liye."],
   [3, "Encoder decoder, जैसे T5 और BART: translation और summarization।",
       "Encoder decoder, jaise T5 aur BART: translation aur summarization."]],
  [[1, "Recap। Scaling root d k से, और attention weights का sum one।",
       "Recap. Scaling root d k se, aur attention weights ka sum one."],
   [2, "Order के लिए positional encoding, और self-attention order n square।",
       "Order ke liye positional encoding, aur self-attention order n square."],
   [3, "BERT encoder और masked LM, GPT decoder और next token।",
       "BERT encoder aur masked LM, GPT decoder aur next token."]],
  [[0, "Week three ख़त्म। Next video, week four: introduction to generative AI।",
       "Week three khatam. Next video, week four: introduction to generative AI."]],
]

VIDEO = video(3, "Week 3 · Attention & transformers", S, STEPS)
