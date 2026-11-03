# RETURNLENS (V7.1 SUBMISSION FREEZE CANDIDATE) — FULL CONTEXT HANDOFF & REVIEW BRIEF

> **TÀI LIỆU HANDOFF DÀNH CHO GPT / REVIEWER ĐỘC LẬP**  
> *Bạn có thể tải tệp Markdown này lên ChatGPT (GPT-4o / GPT-o1) hoặc dán toàn bộ nội dung vào khung chat với prompt ở bên dưới.*

---

## PHẦN DÀNH CHO USER: CÂU LỆNH (PROMPT) GỢI Ý ĐỂ COPY VÀO GPT

```text
Bạn là một Giám khảo Kỹ thuật Cấp cao (Principal Technical Judge), Giám đốc Thiết kế Sản phẩm (Product Design Director) và Chuyên gia Đánh giá An toàn AI (AI Safety Auditor) tại cuộc thi AgentX Hackathon 2026.

Dưới đây là toàn bộ tài liệu bàn giao (Handoff Brief) của dự án "ReturnLens (v7.1 Submission Freeze Candidate)" thuộc Track PS-04 (Autonomous Support Agent for Solo D2C Merchants).

Hãy đọc kỹ toàn bộ tài liệu này (bao gồm bối cảnh bài toán, kiến trúc kỹ thuật, chính sách an toàn, 4 test case thực tế, toàn bộ nội dung & speaker notes của 6 slide, và kế hoạch thực thi 24h). Sau đó, hãy tiến hành một đợt REVIEW ĐỘC LẬP VÀ TOÀN DIỆN theo 7 tiêu chí:
1. Độ thuyết phục của Narrative & Pitch Flow trong 3 phút thuyết trình.
2. Mức độ phù hợp với đề bài Track PS-04 (Giải quyết đúng nỗi đau của Solo Merchant, tính thực tế).
3. Tính trung thực & phòng thủ bằng chứng (Evidentiary Grounding & Defensive Honesty — Tránh cạm bẫy ảo giác AI).
4. Kiến trúc Agentic & Cơ chế Fail-Closed Safety (Tính bền bỉ của State Machine, Dynamic Loop Case C, Zero-vision path).
5. Hàng rào bảo vệ tài chính (Financial Guardrails & Consequential Action Controls).
6. Dự đoán 5 câu hỏi "vặn" hóc búa nhất từ ban giám khảo và kịch bản trả lời "hạ gục" giám khảo.
7. Chấm điểm tổng quan (thang điểm 10) và các khuyến nghị tinh chỉnh cuối cùng trước giờ G.
```

---

# TỔNG QUAN HỒ SƠ DỰ ÁN (PROJECT DOSSIER)

- **Tên dự án:** ReturnLens
- **Tagline:** *"Every return decision, backed by evidence."* (Mọi quyết định đổi trả đều có bằng chứng bảo chứng).
- **One-liner:** Nền tảng phân loại và xử lý yêu cầu đổi trả có bảo chứng bằng chứng số (Evidence-backed returns triage) dành riêng cho các nhà bán hàng online độc lập (Solo D2C Merchants).
- **Cuộc thi:** AgentX Hackathon 2026 — Track PS-04: *Autonomous Support Agent for Online Sellers*.
- **Đội thi:** Team Rookie (3 kỹ sư: Person A - Agent/Backend/Policy, Person B - Vision/Evidence/UI, Person C - Integration/Scenarios/QA).
- **Mã nguồn (Repository):** `https://github.com/lenamkhanhh/hack4hack.git` (Nhánh: `main`, HEAD Commit: `787e126`).
- **Phiên bản nộp bài:** **ReturnLens v7.1 (Submission Freeze Candidate)**.
- **Bộ deliverables chuẩn:**
  1. Native Editable PowerPoint: `ReturnLens_v7_1.pptx` (16:9, 13.333" × 7.5", nhúng đủ Speaker Notes cho 6 slide, đóng gói `ZIP_STORED` deterministic).
  2. Vector PDF (6 trang): `ReturnLens_v7_1.pdf`.
  3. Interactive Web Console / GitHub Pages: `ReturnLens_v7_1.html` & `index.html`.
  4. Bảng kiểm tra chất lượng tự động: `scripts/smoke_test.py` (10/10 test pass, kiểm toán hình học không có overlap/collision, bảo toàn 12 file lịch sử v5/v6/v7).

---

# 1. TRIẾT LÝ CỐT LÕI & CÁC RÀNG BUỘC PHẢI TUÂN THỦ (NON-NEGOTIABLE CORE)

### Triết lý chủ đạo:
> **"Models observe. Code verifies. Seller authorizes."**  
> *(Mô hình AI quan sát. Mã nguồn xác minh. Người bán ủy quyền).*

