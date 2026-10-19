"""Week 4 explainer in Hinglish: introduction to generative AI."""
from vidkit import title, cards, split, traps, end, video

S = [
  title(4, "Introduction to<br>Generative AI", ["Generative vs discriminative", "Autoencoder · VAE", "GAN", "Diffusion", "CLIP"]),

  {"html": cards("What is generative AI?", [
     (1, "Discriminative", "learns P(y | x)", "boundary banata hai: spam ya nahi"),
     (2, "Generative", "learns P(x) or P(x, y)", "naya data sample kar sakta hai"),
     (3, "Outputs", "text, images, audio, video, code, synthetic data", "business: content, chatbots, design")], cols=3)},

  {"html": split("Four model families", 4, 0, [
     (1, "<b>Autoencoder</b>: bottleneck se reconstruct · <b>VAE</b>: loss = reconstruction + KL"),
     (2, "<b>GAN</b>: generator vs discriminator · failure: mode collapse"),
     (3, "<b>Diffusion</b>: forward noise add (fixed), reverse denoise (learned, U-Net)"),
     (4, "<b>CLIP</b>: image–caption contrastive · zero-shot classification")], max_h=400)},

  {"html": cards("Details that get asked", [
     (1, "Reparameterisation", "z = μ + σ·ε", "sampling differentiable ban jaata hai"),
     (2, "GAN problems", "unstable training, mode collapse", "CycleGAN: unpaired translation"),
     (3, "Latent diffusion", "Stable Diffusion", "compressed latent space mein, fast"),
     (4, "Image metrics", "FID: lower better", "VAE images blurry, GAN/diffusion sharp")], cols=2)},

  {"html": traps([
     (1, "Discriminative", "P(y | x)"),
     (1, "VAE loss", "reconstruction + KL"),
     (2, "Little variety from a GAN", "mode collapse"),
     (2, "Diffusion forward process", "fixed, adds noise"),
     (3, "CLIP training", "contrastive image–text"),
     (3, "Diffusion drawback", "slow sampling")])},

  end(4, "Week 5 · Large Language Models"),
]

STEPS = [
  [[0, "Week four: introduction to generative AI। Models जो नया content बनाते हैं।",
       "Week four: introduction to generative AI. Models jo naya content banaate hain."]],
  [[0, "पहले basic difference।",
       "Pehle basic difference."],
   [1, "Discriminative model P of y given x सीखता है, यानी boundary बनाता है, जैसे यह email spam है या नहीं।",
       "Discriminative model P of y given x seekhta hai, yaani boundary banata hai, jaise yeh email spam hai ya nahi."],
   [2, "Generative model data का distribution, P of x, सीखता है, इसलिए नया data sample कर सकता है।",
       "Generative model data ka distribution, P of x, seekhta hai, isliye naya data sample kar sakta hai."],
   [3, "Output हो सकता है text, images, audio, video, code या synthetic data। Business में content, chatbots और design के लिए।",
       "Output ho sakta hai text, images, audio, video, code ya synthetic data. Business mein content, chatbots aur design ke liye."]],
  [[0, "अब चार model families।",
       "Ab chaar model families."],
   [1, "Autoencoder input को bottleneck में compress करके reconstruct करता है। VAE latent को distribution बनाता है, और loss है reconstruction plus KL divergence।",
       "Autoencoder input ko bottleneck mein compress karke reconstruct karta hai. VAE latent ko distribution banata hai, aur loss hai reconstruction plus KL divergence."],
   [2, "GAN में generator fake बनाता है और discriminator real और fake पहचानता है। यह minimax game है। Common failure: mode collapse, यानी variety नहीं।",
       "GAN mein generator fake banata hai aur discriminator real aur fake pehchaanta hai. Yeh minimax game hai. Common failure: mode collapse, yaani variety nahi."],
   [3, "Diffusion में forward process धीरे-धीरे noise add करता है, और एक U-Net reverse में noise हटाना सीखता है।",
       "Diffusion mein forward process dheere-dheere noise add karta hai, aur ek U-Net reverse mein noise hatana seekhta hai."],
   [4, "CLIP images और captions को contrastive तरीके से match करता है। इससे zero-shot classification और text-guided image generation होता है।",
       "CLIP images aur captions ko contrastive tareeke se match karta hai. Isse zero-shot classification aur text-guided image generation hota hai."]],
  [[0, "कुछ details जो exam में पूछी जाती हैं।",
       "Kuch details jo exam mein poochi jaati hain."],
   [1, "Reparameterisation trick: z बराबर mu plus sigma गुणा epsilon। इससे sampling के बाद भी gradients flow करते हैं।",
       "Reparameterisation trick: z barabar mu plus sigma guna epsilon. Isse sampling ke baad bhi gradients flow karte hain."],
   [2, "GAN training unstable होती है। CycleGAN बिना paired images के translation करता है, जैसे horse से zebra।",
       "GAN training unstable hoti hai. CycleGAN bina paired images ke translation karta hai, jaise horse se zebra."],
   [3, "Stable Diffusion latent diffusion है: compressed latent space में काम करता है, इसलिए fast।",
       "Stable Diffusion latent diffusion hai: compressed latent space mein kaam karta hai, isliye fast."],
   [4, "FID जितना कम उतना अच्छा। VAE की images blurry होती हैं, GAN और diffusion की sharp।",
       "FID jitna kam utna achha. VAE ki images blurry hoti hain, GAN aur diffusion ki sharp."]],
  [[1, "Recap। Discriminative P of y given x। VAE loss reconstruction plus KL।",
       "Recap. Discriminative P of y given x. VAE loss reconstruction plus KL."],
   [2, "GAN में variety कम तो mode collapse। Diffusion का forward process fixed है।",
       "GAN mein variety kam toh mode collapse. Diffusion ka forward process fixed hai."],
   [3, "CLIP contrastive है, और diffusion की कमी slow sampling।",
       "CLIP contrastive hai, aur diffusion ki kami slow sampling."]],
  [[0, "Week four ख़त्म। Next video, week five: large language models।",
       "Week four khatam. Next video, week five: large language models."]],
]

VIDEO = video(4, "Week 4 · Introduction to Generative AI", S, STEPS)
