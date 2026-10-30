import os, sqlite3, secrets, hashlib, hmac, json, csv, io, time
from contextlib import contextmanager
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from desempate import clasificar

ROOT=Path(__file__).parent
DB=Path(os.environ.get('TOYP_DB',str(ROOT/'data'/'votacion.sqlite3')))
app=FastAPI(docs_url=None,redoc_url=None,openapi_url=None)
app.mount('/static',StaticFiles(directory=ROOT/'static'),name='static')
@contextmanager
def db():
    DB.parent.mkdir(parents=True,exist_ok=True)
    c=sqlite3.connect(DB,timeout=15);c.row_factory=sqlite3.Row;c.execute('PRAGMA foreign_keys=ON')
    try: yield c; c.commit()
    except Exception: c.rollback(); raise
    finally: c.close()
def hashpw(password,salt): return hashlib.pbkdf2_hmac('sha256',password.encode(),bytes.fromhex(salt),310000).hex()
def setup():
    with db() as c:
        c.executescript('''CREATE TABLE IF NOT EXISTS users(id TEXT PRIMARY KEY,name TEXT NOT NULL,role TEXT NOT NULL,salt TEXT NOT NULL,pwhash TEXT NOT NULL,locked INTEGER NOT NULL DEFAULT 0);CREATE TABLE IF NOT EXISTS sessions(token TEXT PRIMARY KEY,user_id TEXT NOT NULL REFERENCES users(id),expires INTEGER NOT NULL);CREATE TABLE IF NOT EXISTS candidates(id INTEGER PRIMARY KEY,name TEXT NOT NULL,category TEXT NOT NULL,bio TEXT NOT NULL DEFAULT '',photo TEXT NOT NULL DEFAULT '');CREATE TABLE IF NOT EXISTS scores(user_id TEXT NOT NULL REFERENCES users(id),candidate_id INTEGER NOT NULL REFERENCES candidates(id),score INTEGER NOT NULL CHECK(score BETWEEN 1 AND 10),PRIMARY KEY(user_id,candidate_id));CREATE TABLE IF NOT EXISTS rounds(id INTEGER PRIMARY KEY AUTOINCREMENT,created INTEGER NOT NULL,status TEXT NOT NULL DEFAULT 'open');CREATE TABLE IF NOT EXISTS round_candidates(round_id INTEGER NOT NULL REFERENCES rounds(id),candidate_id INTEGER NOT NULL REFERENCES candidates(id),PRIMARY KEY(round_id,candidate_id));CREATE TABLE IF NOT EXISTS round_votes(round_id INTEGER NOT NULL REFERENCES rounds(id),user_id TEXT NOT NULL REFERENCES users(id),candidate_id INTEGER NOT NULL REFERENCES candidates(id),PRIMARY KEY(round_id,user_id));CREATE TABLE IF NOT EXISTS attempts(key TEXT PRIMARY KEY,count INTEGER NOT NULL,until INTEGER NOT NULL);''')
        if c.execute('SELECT count(*) FROM candidates').fetchone()[0]==0:
            c.executemany('INSERT INTO candidates(id,name,category) VALUES(?,?,?)',[(i,f'Postulado {i:02d}','Categoría pendiente') for i in range(1,21)])
setup()
with db() as c:
    if 'sections' not in [r[1] for r in c.execute('PRAGMA table_info(candidates)')]: c.execute("ALTER TABLE candidates ADD COLUMN sections TEXT NOT NULL DEFAULT '{}'")
    if 'version' not in [r[1] for r in c.execute('PRAGMA table_info(scores)')]: c.execute('ALTER TABLE scores ADD COLUMN version INTEGER NOT NULL DEFAULT 1')
    if 'ready' not in [r[1] for r in c.execute('PRAGMA table_info(candidates)')]:
        c.execute('ALTER TABLE candidates ADD COLUMN ready INTEGER NOT NULL DEFAULT 0')
        c.execute("UPDATE candidates SET ready=1 WHERE name NOT LIKE 'Postulado %' AND category!='Categoría pendiente'")
