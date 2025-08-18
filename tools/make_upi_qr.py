import sys, qrcode
from pathlib import Path
def make(pa,pn,tn,am=None,out="upi_qr.png"):
    uri=f"upi://pay?pa={pa}&pn={pn}&tn={tn}&cu=INR"; 
    if am: uri+=f"&am={am}"
    img=qrcode.make(uri); Path("uploads").mkdir(exist_ok=True, parents=True); 
    out=Path("uploads")/out; img.save(out); print("Created", out)
if __name__=="__main__":
    if len(sys.argv)<4: print("Usage: python tools/make_upi_qr.py <pa> <pn(url-encoded)> <tn(url-encoded)> [amount] [out]"); raise SystemExit(1)
    pa, pn, tn = sys.argv[1:4]; am = sys.argv[4] if len(sys.argv)>=5 else None; out = sys.argv[5] if len(sys.argv)>=6 else "upi_qr.png"
    make(pa,pn,tn,am,out)
