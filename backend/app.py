import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from models import db, Article
from news_client import fetch_top_headlines
from datetime import datetime
from sqlalchemy.exc import IntegrityError

# Load .env for local/dev
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Database configuration
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASS = os.getenv("DB_PASS", "password")
    DB_HOST = os.getenv("DB_HOST", "mysql")
    DB_NAME = os.getenv("DB_NAME", "newsdb")

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Health check endpoint for K8s probes
    @app.route("/healthz")
    def health():
        return jsonify({"status": "ok"})

    # Proxy NewsAPI and optionally cache in DB
    @app.route("/api/news", methods=["GET"])
    def get_news():
        country = request.args.get("country")
        category = request.args.get("category")
        q = request.args.get("q")

        try:
            data = fetch_top_headlines(country=country, category=category, q=q)
            articles = data.get("articles", [])
            for a in articles:
                try:
                    art = Article(
                        source=a.get("source", {}).get("name"),
                        author=a.get("author"),
                        title=a.get("title"),
                        description=a.get("description"),
                        url=a.get("url"),
                        urlToImage=a.get("urlToImage"),
                        publishedAt=datetime.fromisoformat(
                            a.get("publishedAt").replace("Z", "+00:00")
                        ) if a.get("publishedAt") else None
                    )
                    db.session.add(art)
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()
            return jsonify(data)
        except Exception as e:
            # Fallback: return cached data if API fails
            cached_articles = Article.query.order_by(Article.cachedAt.desc()).limit(20).all()
            return jsonify({
                "status": "cached",
                "articles": [a.to_dict() for a in cached_articles],
                "error": str(e)
            })

    # Get cached article by ID
    @app.route("/api/articles/<int:article_id>", methods=["GET"])
    def get_article(article_id):
        art = Article.query.get_or_404(article_id)
        return jsonify(art.to_dict())

    @app.before_first_request
    def create_tables():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