def user(req,role=None):
    token=req.cookies.get('toyp_session',''); hashed=hashlib.sha256(token.encode()).hexdigest()
    with db() as c: row=c.execute('SELECT u.* FROM sessions s JOIN users u ON u.id=s.user_id WHERE s.token=? AND s.expires>?',(hashed,int(time.time()))).fetchone()
    if not row: raise HTTPException(401,'Inicia sesión')
    if role and row['role']!=role: raise HTTPException(403,'Acceso restringido')
    return dict(row)
@app.middleware('http')
async def safety(req,call_next):
    if req.method in ('POST','PUT','DELETE'):
        origin=req.headers.get('origin'); host=req.headers.get('host')
        if origin and origin not in ('http://'+host,'https://'+host): return __import__('starlette.responses',fromlist=['JSONResponse']).JSONResponse({'detail':'Origen no permitido'},status_code=403)
    res=await call_next(req);res.headers['Cache-Control']='no-store';res.headers['X-Content-Type-Options']='nosniff';res.headers['X-Frame-Options']='DENY';res.headers['Content-Security-Policy']="default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self'; img-src 'self' data:; frame-ancestors 'none'";return res
async def read_object(req):
    raw=await req.body()
    if len(raw)>750000:raise HTTPException(413,'El contenido es demasiado grande')
    try: data=json.loads(raw)
    except (ValueError,UnicodeDecodeError):raise HTTPException(400,'JSON inválido')
    if not isinstance(data,dict):raise HTTPException(400,'El contenido debe ser un objeto')
    return data
@app.get('/')
def home(): return FileResponse(ROOT/'static'/'index.html')
@app.post('/api/login')
async def login(req:Request):
    data=await read_object(req); uid=str(data.get('id','')).strip().upper(); password=str(data.get('password','')); key=hashlib.sha256((req.client.host+':'+uid).encode()).hexdigest();now=int(time.time())
    with db() as c:
        attempt=c.execute('SELECT * FROM attempts WHERE key=?',(key,)).fetchone()
        if attempt and attempt['until']>now and attempt['count']>=5: raise HTTPException(429,'Demasiados intentos. Intenta en 15 minutos.')
        u=c.execute('SELECT * FROM users WHERE id=?',(uid,)).fetchone()
        if not u or not hmac.compare_digest(hashpw(password,u['salt']),u['pwhash']):
            count=(attempt['count'] if attempt and attempt['until']>now else 0)+1
            c.execute('INSERT OR REPLACE INTO attempts VALUES(?,?,?)',(key,count,now+900));c.commit();raise HTTPException(401,'Credenciales incorrectas')
        c.execute('DELETE FROM attempts WHERE key=?',(key,)); token=secrets.token_urlsafe(32); c.execute('INSERT INTO sessions VALUES(?,?,?)',(hashlib.sha256(token.encode()).hexdigest(),uid,now+28800))
    from fastapi.responses import JSONResponse
    res=JSONResponse({'ok':True});res.set_cookie('toyp_session',token,httponly=True,samesite='strict',secure=os.environ.get('TOYP_HTTPS')=='1',max_age=28800,path='/');return res
@app.post('/api/logout')
def logout(req:Request):
    with db() as c:c.execute('DELETE FROM sessions WHERE token=?',(hashlib.sha256(req.cookies.get('toyp_session','').encode()).hexdigest(),))
    from fastapi.responses import JSONResponse
    r=JSONResponse({'ok':True});r.delete_cookie('toyp_session');return r
@app.get('/api/me')
def me(req:Request):
    u=user(req)
    with db() as c:
        candidates=[dict(x) for x in c.execute('SELECT * FROM candidates ORDER BY id')];scores={str(x['candidate_id']):x['score'] for x in c.execute('SELECT candidate_id,score,version FROM scores WHERE user_id=?',(u['id'],))};versions={str(x['candidate_id']):x['version'] for x in c.execute('SELECT candidate_id,version FROM scores WHERE user_id=?',(u['id'],))};rounds=[]
        for r in c.execute("SELECT * FROM rounds WHERE status='open'").fetchall():
            choices=[dict(x) for x in c.execute('SELECT c.id,c.name FROM round_candidates rc JOIN candidates c ON c.id=rc.candidate_id WHERE rc.round_id=?',(r['id'],))];v=c.execute('SELECT candidate_id FROM round_votes WHERE round_id=? AND user_id=?',(r['id'],u['id'])).fetchone();rounds.append({'id':r['id'],'choices':choices,'vote':v[0] if v else None})
    return {'id':u['id'],'name':u['name'],'role':u['role'],'locked':bool(u['locked']),'candidates':candidates,'scores':scores,'versions':versions,'evaluation_ready':len(candidates)==20 and all(x['ready'] for x in candidates),'rounds':rounds}
