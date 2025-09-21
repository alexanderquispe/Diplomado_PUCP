# -*- coding: utf-8 -*-
"""
api_reddit.py — PRAW (password login)

Uso (Parte 1 - lo que ya tenías):
  # Solo posts
  python code/api_reddit.py --subreddit peru --query "economia" --limit 20

  # Posts + comentarios (hasta N por post)
  python code/api_reddit.py --subreddit peru --query "economia" --limit 20 --comments --max_comments 10

Salidas Parte 1:
  ./salida/reddit_posts.csv
  ./salida/reddit_comments.csv  (si usas --comments)


----------------------------------------------------------------------
NUEVO: Parte 2 (batch para varios subreddits, 20 “top” por subreddit y 5 comentarios)

Ejemplo pedido por la consigna:
  python code/api_reddit.py ^
    --batch_subs politics,PoliticalDiscussion,worldnews ^
    --batch_mode top ^
    --batch_limit 20 ^
    --batch_max_comments 5

Salidas Parte 2 (por subreddit):
  ./salida/<subreddit>_posts.csv
  ./salida/<subreddit>_comments.csv
----------------------------------------------------------------------
"""
import os
import argparse
import pandas as pd
from dotenv import load_dotenv
import praw
from praw.models import MoreComments
from prawcore.exceptions import ResponseException, RequestException, Forbidden


# --------------------------- Login --------------------------- #
def make_client():
    """
    Crea el cliente PRAW usando credenciales del .env (login por contraseña).
    Requiere app de tipo 'script' en https://old.reddit.com/prefs/apps
    """
    load_dotenv()

    cid = os.getenv("REDDIT_CLIENT_ID")
    csec = os.getenv("REDDIT_CLIENT_SECRET")
    uag = os.getenv(
        "REDDIT_USER_AGENT",
        "python:webscrappingProject:v1.0 (by /u/CranberryEqual8083)"
    )
    user = os.getenv("REDDIT_USERNAME")
    pwd = os.getenv("REDDIT_PASSWORD")

    missing = [k for k, v in {
        "REDDIT_CLIENT_ID": cid,
        "REDDIT_CLIENT_SECRET": csec,
        "REDDIT_USER_AGENT": uag,
        "REDDIT_USERNAME": user,
        "REDDIT_PASSWORD": pwd,
    }.items() if not v]
    if missing:
        raise RuntimeError("Faltan variables en .env: " + ", ".join(missing))

    # Login con password (solo funciona si la app es 'script')
    reddit = praw.Reddit(
        client_id=cid,
        client_secret=csec,
        user_agent=uag,
        username=user,
        password=pwd,
    )

    return reddit


# --------------------------- Data (Parte 1) --------------------------- #
def fetch_posts(reddit, subreddit: str, query: str | None, limit: int) -> pd.DataFrame:
    """
    Devuelve posts de un subreddit (por búsqueda o recientes).
    """
    sub = reddit.subreddit(subreddit)

    try:
        submissions = sub.search(query, limit=limit) if query else sub.new(limit=limit)
    except (ResponseException, RequestException, Forbidden) as e:
        raise RuntimeError(f"No se pudo leer el subreddit r/{subreddit}: {e}")

    rows = []
    for s in submissions:
        rows.append({
            "id": s.id,
            "title": s.title,
            "author": getattr(s.author, "name", None),
            "score": s.score,
            "num_comments": s.num_comments,
            "url": s.url,
            "created_utc": s.created_utc,
            "permalink": f"https://www.reddit.com{s.permalink}",
            "subreddit": str(s.subreddit),
        })

    df = pd.DataFrame(rows)
    if not df.empty:
        df["created_dt"] = pd.to_datetime(df["created_utc"], unit="s")
    return df


def fetch_comments(reddit, post_ids: list[str], max_comments: int) -> pd.DataFrame:
    """
    Devuelve hasta max_comments comentarios por post de la lista.
    """
    out = []
    for pid in post_ids:
        try:
            s = reddit.submission(id=pid)
            s.comments.replace_more(limit=0)
        except (ResponseException, RequestException, Forbidden) as e:
            # Continuar con el siguiente post si este falla
            print(f"⚠️  No se pudieron leer comentarios de {pid}: {e}")
            continue

        count = 0
        for c in s.comments.list():
            if isinstance(c, MoreComments):
                continue
            out.append({
                "post_id": pid,
                "comment_id": c.id,
                "author": getattr(c.author, "name", None),
                "score": c.score,
                "body": c.body,
                "created_utc": c.created_utc,
                "permalink": f"https://www.reddit.com{c.permalink}",
            })
            count += 1
            if count >= max_comments:
                break

    cdf = pd.DataFrame(out)
    if not cdf.empty:
        cdf["created_dt"] = pd.to_datetime(cdf["created_utc"], unit="s")
    return cdf


