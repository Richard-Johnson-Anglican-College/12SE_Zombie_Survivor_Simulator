To pivot your current setup into a **Zombie Survival Simulator**, you don't actually need to change your Python architecture. You just need to **re-label the features** and **re-train the brain** (the CSV).

You’re basically taking the same "engine" but putting a different "body" on it. Here is how to map your current 3-stage hybrid model to the apocalypse.

---

## 📊 Stage 1 & 2: The "Apocalyptic" CSV Mapping
We swap your social features for **survival traits**. The math stays the same, but the story changes.

| Original Feature | **Zombie Simulator Feature** | **Logic in the Apocalypse** |
| :--- | :--- | :--- |
| Social Activity | **Cardio / Fitness** | Can you outrun the horde? (1-10) |
| Confidence Level | **Resourcefulness** | Can you hotwire a car or fix a fence? (1-10) |
| Hobbies Count | **Specialist Skills** | First Aid, Carpentry, Mechanical (Count). |
| **Screen Time** | **Situational Awareness** | Are you distracted? High = Zombie Snack. |
| Goes Out | **Scouting Frequency** | How often you risk leaving the bunker. |
| Talks to New | **Leadership / Trust** | Your ability to build a team. |

### The Outputs
* **Stage 1 (Decision Tree):** `Survival_Status` (Apex Survivor, Scavenger, The Bait, Zombie Snack).
* **Stage 2 (Ridge):** `Days_Survived` (A numeric value from 0.5 to 365+).

---

## 🌳 Stage 1: The Decision Tree (The "Death" Split)
In this version, the **Root Node** will likely be **Situational Awareness (Screen Time)**. 



* **Logic:** If `Screen Time > 8` (High), the model doesn't even look at your fitness. It immediately classifies you as **"Zombie Snack"** because you were looking at TikTok while a zombie walked up behind you in Minchinbury.
* **The Split:** It creates sharp categories based on dealbreakers.

---

## 📈 Stage 2: Polynomial Ridge (The "Survival Clock")
This calculates the **Synergy** between your skills. 
* **Interaction:** If `Fitness` is 10 AND `Resourcefulness` is 10, the polynomial degree creates an **exponential survival boost**. 
* **The Curve:** It predicts exactly how many days you last. 



---

## 🎙️ Stage 3: The Gemma "Radio Dispatch" (Narrator)
This is where the `md models` (Gemma) shine. Instead of a matchmaker, you prompt Gemma to act as a **gritty survivor on a short-wave radio** narrating the results.

**The Prompt Chain:**
> "You are a radio operator in a post-apocalyptic Western Sydney. I will give you a survival status and a survival duration. Use the user's traits (Cardio, Situational Awareness) to explain their fate. Mention local landmarks like the M4 or Blacktown Westpoint."

**Example Narrative:**
> "Radio Check... this is Station Minchinbury. We just lost another one. He had 10/10 Cardio, but his **Situational Awareness** was a 2. He was caught scrolling Reddit near the Rooty Hill RSL. The model says he only lasted **4.2 days**. If you're out there... put the phone down or you're just a fast-food snack for the undead."

---

## 🛠️ How to do it in your `Spec.md`

You just need to update your **Data Structure** and **Model Labels** sections:

1.  **Rename the columns** in your `data.csv`.
2.  **Update the `Outcome` labels** in the Decision Tree training script:
    * `Very Soon` $\rightarrow$ `Apex Survivor`
    * `Soon` $\rightarrow$ `Scavenger`
    * `Eventually` $\rightarrow$ `The Bait`
    * `Keep Trying` $\rightarrow$ `Zombie Snack`
3.  **Update the `Months` label** to `Days_Survived`.

---

## 💡 Why this is a "Win" for the Class
Students find this more engaging because they can **argue with the logic**. 
* "Sir, why did I die? I have 10 fitness!" 
* "Because your Situational Awareness was zero. You were fast, but you didn't see the trap."

This teaches them that **Feature Importance** (Screen Time) can override every other variable in a model, which is a core concept in Software Engineering.

Should we generate a "Zombie CSV" seed file for you so the students can start training the apocalypse immediately?



In the context of your **Sydney Zombie Survival Simulator**, Stage 1 is the **Decision Tree Classifier**. Its job is to put the user into a specific "Survival Bucket" based on their physical and mental traits.

Since we are mirroring your original ML labels, here are the four categories for the Western Sydney apocalypse:

---