@app.put('/api/scores/{candidate_id}')
async def score(candidate_id:int,req:Request):
    u=user(req,'juror');d=await read_object(req);value=d.get('score');version=d.get('version')
    if type(value)!=int or not 1<=value<=10 or type(version)!=int or version<0:raise HTTPException(400,'Calificación o versión inválida')
    with db() as c:
        c.execute('BEGIN IMMEDIATE');state=c.execute('SELECT locked FROM users WHERE id=?',(u['id'],)).fetchone()
        if state[0]:raise HTTPException(409,'Tu evaluación ya fue enviada')
        if c.execute('SELECT count(*) FROM candidates WHERE ready=1').fetchone()[0]!=20:raise HTTPException(409,'La organización aún está preparando los perfiles')
        if not c.execute('SELECT 1 FROM candidates WHERE id=?',(candidate_id,)).fetchone():raise HTTPException(404,'Postulado no encontrado')
        existing=c.execute('SELECT score,version FROM scores WHERE user_id=? AND candidate_id=?',(u['id'],candidate_id)).fetchone()
        current=existing['version'] if existing else 0
        if current!=version:
            if existing and existing['score']==value and current==version+1:return {'ok':True,'version':current}
            raise HTTPException(409,'Esta calificación cambió en otro dispositivo. Tu borrador local no se sobrescribió; contacta a la organización.')
        next_version=current+1
        c.execute('INSERT INTO scores(user_id,candidate_id,score,version) VALUES(?,?,?,?) ON CONFLICT(user_id,candidate_id) DO UPDATE SET score=excluded.score,version=excluded.version',(u['id'],candidate_id,value,next_version))
    return {'ok':True,'version':next_version}
@app.post('/api/submit')
def submit(req:Request):
    u=user(req,'juror')
    with db() as c:
        c.execute('BEGIN IMMEDIATE'); state=c.execute('SELECT locked FROM users WHERE id=?',(u['id'],)).fetchone()[0]
        if state:raise HTTPException(409,'Tu evaluación ya fue enviada')
        if c.execute('SELECT count(*) FROM candidates WHERE ready=1').fetchone()[0]!=20:raise HTTPException(409,'La organización aún está preparando los perfiles')
        if c.execute('SELECT count(*) FROM scores WHERE user_id=?',(u['id'],)).fetchone()[0]!=c.execute('SELECT count(*) FROM candidates').fetchone()[0]:raise HTTPException(400,'Califica a todos los postulados antes de enviar')
        c.execute('UPDATE users SET locked=1 WHERE id=?',(u['id'],))
    return {'ok':True}
def report(c):
    candidates=[dict(x) for x in c.execute('SELECT * FROM candidates ORDER BY id')];jurors=[dict(x) for x in c.execute("SELECT id,name,locked FROM users WHERE role='juror' ORDER BY id")];rows=c.execute('SELECT s.* FROM scores s JOIN users u ON u.id=s.user_id WHERE u.locked=1').fetchall();scores={str(x['id']):{} for x in candidates}
    for r in rows:scores[str(r['candidate_id'])][r['user_id']]=r['score']
    eligible={str(k):list(v.values()) for k,v in scores.items() if v}; groups=clasificar(eligible) if eligible else []
    # A completed second ballot refines only its tied group. Equal counts remain tied.
    for rnd in c.execute("SELECT id FROM rounds WHERE status='closed' ORDER BY id").fetchall():
        rows=c.execute('SELECT rc.candidate_id,COUNT(v.user_id) votes FROM round_candidates rc LEFT JOIN round_votes v ON v.round_id=rc.round_id AND v.candidate_id=rc.candidate_id WHERE rc.round_id=? GROUP BY rc.candidate_id',(rnd['id'],)).fetchall()
        ids={str(r['candidate_id']) for r in rows}
        for i,group in enumerate(groups):
            if set(group)==ids:
                counts=sorted({r['votes'] for r in rows},reverse=True)
                groups[i:i+1]=[[str(r['candidate_id']) for r in rows if r['votes']==count] for count in counts]
                break
    return {'candidates':candidates,'jurors':jurors,'scores':scores,'groups':groups,'started':bool(c.execute('SELECT 1 FROM scores LIMIT 1').fetchone()),'complete':len(jurors)==10 and all(x['locked'] for x in jurors)}
