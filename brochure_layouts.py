"""
brochure_layouts.py — Rich Multi-Panel HTML Brochure Layouts for Alpha_Doc Suite
Defines authentic, distinct, multi-column and open-spread brochure templates:
1. Bi-Fold Open Spread (Forest Green, Sage, Warm Gold, Who We Are, Services & Contact)
2. Modern Tech Tri-Fold (Navy, Vibrant Orange, Electric Teal, What We Do & Your Future)
3. Editorial Studio Bi-Fold (Midnight Navy, Warm Terracotta, Sand, Our Approach & Future of Design)
4. Emerald Enterprise Tri-Fold (Deep Emerald Teal, Charcoal Slate, Olive Gold, About Us & What We Offer)
"""

BROCHURE_HTML_BIFOLD = """<div style="font-family: 'Segoe UI', Arial, sans-serif; color: #1e293b; background-color: #ffffff;">
  <!-- Open Bi-Fold Spread Master Table (2 Pages Side-by-Side) -->
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 2px;">
    <tr>
      <!-- LEFT SPREAD PANEL (49% width) -->
      <td width="49%" valign="top" style="background-color: #faf8f5; border: 1px solid #e5e0d8; padding: 8px 10px;">
        <!-- Top Geometric Accent Bar -->
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 4px;">
          <tr>
            <td width="55%" bgcolor="#204634" style="background-color: #204634; height: 5px;"></td>
            <td width="45%" bgcolor="#8ba895" style="background-color: #8ba895; height: 5px;"></td>
          </tr>
        </table>

        <!-- Left Header -->
        <h1 style="color: #1e3a2b; font-family: Georgia, serif; font-size: 14pt; font-weight: 900; letter-spacing: 1px; margin: 4px 0 1px 0; line-height: 1.1;">INNOVATIVE<br>SOLUTIONS</h1>
        <p style="font-size: 7.5pt; color: #4a5d52; margin: 0 0 6px 0; font-weight: 600;">For the Modern Era</p>

        <!-- Central Team Collaboration Frame -->
        <div style="background-color: #eef2ed; border: 1.5px solid #c59b27; padding: 6px 8px; margin: 4px 0 6px 0; border-radius: 4px; text-align: center;">
          <p style="margin: 0; font-size: 7.5pt; font-weight: bold; color: #1e3a2b;">🏢 STRATEGIC COLLABORATION</p>
          <p style="margin: 2px 0 0 0; font-size: 6.5pt; color: #556b5d; line-height: 1.25;">Cross-functional enterprise pods uniting advanced engineering with transformative client outcomes.</p>
        </div>

        <!-- Who We Are Section -->
        <h3 style="color: #1e3a2b; font-family: Georgia, serif; font-size: 8.5pt; font-weight: 800; margin: 4px 0 2px 0; border-bottom: 1.5px solid #c59b27; padding-bottom: 1px;">Who We Are</h3>
        <p style="font-size: 7pt; color: #334155; line-height: 1.25; margin: 1px 0 4px 0;">
          We partner with industry leaders to design and deliver autonomous systems, high-velocity workflows, and sustainable architecture tailored to modern operational complexity.
        </p>
        <p style="font-size: 6.5pt; color: #204634; font-weight: 600; margin: 1px 0 6px 0; line-height: 1.25;">
          ✔ <b>Quality Results</b> — Rigorous engineering standards<br>
          ✔ <b>Client-Focused</b> — Transparent lifecycle execution
        </p>

        <!-- Brand Footer -->
        <div style="text-align: center; margin-top: 6px; border-top: 1px solid #c59b27; padding-top: 3px;">
          <span style="color: #1e3a2b; font-size: 7.5pt; font-weight: bold; letter-spacing: 2px;">— brand —</span>
        </div>
      </td>

      <!-- CENTER SPREAD CREASE / FOLD (2% width) -->
      <td width="2%" valign="middle" align="center" style="background-color: #ede7dc; border-left: 1px dashed #d5cdbf; border-right: 1px dashed #d5cdbf;">
      </td>

      <!-- RIGHT SPREAD PANEL (49% width) -->
      <td width="49%" valign="top" style="background-color: #faf8f5; border: 1px solid #e5e0d8; padding: 8px 10px;">
        <!-- Top Accent Banner -->
        <div style="background-color: #dfcca5; padding: 3px 6px; margin-bottom: 4px; text-align: center; border-radius: 2px;">
          <h2 style="margin: 0; font-family: Georgia, serif; font-size: 9.5pt; font-weight: 900; letter-spacing: 1.5px; color: #1e3a2b;">OUR SERVICES</h2>
        </div>

        <!-- Three Service Highlight Boxes -->
        <table width="100%" cellpadding="3" cellspacing="2" border="0" style="margin-bottom: 4px;">
          <tr>
            <td width="33%" valign="top" style="background-color: #eaf0ec; border-top: 2.5px solid #c59b27; padding: 3px 2px; text-align: center;">
              <div style="font-size: 9pt;">⚙️</div>
              <p style="font-size: 6pt; font-weight: bold; color: #1e3a2b; margin: 1px 0 0 0;">SERVICE ONE</p>
              <p style="font-size: 5.5pt; color: #4a5d52; margin: 0; line-height: 1.15;">Strategic roadmaps and systems alignment.</p>
            </td>
            <td width="33%" valign="top" style="background-color: #eaf0ec; border-top: 2.5px solid #7c9d86; padding: 3px 2px; text-align: center;">
              <div style="font-size: 9pt;">🔍</div>
              <p style="font-size: 6pt; font-weight: bold; color: #1e3a2b; margin: 1px 0 0 0;">SERVICE TWO</p>
              <p style="font-size: 5.5pt; color: #4a5d52; margin: 0; line-height: 1.15;">Autonomous agents and deep workflows.</p>
            </td>
            <td width="33%" valign="top" style="background-color: #eaf0ec; border-top: 2.5px solid #204634; padding: 3px 2px; text-align: center;">
              <div style="font-size: 9pt;">📈</div>
              <p style="font-size: 6pt; font-weight: bold; color: #1e3a2b; margin: 1px 0 0 0;">SERVICE THREE</p>
              <p style="font-size: 5.5pt; color: #4a5d52; margin: 0; line-height: 1.15;">Cloud clusters and data governance.</p>
            </td>
          </tr>
        </table>

        <!-- Central Vision Quote Box -->
        <div style="border: 1.5px solid #c59b27; background-color: #faf8f5; padding: 5px 8px; margin: 4px 0; text-align: center; border-radius: 4px;">
          <p style="margin: 0; font-family: Georgia, serif; font-size: 7.5pt; font-style: italic; font-weight: bold; color: #1e3a2b;">'Transforming vision into reality'</p>
        </div>

        <!-- Get In Touch Contact Section -->
        <h4 style="color: #1e3a2b; font-family: Georgia, serif; font-size: 8pt; font-weight: 800; letter-spacing: 1px; text-align: center; margin: 4px 0 2px 0;">GET IN TOUCH</h4>
        <table width="100%" cellpadding="1" cellspacing="0" border="0" style="font-size: 6pt; color: #37473e; text-align: center; margin-bottom: 4px;">
          <tr>
            <td width="33%">📞 123-456-7890</td>
            <td width="33%">✉ hello@company.com</td>
            <td width="33%">🌐 www.yourbrand.com</td>
          </tr>
        </table>

        <!-- Bottom Geometric Accent Bar -->
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top: 4px;">
          <tr>
            <td width="45%" bgcolor="#8ba895" style="background-color: #8ba895; height: 4px;"></td>
            <td width="55%" bgcolor="#204634" style="background-color: #204634; height: 4px;"></td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</div>"""