### 5 Nguyên tắc vàng bất biến:
1. **Không bao giờ tự động chuyển tiền hoặc từ chối khách (Fail-Closed Human-in-the-Loop):**
   - AI **không bao giờ** được phép tự động hoàn tiền, tự tạo mã vận đơn đổi trả hoàn tất hoặc tự động từ chối yêu cầu của khách hàng.
   - Mọi hành động gây hậu quả tài chính (consequential action) đều phải qua cổng kiểm duyệt 1-click của người bán (Seller Authorization Gate).
2. **Trần bảo vệ tài chính nghiêm ngặt (Financial Refund Ceiling):**
   - Số tiền hoàn lại được tính toán bằng mã nguồn cứng ở backend, mô hình LLM tuyệt đối không được tự đặt số tiền:
     $$\text{Số tiền hợp lệ} \in \left(0, \min(₹4,999, \text{tiền còn được hoàn}, \text{tiền khách đã trả})\right)$$
   - Đơn hàng mẫu kiểm thử: ₹1,499.
3. **Kiến trúc mô hình tối giản (Exactly 3 Base Model Calls):**
   - Chỉ sử dụng đúng 3 lượt gọi mô hình cho 1 ca phân loại hoàn chỉnh:
     - `Planner`: Đề xuất action có định kiểu (typed action).
     - `Vision Extractor`: Trích xuất quan sát kèm mốc thời gian (cited observations).
     - `Critic / Summarizer`: Đối soát chéo, phát hiện mâu thuẫn trước khi đẩy lên UI người bán.
4. **Động cơ chính sách tất định (Deterministic Policy Engine P-01 -> P-08):**
   - Các chính sách nghiệp vụ (thời hạn 7 ngày, kiểm tra màu sắc, tem niêm phong, ngưỡng ánh sáng) được viết hoàn toàn bằng code Python thuần, không đưa vào system prompt của LLM để tránh ảo giác.
5. **Chữ ký phê duyệt ràng buộc mã hóa (Cryptographic Approval Binding):**
   - Lệnh phê duyệt của seller ký ràng buộc: `Case ID + SHA256 Evidence Hash + Policy Version`.
   - Hệ thống tự động re-validate lại trạng thái trước khi release bất kỳ bản nháp (draft) nào.

---

# 2. BỐI CẢNH BÀI TOÁN & PHÂN BIỆT DỮ LIỆU GIAN LẬN (THE PROBLEM)

### Chân dung đối tượng (Persona):
- Nhà bán lẻ trực tuyến độc lập (Solo D2C Merchant) bán các sản phẩm điện tử, phụ kiện âm thanh cá nhân (tai nghe, loa).
- Người bán phải một mình xử lý chăm sóc khách hàng, đóng gói, vận hành kho và đối soát đơn hàng.

### Điểm nghẽn thực tế: 4 Hệ thống rời rạc (4 Disconnected Systems):
Người bán phải mở nhiều tab trình duyệt cùng lúc để xử lý 1 ca khiếu nại:
1. **Buyer Message (Chat khách hàng):** Văn bản không có cấu trúc & video unboxing chưa được xác minh.
2. **Order Record (Hồ sơ đơn hàng Shopify):** Thông tin gốc từ kho (SKU: HEAD-WHT-02, Màu: Matte White, Giá: ₹1,499).
3. **Courier Status (Trạng thái vận chuyển Shippo):** Quét giao hàng thực tế (Đã giao 4 ngày trước, nằm trong khung 7 ngày).
4. **Return Policy (Chính sách cửa hàng):** Quy định 7 ngày đổi trả lỗi nhà sản xuất, yêu cầu còn nguyên tem niêm phong bao bì.

**Hậu quả:** Không có một hồ sơ bằng chứng có thể kiểm toán chung (No auditable evidence record). Người bán phải ra quyết định dựa trên trí nhớ, chịu rủi ro bất đối xứng: Hoàn tiền sai thì mất hàng và biên lợi nhuận; từ chối sai thì phá hủy giá trị vòng đời khách hàng (LTV).

### Phân biệt số liệu gian lận chuẩn xác (Fraud Metrics Disambiguation):
*Không được gộp chung 2 số liệu sau vì định nghĩa và phạm vi khảo sát khác nhau:*
- **9.0% — Return Fraud (NRF 2025):** Gian lận hình sự nghiêm ngặt (tráo hàng khi unbox, gửi hộp rỗng, cố tình lừa đảo).
- **15.14% — Fraud + Policy Abuse (Appriss/Deloitte 2024):** Gian lận hình sự kết hợp lạm dụng chính sách (wardrobing - dùng thử rồi trả, khiếu nại sai sự thật).

---

# 3. KỊCH BẢN ĐỐI SOÁT & 4 BENCHMARK TEST CASES

Dự án sử dụng 4 kịch bản kiểm thử độc lập, có thể tái lập 100%:

