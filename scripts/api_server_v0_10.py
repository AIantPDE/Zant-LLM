from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json, sys, time, argparse
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from zant_llm.inference_contract_v0_10 import infer_contract, batch_infer
LOG=ROOT/'runtime_logs/v0_10/api_requests.jsonl'
LOG.parent.mkdir(parents=True, exist_ok=True)

def log(obj):
    with LOG.open('a', encoding='utf-8') as f:
        f.write(json.dumps(obj, ensure_ascii=False)+'\n')
class Handler(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        data=json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(code); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data)
    def do_GET(self):
        if self.path.startswith('/health'):
            self._send(200, {'ok':True,'branch':'v0.10-runtime-api-batch-harness','runtime_authority_granted':False,'provider_dispatch_enabled':False})
        elif self.path.startswith('/logs'):
            lines=[]
            if LOG.exists(): lines=LOG.read_text(encoding='utf-8').splitlines()[-20:]
            self._send(200, {'log_path':str(LOG),'tail':lines})
        else:
            self._send(404, {'error':'not found'})
    def do_POST(self):
        n=int(self.headers.get('Content-Length','0') or 0)
        try: body=json.loads(self.rfile.read(n).decode('utf-8') if n else '{}')
        except Exception as e: return self._send(400, {'error':'invalid json','detail':str(e)})
        if self.path.startswith('/infer'):
            res=infer_contract(body.get('text',''), body.get('raw_model_output'))
            log({'ts':time.time(),'endpoint':'/infer','request':body,'response':res})
            self._send(200, res)
        elif self.path.startswith('/batch_infer'):
            rows=body.get('rows',[])
            if not isinstance(rows,list): return self._send(400, {'error':'rows must be list'})
            res=batch_infer(rows)
            payload={'count':len(res),'results':res,'runtime_authority_granted':False,'provider_dispatch_enabled':False}
            log({'ts':time.time(),'endpoint':'/batch_infer','count':len(rows)})
            self._send(200, payload)
        else:
            self._send(404, {'error':'not found'})

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--port',type=int,default=7891); args=ap.parse_args()
    print(f'ZANT_LLM_V0_10_API_SERVER_START=True port={args.port}')
    HTTPServer(('127.0.0.1', args.port), Handler).serve_forever()
if __name__=='__main__': main()
