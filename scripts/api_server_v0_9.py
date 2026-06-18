from __future__ import annotations
import json, sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from zant_llm.inference_contract_v0_9 import infer_contract

class Handler(BaseHTTPRequestHandler):
    def _send(self, code:int, obj):
        data=json.dumps(obj,ensure_ascii=False).encode('utf-8')
        self.send_response(code); self.send_header('content-type','application/json; charset=utf-8'); self.send_header('content-length',str(len(data))); self.end_headers(); self.wfile.write(data)
    def do_GET(self):
        if self.path.startswith('/health'):
            return self._send(200, {'ok':True,'branch':'v0.9-inference-contract-stabilization','runtime_authority_granted':False,'provider_dispatch_enabled':False})
        return self._send(404, {'error':'not found'})
    def do_POST(self):
        if not self.path.startswith('/infer'):
            return self._send(404, {'error':'not found'})
        n=int(self.headers.get('content-length','0') or 0)
        obj=json.loads(self.rfile.read(n).decode('utf-8') or '{}')
        return self._send(200, infer_contract(obj.get('text',''), obj.get('model_output')))

def main():
    port=int(sys.argv[1]) if len(sys.argv)>1 else 7890
    print(f'ZANT_LLM_V0_9_API_SERVER_START=True port={port}')
    HTTPServer(('127.0.0.1', port), Handler).serve_forever()
if __name__=='__main__': main()