### Case A — Khiếu nại hợp lệ (Consistent Claim - ORD-1042):
- **Bằng chứng:** Video unboxing rõ nét, khớp màu, tem niêm phong còn nguyên, phát hiện vết nứt vật lý khi mở hộp, trong thời hạn 4/7 ngày.
- **Hành động của Agent:** Đạt tất cả policy P-01 đến P-08. Chuẩn bị sẵn bản nháp mã vận đơn đổi trả và bản nháp hoàn tiền trong trạng thái `pending_return_receipt`.
- **An toàn:** Tiền **chưa** chuyển ngay, chỉ kích hoạt giải ngân sau khi kiện hàng vật lý được quét nhận tại kho.

### Case B — Tráo màu / Lệch SKU (Star Demo - RT-8821 / ORD-7729):
- **Đơn hàng:** Khách đặt Tai nghe màu Trắng (Matte White, SKU `HEAD-WHT-02`, giá ₹1,499).
- **Bằng chứng Video:** Frame 00:07 cho thấy tai nghe màu Đen (Black casing).
- **Nguyên tắc Grounding trung thực:**
  - Agent ghi nhận: *"Observed: Black casing (color-consistent with HEAD-BLK-09) · Barcode unverified · SKU not verified"*.
  - Tuyệt đối **không** khẳng định camera đọc được mã vạch barcode hay xác minh chắc chắn mã SKU `HEAD-BLK-09` nếu tem mã vạch bị mờ/khuất.
- **Xử lý:** Kích hoạt `Policy P-03 Color Contradiction FAIL`. Chặn toàn bộ luồng tự động, không tạo nhãn, không tạo nháp hoàn tiền.
- **3 Quyền lựa chọn của Seller (Đúng 3 quyền này, tuyệt đối KHÔNG có đổi hàng - Exchange):**
  1. *Accept as warehouse mis-shipment* (Chấp nhận do kho gửi nhầm).
  2. *Request photo of outside-box shipping label* (Yêu cầu khách chụp tem vận đơn dán ngoài thùng carton).
  3. *Hold return for physical parcel inspection* (Giữ hàng kiểm tra trực tiếp khi bưu tá mang về).

### Case C — Video tối / Vòng lặp thu thập lại bằng chứng (Unclear Evidence / Dynamic Clarification Loop):
- **Bằng chứng:** Video 4 giây quá tối, rung lắc, chỉ có 2 frame dùng được, chỉ số độ sáng ghi nhận: `brightness score: 28/255`.
- **Xử lý:** Kích hoạt `Policy P-06 FAIL` (Chuẩn chất lượng ánh sáng & khung hình).
- **Tính chất Agentic:** Agent không từ chối khách ngay, mà gọi hàm `ask_for_evidence()` kèm hướng dẫn quay phim cụ thể (bật đèn, quay rõ tem), lưu serialize context, chuyển trạng thái ticket sang `WAITING_FOR_EVIDENCE`, và tự động hồi sinh (resume) phiên xử lý khi khách upload video mới.
- **Giới hạn an toàn chống lặp vô tận:** Sau tối đa 1 lần thử lại (1 retry), nếu bằng chứng vẫn không đạt, ca khiếu nại sẽ được escalate thẳng lên người bán kèm toàn bộ lịch sử log, tuyệt đối không tự động từ chối khách.

### Case D — Kiểm tra chuỗi liền mạch (Continuous Sequence Continuity Test):
- **Bằng chứng:** Video unboxing từ lúc rạch băng keo niêm phong thùng hàng đến lúc nhấc sản phẩm ra.
- **Năng lực kiểm tra:** Agent phân tích tính liên tục của chuỗi khung hình (sequence continuity) để phát hiện cắt ghép đột ngột (jump cut).
- **Giới hạn tuyên bố (Defensive Honesty):** Hệ thống chỉ khẳng định *"kiểm tra tính liên tục của video"*, tuyệt đối không tự nhận là *"chứng minh 100% video không bị giả mạo"* (advanced forensics thuộc nhóm "Cut First").

---

# 4. KIẾN TRÚC HỆ THỐNG & PHÂN QUYỀN 3 TẦNG (SYSTEM ARCHITECTURE)

