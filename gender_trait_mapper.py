import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

st.set_page_config(layout="wide")

st.title("🌀 Gender-Coded Trait Mapper")
st.write("Input traits and assign them gender-coded ratings (5F = Very Feminine, 0 = Neutral, 5M = Very Masculine).")

# Input for traits
num_traits = st.slider("How many traits do you want to enter?", 1, 15, 8)

traits = []
scores = []

with st.form("trait_form"):
    for i in range(num_traits):
        col1, col2 = st.columns([2, 1])
        with col1:
            trait = st.text_input(f"Trait #{i+1}", key=f"trait_{i}")
        with col2:
            display_val = st.select_slider(f"Score for Trait #{i+1} (5F to 5M)", options=[-5.0, -4.5, -4.0, -3.5, -3.0, -2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0], format_func=lambda x: f"{abs(int(x))}{'F' if x < 0 else 'M' if x > 0 else ''}", key=f"score_{i}")
            score = display_val  # keep internal representation the same

        traits.append(trait)
        scores.append(score)

    submitted = st.form_submit_button("Plot Traits")

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
    mean_score = np.mean(scores)
    ax.axvline(mean_score, color='black', linestyle='dotted', linewidth=1)
    ax.text(mean_score, -1.1, f"Mean: {mean_score:.1f}", ha='center', va='top', fontsize=10, fontstyle='italic')

    # Plot trait bubbles
    for idx, (trait, score) in enumerate(zip(traits, scores)):
        y_offset = 0.35 + 0.08 * ((idx % 3) - 1)
        color = plt.cm.tab10(idx % 10)
        ax.plot(score, 0.4, 'o', color=color, markersize=12, alpha=0.95)
        ax.text(score, y_offset, trait, ha='center', va='bottom', fontsize=11, fontweight='bold', rotation=30, color=color)

    ax.text(0, 1.5, "Gender-Coded Spectrum of Traits", fontsize=18, ha='center', fontweight='bold', style='italic')
    st.pyplot(fig)
