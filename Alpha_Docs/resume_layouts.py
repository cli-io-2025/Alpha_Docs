"""
resume_layouts.py — Rich Multi-Column HTML Layout Templates for Alpha_Doc Suite
Defines authentic, distinct, multi-column visual layouts for:
1. Executive Corporate (Navy header, light-blue sidebar, corporate hierarchy)
2. Creative Editorial (Warm ivory linen, circular avatar, serif headings, dot skill meters)
3. Modern Sage Geometric (Sage green full-height sidebar, geometric header, progress bars)
4. Strategic Marketing / Terracotta (Midnight navy sidebar, terracotta copper accents, progress meters)
"""

RESUME_HTML_EXECUTIVE = """<div style="font-family: 'Segoe UI', Arial, sans-serif; color: #1e293b; background-color: #ffffff;">
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 2px;">
    <tr>
      <td style="background-color: #0f2438; color: #ffffff; padding: 8px 10px 5px 10px; text-align: center;">
        <h1 style="margin: 0; font-size: 16pt; font-weight: 800; letter-spacing: 2px; color: #ffffff;">FIRSTNAME LASTNAME</h1>
        <p style="margin: 1px 0 0 0; font-size: 8.5pt; font-weight: 600; color: #cbd5e1; letter-spacing: 1.2px;">PROFESSIONAL TITLE / ROLE</p>
      </td>
    </tr>
    <tr>
      <td style="background-color: #1e3a5f; color: #e2e8f0; padding: 3px 8px; text-align: center; font-size: 7.5pt;">
        <span>✉ email@lpsum.com</span> &nbsp;•&nbsp; 
        <span>📞 (08) 233-4567</span> &nbsp;•&nbsp; 
        <span>📍 Lorem, Location</span> &nbsp;•&nbsp; 
        <span>🔗 in Lorem Ipsum</span>
      </td>
    </tr>
  </table>

  <table width="100%" cellpadding="4" cellspacing="0" border="0">
    <tr>
      <td width="33%" valign="top" style="background-color: #f1f5f9; border-right: 1px solid #e2e8f0; padding: 6px 6px;">
        <h3 style="color: #0f2438; font-size: 8.5pt; font-weight: 800; margin: 0 0 2px 0; border-bottom: 1.5px solid #cbd5e1; padding-bottom: 1px;">CONTACT</h3>
        <p style="font-size: 7.5pt; color: #334155; margin: 1px 0 6px 0; line-height: 1.25;">
          ✉ Lorem Ipsum<br>
          📞 Lorem Ipsum<br>
          📍 Location, Location<br>
          🔗 linkedin Ipsum
        </p>

        <h3 style="color: #0f2438; font-size: 8.5pt; font-weight: 800; margin: 0 0 2px 0; border-bottom: 1.5px solid #cbd5e1; padding-bottom: 1px;">SKILLS</h3>
        <p style="font-size: 7.5pt; color: #334155; margin: 1px 0 6px 0; line-height: 1.3;">
          ✔ Executive Leadership<br>
          ✔ Cloud Infrastructure<br>
          ✔ Strategic Planning<br>
          ✔ Systems Architecture<br>
          ✔ Enterprise Governance
        </p>

        <h3 style="color: #0f2438; font-size: 8.5pt; font-weight: 800; margin: 0 0 2px 0; border-bottom: 1.5px solid #cbd5e1; padding-bottom: 1px;">EDUCATION</h3>
        <p style="font-size: 7.5pt; color: #0f172a; margin: 1px 0 0 0; font-weight: bold;">Master of Science</p>
        <p style="font-size: 7pt; color: #64748b; margin: 0 0 4px 0;">University of California • 2018</p>
        <p style="font-size: 7.5pt; color: #0f172a; margin: 1px 0 0 0; font-weight: bold;">Bachelor of Science</p>
        <p style="font-size: 7pt; color: #64748b; margin: 0 0 6px 0;">State University • 2014</p>

        <h3 style="color: #0f2438; font-size: 8.5pt; font-weight: 800; margin: 0 0 2px 0; border-bottom: 1.5px solid #cbd5e1; padding-bottom: 1px;">CERTIFICATIONS</h3>
        <p style="font-size: 7.5pt; color: #334155; margin: 1px 0; line-height: 1.25;">
          ✔ PMP Certification (2024)<br>
          ✔ AWS Solutions Architect<br>
          ✔ Agile ScrumMaster (2023)
        </p>
      </td>

      <td width="67%" valign="top" style="background-color: #ffffff; padding: 6px 10px;">
        <h3 style="color: #0f2438; font-size: 9.5pt; font-weight: 800; margin: 0 0 2px 0; border-bottom: 1.5px solid #0f2438; padding-bottom: 2px;">PROFESSIONAL SUMMARY</h3>
        <p style="font-size: 8pt; color: #334155; line-height: 1.3; margin: 2px 0 6px 0;">
          Results-driven executive leader with 10+ years of proven expertise directing organizational transformations, scaling mission-critical platforms, and accelerating product delivery cycles across distributed global teams.
        </p>

        <h3 style="color: #0f2438; font-size: 9.5pt; font-weight: 800; margin: 4px 0 2px 0; border-bottom: 1.5px solid #0f2438; padding-bottom: 2px;">WORK EXPERIENCE</h3>
        
        <p style="font-size: 8pt; font-weight: bold; color: #0f172a; margin: 2px 0 0 0;">Job Title / Senior Director</p>
        <p style="font-size: 7pt; color: #64748b; margin: 0 0 2px 0;"><i>Company / 2021 – Present</i></p>
        <p style="font-size: 7.5pt; color: #334155; margin: 1px 0 5px 0; line-height: 1.25;">
          • Spearheaded enterprise infrastructure overhaul, cutting release turnaround by 38%.<br>
          • Managed $18M annual technology budget while reducing operating expenses by 14%.<br>
          • Mentored an international cross-functional engineering team of 35+ developers.
        </p>

        <p style="font-size: 8pt; font-weight: bold; color: #0f172a; margin: 4px 0 0 0;">Job Title / Systems Specialist</p>
        <p style="font-size: 7pt; color: #64748b; margin: 0 0 2px 0;"><i>Company / 2018 – 2021</i></p>
        <p style="font-size: 7.5pt; color: #334155; margin: 1px 0; line-height: 1.25;">
          • Led the re-architecture of customer-facing portals supporting 3M+ active sessions.<br>
          • Optimized database indexing and caching, decreasing average query latency by 52%.
        </p>
      </td>
    </tr>
  </table>
</div>"""

