import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";

function Home() {
  return <div><h2>Home</h2><p>Welcome to Self-Programming AI!</p></div>;
}
function AppPage() {
  return <div><h2>App</h2><p>App features coming soon...</p></div>;
}
function ResearchPage() {
  return <div><h2>Research</h2><p>Research UI coming soon...</p></div>;
}
function GeneratePage() {
  return <div><h2>Generate</h2><p>Code generation UI coming soon...</p></div>;
}
function LearnPage() {
  return <div><h2>Learn</h2><p>Learning UI coming soon...</p></div>;
}
function ImprovePage() {
  return <div><h2>Improve</h2><p>Code improvement UI coming soon...</p></div>;
}

export default function App() {
  return (
    <Router>
      <div className="app-container">
        <header>
          <h1>Self-Programming AI</h1>
          <nav>
            <ul className="nav-list">
              <li><Link to="/">Home</Link></li>
              <li><Link to="/chat">Chat</Link></li>
              <li><Link to="/app">App</Link></li>
              <li><Link to="/research">Research</Link></li>
              <li><Link to="/generate">Generate</Link></li>
              <li><Link to="/learn">Learn</Link></li>
              <li><Link to="/improve">Improve</Link></li>
            </ul>
          </nav>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/chat" element={<div><h2>Chat</h2><p>Chat UI coming soon...</p></div>} />
            <Route path="/app" element={<AppPage />} />
            <Route path="/research" element={<ResearchPage />} />
            <Route path="/generate" element={<GeneratePage />} />
            <Route path="/learn" element={<LearnPage />} />
            <Route path="/improve" element={<ImprovePage />} />
          </Routes>
        </main>
        <footer>
          <span>Inspired by <a href="https://bolt.new/" target="_blank" rel="noopener noreferrer">bolt.new</a></span>
        </footer>
      </div>
    </Router>
  );
}