BROCHURE_HTML_TRIFOLD_TECH = """<div style="font-family: 'Segoe UI', Arial, sans-serif; color: #1e293b; background-color: #ffffff;">
  <!-- Tri-Fold Spread (3 Panels Side-by-Side) -->
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 2px;">
    <tr>
      <!-- PANEL 1: WHAT WE DO (33% width) -->
      <td width="33%" valign="top" style="background-color: #ffffff; border: 1px solid #e2e8f0; padding: 6px 7px;">
        <!-- Top Geometric Banner -->
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 4px;">
          <tr>
            <td width="50%" bgcolor="#0f2438" style="background-color: #0f2438; height: 5px;"></td>
            <td width="25%" bgcolor="#00a896" style="background-color: #00a896; height: 5px;"></td>
            <td width="25%" bgcolor="#f97316" style="background-color: #f97316; height: 5px;"></td>
          </tr>
        </table>

        <h3 style="color: #0f2438; font-size: 8.5pt; font-weight: 900; letter-spacing: 1px; margin: 2px 0 4px 0;">WHAT WE DO</h3>

        <p style="margin: 0; font-size: 7pt; font-weight: bold; color: #0f2438;">⚙️ Service A</p>
        <p style="margin: 1px 0 4px 0; font-size: 6.5pt; color: #475569; line-height: 1.2;">Enterprise systems architecture & strategic infrastructure roadmaps.</p>

        <p style="margin: 0; font-size: 7pt; font-weight: bold; color: #00a896;">🚀 Service B</p>
        <p style="margin: 1px 0 4px 0; font-size: 6.5pt; color: #475569; line-height: 1.2;">Autonomous agent integration & accelerated developer workflows.</p>

        <p style="margin: 0; font-size: 7pt; font-weight: bold; color: #f97316;">📊 Service C</p>
        <p style="margin: 1px 0 5px 0; font-size: 6.5pt; color: #475569; line-height: 1.2;">Continuous telemetry monitoring & high-availability cluster scaling.</p>

        <!-- Get In Touch Dark Footer Card -->
        <div style="background-color: #0f2438; color: #ffffff; padding: 6px 7px; border-radius: 4px; margin-top: 4px;">
          <h4 style="margin: 0 0 2px 0; color: #38bdf8; font-size: 7.5pt; font-weight: 800; letter-spacing: 0.5px;">GET IN TOUCH</h4>
          <p style="margin: 0; font-size: 6pt; color: #cbd5e1; line-height: 1.3;">
            📞 +003-355 7790<br>
            ✉ email@alphabrand.com<br>
            📍 500 Technology Parkway
          </p>
        </div>
      </td>

      <!-- Crease 1 (1%) -->
      <td width="1%" style="background-color: #f1f5f9; border-left: 1px dashed #cbd5e1; border-right: 1px dashed #cbd5e1;"></td>

      <!-- PANEL 2: WHO WE ARE (34% width) -->
      <td width="34%" valign="top" style="background-color: #ffffff; border: 1px solid #e2e8f0; padding: 6px 7px;">
        <!-- Top Geometric Banner -->
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 4px;">
          <tr>
            <td width="30%" bgcolor="#00a896" style="background-color: #00a896; height: 5px;"></td>
            <td width="40%" bgcolor="#f97316" style="background-color: #f97316; height: 5px;"></td>
            <td width="30%" bgcolor="#0f2438" style="background-color: #0f2438; height: 5px;"></td>
          </tr>
        </table>

        <h3 style="color: #0f2438; font-size: 8.5pt; font-weight: 900; letter-spacing: 1px; margin: 2px 0 3px 0;">WHO WE ARE</h3>
        <p style="font-size: 6.5pt; color: #334155; line-height: 1.25; margin: 0 0 4px 0;">
          We are visionary software architects specializing in uniting human expertise with autonomous intelligence to deliver scalable enterprise outcomes.
        </p>

        <p style="font-size: 6.5pt; color: #0f2438; font-weight: 600; line-height: 1.3; margin: 0 0 6px 0;">
          🟠 <b>Proven Mastery</b> — 99.98% uptime<br>
          🟠 <b>Velocity</b> — 38% faster delivery<br>
          🟠 <b>Governance</b> — Zero telemetry leaks
        </p>

        <!-- Circular Team Graphic Frame -->
        <div style="background-color: #e0f2fe; border: 1.5px solid #00a896; padding: 6px 6px; border-radius: 4px; text-align: center; margin-top: 4px;">
          <p style="margin: 0; font-size: 7pt; font-weight: bold; color: #0f2438;">👥 STRATEGIC POD</p>
          <p style="margin: 1px 0 0 0; font-size: 6pt; color: #0369a1; line-height: 1.2;">Cross-functional engineering pods building resilient tomorrow.</p>
        </div>
      </td>

      <!-- Crease 2 (1%) -->
      <td width="1%" style="background-color: #f1f5f9; border-left: 1px dashed #cbd5e1; border-right: 1px dashed #cbd5e1;"></td>

      <!-- PANEL 3: YOUR FUTURE (31% width) -->
      <td width="31%" valign="top" style="background-color: #ffffff; border: 1px solid #e2e8f0; padding: 6px 7px;">
        <!-- Top Accent -->
        <div style="height: 5px; background-color: #f97316; margin-bottom: 4px;"></div>

        <h1 style="color: #f97316; font-size: 13pt; font-weight: 900; letter-spacing: 1.5px; margin: 0; line-height: 1.0;">YOUR</h1>
        <h1 style="color: #00a896; font-size: 13pt; font-weight: 900; letter-spacing: 1.5px; margin: 0; line-height: 1.0;">FUTURE</h1>
        <p style="font-size: 7pt; color: #475569; font-style: italic; font-weight: bold; margin: 2px 0 6px 0;">Innovate & Grow Today</p>

        <!-- Collaboration Showcase Banner -->
        <div style="background-color: #fff7ed; border-left: 3px solid #f97316; padding: 6px 6px; margin: 4px 0 8px 0; border-radius: 2px;">
          <p style="margin: 0; font-size: 7pt; font-weight: bold; color: #9a3412;">🌟 ACCELERATION</p>
          <p style="margin: 2px 0 0 0; font-size: 6pt; color: #431407; line-height: 1.2;">Pioneering next-generation document systems for modern enterprise builders.</p>
        </div>

        <!-- Brand Mark -->
        <div style="text-align: center; margin-top: 10px; padding-top: 6px; border-top: 1px solid #e2e8f0;">
          <span style="color: #0f2438; font-size: 8pt; font-weight: 900; letter-spacing: 1px;">⚡ your_brand</span>
        </div>
      </td>
    </tr>
  </table>
</div>"""

