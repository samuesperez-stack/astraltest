"""Only prepare disposable local fixtures; never run on a real event database."""
import os,sys
from pathlib import Path
p=Path(os.environ.get('TOYP_DB','')).resolve()
if os.environ.get('TOYP_TEST_ONLY')!='YES' or p.parent!=Path('/tmp') or not p.name.startswith('toyp-test-'):
    raise SystemExit('Usa una base temporal /tmp/toyp-test-*.sqlite3 y TOYP_TEST_ONLY=YES')
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import app
names=['Logros culturales y artísticos','Desarrollo científico y tecnológico','Servicio humanitario y voluntariado','Logros empresariales y económicos']
with app.db() as c:
    if c.execute('SELECT count(*) FROM scores').fetchone()[0]:raise SystemExit('La base de prueba ya contiene calificaciones')
    for i in range(1,21):
        category='LOGROS CULTURALES Y ARTISTICOS' if i==5 else names[(i-1)//5]
        c.execute('UPDATE candidates SET ready=1, category=?, bio=? WHERE id=?',(category,'Trayectoria de ejemplo para la vista de prueba.',i))
print('20 fichas de ejemplo listas en cuatro categorías de prueba.')