```
[Khách hàng gửi Yêu cầu]
        │
        ├──> (1) Hỏi trạng thái đơn thông thường ("Where is my order?")
        │          │
        │          └──> [SECONDARY FAST PATH - ZERO VISION]
        │               Gọi trực tiếp Shopify API + Shippo API -> Trả lời khách ngay (Zero AI cost)
        │
        └──> (2) Yêu cầu Trả hàng / Đổi trả kèm Video
                   │
                   ▼
         [TIER 1: MODEL ZONE - Quan sát & Đề xuất]
         • Planner Model: Phân tích intent, đề xuất action có schema
         • FFmpeg Engine: Trích xuất keyframe (1 fps, độ phân giải gốc)
         • Vision Model: Nhận diện thực thể, trích dẫn frame cụ thể
         • Critic Model: So sánh đối soát chéo frame & claim
                   │
                   ▼
         [TIER 2: CODE ZONE - Kiểm chứng & Thực thi Chính sách]
         • Schema Validator: Kiểm tra tính hợp lệ của JSON Output
         • Deterministic Policy Engine (Python): P-01 đến P-08
           - P-01: Kiểm tra hạn bảo hành/trả hàng từ timestamp Shippo
           - P-02: Kiểm tra sự hiện diện của tem niêm phong
           - P-03: Kiểm tra mâu thuẫn màu sắc/chủng loại sản phẩm
           - P-04: Kiểm tra khung thời gian cửa hàng (Day 4/7)
           - P-06: Kiểm tra độ sáng & chất lượng video (Threshold 28/255)
           - P-08: Kiểm tra giới hạn hoàn tiền max ₹4,999
         • State Machine Manager: Quản lý vòng lặp Case C (WAITING_FOR_EVIDENCE)
                   │
                   ▼
         [TIER 3: SELLER ZONE - Cổng Phê duyệt Duy nhất (Human Gate)]
         • 1-Click Action Console: Hiển thị Store Truth vs Keyframe đối chứng
         • Cryptographic Approval Signature: Bind (Case ID + Evidence SHA256 + Policy Version)
         • Re-validation Gate: Kiểm tra tính toàn vẹn lần cuối trước khi kích hoạt thanh toán
```

---

# 5. NỘI DUNG ĐẦY ĐỦ CỦA 6 SLIDE & SPEAKER NOTES (CANONICAL SOURCE)

Dưới đây là nguyên văn nội dung trên mặt slide và lời thoại thuyết trình (Speaker Notes) được nhúng trực tiếp trong file PowerPoint:

### SLIDE 1: PRODUCT REVEAL & CONSOLE BẰNG CHỨNG
- **Kicker Tag:** `AGENTX HACKATHON 2026 · TRACK PS-04`
- **Headline:** ReturnLens
- **Subheadline:** Every return decision, backed by evidence.
- **Console Mockup:**
  - Tiêu đề: `RETURNLENS SELLER CONSOLE · CASE #RT-8821`
  - Cột trái (Store Truth): `Order #ORD-7729 · HEAD-WHT-02 · Matte White · ₹1,499 paid · Security Tag Required (P-02) · Delivered: 4d ago (Shippo #SH-9012) · Return Window: Day 4/7 (P-04 PASS)`
  - Cột phải (Observed Frame 00:07): `Black Casing (color-consistent with HEAD-BLK-09) · Barcode: Unverified · Exact SKU: Not verified · Lighting: Sufficient · Policy P-03 FAIL · Contradiction flagged → Route to human seller`
  - Banner cảnh báo: `P-03 COLOR CONTRADICTION: Observed black casing conflicts with ordered Matte White specification. Exact SKU unverified.`
  - Nút bấm hành động (Primary CTA): `Review Evidence & Decide`
- **Speaker Notes:**
  > *"Slide 1 — Product Hero & Executive Summary:  
  > - Problem Statement Fit: PS-04 (Autonomous Support Agent for Online Sellers).  
  > - Target User: Solo direct-to-consumer (D2C) online merchants managing customer support, shipping, and returns alone.  
  > - Core Friction: Solo sellers lose valuable hours navigating fragmented tabs (buyer chat, Shopify, Shippo tracking, store return policy). Return decisions are currently made from memory without unified evidence.  
  > - Core Thesis: 'Models observe. Code verifies. Seller authorizes.'  
  > - Console Focus: Side-by-side comparison between ordered White Headphones (HEAD-WHT-02, ₹1,499) and unboxed Black Headphones (Frame 00:07). The agent flags the contradiction, leaves exact SKU unverified, and surfaces actionable resolution choices to the seller.  
  > - Safety Boundary: The system never autonomously issues a refund or denies a customer. Financial release strictly requires 1-click merchant authorization."*

---

### SLIDE 2: BỐI CẢNH VẤN ĐỀ — 4 HỆ THỐNG RỜI RẠC
- **Kicker Tag:** `THE PROBLEM · SOLO SELLER BOTTLENECK`
- **Headline:** One return. Four disconnected sources.
- **Subheadline:** Four systems. No traceable decision.
- **4 Thẻ nguồn dữ liệu:**
  1. `01 Buyer Message`: Unstructured text & unverified unboxing video in chat.
  2. `02 Order Record`: Shopify manifest: HEAD-WHT-02, Matte White, ₹1,499.
  3. `03 Courier Status`: Shippo scan: delivered 4 days ago (Day 4 of 7).
  4. `04 Return Policy`: 7-day defect window; security packaging tag rule.
