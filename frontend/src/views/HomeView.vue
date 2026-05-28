<template>
  <section class="home-page">

    <!-- Navbar -->
    <nav class="navbar">
      <div class="nav-inner">
        <div class="nav-brand">
          <span class="brand-icon">+</span>
          <span class="brand-name">GetPlaced</span>
        </div>
        <div class="nav-links">
          <a class="nav-link" href="#">For Recruiters</a>
          <button class="btn-outline" @click="$router.push('/login')">Login</button>
          <button class="btn-primary" @click="$router.push('/register')">Sign up</button>
        </div>
      </div>
    </nav>

    <!-- Grid Background -->
    <div class="grid-bg" aria-hidden="true"></div>

    <!-- Hero Section -->
    <div class="hero">
      <div class="hero-content">
        <h1 class="hero-heading">
          Take your job profile<br />to the <span class="hero-accent">GetPlaced</span>
        </h1>
        <p class="hero-sub">
          Boost your job profile with Kudos from your peers for your skills and traits.
          Land your dream job effortlessly. Our platform matches you with the perfect opportunity.
        </p>
        <div class="hero-actions">
          <button class="btn-primary btn-lg" @click="$router.push('/login')">Get Started</button>
          
        </div>
        <div class="hero-chips">
          <span class="chip chip-purple">🎓 For Students</span>
          <span class="chip chip-teal">🏢 For Recruiters</span>
        </div>
      </div>

      <div class="hero-visual">
        <div class="illustration-wrap">
          <!-- SVG Illustration: person at desk with brain/AI motif -->
          <svg viewBox="0 0 420 340" xmlns="http://www.w3.org/2000/svg" class="hero-svg">
            <!-- Desk -->
            <rect x="60" y="250" width="300" height="12" rx="4" fill="#e2e8f0"/>
            <rect x="80" y="262" width="12" height="50" rx="3" fill="#cbd5e1"/>
            <rect x="328" y="262" width="12" height="50" rx="3" fill="#cbd5e1"/>

            <!-- Monitor -->
            <rect x="100" y="165" width="160" height="90" rx="8" fill="#1e293b"/>
            <rect x="108" y="173" width="144" height="74" rx="4" fill="#0f172a"/>
            <!-- screen lines -->
            <rect x="116" y="183" width="60" height="6" rx="2" fill="#6366f1"/>
            <rect x="116" y="195" width="90" height="4" rx="2" fill="#334155"/>
            <rect x="116" y="205" width="75" height="4" rx="2" fill="#334155"/>
            <rect x="116" y="215" width="50" height="4" rx="2" fill="#334155"/>
            <rect x="116" y="225" width="80" height="4" rx="2" fill="#334155"/>
            <!-- Monitor stand -->
            <rect x="172" y="255" width="16" height="18" rx="2" fill="#cbd5e1"/>
            <rect x="158" y="268" width="44" height="6" rx="2" fill="#e2e8f0"/>

            <!-- Laptop -->
            <rect x="270" y="210" width="110" height="70" rx="6" fill="#1e293b"/>
            <rect x="276" y="216" width="98" height="56" rx="3" fill="#0f172a"/>
            <rect x="256" y="280" width="140" height="8" rx="2" fill="#334155"/>
            <!-- laptop screen content -->
            <rect x="284" y="224" width="45" height="4" rx="2" fill="#6366f1"/>
            <rect x="284" y="233" width="70" height="3" rx="2" fill="#334155"/>
            <rect x="284" y="241" width="55" height="3" rx="2" fill="#334155"/>
            <rect x="284" y="249" width="65" height="3" rx="2" fill="#334155"/>
            <rect x="284" y="257" width="40" height="3" rx="2" fill="#334155"/>
            <!-- Chart bars on laptop -->
            <rect x="340" y="255" width="8" height="14" rx="1" fill="#10b981"/>
            <rect x="352" y="248" width="8" height="21" rx="1" fill="#6366f1"/>
            <rect x="364" y="244" width="8" height="25" rx="1" fill="#f59e0b"/>

            <!-- Person body -->
            <ellipse cx="228" cy="318" rx="42" ry="12" fill="#e2e8f0" opacity="0.6"/>
            <!-- torso -->
            <rect x="200" y="220" width="56" height="75" rx="14" fill="#818cf8"/>
            <!-- shirt collar -->
            <path d="M218 220 Q228 232 238 220" stroke="#6366f1" stroke-width="2" fill="none"/>
            <!-- arms -->
            <path d="M200 240 Q178 255 170 268" stroke="#fbbf24" stroke-width="14" stroke-linecap="round" fill="none"/>
            <path d="M256 240 Q278 255 285 268" stroke="#fbbf24" stroke-width="14" stroke-linecap="round" fill="none"/>
            <!-- hands -->
            <circle cx="168" cy="270" r="8" fill="#fbbf24"/>
            <circle cx="287" cy="270" r="8" fill="#fbbf24"/>
            <!-- neck -->
            <rect x="220" y="200" width="16" height="22" rx="6" fill="#fbbf24"/>
            <!-- head -->
            <ellipse cx="228" cy="188" rx="28" ry="30" fill="#fbbf24"/>
            <!-- hair -->
            <path d="M200 178 Q202 152 228 150 Q254 152 256 178 Q248 162 228 164 Q208 162 200 178 Z" fill="#1e293b"/>
            <!-- face: eyes -->
            <circle cx="218" cy="186" r="3" fill="#1e293b"/>
            <circle cx="238" cy="186" r="3" fill="#1e293b"/>
            <!-- glasses -->
            <rect x="212" y="182" width="12" height="9" rx="3" fill="none" stroke="#334155" stroke-width="1.5"/>
            <rect x="232" y="182" width="12" height="9" rx="3" fill="none" stroke="#334155" stroke-width="1.5"/>
            <line x1="224" y1="186" x2="232" y2="186" stroke="#334155" stroke-width="1.5"/>
            <!-- smile -->
            <path d="M220 196 Q228 202 236 196" stroke="#92400e" stroke-width="1.5" fill="none" stroke-linecap="round"/>

            <!-- Success circle (top right) -->
            <circle cx="348" cy="100" r="58" fill="#d1fae5" stroke="#6ee7b7" stroke-width="1.5"/>
            <text x="348" y="88" text-anchor="middle" font-size="36">🏆</text>
            <text x="348" y="120" text-anchor="middle" font-size="11" fill="#065f46" font-weight="600">Get Placed</text>
            <text x="348" y="136" text-anchor="middle" font-size="10" fill="#059669">Faster</text>

            <!-- Floating cards -->
            <rect x="20" y="80" width="100" height="52" rx="8" fill="white" stroke="#e2e8f0" stroke-width="1.5"/>
            <text x="30" y="100" font-size="9" fill="#64748b" font-weight="600">APPLICATIONS</text>
            <text x="30" y="118" font-size="22" fill="#6366f1" font-weight="700">24</text>

            <rect x="20" y="148" width="100" height="52" rx="8" fill="white" stroke="#e2e8f0" stroke-width="1.5"/>
            <text x="30" y="168" font-size="9" fill="#64748b" font-weight="600">INTERVIEWS</text>
            <text x="30" y="186" font-size="22" fill="#10b981" font-weight="700">6</text>

            <!-- Dots decoration -->
            <circle cx="140" cy="60" r="3" fill="#6366f1" opacity="0.5"/>
            <circle cx="155" cy="75" r="2" fill="#6366f1" opacity="0.4"/>
            <circle cx="125" cy="78" r="2" fill="#10b981" opacity="0.5"/>
            <circle cx="390" cy="60" r="3" fill="#f59e0b" opacity="0.5"/>
            <circle cx="375" cy="45" r="2" fill="#6366f1" opacity="0.4"/>
          </svg>
        </div>
      </div>
    </div>

    <!-- Companies Strip -->
    <div class="companies">
      <p class="companies-label">COMPANIES HIRING ON GETPLACED</p>
      <div class="logo-strip">
        <span class="logo-item">Google</span>
        <span class="logo-item">Microsoft</span>
        <span class="logo-item">Amazon</span>
        <span class="logo-item">LinkedIn</span>
        <span class="logo-item">Wipro</span>
        <span class="logo-item">Infosys</span>
        <span class="logo-item">TCS</span>
      </div>
    </div>

    <!-- Feature Cards -->
    <div class="features">
      <div class="feature-card">
        <div class="feat-icon feat-icon-purple">🎓</div>
        <h2 class="feat-title">For Students</h2>
        <ul class="feat-list">
          <li><span class="check check-purple">✓</span> View and apply for job listings</li>
          <li><span class="check check-purple">✓</span> Track application status</li>
          <li><span class="check check-purple">✓</span> Access placement resources</li>
        </ul>
      </div>

      <div class="feature-card">
        <div class="feat-icon feat-icon-teal">🏢</div>
        <h2 class="feat-title">For Recruiters</h2>
        <ul class="feat-list">
          <li><span class="check check-teal">✓</span> Post job openings</li>
          <li><span class="check check-teal">✓</span> Manage applications</li>
          <li><span class="check check-teal">✓</span> Connect with top talent</li>
        </ul>
      </div>

      <div class="feature-card">
        <div class="feat-icon feat-icon-amber">🚀</div>
        <h2 class="feat-title">Easy Onboarding</h2>
        <ul class="feat-list">
          <li><span class="check check-amber">✓</span> Quick profile setup</li>
          <li><span class="check check-amber">✓</span> Skill-based job suggestions</li>
          <li><span class="check check-amber">✓</span> Real-time notifications</li>
        </ul>
      </div>
    </div>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer-container">
        <div class="footer-brand">
          <h2 class="footer-logo">GetPlaced</h2>
          <p>Empowering students and recruiters through a modern placement platform. Find opportunities, connect with talent, and build careers.</p>
        </div>
        <div class="footer-col">
          <h3>Quick Links</h3>
          <ul>
            <li>Home</li><li>Jobs</li><li>Companies</li><li>Contact</li>
          </ul>
        </div>
        <div class="footer-col">
          <h3>Resources</h3>
          <ul>
            <li>Placement Guide</li><li>Resume Tips</li><li>Interview Prep</li><li>FAQs</li>
          </ul>
        </div>
        <div class="footer-col">
          <h3>Contact Us</h3>
          <p>Email: support@getplaced.com</p>
          <p>Phone: +91 1111111111</p>
          <p>Location: Greater Noida, Uttar Pradesh</p>
        </div>
      </div>
      <div class="footer-bottom">© 2026 GetPlaced. All rights reserved.</div>
    </footer>

  </section>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@400;600;800&family=DM+Sans:wght@400;500&display=swap');