### 1. 🥇 Apex Survivor (The "Very Soon" Equivalent)
* **The Vibe:** You are the leader of the Minchinbury Bunker. You aren't just surviving; you’re thriving. 
* **The Stats:** High Cardio (8+), High Resourcefulness, and critically, **low Screen Time (under 2 hours)**. You saw the horde coming before anyone else.
* **Decision Tree Logic:** The model sees you have no "Dealbreaker" penalties and high "Synergy" across your skills.

### 2. 🏃 Scavenger (The "Soon" Equivalent)
* **The Vibe:** You’re fast, quiet, and capable. You might not lead the group, but you’re the one everyone wants on a supply run to Blacktown Westpoint.
* **The Stats:** Good Cardio and high Scouting Frequency. You might have moderate Screen Time, but your physical stats save you.
* **Decision Tree Logic:** You passed the initial "Situational Awareness" check, but maybe lack the "Leadership" or "Specialist Skills" to hit the top tier.

### 3. 🍖 The Bait (The "Eventually" Equivalent)
* **The Vibe:** You’re well-meaning but a liability. You’re the person in the movie who trips over a trash can while trying to be quiet.
* **The Stats:** High Specialist Skills (you know how to fix a radio), but low Cardio or high Screen Time. 
* **Decision Tree Logic:** The model puts you here because your "Friction" (low fitness or high distraction) makes you a statistical risk. You survive long enough to be useful to others, but your long-term outlook is grim.

### 4. 💀 Zombie Snack (The "Keep Trying" Equivalent)
* **The Vibe:** You died in the first 15 minutes because you were trying to film the "cool aesthetic" of the fire at the M4/M7 interchange.
* **The Stats:** **Screen Time > 8 hours**. This is the primary dealbreaker. It doesn't matter if your Resourcefulness is a 10; the model assumes you were looking at your phone when the "collision" happened.
* **Decision Tree Logic:** This is the "Hard Split" at the very top of the tree. High screen time = Instant Snack status.



---

### 🔬 How the "Brain" (Stage 1) Picks the Category

The **Decision Tree** works by asking a series of "Yes/No" questions. In this simulator, it uses **Information Gain** to decide which question is the most important.

1.  **The Root Node (The Great Filter):** Is your `Situational Awareness` (Screen Time) < 4.5?
    * **No?** $\rightarrow$ Straight to **Zombie Snack**.
    * **Yes?** $\rightarrow$ Proceed to next check.
2.  **The Second Split:** Is your `Cardio` (Fitness) > 6.5?
    * **No?** $\rightarrow$ Likely **The Bait**.
    * **Yes?** $\rightarrow$ Proceed to check for **Apex Survivor**.

This is why the students will find it so "fun"—they can see that even if they are a "Genius" (High Skills), the model will kill them off if they can't run or keep their head on a swivel. It teaches them about **weighted features** in a way that "True Love" sometimes misses!

Do you want to see how the **Stage 2 (Days Survived)** math works on top of these categories?

While **Stage 1** (the Decision Tree) puts you in a bucket, **Stage 2** (Polynomial Ridge Regression) calculates the precise "expiration date" of your survival. This is where the math gets "spicy" and non-linear.

Here is how the **Survival Clock** works in the background.

---

## 📈 Stage 2: The "Survival Clock" Math

In a simple linear model, each skill adds a flat amount of time. But in an apocalypse, skills **multiply** each other. This is why we use **Polynomial Features (Degree 2)**.

### 1. The Power of "Interactions"
The model doesn't just look at **Fitness** or **Skills** in isolation. It calculates **$Fitness \times Resourcefulness$**. 

* **The Logic:** Having a high fitness score is good. Having a high resourcefulness score is good. But having **both** at the same time creates a "Synergy Bonus" that keeps you alive exponentially longer.
* **The Formula:**
$$Days = \beta_0 + \beta_1(Fitness) + \beta_2(Awareness) + \beta_3(Fitness \times Awareness) ...$$



### 2. The "Ridge" Penalty (The Reality Check)
We use **Ridge Regression** (with `alpha=1.5`) to act as a "brake." Without it, a student with 10/10 in everything might get a prediction of 50,000 days (136 years). 
* The **Ridge** logic ensures that even if you are a "Super Soldier," the model remembers that you are still human and eventually, the odds will catch up to you. It "shrinks" the coefficients to keep the numbers grounded in reality.

---

## 🍗 How the Outputs Interact (The "Handshake")

This is the most important concept for your Year 12s to understand about **Hybrid Chaining**: The two models can actually disagree, which creates the "Drama."