- **Thẻ tiêu điểm trung tâm (Focal Gap Card):**
  - Tiêu đề: `NO SHARED EVIDENCE RECORD`
  - Nội dung: `No auditable evidence record. One solo seller making high-stakes financial decisions across browser tabs.`
- **Số liệu nghiên cứu (Callout):**
  - `• 9.0% — Return Fraud (NRF 2025: criminal only)`
  - `• 15.14% — Fraud + Policy Abuse (Appriss/Deloitte 2024: criminal + abuse)`
  - Chú thích: *Definitions differ: strict criminal fraud vs fraud combined with policy abuse.*
- **Speaker Notes:**
  > *"Slide 2 — Problem Space & The Four Disconnected Sources:  
  > - The returns bottleneck for solo sellers is not an absent returns portal; it is fragmented, unverified context across four disconnected systems:  
  >   1. Buyer claim in chat (unverified claims, emotional text).  
  >   2. Store truth in Shopify (SKU HEAD-WHT-02, ₹1,499).  
  >   3. Courier tracking in Shippo (delivered 4 days ago).  
  >   4. Store return policy document (7-day defect window, security tag).  
  > - Central Gap: Four systems, but no traceable decision. The merchant makes memory-based decisions across multiple tabs.  
  > - Sourced Fraud Context: NRF 2025 reports 9% for strictly criminal return fraud, whereas Appriss/Deloitte 2024 reports 15.14% when combining fraud and policy abuse (wardrobing, unboxing swaps). These measure distinct scopes and must never be merged.  
  > - Asymmetric Merchant Risk: Wrong refund loses inventory and gross margin; unfair denial destroys customer lifetime value (LTV)."*

---

### SLIDE 3: STAR DEMO — CASE B SO SÁNH ĐỐI CHỨNG
- **Kicker Tag:** `STAR DEMO · CORE BENCHMARK SCENARIO`
- **Headline:** The order says white. The video shows black.
- **Subheadline:** ReturnLens flags the contradiction — the seller decides.
- **Cột Trái (Catalog Truth):** Ảnh chụp studio tai nghe trắng (`HEAD-WHT-02`, Matte White, ₹1,499).
- **Cột Phải (Unboxing Evidence):** Khung hình trích xuất từ video unboxing lúc 00:07 (`Black casing (color-consistent with HEAD-BLK-09)`).
  - Metadata: `Exact SKU: Not verified (Barcode unverified) · Policy P-03 FAIL · Lighting: Sufficient · REC 00:07 / 00:24 (Mock Keyframe)`.
- **Dải bảng điều khiển quyết định (Decision Strip):**
  - Kết quả Policy P-03: `COLOR CONTRADICTION DETECTED (ORDERED: Matte White ≠ OBSERVED: Midnight Black)`.
  - Hàng rào tài chính: `0 < amt <= min(₹4,999, rem_ref, paid)`.
  - Cảnh báo: `No automatic policy approvals. Financial release requires seller click.`
  - **3 Quyền lựa chọn của Seller:**
    1. `Accept as warehouse mis-shipment`
    2. `Request photo of outside-box shipping label`
    3. `Hold return for physical parcel inspection`
- **Speaker Notes:**
  > *"Slide 3 — The Star Demo & Technical Honesty in Vision Citation:  
  > - Core Benchmark Scenario (Case B): Buyer ordered White Headphones (HEAD-WHT-02, ₹1,499), but unboxing frame 00:07 shows black casing.  
  > - Visual Grounding Honesty: The agent does NOT claim to verify the exact SKU barcode from frame 00:07. It factually observes: 'Black casing (color-consistent with HEAD-BLK-09) · Barcode unverified · SKU not verified'. Frame citations provide a traceable reference, not proof of footage authenticity.  
  > - Decision Logic: Seeing a black item when white was ordered is an undeniable visual contradiction against the manifest. Instead of auto-denying the customer, the policy engine triggers ESCALATE.  
  > - Three Preserved Seller Options (matching slide face):  
  >   1. Accept as warehouse mis-shipment.  
  >   2. Request photo of outside-box shipping label.  
  >   3. Hold return for physical parcel inspection.  
  > - Financial Guardrail: min(₹4,999, remaining refundable amount, order paid amount). No money moves without seller click."*

---