RESUME_HTML_EDITORIAL = """<div style="font-family: Georgia, 'Times New Roman', serif; color: #292524; background-color: #faf7f2;">
  <table width="100%" cellpadding="3" cellspacing="0" border="0" style="margin-bottom: 2px; border-bottom: 1px solid #e7e0d3; padding-bottom: 2px;">
    <tr>
      <td width="48" valign="middle" align="center" style="padding-right: 6px;">
        <div style="width: 38px; height: 38px; border-radius: 19px; border: 1.5px solid #78716c; background-color: #e7e2d8; text-align: center; line-height: 36px; font-size: 18px;">
          👤
        </div>
      </td>
      <td valign="middle">
        <h1 style="margin: 0; font-size: 16pt; font-weight: 900; letter-spacing: 1.5px; color: #1c1917;">FIRSTNAME LASTNAME</h1>
        <p style="margin: 1px 0 0 0; font-size: 8pt; font-weight: bold; letter-spacing: 1.5px; color: #78716c; font-family: 'Segoe UI', Arial, sans-serif;">CREATIVE DIRECTOR / DESIGNER</p>
      </td>
      <td width="180" valign="middle" align="right" style="font-family: 'Segoe UI', Arial, sans-serif; font-size: 7pt; color: #57534e; line-height: 1.3;">
        ✉ email.u@gmail.com<br>
        📞 (912) 235-7889<br>
        📍 Locowestorn, TY<br>
        🌐 portfolio.online.com
      </td>
    </tr>
  </table>

  <table width="100%" cellpadding="4" cellspacing="0" border="0">
    <tr>
      <td width="35%" valign="top" style="border-right: 1px solid #e7e0d3; padding-right: 8px; font-family: 'Segoe UI', Arial, sans-serif;">
        <h3 style="font-family: Georgia, serif; color: #1c1917; font-size: 8.5pt; letter-spacing: 1px; margin: 0 0 2px 0;">SKILLS</h3>
        <p style="font-size: 7.5pt; color: #44403c; margin: 1px 0 6px 0; line-height: 1.35;">
          Graphic Design &nbsp;●●●●○<br>
          UI/UX Design &nbsp;●●●●○<br>
          Project Management &nbsp;●●●○○<br>
          Branding &nbsp;●●●●○<br>
          Webware Design &nbsp;●●●○○<br>
          Design Systems &nbsp;●●●●○
        </p>

        <h3 style="font-family: Georgia, serif; color: #1c1917; font-size: 8.5pt; letter-spacing: 1px; margin: 4px 0 2px 0;">LANGUAGES</h3>
        <p style="font-size: 7.5pt; color: #44403c; margin: 1px 0 6px 0; line-height: 1.25;">
          English (Native)<br>
          Spanish (Conversational)
        </p>

        <h3 style="font-family: Georgia, serif; color: #1c1917; font-size: 8.5pt; letter-spacing: 1px; margin: 4px 0 2px 0;">INTERESTS</h3>
        <p style="font-size: 7.5pt; color: #44403c; margin: 1px 0 6px 0; line-height: 1.35;">
          📷 Photography<br>
          ✈ Traveling<br>
          ✍ Creative Writing
        </p>

        <h3 style="font-family: Georgia, serif; color: #1c1917; font-size: 8.5pt; letter-spacing: 1px; margin: 4px 0 2px 0;">CERTIFICATIONS</h3>
        <p style="font-size: 7.5pt; color: #44403c; margin: 1px 0; line-height: 1.25;">
          Design Theory • 2024<br>
          Design Systems • 2023<br>
          Brand Architecture • 2022
        </p>
      </td>

      <td width="65%" valign="top" style="padding-left: 10px;">
        <h3 style="color: #1c1917; font-size: 9pt; letter-spacing: 1px; margin: 0 0 2px 0;">ABOUT ME</h3>
        <p style="font-size: 8pt; color: #44403c; line-height: 1.3; margin: 2px 0 6px 0; font-family: 'Segoe UI', Arial, sans-serif;">
          Visionary creative director with extensive experience building resonant brand identities, cohesive design systems, and engaging visual narratives across digital, editorial, and physical touchpoints.
        </p>

        <h3 style="color: #1c1917; font-size: 9pt; letter-spacing: 1px; margin: 4px 0 2px 0;">WORK EXPERIENCE</h3>
        
        <p style="font-size: 8pt; font-weight: bold; color: #1c1917; margin: 2px 0 0 0;">Lead Creative Designer</p>
        <p style="font-size: 7pt; color: #78716c; margin: 0 0 2px 0; font-family: 'Segoe UI', Arial, sans-serif;"><i>Brand & Co. • Jan 2023 – Present</i></p>
        <p style="font-size: 7.5pt; color: #44403c; margin: 1px 0 5px 0; font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.25;">
          • Led creative direction for over 20+ successful multi-channel marketing campaigns.<br>
          • Collaborated with cross-functional product and engineering teams to design brand systems.
        </p>

        <p style="font-size: 8pt; font-weight: bold; color: #1c1917; margin: 3px 0 0 0;">Graphic Designer</p>
        <p style="font-size: 7pt; color: #78716c; margin: 0 0 2px 0; font-family: 'Segoe UI', Arial, sans-serif;"><i>Studio Nexus • Mar 2020 – Dec 2022</i></p>
        <p style="font-size: 7.5pt; color: #44403c; margin: 1px 0 6px 0; font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.25;">
          • Created engaging visual content across digital channels, increasing engagement by 40%.<br>
          • Successfully rebranded flagship retail clients, elevating digital conversion rates.
        </p>

        <h3 style="color: #1c1917; font-size: 9pt; letter-spacing: 1px; margin: 4px 0 2px 0;">EDUCATION</h3>
        <p style="font-size: 8pt; font-weight: bold; color: #1c1917; margin: 2px 0 0 0;">Master of Fine Arts</p>
        <p style="font-size: 7pt; color: #78716c; margin: 0 0 2px 0; font-family: 'Segoe UI', Arial, sans-serif;">Design University • 2018 – 2020</p>
        <p style="font-size: 8pt; font-weight: bold; color: #1c1917; margin: 2px 0 0 0;">Bachelor of Design</p>
        <p style="font-size: 7pt; color: #78716c; margin: 0; font-family: 'Segoe UI', Arial, sans-serif;">Creative Institute • 2014 – 2018</p>
      </td>
    </tr>
  </table>
</div>"""

