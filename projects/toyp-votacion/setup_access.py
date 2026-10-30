import os,secrets,argparse
from pathlib import Path
from app import db,hashpw
parser=argparse.ArgumentParser();parser.add_argument('--output',required=True,help='Archivo privado nuevo donde guardar las credenciales');args=parser.parse_args()
with db() as c:
    if c.execute('SELECT count(*) FROM users').fetchone()[0]: raise SystemExit('Ya existen cuentas; no se sobrescriben.')
    lines=[]
    for i in range(11):
        uid='ADMIN' if i==0 else f'JUR-{i:02d}';name='Administración' if i==0 else f'Jurado {i:02d}';role='admin' if i==0 else 'juror';pw=secrets.token_urlsafe(18);salt=secrets.token_hex(16);c.execute('INSERT INTO users(id,name,role,salt,pwhash) VALUES(?,?,?,?,?)',(uid,name,role,salt,hashpw(pw,salt)));lines.append(f'{uid}\t{pw}')
    fd=os.open(args.output,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,'w') as f:f.write('\n'.join(lines)+'\n')
print('Cuentas creadas. Credenciales guardadas en el archivo privado indicado.')