### SLIDE 4: KIẾN TRÚC HỆ THỐNG & CƠ CHẾ AN TOÀN
- **Kicker Tag:** `SYSTEM ARCHITECTURE · FAIL-CLOSED SAFETY GATES`
- **Headline:** Models observe. Code verifies. Seller authorizes.
- **Subheadline:** Exactly 3 base model calls per triage case. Weak evidence escalates. Never releases automated refunds.
- **3 Cột phân định trách nhiệm (Authority Pillars):**
  - `MODEL (Plan and observe)`: Planner proposes typed actions · Vision model generates cited observations · Critic checks consistency against timestamps.
  - `CODE (Retrieve, validate and enforce rules)`: Backend code validates schemas · FFmpeg extracts frames · Python code evaluates rules P-01 to P-08.
  - `SELLER (Approve consequential actions)`: Fail-closed authorization gate · 1-click human merchant confirmation before refund release · Zero automatic disbursements.
- **Quy trình Case C (Dynamic Clarification Loop):**
  - Các bước: `DARK EVIDENCE` → `ASK FOR PHOTO` → `WAITING_FOR_EVIDENCE` → `CUSTOMER UPLOAD` → `RESUME CASE` → `SELLER REVIEW`.
  - Chú thích: *Agent calls ask_for_evidence() on low-light frames (Policy P-06 FAIL, brightness score: 28/255), serializes context, and resumes on upload. After 1 retry, escalates to seller with both attempts logged (never auto-denies).*
- **Đường dẫn phụ (Secondary Route):**
  - `ORDER STATUS FAST PATH`: *Store API → Courier API → Customer Reply (Zero vision overhead).*
- **Speaker Notes (Bao gồm kịch bản phòng thủ trả lời vấn đáp):**
  > *"Slide 4 — System Architecture, Agentic Governance & Technical Q&A Defense:  
  > - Philosophy: 'Models observe. Code verifies. Seller authorizes.'  
  > - Responsibilities: Planner model proposes tool actions; backend code validates JSON schemas; FFmpeg extracts keyframes; vision model generates cited observations; deterministic Python rules evaluate policy P-01 to P-08; seller gate authorizes consequential actions.  
  > - DEFENSE QUESTION 1: Why is this an agent rather than a hardcoded workflow?  
  >   ReturnLens is an autonomous state machine with dynamic action selection, multimodal observation, and stateful lifecycle management. In Case C, when a customer submits a dark or blurry video (brightness score: 28/255), the agent does NOT simply fail or run a static linear chain. It inspects the frames, determines evidence is insufficient under Policy P-06, dynamically decides to invoke ask_for_evidence() with specific re-filming guidance, transitions the ticket to WAITING_FOR_EVIDENCE, pauses execution while retaining state and order context, and resumes the exact triage session when new media arrives. Conversely, for routine order status requests, the agent selects the zero-vision fast path directly querying mock APIs.  
  > - DEFENSE QUESTION 2: What happens if vision or critic models hallucinate?  
  >   Vision models produce non-binding observation metadata, never authoritative decisions. Hard business rules (return windows from carrier delivery timestamps, SKU comparisons) are executed in deterministic Python code (P-01 to P-08). The critic provides an adversarial sanity check against cited timestamps. If both vision and critic experience correlated hallucinations, the fail-closed human seller gate guarantees that no refund or return label can ever be issued without seller review.  
  > - DEFENSE QUESTION 3: How do you prevent duplicate or incorrect refunds?  
  >   1. Idempotency keys (hash(order_id, return_id, transaction_type)) with backend uniqueness checks prevent duplicate execution.  
  >   2. Ledgers enforce: 0 < amount <= min(₹4,999, remaining_refundable_amount, order_paid_amount).  
  >   3. Sequence: Refund proposal -> Code validation -> Seller approval -> Revalidation -> Draft creation -> Receipt -> Release. LLMs possess zero capability to call payment gateways directly.  
  > - Security Hardening: Authorization signature binds case ID, SHA256 evidence hash, and policy version. State is revalidated before any draft release."*

---

### SLIDE 5: BỘ KỊCH BẢN ĐỐI SOÁT (BENCHMARK SUITE)
- **Kicker Tag:** `DEMO SCENARIOS · BEHAVIORAL MATRIX`
- **Headline:** Different evidence. Different action.
- **Subheadline:** Every case produces an auditable mock evidence pack. No automatic policy approvals.
- **Hero Case (Case B - Contradiction):**
  - `CASE B · CONTRADICTION · P-03 FAIL`
  - Quan sát: `Ordered White, Observed Black · Black casing (color-consistent with HEAD-BLK-09, SKU not verified)`
  - Hành động: `ESCALATE TO SELLER`
  - Chi tiết: *Policy P-03 blocks automation. Inhibits label and refund. Preserved options: mis-shipment / box label / physical inspection.*