RESUME_HTML_SAGE = """<div style="font-family: 'Segoe UI', Arial, Helvetica, sans-serif; color: #1e293b; background-color: #ffffff;">
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 3px;">
    <tr>
      <td width="35%" bgcolor="#204634" style="background-color: #204634; height: 6px;"></td>
      <td width="65%" bgcolor="#c59b27" style="background-color: #c59b27; height: 6px;"></td>
    </tr>
    <tr>
      <td colspan="2" style="padding: 8px 6px 4px 6px; text-align: center;">
        <h1 style="margin: 0; font-size: 16pt; font-weight: 800; letter-spacing: 2px; color: #1e3a2b; font-family: Georgia, serif;">FIRSTNAME LASTNAME</h1>
        <p style="margin: 1px 0 0 0; font-size: 8pt; font-weight: bold; letter-spacing: 1.5px; color: #4a5568;">CREATIVE DIRECTOR / STRATEGIST</p>
      </td>
    </tr>
  </table>

  <table width="100%" cellpadding="4" cellspacing="0" border="0">
    <tr>
      <td width="35%" valign="top" bgcolor="#bccfc1" style="background-color: #bccfc1; padding: 8px 6px; border-radius: 4px;">
        <h3 style="color: #143022; font-size: 8.5pt; font-weight: 800; letter-spacing: 1px; margin: 0 0 2px 0;">CONTACT</h3>
        <p style="font-size: 7.5pt; color: #1f2937; margin: 1px 0 6px 0; line-height: 1.3;">
          ✉ email@domain.com<br>
          📞 (555) 019-2834<br>
          📍 San Francisco, CA<br>
          🔗 linkedin.com/in/profile
        </p>

        <h3 style="color: #143022; font-size: 8.5pt; font-weight: 800; letter-spacing: 1px; margin: 0 0 2px 0;">SKILLS</h3>
        <p style="font-size: 7.5pt; color: #1f2937; margin: 1px 0 6px 0; line-height: 1.35;">
          Brand Identity &nbsp;●●●●●●<br>
          Art Direction &nbsp;●●●●●○<br>
          Digital Marketing:<br>
          [████████░░] 80%<br>
          Project Management:<br>
          [█████████░] 90%
        </p>

        <h3 style="color: #143022; font-size: 8.5pt; font-weight: 800; letter-spacing: 1px; margin: 0 0 2px 0;">EDUCATION</h3>
        <p style="font-size: 7.5pt; color: #143022; font-weight: bold; margin: 1px 0;">Degree of Creative Arts</p>
        <p style="font-size: 7pt; color: #374151; margin: 0 0 3px 0;">University of College • 2022 – 2024</p>
        <p style="font-size: 7.5pt; color: #143022; font-weight: bold; margin: 1px 0;">Degree of Science</p>
        <p style="font-size: 7pt; color: #374151; margin: 0 0 6px 0;">University of Science • 2018 – 2022</p>

        <h3 style="color: #143022; font-size: 8.5pt; font-weight: 800; letter-spacing: 1px; margin: 0 0 2px 0;">LANGUAGES</h3>
        <p style="font-size: 7.5pt; color: #1f2937; margin: 1px 0; line-height: 1.25;">
          English (Native)<br>
          German (Professional)<br>
          Spanish (Elementary)
        </p>
      </td>

      <td width="65%" valign="top" style="background-color: #ffffff; padding: 6px 10px;">
        <h3 style="color: #1e3a2b; font-size: 9pt; font-weight: 800; letter-spacing: 1px; margin: 0 0 2px 0; border-bottom: 1.5px solid #c59b27; padding-bottom: 2px;">PROFILE SUMMARY</h3>
        <p style="font-size: 8pt; color: #334155; line-height: 1.3; margin: 2px 0 6px 0;">
          Strategic creative director specializing in multi-channel brand architecture, product design, and high-performance cross-functional pod leadership.
        </p>

        <h3 style="color: #1e3a2b; font-size: 9pt; font-weight: 800; letter-spacing: 1px; margin: 4px 0 2px 0; border-bottom: 1.5px solid #c59b27; padding-bottom: 2px;">WORK EXPERIENCE</h3>
        
        <p style="font-size: 8pt; font-weight: bold; color: #0f172a; margin: 2px 0 0 0;">Lead Creative Designer</p>
        <p style="font-size: 7pt; color: #64748b; margin: 0 0 2px 0;"><i>2022 – Present • Company Name</i></p>
        <p style="font-size: 7.5pt; color: #334155; margin: 1px 0 5px 0; line-height: 1.25;">
          • Led brand overhaul to align visual procedures with modern digital benchmarks.<br>
          • Collaborated with cross-functional engineering and visual identity pods.
        </p>

        <p style="font-size: 8pt; font-weight: bold; color: #0f172a; margin: 3px 0 0 0;">Visual Designer</p>
        <p style="font-size: 7pt; color: #64748b; margin: 0 0 2px 0;"><i>2020 – 2022 • Company Name</i></p>
        <p style="font-size: 7.5pt; color: #334155; margin: 1px 0 6px 0; line-height: 1.25;">
          • Directed visual campaign executions across digital and print touchpoints.<br>
          • Created modular UI design systems and interactive motion prototypes.
        </p>

        <h3 style="color: #1e3a2b; font-size: 9pt; font-weight: 800; letter-spacing: 1px; margin: 4px 0 2px 0; border-bottom: 1.5px solid #c59b27; padding-bottom: 2px;">AWARDS & RECOGNITION</h3>
        <p style="font-size: 7.5pt; color: #334155; margin: 2px 0; line-height: 1.35;">
          🏆 <b>Awwwards Site of the Year Nominee</b> — Horizon Interactive (2023)<br>
          🥇 <b>International Design Excellence Award (IDEA)</b> — Gold in Brand Strategy (2022)<br>
          🎖 <b>National American Advertising Award (ADDY)</b> — Integrated Campaign (2021)
        </p>
      </td>
    </tr>
  </table>
</div>"""

