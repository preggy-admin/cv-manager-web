# 🛠️ SmartCV: De-Commodified Academic Portfolio Compiler
### Secure, Privacy-First, and Open-Source Dossier Synthesiser for Global Scholars

> "Education and academic advancement should never be locked behind paywalls, nor should a scholar's professional history be treated as data-commodities for corporate scraping networks." — Dr. Preggy Reddy

**SmartCV** (`https://smartcv.edufusionai.co.za`) is a production-grade, privacy-first web application designed to democratize academic career progression. It empowers educators, researchers, and postgraduate students—particularly those navigating under-resourced environments in the Global South—to translate unstructured scholarly portfolios into highly polished, standards-compliant academic dossiers (such as Swedish GGI, Fulbright, and NRF formats) without falling victim to predatory commercial resume builders.

To ensure this remains a permanent public good, the core engine of SmartCV is **100% open-source, self-hostable, and free to use under the GNU AGPL-3.0 License**.

---

## 🌹 The Philosophical Moat: Digital Socialism in Action

Modern edtech and recruitment platforms operate on models of extractive capitalism: they charge premium subscription fees to desperate job-seekers while quietly caching and selling their personal data. 

SmartCV is engineered as an explicit counter-measure:
1. **De-Commodification:** Zero paywalls, zero premium tiers, and zero advertisements. The hosted version is run entirely budget-neutral, offset by our private cloud credits.
2. **Anti-Surveillance Architecture (Zero Data Retention):** Built using a stateless, in-memory processing pipeline. Your CV, publications, and personal credentials are processed purely in Volatile RAM and cleared instantly upon session termination. We write nothing to permanent disk, neutralizing corporate data-harvesting.
3. **Empowering the Global South:** Standard AI resume parsers are structurally biased toward Western corporate resume templates. SmartCV is optimized to recognize and elevate non-traditional, community-driven, and developmental academic achievements common in developing higher education sectors.

---

## ⚙️ Technical Architecture (The "Scholar-as-Builder" Stack)

SmartCV is decoupled and containerized to allow seamless local deployment by universities, student unions, or individual scholars:

*   **Backend:** High-performance FastAPI (Python 3.12) routing stateless data pipelines.
*   **Frontend:** Responsive, highly accessible React/TypeScript interface optimized for WCAG 2.1 AA compliance.
*   **Privacy Layer:** Volatile RAM-only processing nodes implementing secure multi-tenant schema isolation.
*   **Deployment:** Fully Dockerized for instant orchestration on Kubernetes or local lightweight server sandboxes.
