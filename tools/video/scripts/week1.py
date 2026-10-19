"""Week 1 explainer in Hinglish: Natural Language Processing."""
from vidkit import title, cards, split, traps, end, video

S = [
  title(1, "Natural Language<br>Processing", ["Stemming vs lemma", "BoW &amp; TF-IDF", "One-hot", "Word2Vec · GloVe · FastText", "Cosine similarity"]),

  {"html": split("Text → numbers", 1, 0, [
     (1, "<b>Tokenize</b>: text ko tokens mein todo (word, character, subword)"),
     (2, "<b>Stemming</b> suffix kaatta hai: studies → studi · <b>Lemmatization</b> dictionary form: better → good"),
     (3, "<b>Subword</b> (BPE, WordPiece): unknown words bhi pieces mein toot jaate hain"),
     (4, "Phir <b>vectorise</b>: sparse (BoW, TF-IDF) ya dense (embeddings)")])},

  {"html": cards("Counting words", [
     (1, "Bag of words", "word counts, order lost", "dog bites man = man bites dog"),
     (2, "n-grams", "consecutive word groups", "bigram = 2 words, thoda order bachta hai"),
     (3, "TF-IDF", "TF × log(N / df)", "har document mein word → IDF 0"),
     (4, "One-hot", "length = vocabulary", "sab words orthogonal, koi similarity nahi")], cols=2)},

  {"html": cards("Word embeddings", [
     (1, "Idea", "similar context → similar meaning", "distributional hypothesis"),
     (2, "Word2Vec", "CBOW: context → word<br>Skip-gram: word → context", "skip-gram rare words ke liye better"),
     (3, "GloVe · FastText", "GloVe: global co-occurrence<br>FastText: character n-grams", "FastText unseen words bhi handle karta hai"),
     (4, "Static vs contextual", "Word2Vec: bank ka ek hi vector", "BERT, ELMo: context ke hisaab se")], cols=2)},

  {"html": cards("Similarity &amp; tasks", [
     (1, "Cosine", "a·b / (‖a‖ ‖b‖)", "1 = same direction, 0 = unrelated"),
     (2, "Analogy", "king − man + woman", "≈ queen"),
     (3, "Tasks", "sentiment, NER, POS, translation, summarization, QA", "NLU vs NLG")], cols=3)},

  {"html": traps([
     (1, "Stemming output", "real word nahi bhi ho sakta"),
     (1, "Word in every document", "TF-IDF = 0"),
     (2, "CBOW", "context → word"),
     (2, "Skip-gram", "word → context, rare words"),
     (3, "Word2Vec, GloVe", "static embeddings"),
     (3, "One-hot similarity", "zero")])},

  end(1, "Week 2 · RNNs, LSTM &amp; encoder–decoder"),
]

