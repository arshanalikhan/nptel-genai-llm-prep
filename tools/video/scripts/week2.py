"""Week 2 explainer in Hinglish: sequential data, RNNs, encoder–decoder."""
from vidkit import title, cards, split, traps, end, video

S = [
  title(2, "Sequential data, RNNs<br>&amp; encoder–decoder", ["Hidden state", "BPTT", "Vanishing gradients", "LSTM · GRU", "Seq2seq · beam search"]),

  {"html": cards("Why RNNs", [
     (1, "Sequential data", "text, speech, time series, stock prices", "order matters"),
     (2, "RNN", "hidden state + same weights every step", "h_t = tanh(W h_(t−1) + U x_t + b)"),
     (3, "Shapes", "one-to-many: captioning<br>many-to-one: sentiment", "many-to-many: tagging, translation"),
     (4, "Training", "backprop through time (BPTT)", "steps one by one, no parallel")], cols=2)},

  {"html": cards("Gradient problems &amp; gates", [
     (1, "Vanishing", "gradients shrink over many steps", "long-range memory lost"),
     (2, "Exploding", "gradients blow up", "fix: gradient clipping"),
     (3, "LSTM", "forget · input · output gates + cell state", "additive cell → gradients flow"),
     (4, "GRU", "update · reset gates, no cell", "fewer parameters")], cols=2)},

  {"html": split("Encoder–decoder (seq2seq)", 2, 0, [
     (1, "<b>Encoder</b> poora input padh kar ek context vector banata hai"),
     (2, "<b>Decoder</b> ek-ek token output likhta hai; lengths alag ho sakti hain"),
     (3, "<b>Bottleneck</b>: ek fixed vector, lambe sentence ka detail kho jaata hai"),
     (4, "<b>Teacher forcing</b>: training mein true previous token · <b>Beam search</b>: top-B paths")])},

  {"html": traps([
     (1, "Exploding gradients", "gradient clipping"),
     (1, "Vanishing gradients", "LSTM / GRU"),
     (2, "LSTM gates", "forget, input, output (3)"),
     (2, "Reset gate", "GRU ka hai"),
     (3, "Beam width 1", "greedy"),
     (3, "Bidirectional RNN", "generation ke liye nahi")])},

  end(2, "Week 3 · Attention &amp; transformers"),
]

STEPS = [
  [[0, "Week two: sequential data, RNN और encoder decoder model।",
       "Week two: sequential data, RNN aur encoder decoder model."]],
  [[0, "पहले, RNN की ज़रूरत क्यों है?",
       "Pehle, RNN ki zaroorat kyon hai?"],
   [1, "Sequential data में order मायने रखता है: text, speech, time series, stock prices।",
       "Sequential data mein order maayne rakhta hai: text, speech, time series, stock prices."],
   [2, "RNN एक hidden state रखता है, यानी memory, और हर time step पर same weights use करता है।",
       "RNN ek hidden state rakhta hai, yaani memory, aur har time step par same weights use karta hai."],
   [3, "Shapes याद रखिए: image captioning one to many, sentiment many to one, tagging और translation many to many।",
       "Shapes yaad rakhiye: image captioning one to many, sentiment many to one, tagging aur translation many to many."],
   [4, "Training backpropagation through time से होती है। Steps एक-एक करके चलते हैं, इसलिए parallel नहीं हो सकता।",
       "Training backpropagation through time se hoti hai. Steps ek-ek karke chalte hain, isliye parallel nahi ho sakta."]],
  [[0, "अब gradient की problems।",
       "Ab gradient ki problems."],
   [1, "Vanishing gradient: बहुत steps पर gradient छोटा होता जाता है, तो पुराने words की memory खो जाती है।",
       "Vanishing gradient: bahut steps par gradient chhota hota jaata hai, toh purane words ki memory kho jaati hai."],
   [2, "Exploding gradient: gradient बहुत बड़ा हो जाता है। Fix है gradient clipping।",
       "Exploding gradient: gradient bahut bada ho jaata hai. Fix hai gradient clipping."],
   [3, "LSTM में तीन gates हैं: forget, input और output, साथ में एक cell state। Cell additively update होता है, तो gradient flow करता है।",
       "LSTM mein teen gates hain: forget, input aur output, saath mein ek cell state. Cell additively update hota hai, toh gradient flow karta hai."],
   [4, "GRU में दो gates हैं, update और reset, अलग cell नहीं। Parameters कम, accuracy अक्सर similar।",
       "GRU mein do gates hain, update aur reset, alag cell nahi. Parameters kam, accuracy aksar similar."]],
  [[0, "अब encoder decoder, यानी seq2seq model।",
       "Ab encoder decoder, yaani seq2seq model."],
   [1, "Encoder पूरा input पढ़ता है और एक context vector बनाता है।",
       "Encoder poora input padhta hai aur ek context vector banata hai."],
   [2, "Decoder उस vector से एक-एक token output लिखता है। Input और output की length अलग हो सकती है।",
       "Decoder us vector se ek-ek token output likhta hai. Input aur output ki length alag ho sakti hai."],
   [3, "Problem है bottleneck: पूरा sentence एक fixed vector में, तो लंबे sentences का detail खो जाता है। Week three का attention इसे fix करता है।",
       "Problem hai bottleneck: poora sentence ek fixed vector mein, toh lambe sentences ka detail kho jaata hai. Week three ka attention ise fix karta hai."],
   [4, "Teacher forcing में training के दौरान decoder को सही previous token मिलता है। और beam search top B sequences साथ रखता है।",
       "Teacher forcing mein training ke dauraan decoder ko sahi previous token milta hai. Aur beam search top B sequences saath rakhta hai."]],
  [[1, "Recap। Exploding gradient का fix clipping, vanishing का LSTM या GRU।",
       "Recap. Exploding gradient ka fix clipping, vanishing ka LSTM ya GRU."],
   [2, "LSTM के तीन gates, और reset gate GRU का है।",
       "LSTM ke teen gates, aur reset gate GRU ka hai."],
   [3, "Beam width one मतलब greedy, और bidirectional RNN generation के लिए नहीं, क्योंकि future tokens अभी हैं ही नहीं।",
       "Beam width one matlab greedy, aur bidirectional RNN generation ke liye nahi, kyonki future tokens abhi hain hi nahi."]],
  [[0, "Week two ख़त्म। Next video, week three: attention और transformers।",
       "Week two khatam. Next video, week three: attention aur transformers."]],
]

VIDEO = video(2, "Week 2 · RNNs & encoder–decoder", S, STEPS)