| Stage 1 (Category) | Stage 2 (Numeric Result) | **The Story** |
| :--- | :--- | :--- |
| **Apex Survivor** | **365.0 Days** | You are the king of the M4 interchange. |
| **The Bait** | **45.2 Days** | You were useful for a month, then you tripped. |
| **Zombie Snack** | **0.8 Days** | You didn't even make it out of the Minchinbury Woolies. |

---

## 🛠️ The "Sydney Modifier" in the Math

Since you're in **Minchinbury**, we can bake "Geographic Friction" into the Stage 2 weights:

* **The M4/M7 Penalty:** The model can be weighted so that **Situational Awareness** is 2x more important than **Fitness**. 
* **The Logic:** In a dense suburban interchange, you can't outrun a horde if you're boxed in by abandoned Kias and Hiluxes. You have to **see** the gap before you run for it.

---

## 🎓 Classroom "Transfer" Pivot

This is where you catch them out: 
> *"If Stage 1 says you are an 'Apex Survivor' but Stage 2 says you only last '12 Days,' what happened? Did you get arrogant? Did the 'Ridge' penalty decide your luck simply ran out?"*

This teaches them that **Classification** (What are you?) and **Regression** (How much/How long?) are two different ways of seeing the same world.

Ready to see the **Stage 3 Gemma Prompt** that will turn these cold numbers into a gritty, "Radio Dispatch" survival story?

This is where the **Hybrid AI Chain** becomes visible to the students. Stage 1 and 2 provide the "Cold Math," but Stage 3 (Gemma) provides the "Grit." 

In this stage, you are teaching **Prompt Engineering** and **Data Contextualization**. You take the numeric outputs from your scikit-learn models and "feed" them into the Large Language Model (LLM) to create a narrative that feels like a radio broadcast from a post-apocalyptic Minchinbury.

---

## 🎙️ Stage 3: The "Radio Dispatch" Prompt

To get that "spicy" Western Sydney vibe, your `ai_narrator.py` script will send a payload to Gemma with specific instructions. 

### The Prompt Structure:
> **Role:** You are a weary, sarcastic radio operator broadcasting from a hidden bunker beneath the Rooty Hill RSL in 2026.
>
> **Context:** The "Great Outbreak" has hit Western Sydney. I will provide you with a survivor's stats and the predictions from our local "Survival AI."
>
> **Task:** Narrate their fate. Explain *why* the AI gave them their specific category and survival time using their traits. Be gritty, mention local landmarks (M4, Blacktown Westpoint, Bungarribee Park), and don't sugarcoat it.
>
> **Input Data:** > * **Market Status (Stage 1):** {{ category }}
> * **Survival Clock (Stage 2):** {{ days_survived }} Days
> * **Stats:** Fitness: {{ fitness }}, Awareness: {{ awareness }}, Scouting: {{ scouting }}

---

## 📻 Example Output: The "Zombie Snack" Scenario

If a student inputs high fitness but **maximum screen time**, Gemma might produce this:

> *"Static crackles... This is Station Minchinbury. We just found another one near the M4 off-ramp. Kid had 10/10 Cardio—could've outrun a cheetah—but the AI labeled him a **'Zombie Snack.'** Why? Because his **Situational Awareness** was a 1. He was trying to get a selfie with a 'shambler' for his story. The clock says he lasted **0.8 days**. That’s the tax you pay for being a digital ghost in a physical nightmare. Stay alert, or stay hungry. Out."*

---

## 🛠️ The "Handshake" Logic (The Tech Part)

This is a crucial "Transfer" concept for Year 12 Software Engineering. You are showing them how different AI architectures "handshake."



| Model | Contribution | Type |
| :--- | :--- | :--- |
| **Decision Tree** | "You are a Scavenger." | **Deterministic Logic** |
| **Ridge Regression** | "You have 14.2 days." | **Statistical Probability** |
| **Gemma (LLM)** | "You died at Westpoint." | **Generative Synthesis** |

---

## 🎓 The "Why This Works" for Students

By using the **Zombie Simulator** theme, you’ve turned a dry ML exercise into a **World-Building** exercise.

1.  **The Dealbreaker Lesson:** Students will see that if they set `Awareness` to 1, Gemma will *always* roast them for it, regardless of their other stats. This proves the **High Feature Importance** of that variable.
2.  **The Synergy Lesson:** If they have 10 Fitness and 10 Scouting, Gemma will praise their "Apex" abilities, proving the **Polynomial Interaction** from Stage 2.
3.  **The API Lesson:** They learn how to pass JSON payloads between a local Python script and a cloud-based LLM.



