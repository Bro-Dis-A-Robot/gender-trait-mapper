import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

st.set_page_config(layout="wide")

st.title("🌀 Gender-Coded Trait Mapper")
st.write("Input traits and assign them gender-coded ratings (5F = Very Feminine, 0 = Neutral, 5M = Very Masculine).")

# Input for traits
num_traits = st.slider("How many traits do you want to enter?", 1, 15, 8)

# Preset traits and scores
preset_trait_groups = {
    "Emotional Traits": {
        "Nurturing": -4.5,
        "Empathetic": -4.0,
        "Stoic": 4.5,
        "Patient": -3.5,
        "Supportive": -3.5
    },
    "Cognitive Traits": {
        "Analytical": 3.5,
        "Decisive": 3.5,
        "Creative": -2.5,
        "Adaptable": 0.5,
        "Responsible": 0.5
    },
    "Social Traits": {
        "Assertive": 4.0,
        "Charismatic": 2.5,
        "Ambitious": 3.5,
        "Dominant": 4.5,
        "Independent": 2.5
    },
    "Physical/Practical Traits": {
        "Athletic": 3.5,
        "Handy": 3.0,
        "Outdoorsy": 2.5,
        "Organized": -1.5,
        "Graceful": -4.5
    },
    "Style/Presentation": {
        "Stylish": -3.0,
        "Garish Style": -1.0,
        "Reserved Style": 1.0,
        "Masc Presenting": 5.0,
        "Fem Presenting": -5.0
    }
}

flattened_traits = {
    f"{category}: {trait}": score
    for category, traits in preset_trait_groups.items()
    for trait, score in traits.items()
}

input_traits = []
input_scores = []

st.markdown("### Or click to autofill from preset traits:")
selected_preset = []
trait_columns = st.columns(len(preset_trait_groups))
for idx, (category, traits) in enumerate(preset_trait_groups.items()):
    with trait_columns[idx]:
        selection = st.multiselect(f"{category}", options=list(traits.keys()), key=f"cat_{idx}")
        selected_preset.extend(selection)

default_traits = selected_preset + ["" for _ in range(num_traits - len(selected_preset))]
default_scores = [flattened_traits[f"{cat}: {t}"] for cat in preset_trait_groups for t in preset_trait_groups[cat] if t in selected_preset] + [0.0 for _ in range(num_traits - len(selected_preset))]

for i in range(num_traits):
    col1, col2 = st.columns([2, 1])
    with col1:
        trait = st.text_input(f"Trait #{i+1}", value=default_traits[i] if i < len(default_traits) else "", key=f"trait_{i}")
    with col2:
        display_val = st.select_slider(
            f"Score for Trait #{i+1} (5F to 5M)",
            options=[-5.0, -4.5, -4.0, -3.5, -3.0, -2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
            value=default_scores[i] if i < len(default_scores) else 0.0,
            format_func=lambda x: f"{abs(x)}{'F' if x < 0 else 'M' if x > 0 else ''}",
            key=f"score_{i}"
        )
        score = display_val

    input_traits.append(trait)
    input_scores.append(score)

# Automatically render the plot
submitted = True

# Filter out empty trait names and match scores
filtered_pairs = [(t, s) for t, s in zip(input_traits, input_scores) if t.strip() != ""]
if filtered_pairs:
    filtered_traits, filtered_scores = zip(*filtered_pairs)
else:
    filtered_traits, filtered_scores = [], []

if submitted:
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set_xlim(-5.5, 5.5)
    ax.set_ylim(-1.5, 1.8)
    ax.axis('off')

    # Background gradient
    for x in range(-5, 6):
        color = (1 - abs(x)/5, 0.85, 1 if x < 0 else 0.9) if x < 0 else (0.85, 0.85 - x*0.1, 1 - x*0.1)
        rect = patches.Rectangle((x - 0.5, -0.3), 1, 0.6, color=color, alpha=0.3)
        ax.add_patch(rect)

    # Spectrum line
    ax.hlines(0, -5, 5, color='black', linewidth=1)
    for i in range(-5, 6):
        ax.plot(i, 0, 'o', color='black' if i == 0 else 'gray', markersize=4)
        ax.text(i, -0.5, f"{abs(i)}{'F' if i < 0 else 'M' if i > 0 else ''}", ha='center', va='center', fontsize=10, fontweight='bold')

    # Mean line
    mean_score = np.mean(filtered_scores) if filtered_scores else 0
    ax.axvline(mean_score, color='black', linestyle='dotted', linewidth=1)
    ax.text(mean_score, -1.1, f"Mean: {mean_score:.1f}", ha='center', va='top', fontsize=10, fontstyle='italic')

    # Plot trait bubbles
    for idx, (trait, score) in enumerate(zip(filtered_traits, filtered_scores)):
        y_offset = 0.35 + 0.08 * ((idx % 3) - 1)
        color = plt.cm.tab10(idx % 10)
        ax.plot(score, 0.4, 'o', color=color, markersize=12, alpha=0.95)
        ax.text(score, y_offset, trait, ha='center', va='bottom', fontsize=11, fontweight='bold', rotation=30, color=color)

    ax.text(0, 1.5, "Gender-Coded Spectrum of Traits", fontsize=18, ha='center', fontweight='bold', style='italic')
    st.pyplot(fig)
