import React from "react";

export default function App() {
  return (
    <div className="app-container">
      <header>
        <h1>Self-Programming AI</h1>
        <p>AI-powered coding, research, and self-improvement platform</p>
      </header>
      <main>
        <section className="panel chat-panel">
          <h2>Chat Assistant</h2>
          <div className="placeholder">Chat UI coming soon...</div>
        </section>
        <section className="panel code-panel">
          <h2>Code Generation</h2>
          <div className="placeholder">Code generation UI coming soon...</div>
        </section>
        <section className="panel research-panel">
          <h2>Web Research</h2>
          <div className="placeholder">Research UI coming soon...</div>
        </section>
        <section className="panel knowledge-panel">
          <h2>Knowledge Base</h2>
          <div className="placeholder">Knowledge UI coming soon...</div>
        </section>
      </main>
      <footer>
        <span>Inspired by <a href="https://bolt.new/" target="_blank" rel="noopener noreferrer">bolt.new</a></span>
      </footer>
    </div>
  );
}
