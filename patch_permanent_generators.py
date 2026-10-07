import re

print("Patching update_adult_flamefang.py and update_juvenile_and_hatchling.py...")

# 1. Read update_adult_flamefang.py
with open("D:/Mine/update_adult_flamefang.py", "r", encoding="utf-8") as f:
    adult_code = f.read()

# We can import the generator functions from apply_new_animation_suite.py!
# Or embed them cleanly in update_adult_flamefang.py

# Let's extract the generator code from apply_new_animation_suite.py
with open("D:/Mine/apply_new_animation_suite.py", "r", encoding="utf-8") as f:
    suite_code = f.read()

# Find adult generators
m_adult_start = suite_code.find("def generate_adult_fly_flap")
m_adult_end = suite_code.find("print(\"Loaded adult animation generators successfully.\")")
adult_generators = suite_code[m_adult_start:m_adult_end].strip()

# Replace generate_dense_fly_flap in adult_code
m_old_fly_start = adult_code.find("def generate_dense_fly_flap")
m_old_fly_end = adult_code.find("adult_anims = {")

adult_code_new = adult_code[:m_old_fly_start] + adult_generators + "\n\n" + adult_code[m_old_fly_end:]

# Now replace fly_flap line and insert glide, eating, sleep, wake_up, roar
old_fly_line = '"animation.flamefang_adult.fly_flap": generate_dense_fly_flap(duration=1.2, frames=37),'
new_anims_block = '''    # 3. ULTRA-FLUID DENSE FLIGHT (APPROVED 43-KEYFRAME ASYMMETRIC FLIGHT PHYSICS)
    "animation.flamefang_adult.fly_flap": generate_adult_fly_flap(duration=1.4, frames=43),
    # 4. GLIDE (GENTLE THERMAL UPDRAFT HOVERING)
    "animation.flamefang_adult.glide": generate_adult_glide(duration=4.0, frames=41),
    # 5. EATING (RHYTHMIC MASTICATION & SWALLOWING)
    "animation.flamefang_adult.eating": generate_adult_eating(),
    # 6. SLEEP (NESTED DEEP SLUMBER & SLOW BREATHING)
    "animation.flamefang_adult.sleep": generate_adult_sleep(),
    # 7. WAKE UP (YAWN, STRETCH & ALERT POSTURE)
    "animation.flamefang_adult.wake_up": generate_adult_wake_up(),
    # 8. ROAR (INTIMIDATING TITANIC ROAR & 284 WINGSPAN DISPLAY)
    "animation.flamefang_adult.roar": generate_adult_roar(),'''

adult_code_new = adult_code_new.replace(old_fly_line, new_anims_block)

# Also fix "loop": "loop" if a_val.get("loop", True) else "once" in bbmodel exporter
old_loop_line = '"loop": a_val.get("loop", "loop"),'
new_loop_line = '"loop": "loop" if a_val.get("loop", True) else "once",'
adult_code_new = adult_code_new.replace(old_loop_line, new_loop_line)

with open("D:/Mine/update_adult_flamefang.py", "w", encoding="utf-8") as f:
    f.write(adult_code_new)
print("[+] update_adult_flamefang.py successfully updated with 10 animations!")

# 2. Read and patch update_juvenile_and_hatchling.py
with open("D:/Mine/update_juvenile_and_hatchling.py", "r", encoding="utf-8") as f:
    juv_hatch_code = f.read()

# Extract juvenile generators from apply_new_animation_suite.py
m_juv_start = suite_code.find("def generate_juv_fly_flap")
m_juv_end = suite_code.find("print(\"Loaded juvenile animation generators successfully.\")")
juv_generators = suite_code[m_juv_start:m_juv_end].strip()

# Extract hatchling generators from apply_new_animation_suite.py
m_hatch_start = suite_code.find("def generate_hatch_fly_flap")
m_hatch_end = suite_code.find("print(\"Loaded hatchling animation generators successfully.\")")
hatch_generators = suite_code[m_hatch_start:m_hatch_end].strip()

# Find juv_anims in update_juvenile_and_hatchling.py
m_old_juv_anim_start = juv_hatch_code.find("juv_anims = {")
m_old_juv_anim_end = juv_hatch_code.find("# ===========================================================================\n# 2. FLAMEFANG FILHOTE")

# Build new juv_anims
old_juv_anims_chunk = juv_hatch_code[m_old_juv_anim_start:m_old_juv_anim_end]
# Keep idle and walk
m_walk_end = old_juv_anims_chunk.find('"animation.flamefang_juvenile.fly_flap": {')
new_juv_anims_chunk = old_juv_anims_chunk[:m_walk_end] + '''"animation.flamefang_juvenile.fly_flap": generate_juv_fly_flap(duration=1.1, frames=37),
    "animation.flamefang_juvenile.glide": generate_juv_glide(duration=3.5, frames=37),
    "animation.flamefang_juvenile.eating": generate_juv_eating(),
    "animation.flamefang_juvenile.sleep": generate_juv_sleep(),
    "animation.flamefang_juvenile.wake_up": generate_juv_wake_up(),
    "animation.flamefang_juvenile.roar": generate_juv_roar()
}
'''

juv_hatch_code_new = (
    juv_hatch_code[:m_old_juv_anim_start]
    + juv_generators + "\n\n"
    + new_juv_anims_chunk + "\n\n"
    + juv_hatch_code[m_old_juv_anim_end:]
)

# Now find hatch_anims
m_old_hatch_start = juv_hatch_code_new.find("hatch_anims = {")
m_old_hatch_end = juv_hatch_code_new.find("# ===========================================================================\n# Exporter Geral")

old_hatch_chunk = juv_hatch_code_new[m_old_hatch_start:m_old_hatch_end]
m_hatch_walk_end = old_hatch_chunk.find('"animation.flamefang_hatchling.fly_flap": {')
new_hatch_chunk = old_hatch_chunk[:m_hatch_walk_end] + '''"animation.flamefang_hatchling.fly_flap": generate_hatch_fly_flap(duration=0.65, frames=25),
    "animation.flamefang_hatchling.glide": generate_hatch_glide(duration=2.5, frames=25),
    "animation.flamefang_hatchling.eating": generate_hatch_eating(),
    "animation.flamefang_hatchling.sleep": generate_hatch_sleep(),
    "animation.flamefang_hatchling.wake_up": generate_hatch_wake_up(),
    "animation.flamefang_hatchling.roar": generate_hatch_roar()
}
'''

juv_hatch_code_new = (
    juv_hatch_code_new[:m_old_hatch_start]
    + hatch_generators + "\n\n"
    + new_hatch_chunk + "\n\n"
    + juv_hatch_code_new[m_old_hatch_end:]
)

# Also fix "loop" in export_stage_model if needed
juv_hatch_code_new = juv_hatch_code_new.replace(
    '"loop": a_val.get("loop", "loop"),',
    '"loop": "loop" if a_val.get("loop", True) else "once",'
)

with open("D:/Mine/update_juvenile_and_hatchling.py", "w", encoding="utf-8") as f:
    f.write(juv_hatch_code_new)
print("[+] update_juvenile_and_hatchling.py successfully updated with 8 animations each!")