# --------------------------- Data (Parte 2) --------------------------- #
def fetch_posts_top_hot(reddit, subreddit: str, mode: str, limit: int) -> pd.DataFrame:
    """
    Devuelve posts 'top' (por año) o 'hot' de un subreddit.
    Campos: id, title, score, num_comments, url, permalink, created_utc, subreddit.
    """
    sr = reddit.subreddit(subreddit)
    try:
        if mode == "top":
            subs = sr.top(limit=limit, time_filter="year")
        else:
            subs = sr.hot(limit=limit)
    except (ResponseException, RequestException, Forbidden) as e:
        raise RuntimeError(f"No se pudo leer r/{subreddit} ({mode}): {e}")

    rows = []
    for s in subs:
        rows.append({
            "id": s.id,
            "title": s.title,
            "score": int(getattr(s, "score", 0)),
            "num_comments": int(getattr(s, "num_comments", 0)),
            "url": s.url,
            "permalink": f"https://www.reddit.com{s.permalink}",
            "created_utc": int(getattr(s, "created_utc", 0)),
            "subreddit": str(s.subreddit),
        })
    df = pd.DataFrame(rows)
    if not df.empty:
        df["created_dt"] = pd.to_datetime(df["created_utc"], unit="s")
    return df


# --------------------------- CLI --------------------------- #
def main():
    ap = argparse.ArgumentParser()

    # ====== MODO PARTE 1 (ya existente) ======
    ap.add_argument("--subreddit", help="Nombre del subreddit (sin r/)")
    ap.add_argument("--query", help="Texto de búsqueda (usa comillas si tiene espacios)")
    ap.add_argument("--limit", type=int, default=50, help="Número de posts a leer")
    ap.add_argument("--comments", action="store_true", help="Si se indica, también descarga comentarios")
    ap.add_argument("--max_comments", type=int, default=20, help="Máx. comentarios por post")
    ap.add_argument("--out_posts", default="./salida/reddit_posts.csv")
    ap.add_argument("--out_comments", default="./salida/reddit_comments.csv")

    # ====== NUEVO: MODO PARTE 2 (batch) ======
    ap.add_argument("--batch_subs",
                    help="Lista de subreddits separados por coma (ej: politics,PoliticalDiscussion,worldnews)")
    ap.add_argument("--batch_mode", choices=["top", "hot"], default="top",
                    help="Fuente de posts para batch: top (default) o hot")
    ap.add_argument("--batch_limit", type=int, default=20,
                    help="N° de posts por subreddit en batch (default 20)")
    ap.add_argument("--batch_max_comments", type=int, default=5,
                    help="N° de comentarios por post en batch (default 5)")

    args = ap.parse_args()

    # carpeta de salida (Parte 1; en Parte 2 se crean por archivo)
    if args.out_posts:
        os.makedirs(os.path.dirname(args.out_posts), exist_ok=True)

    # crear cliente
    try:
        reddit = make_client()
        me = reddit.user.me()
        print(f"✅ Autenticado como: {me}")
    except ResponseException as e:
        print(f"❌ Error de autenticación: {e}")
        return
    except Exception as e:
        print(f"❌ Error creando cliente: {e}")
        return

    # =========================
    # MODO PARTE 2 (batch)
    # =========================
    if args.batch_subs:
        subs = [s.strip() for s in args.batch_subs.split(",") if s.strip()]
        if not subs:
            print("⚠️  No se especificaron subreddits en --batch_subs.")
            return

        for sr in subs:
            print(f"\n🔹 r/{sr} | modo: {args.batch_mode} | posts: {args.batch_limit}")
            try:
                posts_df = fetch_posts_top_hot(reddit, sr, args.batch_mode, args.batch_limit)
            except Exception as e:
                print(f"❌ Error leyendo r/{sr}: {e}")
                continue

            out_posts = f"./salida/{sr}_posts.csv"
            if posts_df.empty:
                print(f"⚠️  r/{sr}: sin posts.")
            else:
                posts_df.to_csv(out_posts, index=False, encoding="utf-8-sig")
                print(f"✅ Posts guardados en: {out_posts}  ({len(posts_df)} filas)")

            # Comentarios
            if not posts_df.empty:
                post_ids = posts_df["id"].tolist()
                comments_df = fetch_comments(reddit, post_ids, args.batch_max_comments)
                out_comments = f"./salida/{sr}_comments.csv"
                if comments_df.empty:
                    print(f"⚠️  r/{sr}: sin comentarios.")
                else:
                    comments_df.to_csv(out_comments, index=False, encoding="utf-8-sig")
                    print(f"✅ Comentarios guardados en: {out_comments}  ({len(comments_df)} filas)")
        return

    # =========================
    # MODO PARTE 1 (original)
    # =========================
    if not args.subreddit:
        print("❗ Debes indicar --subreddit (o usar --batch_subs para el modo Parte 2).")
        return

    # posts
    try:
        posts = fetch_posts(reddit, args.subreddit, args.query, args.limit)
    except Exception as e:
        print(f"❌ Error al leer subreddit r/{args.subreddit}: {e}")
        return

    if posts.empty:
        print("⚠️  No se obtuvieron posts (resultado vacío).")
    else:
        posts.to_csv(args.out_posts, index=False, encoding="utf-8-sig")
        print(f"✅ Posts guardados en: {args.out_posts}  ({len(posts)} filas)")

    # comentarios (opcional)
    if args.comments and not posts.empty:
        comments = fetch_comments(reddit, posts["id"].tolist(), args.max_comments)
        if comments.empty:
            print("⚠️  No se obtuvieron comentarios.")
        else:
            comments.to_csv(args.out_comments, index=False, encoding="utf-8-sig")
            print(f"✅ Comentarios guardados en: {args.out_comments}  ({len(comments)} filas)")


if __name__ == "__main__":
    main()