BROCHURE_HTML_EDITORIAL_TERRACOTTA = """<div style="font-family: 'Segoe UI', Arial, sans-serif; color: #1e293b; background-color: #ffffff;">
  <!-- Open Bi-Fold Spread (2 Panels Side-by-Side) -->
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 2px;">
    <tr>
      <!-- LEFT SPREAD PANEL (49% width) -->
      <td width="49%" valign="top" style="background-color: #f7f4ee; border: 1px solid #e7dfd3; padding: 8px 10px;">
        <!-- Top Navy Header Banner -->
        <div style="background-color: #152840; color: #f4eee6; padding: 6px 8px; border-radius: 3px; margin-bottom: 6px;">
          <h2 style="margin: 0; font-family: Georgia, serif; font-size: 11pt; font-weight: 900; letter-spacing: 1.5px; color: #f4eee6;">OUR APPROACH</h2>
        </div>

        <!-- Creative Process Section -->
        <h4 style="color: #b85d3b; font-size: 7.5pt; font-weight: 800; letter-spacing: 1px; margin: 4px 0 3px 0;">CREATIVE PROCESS</h4>
        
        <p style="margin: 0; font-size: 6.5pt; font-weight: bold; color: #152840;">💡 1. Conceptual Synthesis</p>
        <p style="margin: 0 0 3px 0; font-size: 6pt; color: #57534e; line-height: 1.2;">Rigorous contextual research and brand positioning audit.</p>

        <p style="margin: 0; font-size: 6.5pt; font-weight: bold; color: #152840;">⚙️ 2. Iterative Architecture</p>
        <p style="margin: 0 0 3px 0; font-size: 6pt; color: #57534e; line-height: 1.2;">Interactive motion prototypes and scalable design systems.</p>

        <p style="margin: 0; font-size: 6.5pt; font-weight: bold; color: #152840;">✔ 3. Cross-Medium Deployment</p>
        <p style="margin: 0 0 5px 0; font-size: 6pt; color: #57534e; line-height: 1.2;">Precision execution across digital, editorial, and physical touchpoints.</p>

        <!-- Collaboration & Impact Block -->
        <div style="background-color: #ffffff; border-left: 3px solid #b85d3b; padding: 5px 7px; margin: 4px 0; border-radius: 2px;">
          <h4 style="margin: 0 0 2px 0; color: #152840; font-size: 7pt; font-weight: bold;">COLLABORATION & IMPACT</h4>
          <p style="margin: 0 0 3px 0; font-size: 6pt; color: #57534e; font-style: italic;">"Transformative design that shifts perspectives and elevates brand equity."</p>
          <p style="margin: 0; font-size: 6pt; color: #152840; line-height: 1.25;">
            • Proven enterprise velocity<br>
            • Modular scalable components<br>
            • Cohesive cultural resonance
          </p>
        </div>

        <!-- Left Footer -->
        <div style="background-color: #152840; color: #f4eee6; padding: 4px 8px; border-radius: 12px; text-align: center; margin-top: 6px;">
          <span style="font-size: 6pt; letter-spacing: 0.5px;">🌐 www.yourbrand.com &nbsp;•&nbsp; ✉ hello@agency.com</span>
        </div>
      </td>

      <!-- CENTER CREASE / FOLD (2% width) -->
      <td width="2%" valign="middle" align="center" style="background-color: #ece4d7; border-left: 1px dashed #d5cdbf; border-right: 1px dashed #d5cdbf;"></td>

      <!-- RIGHT SPREAD PANEL (49% width) -->
      <td width="49%" valign="top" style="background-color: #f7f4ee; border: 1px solid #e7dfd3; padding: 8px 10px;">
        <!-- Geometric Accent Header -->
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 6px;">
          <tr>
            <td width="60%" bgcolor="#b85d3b" style="background-color: #b85d3b; height: 5px;"></td>
            <td width="40%" bgcolor="#152840" style="background-color: #152840; height: 5px;"></td>
          </tr>
        </table>

        <!-- Central Circular Hero Visual Frame -->
        <div style="background-color: #ffffff; border: 2px solid #b85d3b; border-radius: 6px; padding: 10px 8px; text-align: center; margin: 4px 0 8px 0;">
          <div style="font-size: 16pt; margin-bottom: 2px;">🎨</div>
          <p style="margin: 0; font-family: Georgia, serif; font-size: 8pt; font-weight: bold; color: #152840;">STUDIO NEXUS</p>
          <p style="margin: 2px 0 0 0; font-size: 6pt; color: #78716c; line-height: 1.2;">Spatial Design • Editorial Systems • Cultural Identity</p>
        </div>

        <!-- Main Headline -->
        <h1 style="color: #b85d3b; font-family: Georgia, serif; font-size: 13pt; font-weight: 900; letter-spacing: 1px; margin: 4px 0 1px 0; line-height: 1.1;">THE FUTURE<br>OF DESIGN</h1>
        <h2 style="color: #152840; font-family: 'Segoe UI', Arial, sans-serif; font-size: 10pt; font-weight: 800; margin: 2px 0 2px 0;">Innovation in Motion</h2>
        <p style="font-size: 7pt; color: #78716c; font-style: italic; margin: 0 0 8px 0;">creative agency</p>

        <!-- Capability Pillars -->
        <div style="background-color: #ede4d8; padding: 5px 6px; border-radius: 3px; margin-bottom: 6px;">
          <p style="margin: 0; font-size: 6pt; color: #44403c; line-height: 1.25;">
            ✔ <b>Identity:</b> Comprehensive visual frameworks.<br>
            ✔ <b>Digital:</b> Interactive and multi-modal experiences.<br>
            ✔ <b>Spatial:</b> Architectural environments and installations.
          </p>
        </div>

        <!-- Brand Emblem Footer -->
        <div style="text-align: center; margin-top: 6px; padding-top: 4px; border-top: 1px solid #d5cdbf;">
          <span style="color: #152840; font-size: 7.5pt; font-weight: bold; letter-spacing: 1.5px;">❖ yourbrand studio</span>
        </div>
      </td>
    </tr>
  </table>
</div>"""