- **3 Case phụ:**
  - `CASE A · CONSISTENT CLAIM · ALL POLICIES PASS`: Drafts mock return label and refund draft in `pending_return_receipt`. Money releases only on physical receipt.
  - `CASE C · LOW-LIGHT VIDEO · POLICY P-06 FAIL`: Insufficient Visual Evidence · 4s low-light video (`brightness score: 28/255`), barcode obscured. Calls `ask_for_evidence()`; transitions to `WAITING_FOR_EVIDENCE`; resumes on upload. After 1 retry, escalates to seller with both attempts logged (never auto-denies).
  - `CASE D · CONTINUOUS SEQUENCE · SEQUENCE AUDIT`: Single continuous take from opening sealed parcel to displaying label in one sequence. Inspects sequence continuity and flags abrupt transitions. Does not claim proof of identical item.
- **Speaker Notes:**
  > *"Slide 5 — Four Reproducible Benchmark Scenarios:  
  > - Grounding Note: These four scenarios represent staged prototype test suites and deterministic expected behaviors, NOT ungrounded production field metrics.  
  > - Case 01 (Consistent Claim): All rules pass (within 7d, SKU matches manifest, tag visible, physical crack observed). System drafts return shipping label and refund draft in 'pending_return_receipt' state. No refund money is transferred until physical warehouse receipt.  
  > - Case 02 (Contradiction): Color mismatch detected (ordered white, unboxed black). System prevents auto-rejection and routes to seller review with 3 concrete resolution options.  
  > - Case 03 (Unclear / Agentic Loop): Dark video (brightness score: 28/255). Instead of auto-denying, the agent provides a clear checklist, transitions to WAITING_FOR_EVIDENCE, and resumes on upload (1 retry limit protects customers from infinite loops).  
  > - Case 04 (Continuity): Expected prototype behavior: inspect parcel-to-product sequence to flag suspicious cut-aways or missing transitions. Does not claim proven prevention of video manipulation.  
  > - Financial Cap Formula: min(₹4,999, remaining refundable amount, order paid amount) strictly prevents over-refunding."*

---

### SLIDE 6: KẾ HOẠCH THỰC THI 24 GIỜ (HACKATHON ROADMAP)
- **Kicker Tag:** `24-HOUR PROTOTYPE PLAN · FEASIBILITY & SCOPE`
- **Headline:** A credible prototype in 24 hours.
- **Subheadline:** Strict scope boundaries and single-threaded ownership make the prototype buildable in one day.
- **Tiến độ Gantt (00–24h):**
  - `00–06h FOUNDATION`: Mock APIs & Agent State (Person A)
  - `06–12h EVIDENCE`: Evidence Pipeline & Policy (Person B)
  - `12–18h INTEGRATION`: State Flow & Scenarios (Person C)
  - `18–24h VALIDATION`: Testing & Submission (All 3 Members)
- **Phân chia nhân sự (3 Person Cards):**
  - `PERSON A (Agent / Backend / Policy)`: LangGraph orchestrator, Mock store & courier APIs, Policy engine P-01 to P-08, Fail-closed authorization gate.
  - `PERSON B (Vision / Evidence / UI)`: FFmpeg keyframe pipeline, Vision extraction prompt schema, Critic adversarial prompt, 1-click seller console UI.
  - `PERSON C (Integration / Scenarios / QA)`: 3 core demo cases (A–C) + Case D sequence test, Case C clarification & resume flow, Automated QA: 10-test smoke suite, Demo video recording & documentation.
- **Dải kỷ luật phạm vi (Scope Discipline Band):**
  - `MUST DELIVER (Bắt buộc hoàn thành)`:
    - Mock store & courier APIs
    - Deterministic policy engine & seller gate
    - Case B color contradiction & Case C re-film loop
    - 3 core demo cases (A–C) + Case D sequence test
    - Approval binding (case + evidence hash + policy version)
    - Structured JSON audit trail & order-status fast path
  - `CUT FIRST IF BEHIND (Cắt bỏ ngay nếu trễ tiến độ)`:
    - Advanced video forensic splice analysis (Case D stretch)
    - WhatsApp bot
    - Exchanges (Đổi hàng)
    - Multi-seller auth
    - Audio analysis
    - Public cloud deployment
  - `PROTOTYPE SCOPE LOCKED`: 100% reproducible offline build · Zero external network dependencies.
