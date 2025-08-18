import typer
from godai.affiliate import ensure_amazon_in
app = typer.Typer(add_completion=False)
@app.command()
def link(url: str):
    print(ensure_amazon_in(url))
if __name__ == "__main__":
    app()