@app.get('/api/admin')
def admin(req:Request):
    user(req,'admin')
    with db() as c:
        result=report(c);result['rounds']=[]
        for r in c.execute('SELECT * FROM rounds ORDER BY id DESC').fetchall():
            choices=[dict(x) for x in c.execute('SELECT c.id,c.name,COUNT(v.user_id) votes FROM round_candidates rc JOIN candidates c ON c.id=rc.candidate_id LEFT JOIN round_votes v ON v.round_id=rc.round_id AND v.candidate_id=rc.candidate_id WHERE rc.round_id=? GROUP BY c.id ORDER BY votes DESC,c.id',(r['id'],))];result['rounds'].append({'id':r['id'],'status':r['status'],'choices':choices})
        return result
@app.post('/api/admin/round')
async def create_round(req:Request):
    user(req,'admin');data=await read_object(req);ids=data.get('ids')
    if not isinstance(ids,list) or len(ids)<2 or any(type(x)!=int for x in ids) or len(set(ids))!=len(ids):raise HTTPException(400,'Selección inválida')
    with db() as c:
        c.execute('BEGIN IMMEDIATE');r=report(c)
        if not r['complete']:raise HTTPException(400,'Espera el envío final de los 10 jurados')
        if set(map(str,ids)) not in [set(g) for g in r['groups'] if len(g)>1]:raise HTTPException(400,'Selecciona un grupo empatado completo')
        if c.execute("SELECT 1 FROM rounds WHERE status='open'").fetchone():raise HTTPException(409,'Ya hay una segunda votación abierta')
        rid=c.execute('INSERT INTO rounds(created) VALUES(?)',(int(time.time()),)).lastrowid;c.executemany('INSERT INTO round_candidates VALUES(?,?)',[(rid,x) for x in ids])
    return {'ok':True}
@app.post('/api/round/{rid}/vote')
async def round_vote(rid:int,req:Request):
    u=user(req,'juror');cid=(await read_object(req)).get('candidate_id')
    if type(cid)!=int:raise HTTPException(400,'Selección inválida')
    with db() as c:
        c.execute('BEGIN IMMEDIATE')
        if not c.execute("SELECT 1 FROM rounds WHERE id=? AND status='open'",(rid,)).fetchone() or not c.execute('SELECT 1 FROM round_candidates WHERE round_id=? AND candidate_id=?',(rid,cid)).fetchone():raise HTTPException(400,'Votación o candidato inválido')
        try:c.execute('INSERT INTO round_votes VALUES(?,?,?)',(rid,u['id'],cid))
        except sqlite3.IntegrityError:raise HTTPException(409,'Ya participaste en esta segunda votación')
    return {'ok':True}
@app.post('/api/admin/round/{rid}/close')
def close_round(rid:int,req:Request):
    user(req,'admin')
    with db() as c:
        c.execute('BEGIN IMMEDIATE')
        if c.execute('SELECT count(*) FROM round_votes WHERE round_id=?',(rid,)).fetchone()[0]!=10:raise HTTPException(400,'Faltan votos de jurados')
        if not c.execute("UPDATE rounds SET status='closed' WHERE id=? AND status='open'",(rid,)).rowcount:raise HTTPException(404,'Votación no encontrada')
    return {'ok':True}
@app.get('/api/admin/export')
def export(req:Request):
    user(req,'admin')
    with db() as c:r=report(c)
    out=io.StringIO();w=csv.writer(out);w.writerow(['Postulado','Categoría',*[j['id'] for j in r['jurors']],'Total'])
    for x in r['candidates']:
        vals=r['scores'][str(x['id'])];safe=lambda s: "'"+s if s and (s[0] in '=+-@\t\r' or s.lstrip().startswith(('=','+','-','@'))) else s
        w.writerow([safe(x['name']),safe(x['category']),*[vals.get(j['id'],'') for j in r['jurors']],sum(vals.values())])
    return StreamingResponse(iter(['\ufeff'+out.getvalue()]),media_type='text/csv',headers={'Content-Disposition':'attachment; filename="toyp-resultados.csv"'})