BROCHURE_HTML_EMERALD_GOLD = """<div style="font-family: 'Segoe UI', Arial, sans-serif; color: #ffffff; background-color: #ffffff;">
  <!-- Tri-Fold Spread (3 Panels Side-by-Side) -->
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 2px;">
    <tr>
      <!-- PANEL 1: ABOUT US (Deep Emerald Teal, 33%) -->
      <td width="33%" valign="top" bgcolor="#006d68" style="background-color: #006d68; color: #ffffff; padding: 7px 8px; border-radius: 3px 0 0 3px;">
        <!-- Top Gold Accent -->
        <div style="height: 4px; background-color: #c5a046; margin-bottom: 4px;"></div>

        <h3 style="color: #ffffff; font-size: 9pt; font-weight: 900; letter-spacing: 1px; margin: 2px 0 2px 0; border-bottom: 1.5px solid #c5a046; padding-bottom: 2px;">ABOUT US</h3>
        
        <p style="font-size: 6.5pt; color: #e6fffa; line-height: 1.25; margin: 3px 0 6px 0;">
          We build enterprise-grade desktop intelligence tools, native AST document processing engines, and resilient autonomous workflows tailored to ambitious teams.
        </p>

        <!-- Leadership Graphic Box -->
        <div style="background-color: rgba(255, 255, 255, 0.12); border: 1px solid #c5a046; padding: 5px 6px; border-radius: 4px; text-align: center; margin-bottom: 6px;">
          <p style="margin: 0; font-size: 7pt; font-weight: bold; color: #ffffff;">👥 LEADERSHIP POD</p>
          <p style="margin: 2px 0 0 0; font-size: 6pt; color: #b2f5ea; line-height: 1.2;">Mastering complex desktop document architectures.</p>
        </div>

        <p style="font-size: 6pt; color: #e6fffa; margin: 0; line-height: 1.3;">
          ✔ 99.98% Native Cluster Uptime<br>
          ✔ Absolute Data Sovereignty<br>
          ✔ Real-Time Collaborative Sync
        </p>

        <div style="margin-top: 8px; padding-top: 4px; border-top: 1px solid rgba(255, 255, 255, 0.2); font-size: 5.5pt; color: #b2f5ea; text-align: center;">
          🌐 alphadocs.io &nbsp;•&nbsp; ✉ contact@alphadocs.io
        </div>
      </td>

      <!-- Crease 1 (1%) -->
      <td width="1%" style="background-color: #1a202c; border-left: 1px dashed #4a5568; border-right: 1px dashed #4a5568;"></td>

      <!-- PANEL 2: WHAT WE OFFER (Charcoal Slate, 34%) -->
      <td width="34%" valign="top" bgcolor="#222629" style="background-color: #222629; color: #ffffff; padding: 7px 8px;">
        <!-- Top Gold Accent -->
        <div style="height: 4px; background-color: #c5a046; margin-bottom: 4px;"></div>

        <h3 style="color: #c5a046; font-size: 9pt; font-weight: 900; letter-spacing: 1px; margin: 2px 0 4px 0;">WHAT WE OFFER</h3>

        <p style="margin: 0; font-size: 6.5pt; font-weight: bold; color: #ffffff;">📄 Document Design</p>
        <p style="margin: 1px 0 4px 0; font-size: 6pt; color: #cbd5e1; line-height: 1.2;">High-precision typography & paged viewports.</p>

        <p style="margin: 0; font-size: 6.5pt; font-weight: bold; color: #ffffff;">🖼️ Media Assets</p>
        <p style="margin: 1px 0 4px 0; font-size: 6pt; color: #cbd5e1; line-height: 1.2;">Native rasterization & vector graphics rendering.</p>

        <p style="margin: 0; font-size: 6.5pt; font-weight: bold; color: #ffffff;">⚡ Dynamic Templates</p>
        <p style="margin: 1px 0 4px 0; font-size: 6pt; color: #cbd5e1; line-height: 1.2;">Instant clone & live AST compilation.</p>

        <p style="margin: 0; font-size: 6.5pt; font-weight: bold; color: #ffffff;">🛠️ Creator Templates</p>
        <p style="margin: 1px 0 4px 0; font-size: 6pt; color: #cbd5e1; line-height: 1.2;">Multi-column executive & editorial layouts.</p>

        <!-- Bottom Gold Accent Block -->
        <div style="background-color: #c5a046; color: #1a202c; padding: 3px 6px; border-radius: 2px; text-align: center; margin-top: 6px;">
          <span style="font-size: 6pt; font-weight: 800; letter-spacing: 0.5px;">ENTERPRISE CAPABILITIES</span>
        </div>
      </td>

      <!-- Crease 2 (1%) -->
      <td width="1%" style="background-color: #1a202c; border-left: 1px dashed #4a5568; border-right: 1px dashed #4a5568;"></td>

      <!-- PANEL 3: INNOVATIVE SOLUTIONS (Dark Charcoal & Teal Hero, 31%) -->
      <td width="31%" valign="top" bgcolor="#1c1f22" style="background-color: #1c1f22; color: #ffffff; padding: 7px 8px; border-radius: 0 3px 3px 0;">
        <!-- Top Accent Tile Bar -->
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 6px;">
          <tr>
            <td width="40%" bgcolor="#006d68" style="background-color: #006d68; height: 5px;"></td>
            <td width="60%" bgcolor="#c5a046" style="background-color: #c5a046; height: 5px;"></td>
          </tr>
        </table>

        <!-- Hero Typography -->
        <h1 style="color: #ffffff; font-size: 12pt; font-weight: 900; letter-spacing: 1.5px; margin: 0; line-height: 1.0;">INNOVATIVE</h1>
        <h1 style="color: #c5a046; font-size: 12pt; font-weight: 900; letter-spacing: 1.5px; margin: 0; line-height: 1.0;">SOLUTIONS</h1>
        
        <p style="font-size: 6.5pt; color: #94a3b8; font-weight: bold; margin: 3px 0 4px 0; letter-spacing: 0.5px;">Create. Edit. Elevate.</p>

        <p style="font-size: 6pt; color: #cbd5e1; line-height: 1.25; margin: 0 0 6px 0; font-style: italic;">
          "A modern, creative business or editor suite designed for unmatched performance."
        </p>

        <!-- Feature Highlight Box -->
        <div style="background-color: rgba(0, 109, 104, 0.3); border: 1px solid #006d68; padding: 5px 6px; border-radius: 4px; margin-bottom: 6px;">
          <p style="margin: 0; font-size: 6.5pt; font-weight: bold; color: #c5a046;">✨ DESKTOP MASTERY</p>
          <p style="margin: 1px 0 0 0; font-size: 5.5pt; color: #e2e8f0; line-height: 1.2;">Offline-first local intelligence with full data privacy.</p>
        </div>

        <!-- Brand Mark -->
        <div style="text-align: center; margin-top: 8px; padding-top: 4px; border-top: 1px solid #334155;">
          <span style="color: #c5a046; font-size: 7pt; font-weight: 800; letter-spacing: 1px;">Alpha_Docs Suite</span>
        </div>
      </td>
    </tr>
  </table>
</div>"""
