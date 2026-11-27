"""Las citas de la obra propia del autor pasan a primera persona."""
OBRA = '*Derecho municipal: impugnación, veto y revisión de actos administrativos*'
C = {
 '/home/claude/libro/cap02/src/all.md': [
  ('Cortés García la recuerda como', f'En {OBRA} la recordé como'),
  ('y sostiene que su extinción', 'y sostuve que su extinción'),
  ('Cortés García describe la diarquía municipal,', 'En *Derecho municipal* describí la diarquía municipal,'),
  ('y el libro de Cortés García existe para eso:', 'y escribí aquel libro para eso:')],
 '/home/claude/libro/cap04/src/cap04.md': [
  ('Cortés García llama a esa regla', f'En {OBRA} llamé a esa regla'),
  ('y explica que "trasciende', 'y expliqué que "trasciende'),
  ('Cortés García advierte que', 'En *Derecho municipal* advertí que'),
  ('y recuerda que el poder sancionador', 'y recordé que el poder sancionador'),
  ('Cortés García explica el fundamento:', 'En *Derecho municipal* expliqué el fundamento:')]}
for f, rs in C.items():
    s = open(f, encoding='utf-8').read()
    for a, b in rs:
        if b in s: continue
        assert s.count(a) == 1, a
        s = s.replace(a, b)
    open(f, 'w', encoding='utf-8').write(s)
print('ok')