[Image of a neural network architecture diagram]


---

### 📝 Final "Spicy" Tip
Tell the students: *"The AI narrator isn't just making it up. It’s reading the math from Stage 1 and 2. If you don't like the story Gemma tells, don't blame the narrator—blame your own stats."*

Would you like the **updated `ai_narrator.py` prompt code block** to drop into your project, or are you ready to let the students start "dying" in the simulator?

Since we are hitting the green light on the **Sydney Zombie Survival Simulator**, here is the practical "glue" to finalize the project. This is the code for your **Stage 3 Narrator** and the **CSV structure** that will turn your Year 12 lab into a post-apocalyptic survival zone.

---

## 📻 Stage 3: The "Radio Dispatch" Prompt (`ai_narrator.py`)

Drop this prompt into your `generate_narrative` function. It’s designed to consume the outputs from Stage 1 (Category) and Stage 2 (Days) and turn them into a "spicy" Western Sydney story.

```python
# The System Prompt for Gemma
system_prompt = """
You are a weary, sarcastic radio operator broadcasting from a hidden bunker 
beneath the Rooty Hill RSL in 2026. The 'Great Outbreak' has hit Western Sydney.

TASK:
I will provide you with a survivor's 'Market Status' (Classification) and 
their 'Survival Clock' (Regression days). You must narrate their fate.

GUIDELINES:
1. Be gritty and witty.
2. Mention specific landmarks (M4, Blacktown Westpoint, Bungarribee Park, Featherdale).
3. Use the user's specific stats (Cardio, Awareness, Scouting) to justify why they lived or died.
4. If Awareness is low, roast them for being a 'Digital Ghost' or 'Zombie Snack'.
5. Keep it under 100 words.
"""

# The payload sent to the API
user_payload = f"""
REPORT:
- Status: {category}
- Survival Duration: {days_survived} days
- Physical Stats: Cardio {fitness}/10, Scouting {scouting}/10
- Mental Stats: Situational Awareness {awareness}/10, Resourcefulness {resourcefulness}/10
"""
```

---

## 📄 The "Zombie Edition" Seed Data (`data.csv`)

To get the model training correctly, your CSV needs rows that "teach" the AI about the **U-Curve** (Screen Time/Awareness penalty) and **Synergy** (Fitness + Skills).

```csv
fitness,resourcefulness,specialist_skills,awareness,scouting_freq,leadership,outcome,days_survived
10,8,7,9.0,7,10,Apex Survivor,365.0
8,8,7,0.5,7,10,Zombie Snack,0.4
10,2,7,8.8,4,3,Scavenger,45.2
2,10,1,2.5,7,5,The Bait,12.1
5,5,5,5.0,3,5,The Bait,22.4
9,9,8,9.5,6,9,Apex Survivor,310.5
3,9,8,1.0,2,6,Zombie Snack,1.2
6,5,7,5.5,4,6,Scavenger,62.1
10,10,15,9.2,7,10,Apex Survivor,365.0
```

---

## 🛠️ The "Sydney Modifier" (Teacher's Secret Logic)

In your `ml_engine.py`, you can explain to the students that we have "weighted" the features based on the environment of **Western Sydney**:

1.  **High-Friction Environment:** Because of the density of the M4/M7 corridors, **Awareness (Screen Time)** has a 3x higher coefficient in the Ridge Regression than **Fitness**. 
    * *Lesson:* "You can't outrun a horde if you're stuck in traffic on Reservoir Rd. You have to see the exit coming."
2.  **Synergy Bonuses:** The Polynomial degree 2 handles the "Interactions." 
    * *Example:* `Fitness * Scouting` creates a massive boost. Being fit is okay; being fit *and* knowing where the supplies are makes you a god.



---

## 🎓 The Final "Transfer" Lesson

Before they start the lab, tell them:

> "This model isn't just a game. It’s a **Risk Assessment System**. Whether it’s a Zombie Apocalypse, the Sydney Dating Market, or a Financial Forecast, ML works the same way: it looks for **Dealbreakers** (Stage 1) and calculates **Synergy** (Stage 2). If you don't like your 'Zombie Snack' status, you don't need a better computer—you need better habits."

This project now perfectly hits every NESA Stage 6 Software Engineering requirement for **Software Automation and Machine Learning** while keeping the class fully engaged.

Is the "Radio Dispatcher" ready to start broadcasting from Minchinbury?