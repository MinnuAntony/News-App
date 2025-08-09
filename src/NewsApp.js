import React, { useState, useEffect, useRef } from "react";
import "./NewsApp.css";
/*const API_KEY = "2ed750521f7b42fd856727e05e751381";*/
const API_KEY = "d432cff58cdf43f6b8d844a1e5f18077";
const BASE_URL = "https://newsapi.org/v2/everything?q=";

function NewsApp() {
  const [articles, setArticles] = useState([]);
  const [query, setQuery] = useState("India");
  const [activeNav, setActiveNav] = useState(null);
  const searchInputRef = useRef(null);

  useEffect(() => {
    fetchNews("India");
  }, []);

  async function fetchNews(searchQuery) {
    try {
      const res = await fetch(`${BASE_URL}${searchQuery}&apiKey=${API_KEY}`);
      if (!res.ok) {
        console.error("Error fetching news:", res.status, res.statusText);
        setArticles([]);
        return;
      }
      const data = await res.json();
      setArticles(data.articles || []);
    } catch (error) {
      console.error("Network error:", error);
      setArticles([]);
    }
  }

  function handleNavClick(id) {
    setActiveNav(id);
    fetchNews(id);
    setQuery("");
    if (searchInputRef.current) {
      searchInputRef.current.value = "";
    }
  }

  function handleSearch() {
    if (!query) return;
    setActiveNav(null);
    fetchNews(query);
  }

  function handleReload() {
    setActiveNav(null);
    setQuery("");
    fetchNews("India");
    if (searchInputRef.current) {
      searchInputRef.current.value = "";
    }
  }

  return (
    <div>
      <nav>
        <div className="main-nav container flex">
          <a href="#" onClick={handleReload} className="company-logo">
            <img src="./new.jpg" alt="company logo" />
          </a>
          <div className="nav-links">
            <ul className="flex">
              {["ipl", "finance", "politics"].map((navId) => (
                <li
                  key={navId}
                  className={`hover-link nav-item ${
                    activeNav === navId ? "active" : ""
                  }`}
                  onClick={() => handleNavClick(navId)}
                >
                  {navId.toUpperCase()}
                </li>
              ))}
            </ul>
          </div>
          <div className="search-bar flex">
            <input
              id="search-text"
              type="text"
              className="news-input"
              placeholder="e.g. Science"
              ref={searchInputRef}
              onChange={(e) => setQuery(e.target.value)}
            />
            <button
              id="search-button"
              className="search-button"
              onClick={handleSearch}
            >
              Search
            </button>
          </div>
        </div>
      </nav>

      <main>
        <div className="cards-container container flex" id="cards-container">
          {articles.length === 0 ? (
            <p>No news articles found.</p>
          ) : (
            articles.map((article, idx) => {
              if (!article.urlToImage) return null;
              const date = new Date(article.publishedAt).toLocaleString("en-US", {
                timeZone: "Asia/Jakarta",
              });
              return (
                <div className="card" key={idx} onClick={() => window.open(article.url, "_blank")}>
                  <div className="card-header">
                    <img
                      src={article.urlToImage}
                      alt={article.title}
                      className="news-img"
                    />
                  </div>
                  <div className="card-content">
                    <h3 className="news-title">{article.title}</h3>
                    <h6 className="news-source">
                      {article.source.name} · {date}
                    </h6>
                    <p className="news-desc">{article.description}</p>
                  </div>
                </div>
              );
            })
          )}
        </div>
      </main>
    </div>
  );
}

export default NewsApp;
