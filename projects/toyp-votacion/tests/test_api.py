"""Self-contained checks; uses a temporary SQLite database, never real votes."""
import asyncio, os, sys, tempfile
from pathlib import Path
import httpx
from httpx import ASGITransport
with tempfile.TemporaryDirectory(prefix='toyp-api-test-') as temp:
    os.environ['TOYP_DB']=str(Path(temp)/'test.sqlite3')
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
    import app
    async def run():
        with app.db() as c:
            for uid,role in [('ADMIN','admin'),('JUR-01','juror'),('JUR-02','juror')]:
                salt='00'*16
                c.execute('INSERT INTO users(id,name,role,salt,pwhash) VALUES(?,?,?,?,?)',(uid,uid,role,salt,app.hashpw('testing-only',salt)))
        transport=ASGITransport(app=app.app)
        async with httpx.AsyncClient(transport=transport,base_url='http://test') as admin, httpx.AsyncClient(transport=transport,base_url='http://test') as jury:
            assert (await admin.get('/api/admin')).status_code==401
            assert (await admin.post('/api/login',json=[])).status_code==400
            assert (await admin.post('/api/login',content=b'x'*750001)).status_code==413
            for _ in range(5):
                assert (await jury.post('/api/login',json={'id':'JUR-01','password':'incorrect'})).status_code==401
            assert (await jury.post('/api/login',json={'id':'JUR-01','password':'testing-only'})).status_code==429
            with app.db() as c:c.execute('UPDATE attempts SET until=0')
            assert (await admin.post('/api/login',json={'id':'ADMIN','password':'testing-only'})).status_code==200
            assert (await jury.post('/api/login',json={'id':'JUR-01','password':'testing-only'})).status_code==200
            assert (await jury.get('/api/admin')).status_code==403
            assert (await jury.put('/api/scores/1',json={'score':10,'version':0})).status_code==409
            ballot={'jurorId':'JUR-02','isFinal':True,'scores':{str(i):8 for i in range(1,21)}}
            assert (await admin.post('/api/admin/import',json=ballot)).status_code==409
            for i in range(1,21):
                data={'name':f'Persona {i}','category':'Ejemplo','sections':{'valoresEtica':'Honestidad'}}
                assert (await admin.put(f'/api/admin/candidate/{i}',json=data)).status_code==200
            assert (await jury.put('/api/scores/1',json={'score':8,'version':0})).json()['version']==1
            # Retry after a lost response is idempotent; a different stale value is rejected.
            assert (await jury.put('/api/scores/1',json={'score':8,'version':0})).status_code==200
            assert (await jury.put('/api/scores/1',json={'score':10,'version':0})).status_code==409
            assert (await jury.post('/api/submit')).status_code==400
            assert (await admin.put('/api/admin/candidate/1',json={'name':'Cambio','category':'Ejemplo'})).status_code==409
            assert (await admin.post('/api/admin/import',json=ballot)).status_code==200
            assert (await admin.post('/api/admin/import',json=ballot)).status_code==409
            assert (await admin.post('/api/admin/round',headers={'Origin':'https://evil.example'},json={'ids':[1,2]})).status_code==403
            with app.db() as c: assert c.execute('SELECT count(*) FROM audit').fetchone()[0]==1
        print('OK: accesos, preparación, concurrencia, bloqueo, importación y origen.')
    asyncio.run(run())