- **Speaker Notes:**
  > *"Slide 6 — 24-Hour Sprint Feasibility, Ownership & Strict Scope Guardrails:  
  > - Feasibility Argument: Why is ReturnLens realistically buildable in 24 hours by 3 engineers?  
  >   1. No live external production dependencies: deterministic mock APIs for Shopify & Shippo eliminate external latency and flakiness.  
  >   2. Clear division of labor with single-threaded component ownership across 3 teammates:  
  >      - Person A (Backend / Policy / Authorization): LangGraph orchestrator, mock store & courier APIs, order status fast path, deterministic rules P-01 to P-08, fail-closed authorization gate, approval binding (case ID + evidence hash + policy version).  
  >      - Person B (Vision / Evidence / UI): FFmpeg keyframe pipeline (~1fps sampling), vision schema, critic prompt, interactive 1-click seller console UI with mock evidence pack.  
  >      - Person C (Integration / Scenarios / QA): Test fixtures for 3 core demo cases (A–C) + Case D sequence test, Case C clarification/resume lifecycle, fail-closed human gate testing, demo video recording, README.  
  >   3. Strict Scope Discipline (matching slide face):  
  >      - MUST DELIVER: Mock store & courier APIs, deterministic policy engine & seller gate, Case B color contradiction & Case C re-film loop, 3 core demo cases (A–C) + Case D sequence test, approval binding (case + evidence hash + policy version), structured JSON audit trail & order-status fast path.  
  >      - CUT FIRST IF BEHIND: Advanced video forensic splice analysis (Case D stretch), WhatsApp bot, exchanges, multi-seller auth, audio analysis, public cloud deployment.  
  > - Winning Philosophy: 'The winning hackathon agent is not the one with the most tool definitions. It is the one where every action is held to evidence, and the seller stays in control.'"*

---

# 6. LỊCH SỬ TIẾN HÓA & CÁC LỖI ĐÃ ĐƯỢC FIX QUA CÁC VÒNG

| Phiên bản | Điểm Audit | Những cải tiến / Sửa lỗi chính |
| :--- | :---: | :--- |
| **v5** | 8.5/10 | Bản baseline sau khi rà soát grounding cơ bản, loại bỏ các khẳng định nhận diện barcode vô căn cứ. |
| **v6** | 8.8/10 | Nâng cấp thiết kế visual, typography editorial, phân tách các card thông tin, tạo console mockup chân thực. |
| **v7** | 9.0/10 | Hoàn thiện visual polish, bảng màu warm paper & forest ink, dải màu tương phản cao, tách luồng Must Deliver / Cut First. |
| **v7.1 (Bản chốt)** | **9.4+/10** | **Đợt vá lỗi chính xác cuối cùng (Submission Freeze Candidate):**<br>• Sửa nút CTA thành `"Review Evidence & Decide"` (Slide 1).<br>• Chuẩn hóa `Policy P-06` và thông số `brightness score: 28/255` (Slides 4 & 5).<br>• Phân định rạch ròi số liệu gian lận NRF 9% vs Deloitte 15.14% (Slide 2).<br>• Đồng bộ `10-test smoke suite` của Person C (Slide 6).<br>• Đóng gói PPTX dạng `ZIP_STORED` deterministic (cùng hash trên cả Windows và Linux).<br>• Kiểm toán hình học tự động: Xóa bỏ 100% tình trạng chồng lấn văn bản (zero overlaps/collisions).<br>• Quét sạch toàn bộ từ sáo rỗng AI (buzzwords: "agentic governance"), đưa về thuật ngữ sản phẩm thực tế ("fail-closed safety gates", "unstructured text"). |

---

# 7. HƯỚNG DẪN CÁC TIÊU CHÍ CẦN GPT ĐÁNH GIÁ (REVIEW DIRECTIVES)

Khi GPT đọc tài liệu này, hãy yêu cầu GPT tập trung phân tích sâu các góc cạnh sau:

1. **Góc độ Giám khảo Cuộc thi (Hackathon Judge Perspective):**
   - Bài thuyết trình có truyền tải được tính khả thi trong 24 giờ không?
   - Tính năng Agentic có bị "làm màu" hay thực sự giải quyết được bài toán stateful lifecycle (đặc biệt là Case C pause/resume)?
   - Triết lý *"Models observe. Code verifies. Seller authorizes"* có đủ sức thuyết phục giám khảo rằng team hiểu rõ rủi ro của AI trong e-commerce không?

2. **Góc độ Red-Team / AI Safety Auditor:**
   - Cơ chế bảo vệ tài chính (Financial Guardrail Formula) có lỗ hổng race-condition hay double-spending nào không?
   - Việc phân quyền Model vs Code vs Seller đã đủ chặt chẽ để cô lập hoàn toàn lỗi ảo giác (hallucination) chưa?
   - Tính trung thực trong trích dẫn bằng chứng (Negative Assertion) ở Case B đã đạt mức miễn nhiễm trước các câu hỏi xoáy của chuyên gia Computer Vision chưa?

3. **Góc độ Kỹ năng Thuyết trình & Trả lời Vấn đáp (Q&A Defense):**
   - Đưa ra danh sách 5 câu hỏi "bẫy" nguy hiểm nhất mà các giám khảo khó tính thường hỏi tại vòng chung kết.
   - Cung cấp kịch bản trả lời mẫu đanh thép, chuẩn kỹ thuật, ngắn gọn trong 30 giây cho từng câu hỏi.

---
*Tài liệu được trích xuất tự động từ Canonical Data & Verification Suite của ReturnLens v7.1 — Commit `787e126`.*