STEPS = [
  [[0, "Week one: Natural Language Processing। आज देखेंगे कि text को numbers में कैसे बदलते हैं, ताकि model उसे समझ सके।",
       "Week one: Natural Language Processing. Aaj dekhenge ki text ko numbers mein kaise badalte hain, taaki model use samajh sake."]],
  [[0, "Model सिर्फ numbers समझता है। इसलिए पहले एक pipeline चलती है।",
       "Model sirf numbers samajhta hai. Isliye pehle ek pipeline chalti hai."],
   [1, "पहला step tokenization: text को tokens में तोड़ना। Tokens words, characters या subwords हो सकते हैं।",
       "Pehla step tokenization: text ko tokens mein todna. Tokens words, characters ya subwords ho sakte hain."],
   [2, "फिर normalisation। Stemming सिर्फ suffix काटता है, जैसे studies से studi, जो असली word नहीं है। Lemmatization dictionary form देता है, जैसे better से good।",
       "Phir normalisation. Stemming sirf suffix kaatta hai, jaise studies se studi, jo asli word nahi hai. Lemmatization dictionary form deta hai, jaise better se good."],
   [3, "BPE और WordPiece जैसे subword tokenizers नए words को known pieces में तोड़ देते हैं, तो out of vocabulary problem नहीं आती।",
       "BPE aur WordPiece jaise subword tokenizers naye words ko known pieces mein tod dete hain, toh out of vocabulary problem nahi aati."],
   [4, "आख़िर में vectorisation: sparse vectors जैसे bag of words और TF-IDF, या dense embeddings।",
       "Aakhir mein vectorisation: sparse vectors jaise bag of words aur TF-IDF, ya dense embeddings."]],
  [[0, "पहले counting वाले तरीके।",
       "Pehle counting wale tareeke."],
   [1, "Bag of words सिर्फ counts रखता है, order खो जाता है। Dog bites man और man bites dog एक जैसे दिखते हैं।",
       "Bag of words sirf counts rakhta hai, order kho jaata hai. Dog bites man aur man bites dog ek jaise dikhte hain."],
   [2, "N-grams लगातार words के groups हैं। Bigram यानी दो words, इससे थोड़ा order बचता है।",
       "N-grams lagaatar words ke groups hain. Bigram yaani do words, isse thoda order bachta hai."],
   [3, "TF-IDF बराबर है term frequency गुणा log of N बटा document frequency। जो word हर document में है, उसका IDF zero, तो TF-IDF भी zero।",
       "TF-IDF barabar hai term frequency guna log of N bata document frequency. Jo word har document mein hai, uska IDF zero, toh TF-IDF bhi zero."],
   [4, "One-hot vector की length vocabulary जितनी होती है। सारे words आपस में orthogonal हैं, तो कोई similarity नहीं दिखती।",
       "One-hot vector ki length vocabulary jitni hoti hai. Saare words aapas mein orthogonal hain, toh koi similarity nahi dikhti."]],
  [[0, "अब word embeddings: dense vectors जो meaning पकड़ते हैं।",
       "Ab word embeddings: dense vectors jo meaning pakadte hain."],
   [1, "Idea है distributional hypothesis: जो words similar context में आते हैं, उनका meaning भी similar होता है।",
       "Idea hai distributional hypothesis: jo words similar context mein aate hain, unka meaning bhi similar hota hai."],
   [2, "Word2Vec के दो versions। CBOW context से बीच का word predict करता है। Skip-gram word से context predict करता है, और rare words के लिए better है।",
       "Word2Vec ke do versions. CBOW context se beech ka word predict karta hai. Skip-gram word se context predict karta hai, aur rare words ke liye better hai."],
   [3, "GloVe global co-occurrence counts use करता है। FastText character n-grams use करता है, इसलिए नए words का vector भी बना लेता है।",
       "GloVe global co-occurrence counts use karta hai. FastText character n-grams use karta hai, isliye naye words ka vector bhi bana leta hai."],
   [4, "ये सब static हैं: river bank और bank loan, दोनों में bank का एक ही vector। BERT और ELMo contextual हैं।",
       "Yeh sab static hain: river bank aur bank loan, dono mein bank ka ek hi vector. BERT aur ELMo contextual hain."]],
  [[0, "Similarity कैसे नापें?",
       "Similarity kaise naapein?"],
   [1, "Cosine similarity: dot product बटा दोनों lengths का गुणा। One मतलब same direction, zero मतलब unrelated।",
       "Cosine similarity: dot product bata dono lengths ka guna. One matlab same direction, zero matlab unrelated."],
   [2, "Embeddings में analogies भी काम करती हैं: king minus man plus woman लगभग queen।",
       "Embeddings mein analogies bhi kaam karti hain: king minus man plus woman lagbhag queen."],
   [3, "Common NLP tasks: sentiment, named entity recognition, POS tagging, translation, summarization और question answering।",
       "Common NLP tasks: sentiment, named entity recognition, POS tagging, translation, summarization aur question answering."]],
  [[1, "Quick recap। Stemming का output असली word नहीं भी हो सकता। और हर document में आने वाले word का TF-IDF zero।",
       "Quick recap. Stemming ka output asli word nahi bhi ho sakta. Aur har document mein aane wale word ka TF-IDF zero."],
   [2, "CBOW context से word, skip-gram word से context।",
       "CBOW context se word, skip-gram word se context."],
   [3, "Word2Vec और GloVe static हैं, और one-hot vectors में similarity zero।",
       "Word2Vec aur GloVe static hain, aur one-hot vectors mein similarity zero."]],
  [[0, "Week one ख़त्म। Practice कीजिए, फिर next video, week two: RNN, LSTM और encoder decoder।",
       "Week one khatam. Practice kijiye, phir next video, week two: RNN, LSTM aur encoder decoder."]],
]

VIDEO = video(1, "Week 1 · Natural Language Processing", S, STEPS)