RESUME_HTML_TERRACOTTA = """<div style="font-family: 'Segoe UI', Arial, sans-serif; color: #1e293b; background-color: #faf7f2;">
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 2px;">
    <tr>
      <td width="34%" bgcolor="#16253b" style="background-color: #16253b; height: 5px;"></td>
      <td width="66%" bgcolor="#c26d43" style="background-color: #c26d43; height: 5px;"></td>
    </tr>
    <tr>
      <td colspan="2" style="background-color: #faf7f2; padding: 6px 8px 3px 8px; text-align: center;">
        <h1 style="margin: 0; font-size: 15pt; font-weight: 800; letter-spacing: 2px; color: #152336;">FIRSTNAME LASTNAME</h1>
        <p style="margin: 1px 0 0 0; font-size: 8pt; font-weight: bold; letter-spacing: 1.5px; color: #c26d43;">MARKETING DIRECTOR / STRATEGIST</p>
      </td>
    </tr>
  </table>

  <table width="100%" cellpadding="4" cellspacing="0" border="0">
    <tr>
      <!-- Left Column: Midnight Navy Sidebar (34%) -->
      <td width="34%" valign="top" bgcolor="#16253b" style="background-color: #16253b; color: #ffffff; padding: 6px 6px; border-radius: 4px;">
        <h3 style="color: #ffffff; font-size: 8pt; font-weight: 800; letter-spacing: 1px; margin: 0 0 2px 0; border-bottom: 1.5px solid #c26d43; padding-bottom: 1px;">CONTACT</h3>
        <p style="font-size: 7pt; color: #e2e8f0; margin: 1px 0 5px 0; line-height: 1.25;">
          ✉ e-mail@memail.com<br>
          📞 (123) 456-7889<br>
          📍 San Francisco, CA<br>
          🔗 in/marketing-lead
        </p>

        <h3 style="color: #ffffff; font-size: 8pt; font-weight: 800; letter-spacing: 1px; margin: 2px 0 2px 0; border-bottom: 1.5px solid #c26d43; padding-bottom: 1px;">SKILLS</h3>
        <p style="font-size: 7pt; color: #e2e8f0; margin: 1px 0 5px 0; line-height: 1.3;">
          Brand Strategy<br>
          <span style="color: #c26d43;">■■■■■■■■</span><span style="color: #2a3d58;">■■</span><br>
          Digital Marketing<br>
          <span style="color: #c26d43;">■■■■■■■■■</span><span style="color: #2a3d58;">■</span><br>
          Campaign Mgmt<br>
          <span style="color: #c26d43;">■■■■■■■■</span><span style="color: #2a3d58;">■■</span><br>
          Data Analytics<br>
          <span style="color: #c26d43;">■■■■■■■</span><span style="color: #2a3d58;">■■■</span>
        </p>

        <h3 style="color: #ffffff; font-size: 8pt; font-weight: 800; letter-spacing: 1px; margin: 2px 0 2px 0; border-bottom: 1.5px solid #c26d43; padding-bottom: 1px;">LANGUAGES</h3>
        <p style="font-size: 7pt; color: #e2e8f0; margin: 1px 0; line-height: 1.25;">
          English (Native) &nbsp;<span style="color: #c26d43;">●●●●●</span><br>
          German (Proficient) &nbsp;<span style="color: #c26d43;">●●●●○</span><br>
          Spanish (Elementary) &nbsp;<span style="color: #c26d43;">●●●○○</span>
        </p>
      </td>

      <!-- Right Column: Warm Ivory Linen (66%) -->
      <td width="66%" valign="top" style="background-color: #faf7f2; padding: 4px 8px;">
        <h3 style="color: #152336; font-size: 8.5pt; font-weight: 800; letter-spacing: 1px; margin: 0 0 2px 0; border-bottom: 1.5px solid #152336; padding-bottom: 1px;">PROFILE SUMMARY</h3>
        <p style="font-size: 7.5pt; color: #334155; line-height: 1.25; margin: 1px 0 4px 0;">
          Proactive and visionary Marketing Director with 10+ years directing multi-channel campaigns, high-impact brand strategies, and cross-functional team growth across dynamic global markets.
        </p>

        <h3 style="color: #152336; font-size: 8.5pt; font-weight: 800; letter-spacing: 1px; margin: 3px 0 2px 0; border-bottom: 1.5px solid #152336; padding-bottom: 1px;">EXPERIENCE</h3>
        
        <p style="font-size: 7.5pt; font-weight: bold; color: #0f172a; margin: 1px 0 0 0;">Senior Marketing Manager</p>
        <p style="font-size: 6.5pt; color: #c26d43; margin: 0 0 1px 0;"><i>Company Name / 2021 – Present</i></p>
        <p style="font-size: 7pt; color: #334155; margin: 1px 0 3px 0; line-height: 1.2;">
          • Spearheaded marketing overhaul, driving 42% YoY user acquisition growth.<br>
          • Orchestrated cross-channel digital campaigns across search, social, and PR.
        </p>

        <p style="font-size: 7.5pt; font-weight: bold; color: #0f172a; margin: 2px 0 0 0;">Brand Strategist</p>
        <p style="font-size: 6.5pt; color: #c26d43; margin: 0 0 1px 0;"><i>Company Name / 2018 – 2021</i></p>
        <p style="font-size: 7pt; color: #334155; margin: 1px 0 3px 0; line-height: 1.2;">
          • Developed comprehensive brand positioning and messaging architecture.<br>
          • Conducted audience segmentation studies to optimize marketing conversion.
        </p>

        <p style="font-size: 7.5pt; font-weight: bold; color: #0f172a; margin: 2px 0 0 0;">Campaign Lead</p>
        <p style="font-size: 6.5pt; color: #c26d43; margin: 0 0 1px 0;"><i>Company Name / 2016 – 2018</i></p>
        <p style="font-size: 7pt; color: #334155; margin: 1px 0 4px 0; line-height: 1.2;">
          • Coordinated consumer research and brand alignment across international markets.
        </p>

        <h3 style="color: #152336; font-size: 8.5pt; font-weight: 800; letter-spacing: 1px; margin: 3px 0 2px 0; border-bottom: 1.5px solid #152336; padding-bottom: 1px;">EDUCATION</h3>
        <p style="font-size: 7.5pt; font-weight: bold; color: #0f172a; margin: 1px 0 0 0;">Master of Business Administration (Marketing)</p>
        <p style="font-size: 6.5pt; color: #c26d43; margin: 0 0 2px 0;">University of Brant, Institution / 2020 – 2022</p>
        <p style="font-size: 7.5pt; font-weight: bold; color: #0f172a; margin: 1px 0 0 0;">Bachelor of Arts in Communications</p>
        <p style="font-size: 6.5pt; color: #c26d43; margin: 0 0 4px 0;">University of Brant, Institution / 2016 – 2020</p>

        <h3 style="color: #152336; font-size: 8.5pt; font-weight: 800; letter-spacing: 1px; margin: 3px 0 2px 0; border-bottom: 1.5px solid #152336; padding-bottom: 1px;">AWARDS</h3>
        <p style="font-size: 7pt; color: #334155; margin: 1px 0; line-height: 1.25;">
          🏆 <b>Awards Prinzar Education</b> — Marketing Excellence (2023)<br>
          🥇 <b>Awards Finqnision</b> — Brand Strategy Innovation (2021)
        </p>
      </td>
    </tr>
  </table>
</div>"""