@app.put('/api/admin/candidate/{cid}')
async def edit_candidate(cid:int,req:Request):
    user(req,'admin');d=await read_object(req);name=str(d.get('name','')).strip();category=str(d.get('category','')).strip();bio=str(d.get('bio','')).strip(); sections=d.get('sections',{}); photo=d.get('photo','')
    if not name or not category or max(len(name),len(category))>120 or len(bio)>3000:raise HTTPException(400,'Revisa los datos del perfil')
    allowed={'titulosCertificaciones','resumenCarrera','logrosSignificativos','liderazgoImpacto','valoresEtica'}
    if not isinstance(sections,dict) or set(sections)-allowed or any(not isinstance(v,str) or len(v)>3000 for v in sections.values()):raise HTTPException(400,'Secciones inválidas')
    if not isinstance(photo,str) or len(photo)>500000:raise HTTPException(400,'Imagen demasiado grande')
    if photo:
        import base64,binascii
        try:
            head,raw=photo.split(',',1); img=base64.b64decode(raw,validate=True)
            if not ((head=='data:image/jpeg;base64' and img.startswith(b'\xff\xd8\xff')) or (head=='data:image/png;base64' and img.startswith(b'\x89PNG\r\n\x1a\n'))):raise ValueError()
        except (ValueError,binascii.Error):raise HTTPException(400,'La foto debe ser JPEG o PNG')
    with db() as c:
        c.execute('BEGIN IMMEDIATE')
        if c.execute('SELECT count(*) FROM scores').fetchone()[0]:raise HTTPException(409,'Los perfiles quedan bloqueados cuando inicia la evaluación')
        if not c.execute('UPDATE candidates SET name=?,category=?,bio=?,sections=?,photo=?,ready=1 WHERE id=?',(name,category,bio,json.dumps(sections,ensure_ascii=False),photo,cid)).rowcount:raise HTTPException(404,'Postulado no encontrado')
    return {'ok':True}
@app.post('/api/admin/import')
async def import_ballot(req:Request):
    admin_user=user(req,'admin');data=await read_object(req)
    if not isinstance(data,dict):raise HTTPException(400,'Archivo inválido')
    uid=str(data.get('jurorId','')).strip().upper();scores=data.get('scores');final=data.get('isFinal')
    if final is not True or not isinstance(scores,dict):raise HTTPException(400,'El archivo debe contener una evaluación final.')
    with db() as c:
        c.execute('BEGIN IMMEDIATE')
        if c.execute('SELECT count(*) FROM candidates WHERE ready=1').fetchone()[0]!=20:raise HTTPException(409,'La organización aún está preparando los perfiles')
        juror=c.execute("SELECT locked FROM users WHERE id=? AND role='juror'",(uid,)).fetchone()
        if not juror:raise HTTPException(400,'Jurado no reconocido')
        if juror[0]:raise HTTPException(409,'Este jurado ya tiene una evaluación final')
        ids={str(r[0]) for r in c.execute('SELECT id FROM candidates')}
        if set(scores)!=ids or any(type(v)!=int or not 1<=v<=10 for v in scores.values()):raise HTTPException(400,'El archivo debe contener las 20 calificaciones válidas')
        c.executemany('INSERT INTO scores(user_id,candidate_id,score,version) VALUES(?,?,?,1) ON CONFLICT(user_id,candidate_id) DO UPDATE SET score=excluded.score,version=scores.version+1',[(uid,int(cid),v) for cid,v in scores.items()])
        c.execute('UPDATE users SET locked=1 WHERE id=?',(uid,))
        c.execute('CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY,actor TEXT NOT NULL,action TEXT NOT NULL,target TEXT NOT NULL,created INTEGER NOT NULL)')
        c.execute('INSERT INTO audit(actor,action,target,created) VALUES(?,?,?,?)',(admin_user['id'],'import_final',uid,int(time.time())))
    return {'ok':True}
