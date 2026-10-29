# 2050 Strategy Practice Monitoring System (v2.0)
## Multi-User Authenticated & Role-Isolated Python/Streamlit System

### Overview
This repository contains **Version 2.0** of the **2050 Strategy Practice Monitoring System** (`2050_Practice_Monitoring_System_App-v2.py`), updated to include **secure authentication, role-based access control (RBAC), custom TAG visual branding, and role-isolated data submission views**.

---

### Key Features Added in Version 2.0

#### 1. Authenticated Login Portal
- **Login Gateway:** Replaces open access with a secure sign-in interface powered by Streamlit Session State (`st.session_state`).
- **User Roles:**
  - **👑 System Admin (`sysadmin` / `admin123`):** Universal system access, dynamic role impersonation/switching, raw database inspection, and diagnostic controls.
  - **🛡️ MEL Admin (`mel_admin` / `mel2050`):** Secretariat access to the cross-cutting regional dashboard, AI review queue, submission approvals/returns, and indicator management.
  - **TAG Focal Points (x7):** Dedicated credentials for each of the 7 Thematic Advisory Groups (`ta1_lead` through `ta7_lead`).

#### 2. Custom Thematic Branding & Profile Headers
When a TAG user logs in, they are greeted by a custom-designed visual header tailored to their specific thematic area:
- **TA1 (Political Leadership & Regionalism):** 🏛️ Navy & Gold (`#1F4E79`, `#D4AF37`) — *"Fostering Pacific Solidarity, Sovereignty & High-Level Diplomacy"*
- **TA2 (People-Centred Development):** 👥 Coral & Sunset Teal (`#E07A5F`, `#2A9D8F`) — *"Inclusivity, Health, Gender Equality, Youth & Cultural Heritage"*
- **TA3 (Peace & Security):** 🛡️ Steel Blue & Guard Gold (`#2B4C7E`, `#E9C46A`) — *"Implementing the Boe Declaration for a Safe & Secure Blue Pacific"*
- **TA4 (Resource & Economic Development):** 📈 Emerald & Financial Navy (`#2A9D8F`, `#264653`) — *"Sustainable Fisheries, Trade Expansion & Blue Economy Growth"*
- **TA5 (Climate Change & Disasters):** 🌪️ Crimson & Storm Orange (`#E76F51`, `#F4A261`) — *"Building Climate Resilience, Loss & Damage & Disaster Mobilisation"*
- **TA6 (Ocean & Natural Environment):** 🌊 Deep Azure & Marine Teal (`#0077B6`, `#00B4D8`) — *"Stewardship of the Ocean Realm, Biodiversity & BBNJ Treaty"*
- **TA7 (Technology & Connectivity):** ⚡ Cyber Violet & Digital Blue (`#6C5CE7`, `#0984E3`) — *"Digital Transformation, Cyber Security & Regional Telecommunications"*

#### 3. Strict Role-Isolated Data Privacy
- **TAG Level Privacy:** TAG users can **ONLY** view, inspect, and manage submissions originating from their specific thematic area.
- **My Submissions Queue:** Automatically filters out all other TAG records to prevent cross-agency data leakage.

#### 4. TAG Mini-Dashboard & Analytics
Integrated directly into each TAG's profile page:
- **KPI Summary Cards:** Total Logged Submissions, Approved Count, Awaiting Review, and Returned/Action Needed.
- **Donut Chart:** Submissions breakdown by lifecycle status (*Draft, Submitted, Awaiting Review, Approved, Returned*).
- **Gauge Indicator:** Real-time performance benchmark comparing reported actuals against 2026 targets.

---

### User Credentials Reference Table

| Role / Thematic Area | Username | Password | Default Scope |
| :--- | :--- | :--- | :--- |
| **👑 System Admin** | `sysadmin` | `admin123` | Full Access & Role Switcher |
| **🛡️ MEL Admin** | `mel_admin` | `mel2050` | Secretariat Review & Approvals Queue |
| **🏛️ TA1 Lead** | `ta1_lead` | `ta1_pass` | Political Leadership & Regionalism TAG |
| **👥 TA2 Lead** | `ta2_lead` | `ta2_pass` | People-Centred Development TAG |
| **🛡️ TA3 Lead** | `ta3_lead` | `ta3_pass` | Peace & Security TAG |
| **📈 TA4 Lead** | `ta4_lead` | `ta4_pass` | Resource & Economic Development TAG |
| **🌪️ TA5 Lead** | `ta5_lead` | `ta5_pass` | Climate Change & Disasters TAG |
| **🌊 TA6 Lead** | `ta6_lead` | `ta6_pass` | Ocean & Natural Environment TAG |
| **⚡ TA7 Lead** | `ta7_lead` | `ta7_pass` | Technology & Connectivity TAG |

---

### Local Quickstart Instructions

1. **Install Dependencies:**
   ```bash
   pip install streamlit pandas plotly
   ```

2. **Launch Application:**
   ```bash
   streamlit run 2050_Practice_Monitoring_System_App-v2.py
   ```

3. **Log in:** Use any of the credentials listed in the reference table above to test role-isolated views and custom TAG headers.
