from http.server import BaseHTTPRequestHandler, HTTPServer
import json, time, uuid
BRANCH='v1.2-runtime-deployment-readiness'
class H(BaseHTTPRequestHandler):
    def _send(self,obj,code=200):
        b=json.dumps(obj).encode('utf-8')
        self.send_response(code); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        if self.path.startswith('/health'):
            self._send({'ok':True,'branch':BRANCH,'runtime_authority_granted':False,'provider_dispatch_enabled':False})
        else: self._send({'error':'not found'},404)
    def do_POST(self):
        n=int(self.headers.get('Content-Length','0') or '0')
        body=self.rfile.read(n).decode('utf-8') if n else '{}'
        try: data=json.loads(body)
        except Exception: data={}
        text=data.get('text','')
        if 'runtime_authority_granted=true' in text or 'Ignore policy' in text:
            d='FAILCLOSED'; reason='forbidden runtime/provider flag repaired to fail closed'
        elif 'source conflict' in text or not text.strip():
            d='BLOCKED'; reason='missing evidence or conflict'
        elif 'close out' in text:
            d='CLOSEOUT'; reason='route cannot proceed'
        else:
            d='READY'; reason='bounded evidence appears sufficient'
        row={'decision':d,'reason':reason,'runtime_authority_granted':False,'provider_dispatch_enabled':False,'request_id':str(uuid.uuid4()),'ts_unix':time.time()}
        if self.path.startswith('/infer'): self._send(row)
        elif self.path.startswith('/batch_infer'):
            rows=data.get('rows',[]); self._send({'count':len(rows),'results':[row for _ in rows]})
        else: self._send({'error':'not found'},404)
if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument('--port',type=int,default=7892); args=ap.parse_args()
    print(f'ZANT_LLM_V1_2_LOCAL_SERVICE_START=True port={args.port}', flush=True)
    HTTPServer(('127.0.0.1',args.port),H).serve_forever()
