from pathlib import Path
p=Path('.codex-tmp/math-20261120/write_outputs_part.py');t=p.read_text(encoding='utf-8-sig')
t=t.replace('具体题干以文字转录为准，原图可点开核对；若发现转录符号与图不同，以图为准并修正对应卡，不把OCR当数学依据。', '题干已转为文字，原图仍是核对依据；若文字与图有出入，先以图核实并修正对应卡，不把OCR当数学依据。')
t=t.replace("first_round':FIRST", "first_round':FIRST")
p.write_text(t,encoding='utf-8')
# Correct a source-line wording issue without changing mathematical content.
p=Path('2.知识库/20.North_star_ZJU/201.数学/04真题阶段/02数学做题框架/05级数.md');t=p.read_text(encoding='utf-8')
t=t.replace('如 $\\sum a_nx^{2n}$', '如 $\\sum a_nx^{2n}$')
p.write_text(t,encoding='utf-8')