/* ── Reset & Base ── */
* { box-sizing: border-box; margin: 0; padding: 0; }

.home-page {
  font-family: 'DM Sans', sans-serif;
  background: #f8f7f4;
  color: #0f0f0f;
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
}

/* ── Grid Background ── */
.grid-bg {
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(0,0,0,0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,0,0,0.05) 1px, transparent 1px);
  background-size: 48px 48px;
  pointer-events: none;
  z-index: 0;
}

/* ── Navbar ── */
.navbar {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 100;
  background: rgba(248,247,244,0.85);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(0,0,0,0.08);
}

.nav-inner {
  max-width: 1100px;
  margin: 0 auto;
  padding: 14px 28px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'Bricolage Grotesque', sans-serif;
  font-weight: 800;
  font-size: 18px;
  color: #0f0f0f;
}

.brand-icon {
  width: 28px;
  height: 28px;
  background: #0f0f0f;
  color: white;
  border-radius: 7px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 700;
  line-height: 1;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 16px;
}

.nav-link {
  font-size: 14px;
  color: #444;
  text-decoration: none;
  font-weight: 500;
}

.btn-outline {
  padding: 8px 20px;
  border: 1.5px solid #0f0f0f;
  border-radius: 8px;
  background: transparent;
  color: #0f0f0f;
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.18s, color 0.18s;
}
.btn-outline:hover { background: #0f0f0f; color: white; }

.btn-primary {
  padding: 8px 20px;
  border: none;
  border-radius: 8px;
  background: #0f0f0f;
  color: white;
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: opacity 0.18s, transform 0.18s;
}
.btn-primary:hover { opacity: 0.85; transform: translateY(-1px); }

/* ── Hero ── */
.hero {
  max-width: 1100px;
  margin: 0 auto;
  padding: 140px 28px 80px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px;
  align-items: center;
  position: relative;
  z-index: 1;
}

.hero-content { display: flex; flex-direction: column; gap: 24px; }

.hero-heading {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: clamp(36px, 5vw, 58px);
  font-weight: 800;
  line-height: 1.08;
  color: #0f0f0f;
  letter-spacing: -1.5px;
}

.hero-accent {
  position: relative;
  display: inline-block;
}
.hero-accent::after {
  content: '';
  position: absolute;
  bottom: 2px; left: 0; right: 0;
  height: 4px;
  background: #6366f1;
  border-radius: 2px;
}

.hero-sub {
  font-size: 17px;
  line-height: 1.7;
  color: #555;
  max-width: 480px;
}

.hero-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.btn-lg { padding: 13px 32px !important; font-size: 16px !important; border-radius: 10px !important; }

.btn-ghost {
  padding: 8px 20px;
  border: 1.5px solid #ddd;
  border-radius: 8px;
  background: transparent;
  color: #555;
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: border-color 0.18s;
}
.btn-ghost:hover { border-color: #999; }

.hero-chips {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.chip {
  padding: 6px 14px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 500;
  border: 1px solid transparent;
}
.chip-purple { background: #ede9fe; color: #5b21b6; border-color: #c4b5fd; }
.chip-teal   { background: #d1fae5; color: #065f46; border-color: #6ee7b7; }

/* Hero Visual */
.hero-visual {
  display: flex;
  align-items: center;
  justify-content: center;
}

.illustration-wrap {
  width: 100%;
  max-width: 460px;
  background: white;
  border-radius: 20px;
  border: 1px solid rgba(0,0,0,0.07);
  padding: 24px;
  box-shadow: 0 4px 40px rgba(0,0,0,0.06);
}

.hero-svg { width: 100%; height: auto; }

/* ── Companies ── */
.companies {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 28px 80px;
  position: relative;
  z-index: 1;
  border-top: 1px solid rgba(0,0,0,0.08);
  padding-top: 60px;
}

.companies-label {
  text-align: center;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.1em;
  color: #888;
  margin-bottom: 32px;
}

.logo-strip {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 40px;
}

.logo-item {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 20px;
  font-weight: 600;
  color: #aaa;
  letter-spacing: -0.5px;
  transition: color 0.2s;
}
.logo-item:hover { color: #333; }

/* ── Feature Cards ── */
.features {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 28px 100px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  position: relative;
  z-index: 1;
}

.feature-card {
  background: white;
  border: 1px solid rgba(0,0,0,0.07);
  border-radius: 16px;
  padding: 28px;
  transition: box-shadow 0.2s, transform 0.2s;
}
.feature-card:hover {
  box-shadow: 0 8px 32px rgba(0,0,0,0.08);
  transform: translateY(-3px);
}

.feat-icon {
  width: 48px; height: 48px;
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-size: 22px;
  margin-bottom: 18px;
}
.feat-icon-purple { background: #ede9fe; }
.feat-icon-teal   { background: #d1fae5; }
.feat-icon-amber  { background: #fef3c7; }

.feat-title {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 20px;
  font-weight: 700;
  color: #0f0f0f;
  margin-bottom: 16px;
}

.feat-list {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0;
}

.feat-list li {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 11px 0;
  color: #555;
  font-size: 15px;
  border-bottom: 1px solid rgba(0,0,0,0.06);
}
.feat-list li:last-child { border-bottom: none; }

.check {
  width: 20px; height: 20px;
  border-radius: 50%;
  font-size: 10px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.check-purple { background: #ede9fe; color: #7c3aed; }
.check-teal   { background: #d1fae5; color: #059669; }
.check-amber  { background: #fef3c7; color: #d97706; }

/* ── Footer ── */
.footer {
  background: #0f0f0f;
  color: #ccc;
  padding: 60px 28px 24px;
  position: relative;
  z-index: 1;
}

.footer-container {
  max-width: 1100px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 2fr repeat(3, 1fr);
  gap: 48px;
  padding-bottom: 48px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
}

.footer-logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 20px;
  font-weight: 800;
  color: white;
  margin-bottom: 14px;
}

.brand-icon-sm {
  width: 24px; height: 24px;
  background: white;
  color: #0f0f0f;
  border-radius: 6px;
  display: inline-flex; align-items: center; justify-content: center;
  font-size: 14px; font-weight: 700; line-height: 1;
}

.footer-brand p {
  font-size: 14px;
  line-height: 1.7;
  color: #888;
  max-width: 280px;
}

.footer-col h3 {
  color: white;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 16px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.footer-col ul { list-style: none; padding: 0; }
.footer-col li, .footer-col p {
  font-size: 14px;
  color: #888;
  line-height: 2;
}

.footer-bottom {
  max-width: 1100px;
  margin: 24px auto 0;
  text-align: center;
  font-size: 13px;
  color: #555;
}

/* ── Responsive ── */
@media (max-width: 800px) {
  .hero {
    grid-template-columns: 1fr;
    padding-top: 100px;
  }
  .hero-visual { order: -1; }
  .footer-container { grid-template-columns: 1fr 1fr; }
  .nav-links .nav-link { display: none; }
}

@media (max-width: 520px) {
  .footer-container { grid-template-columns: 1fr; }
  .features { grid-template-columns: 1fr; }
}
</style>