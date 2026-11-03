# RETURNLENS V7.2 (PRECISION & HONEST GROUNDING) — FULL CONTEXT HANDOFF & REVIEW BRIEF

> **TÀI LIỆU BÀN GIAO TOÀN DIỆN DÀNH CHO GPT / REVIEWER ĐỘC LẬP**  
> *Bạn có thể tải tệp Markdown này lên ChatGPT (GPT-4o / GPT-o1) hoặc dán toàn bộ nội dung vào khung chat với prompt ở bên dưới.*

---

## PHẦN DÀNH CHO USER: CÂU LỆNH (PROMPT) GỢI Ý ĐỂ COPY VÀO GPT

```text
Bạn là một Giám khảo Kỹ thuật Cấp cao (Principal Technical Judge), Giám đốc Thiết kế Sản phẩm (Product Design Director) và Chuyên gia Đánh giá An toàn AI (AI Safety Auditor) tại cuộc thi AgentX Hackathon 2026.

Dưới đây là toàn bộ tài liệu bàn giao (Handoff Brief) của dự án "ReturnLens v7.2 — Precision & Honest Grounding Edition" thuộc Track PS-04 (Autonomous Support Agent for Solo D2C Merchants).

Hãy đọc kỹ toàn bộ tài liệu này (bao gồm bối cảnh bài toán, kiến trúc kỹ thuật, ngân sách gọi mô hình, đường tắt zero-LLM, chính sách an toàn tất định P-01 đến P-08, 4 benchmark test cases, toàn bộ nội dung & speaker notes của 6 slide, và kế hoạch thực thi 24h). Sau đó, hãy tiến hành một đợt REVIEW ĐỘC LẬP VÀ TOÀN DIỆN theo 7 tiêu chí:
1. Độ thuyết phục của Narrative & Pitch Flow trong 3 phút thuyết trình (Vấn đề của Solo Seller -> Star Demo -> Kiến trúc -> 4 Test Cases -> Roadmap 24h).
2. Mức độ giải quyết đúng đề bài Track PS-04 (Nỗi đau của Solo Merchant, tính khả thi trong môi trường thực tế).
3. Tính trung thực & phòng thủ bằng chứng (Evidentiary Grounding & Defensive Honesty — Tránh cạm bẫy ảo giác AI, thừa nhận trung thực giới hạn camera/mã vạch).
4. Kiến trúc Agentic & Cơ chế Fail-Closed Safety (Ngân sách 3 calls/pass, max 6 calls cho Case C, Zero-LLM Fast Path, State Machine có phục hồi phiên).
5. Hàng rào bảo vệ tài chính (Server-computed refund limits, trần ₹4,999, trạng thái pending_return_receipt, chống race condition bằng idempotency nonce).
6. Độ vững chắc của 5 câu trả lời bảo vệ kỹ thuật trước ban giám khảo (Model call explosion, Cold-start uncataloged items, Deepfake/Adversarial video, Fast path routing, Fail-closed authorization).
7. Chấm điểm tổng quan (thang điểm 10) và các khuyến nghị tinh chỉnh cuối cùng trước khi thuyết trình.
```

---

# TỔNG QUAN HỒ SƠ DỰ ÁN (PROJECT DOSSIER)

- **Tên dự án:** ReturnLens
- **Tagline:** *"Every return decision, backed by evidence."* (Mọi quyết định đổi trả đều có bằng chứng bảo chứng).
- **One-liner:** Nền tảng phân loại và xử lý khiếu nại đổi trả có bảo chứng bằng chứng số (Evidence-backed returns triage) dành riêng cho các nhà bán hàng trực tuyến độc lập (Solo D2C Merchants).
- **Cuộc thi:** AgentX Hackathon 2026 — Track PS-04: *Autonomous Support Agent for Online Sellers*.
- **Đội thi:** Team Rookie (3 thành viên: Person A - Agent/Backend/Policy, Person B - Vision/Evidence/UI, Person C - Integration/Scenarios/QA).
- **Mã nguồn (Repository):** `https://github.com/lenamkhanhh/hack4hack.git` (Nhánh: `main`).
- **Phiên bản hoàn thiện:** **ReturnLens v7.2 — Precision & Honest Grounding Edition**.
- **Tính chất hiện thực của Repository (Prototype Reality & Honest Demarcation):**
  - ReturnLens tại vòng thi này là một **Đề án Kiến trúc Hệ thống hoàn chỉnh (Architecture Proposal)** và **Bộ đặc tả kiểm thử tự động (Test Specification & Executable Prototype Baseline)**.
  - Dự án sử dụng bộ dữ liệu kiểm thử chuẩn (mock fixtures), trích xuất keyframe thực tế từ video, ghi log kiểm toán cục bộ (SQLite simulation), và quy trình xác thực tất định.
  - Dự án **chưa** kết nối webhook trực tiếp với Shopify live production hay API chuyển tiền tự động của Stripe/ngân hàng. Mọi tuyên bố kỹ thuật về chữ ký mã hóa, giới hạn tài chính và chống race condition được trình bày dưới dạng thiết kế kiến trúc chuẩn mực và mô phỏng bảo vệ an toàn (defense-in-depth architecture).
- **Bộ Deliverables chuẩn v7.2:**
  1. `ReturnLens_v7_2.pptx` & `deliverables/ReturnLens_v7_2.pptx` (1,421,127 B, SHA256: `01a6b6307bcf...`, 16:9, nhúng đủ Speaker Notes cho 6 slide, đóng gói `ZIP_STORED` deterministic).
  2. `ReturnLens_v7_2.pdf` & `deliverables/ReturnLens_v7_2.pdf` (1,824,379 B, SHA256: `020ddb2bbf69...`, Vector 6 trang).
  3. `ReturnLens_v7_2.html` & `deliverables/ReturnLens_v7_2.html` (3,138,338 B, SHA256: `e047974f678b...`, Interactive Console, offline-resilient font stacks).
  4. `ReturnLens_v7_2_preview.png` & `deliverables/ReturnLens_v7_2_preview.png` (891,812 B, SHA256: `8c45beb77ed2...`, Contact Sheet 2352×882).
  5. Bộ ảnh render PPTX 1920×1080: `src/assets/v7_2_pptx_renders/` kèm `render_manifest.json`.
  6. Extended Smoke Test: `scripts/smoke_test_v7_2.py` (10/10 PASS).
  7. Báo cáo chất lượng: `V7_2_QA_REPORT.md`.

---

# 1. TRIẾT LÝ CỐT LÕI & CÁC NGUYÊN TẮC BẢO VỆ AN TOÀN (CORE PRINCIPLES)

### Triết lý chủ đạo:
> **"Models observe. Code verifies. Seller authorizes."**  
> *(Mô hình AI quan sát. Mã nguồn xác minh. Người bán ủy quyền).*

### 5 Nguyên tắc vàng bảo vệ hệ thống:
1. **Không bao giờ tự động chuyển tiền hay tự động từ chối (Fail-Closed Human Seller Gate):**
   - AI **tuyệt đối không** có quyền tự động giải ngân, tự động phát hành nhãn vận chuyển hoàn tất hay tự động gửi tin nhắn từ chối khiếu nại của khách hàng.
   - Mọi hành động gây hậu quả tài chính (consequential action) đều phải dừng lại ở trạng thái dự thảo (`draft`) và yêu cầu sự xác nhận 1-click của người bán (Human-in-the-loop).
2. **Hàng rào bảo vệ tài chính do Server tính toán (Server-Computed Financial Guardrails):**
   - Số tiền hoàn lại được tính bằng mã nguồn cứng ở backend theo công thức:
     $$\text{Số tiền hợp lệ} \le \min(₹4,999, \text{tiền còn được hoàn}, \text{tiền khách đã trả})$$
   - LLM tuyệt đối không được tự sinh ra số tiền hoàn lại.
   - Trạng thái hoàn tiền luôn bị khóa ở mức `pending_return_receipt` — chỉ có thể giải ngân sau khi kiện hàng vật lý được quét nhập kho.
   - Ngăn chặn race condition bằng cặp khóa định danh duy nhất: `hash(order_id, return_id, action_nonce)`.
3. **Ngân sách gọi mô hình có kiểm soát chặt chẽ (Model Call Budget & Lifecycle Limits):**
   - **Routine Cases (A, B, D):** Đúng **3 model calls cho 1 lượt phân loại (triage pass)**:
     - `Planner`: Phân tích ý định và cấu trúc dữ liệu đơn hàng.
     - `Vision Extractor`: Trích xuất quan sát kèm mốc thời gian (cited timestamps).
     - `Critic`: Phản biện chéo đối chiếu với quy định chính sách.
   - **Dynamic Clarification Case (Case C):** Khi video unboxing quá tối hoặc mờ, agent yêu cầu khách quay lại. Lượt tải lên lại của khách kích hoạt Pass 2 (tối đa thêm 3 calls). Tổng vòng đời của 1 ca có retry bị giới hạn cứng ở mức **tối đa 6 calls**.
   - **Chống lặp vô tận (Infinite Loop Prevention):** Quy tắc cứng **tối đa 1 lần thử lại (1 retry)**. Nếu video gửi lại vẫn không đạt chuẩn, ca khiếu nại chuyển thẳng lên người bán xử lý thủ công kèm toàn bộ log.
4. **Đường tắt không dùng LLM cho tra cứu đơn hàng (Zero-LLM Fast Path):**
   - Các câu hỏi phổ biến thuộc đề bài PS-04 như *"Đơn hàng của tôi đang ở đâu?"*, *"Tra cứu trạng thái vận chuyển"* được bộ định tuyến (router) chặn ngay tại cổng và xử lý trực tiếp bằng truy vấn dữ liệu thuần (`/order/:id/status`).
   - Tiêu tốn **0 token LLM**, phản hồi <50ms, triệt tiêu 100% rủi ro hallucination.
5. **Động cơ chính sách tất định (Deterministic Policy Engine P-01 -> P-08):**
   - Toàn bộ logic nghiệp vụ được viết bằng code Python thuần túy, chạy độc lập ngoài context của LLM.

---

# 2. ĐẶC TẢ CHI TIẾT CHÍNH SÁCH TẤT ĐỊNH (POLICIES P-01 ĐẾN P-08)

Để tránh nhầm lẫn giữa việc xác nhận giao hàng và thời hạn đổi trả, ReturnLens v7.2 tách biệt rõ ràng:

- **Policy P-01 — Carrier Delivery Verification (Xác minh giao hàng thực tế):**  
  Kiểm tra dữ liệu quét của đơn vị vận chuyển (Shippo tracking scan). Xác nhận kiện hàng đã được giao tận tay khách (ví dụ: Shippo #SH-9012 xác nhận Delivered 4 ngày trước).
- **Policy P-02 — Security Tag Requirement (Yêu cầu tem niêm phong):**  
  Đối chiếu danh mục sản phẩm của Shopify. Nếu sản phẩm thuộc danh mục tai nghe cao cấp, hệ thống bắt buộc kiểm tra sự hiện diện của tem niêm phong / seal bọc hộp chưa bị rách trước khi unbox.
- **Policy P-03 — Color & Casing Consistency (Tính đồng nhất màu sắc & vỏ máy):**  
  Đối chiếu màu sắc quan sát được từ keyframe video với màu sắc trong hồ sơ đơn hàng Shopify. Nếu phát hiện sai lệch (khách đặt Matte White, quan sát thấy Black casing), kích hoạt cờ mâu thuẫn màu sắc (P-03 FAIL).
- **Policy P-04 — Return Policy Window Compliance (Tuân thủ khung thời hạn 7 ngày):**  
  Tính toán thời gian: $\Delta t = \text{request\_date} - \text{delivery\_date}$. Yêu cầu $\Delta t \le 7\text{ ngày}$. Trường hợp mẫu: Ngày 4 trên 7 $\rightarrow$ P-04 PASS.
- **Policy P-05 — Physical Defect Verification (Xác minh lỗi hư hỏng vật lý):**  
  Đối với khiếu nại hàng vỡ/hỏng (như Case A), keyframe trích xuất phải thể hiện rõ vết nứt/gãy cấu trúc cơ học tại thời điểm mở hộp.
- **Policy P-06 — Evidence Quality & Illumination Standard (Chuẩn chất lượng ánh sáng & khung hình):**  
  Đo lường độ sáng trung bình của các keyframe. Ngưỡng chấp nhận tối thiểu là $50/255$. Nếu $\text{brightness score} < 50/255$ (ví dụ Case C có $\text{brightness score} = 28/255$), kích hoạt P-06 FAIL và chuyển sang luồng hướng dẫn khách quay lại video.
- **Policy P-07 — Financial Guardrail Enforcement (Áp dụng trần tài chính):**  
  Mã nguồn máy chủ tự động giới hạn số tiền hoàn lại: $\text{amount} \le \min(₹4,999, \text{remaining\_refundable}, \text{order\_paid})$.
- **Policy P-08 — Cryptographic Authorization Binding (Ràng buộc chữ ký phê duyệt):**  
  Gói ủy quyền của người bán gắn liền chữ ký hàm băm: $\text{HMAC}(\text{case\_id} + \text{evidence\_sha256} + \text{policy\_version} + \text{nonce})$. Bất kỳ sự thay đổi nào đối với bằng chứng đều làm mất hiệu lực của lệnh phê duyệt.

---

# 3. BỐI CẢNH BÀI TOÁN & PHÂN BIỆT DỮ LIỆU GIAN LẬN (THE PROBLEM)

### Điểm nghẽn thực tế của Solo Merchant:
Solo D2C merchant kinh doanh phụ kiện âm thanh cá nhân (tai nghe, loa) phải một mình gánh vác: chăm sóc khách hàng, đóng gói, liên hệ vận chuyển và đối soát khiếu nại. Khi khách yêu cầu đổi trả, người bán bị kẹt giữa 4 nguồn dữ liệu phân mảnh:
1. **Chat khách hàng:** Văn bản tự do kèm video unboxing chưa được xác minh.
2. **Đơn hàng Shopify:** Thông tin kỹ thuật từ kho (SKU: HEAD-WHT-02, Màu: Matte White, Giá: ₹1,499).
3. **Trạng thái Shippo:** Lịch sử quét bưu tá (Đã giao 4 ngày trước).
4. **Chính sách cửa hàng:** 7 ngày đổi trả, bắt buộc còn nguyên seal.

**Hậu quả:** Không có hồ sơ bằng chứng hợp nhất (No shared evidence record). Người bán phải ra quyết định từ trí nhớ hoặc cảm tính:
- *Hoàn tiền bừa:* Mất hàng, mất tiền, bào mòn biên lợi nhuận mỏng manh.
- *Từ chối cứng nhắc:* Phá hủy uy tín thương hiệu và giá trị vòng đời khách hàng (LTV).

### Phân biệt số liệu gian lận chuẩn xác:
- **9.0% — Return Fraud (NRF/Appriss 2024):** Gian lận hình sự nghiêm ngặt (tráo hàng unbox, gửi hộp rỗng, lừa đảo chiếm đoạt tài sản — quy mô $101 tỷ USD tại bán lẻ Mỹ).
- **15.14% — Fraud + Policy Abuse (Appriss/Deloitte 2024):** Gian lận hình sự kết hợp lạm dụng chính sách (wardrobing — mua dùng thử dịp lễ rồi trả lại, khiếu nại sai sự thật).
*Hai số liệu này đo lường hai phạm vi khác nhau và được đồng bộ chuẩn xác trên toàn bộ deliverables v7.2.*

---

# 4. KỊCH BẢN ĐỐI SOÁT & 4 BENCHMARK TEST CASES

### Case A — Khiếu nại vỡ hỏng hợp lệ (Consistent Claim - ORD-1042):
- **Bằng chứng:** Video unboxing 1080p đủ sáng, tem niêm phong còn nguyên, phát hiện vết nứt vật lý trên gọng tai nghe khi vừa mở hộp, trong thời hạn ngày 4/7.
- **Xử lý:** Đạt toàn bộ P-01 đến P-08. Agent chuẩn bị sẵn bản nháp mã vận đơn đổi trả và bản nháp hoàn tiền ở trạng thái `pending_return_receipt`.
- **An toàn:** Tiền **chưa** giải ngân ngay; lệnh chuyển tiền chỉ kích hoạt sau khi kiện hàng được bưu tá quét nhận tại kho.

### Case B — Tráo màu / Lệch SKU (Star Demo - RT-8821 / ORD-7729):
- **Đơn hàng:** Khách đặt Tai nghe Studio màu Trắng (Matte White, SKU `HEAD-WHT-02`, giá ₹1,499).
- **Quan sát từ Video:** Frame 00:07 thể hiện tai nghe màu Đen (Black casing).
- **Nguyên tắc Grounding trung thực:**
  - Agent ghi nhận chính xác: *"Observed: Black casing (color-consistent with HEAD-BLK-09) · Barcode unverified · SKU not verified"*.
  - Tuyệt đối **không overclaim** rằng camera AI đã quét được mã vạch barcode hay khẳng định chắc chắn 100% mã SKU `HEAD-BLK-09`.
- **Xử lý:** Kích hoạt `Policy P-03 Color Contradiction FAIL`. Chặn đứng tự động hóa, không tạo nhãn, không tạo nháp hoàn tiền.
- **3 Quyền lựa chọn của Seller (Đúng 3 quyền này, tuyệt đối KHÔNG có đổi hàng - Exchange):**
  1. *Accept warehouse mis-shipment* (Chấp nhận lỗi kho gửi nhầm hàng đen).
  2. *Request outside-box label photo* (Yêu cầu khách chụp ảnh tem vận chuyển dán ngoài hộp carton).
  3. *Hold for parcel inspection* (Giữ hàng kiểm tra trực tiếp khi bưu tá mang về).

### Case C — Video quá tối / Vòng lặp thu thập lại bằng chứng (Dynamic Clarification Loop):
- **Bằng chứng:** Video 4 giây bị thiếu sáng nghiêm trọng, rung lắc, chỉ số độ sáng ghi nhận: `brightness score: 28/255 < 50/255`.
- **Xử lý:** Kích hoạt `Policy P-06 FAIL` (Chuẩn ánh sáng không đạt).
- **Cơ chế Agentic:** Agent gọi hàm `ask_for_evidence()` kèm hướng dẫn thân thiện (bật đèn, giữ yên máy quay rõ tem), serialize trạng thái hội thoại sang `WAITING_FOR_EVIDENCE`, và tự động phục hồi phiên khi khách tải lên video mới.
- **Ngân sách:** Tải video mới kích hoạt Pass 2 (tối đa thêm 3 calls), tổng lifecycle tối đa 6 calls.
- **Chống lặp:** Giới hạn cứng 1 lần thử lại (1 retry). Nếu vẫn không đạt, escalate thẳng lên người bán.

### Case D — Kiểm tra tính liền mạch chuỗi khung hình (Sequence Continuity Test):
- **Bằng chứng:** Video cắt ghép hoặc có hiện tượng gián đoạn giữa lúc unbox và lúc tráo sản phẩm.
- **Xử lý:** Agent kiểm tra tính liên tục của chuỗi khung hình (sequence continuity inspection). Khi phát hiện bước nhảy khung hình đáng ngờ, agent hạ điểm tin cậy và gắn cờ cần seller kiểm tra thủ công.

---

# 5. CHI TIẾT 6 SLIDES & FULL TECHNICAL SPEAKER NOTES (KÈM BẢO VỆ 5 CÂU HỎI HÓC BÚA)

### Slide 1: Product Reveal & Verifiable Evidence Console
- **Headline:** ReturnLens
- **Subheadline:** Every return decision, backed by evidence.
- **Left Column:** Bối cảnh Solo Merchant, giải pháp trích xuất keyframe video và đối soát chính sách. Khối triết lý cốt lõi: *"Models observe. Code verifies. Seller authorizes."* (Zero automated refunds · Zero automated denials).
- **Right Column (macOS Console Mockup):**
  - Order Truth: `HEAD-WHT-02 (Matte White)`, ₹1,499 paid, Security Tag Required (P-02), Delivered 4d ago (Shippo #SH-9012, P-01 verified), Return Window: Day 4/7 (P-04 PASS).
  - Observed Video Frame 00:07: Black casing (color-consistent with HEAD-BLK-09), Barcode: Unverified, Exact SKU: Not verified, Lighting: Sufficient.
  - Contradiction Banner: `P-03 COLOR CONTRADICTION: Observed black casing conflicts with ordered Matte White specification. Exact SKU unverified.`
  - Action Bar: `● SELLER GATE (FAIL-CLOSED)`, Nút phụ `Request Box Label`, Nút chính: **`Review Evidence & Decide →`**.
- **Speaker Notes (Trích đoạn):**
  > "Chào ban giám khảo, đây là ReturnLens... Hãy nhìn góc dưới bên phải: nút bấm ghi rõ 'Review Evidence & Decide' thay vì tự động hoàn tiền. Hệ thống của chúng tôi không bao giờ thay thế quyền phán quyết của người bán."

### Slide 2: The Problem: 4 Disconnected Systems
- **Headline:** One return. Four disconnected systems. Zero shared record.
- **Visual:** 4 thẻ nguồn dữ liệu (Chat khách, Đơn Shopify, Vận chuyển Shippo, Chính sách shop) hội tụ về vùng trung tâm thể hiện khoảng trống kiểm toán.
- **Số liệu gian lận phân biệt:**
  - `9.0% Return Fraud (NRF 2025: criminal only)`: Gian lận hình sự nghiêm ngặt.
  - `15.14% Fraud + Policy Abuse (Appriss/Deloitte 2024: criminal + abuse)`: Gian lận kết hợp lạm dụng chính sách.

### Slide 3: Star Demo: Case B Evidence Comparison
- **Headline:** Case B: The Color Swap. Caught in 7 seconds.
- **Visual:** Thẻ so sánh trực quan giữa ảnh studio sản phẩm trắng và ảnh trích xuất video tai nghe đen tại 00:07 với huy hiệu lệch màu `≠`. Bảng đối chiếu chính sách tất định và 3 quyền lựa chọn của seller.

### Slide 4: System Architecture & Governance (KÈM PHÒNG THỦ 5 CÂU HỎI KỸ THUẬT)
- **Headline:** Models observe. Code verifies. Seller authorizes.
- **Visual:** Nền tối Obsidian (`#0B1613`), quy trình 6 bước với đúng 3 model calls được đánh dấu rõ ràng. Khối Zero-LLM Fast Path cho tra cứu đơn hàng. Khối Dynamic Clarification Loop cho Case C (`WAITING_FOR_EVIDENCE`, max 6 calls).
- **FULL SPEAKER NOTES — PHÒNG THỦ 5 CÂU HỎI HÓC BÚA NHẤT CỦA GIÁM KHẢO:**
  1. **Câu hỏi 1 (Model Call Explosion & Cost):**  
     *"Nếu khách hàng gửi tin nhắn rác hoặc video không liên quan, chi phí gọi mô hình của bạn có bị bùng nổ không?"*  
     $\rightarrow$ **Trả lời:** "Hệ thống áp dụng 3 tầng kiểm soát nghiêm ngặt: (1) Fast Path Router lọc các câu hỏi tra cứu đơn hàng thông thường bằng code SQL thuần, tiêu tốn 0 token LLM; (2) Mỗi lượt triage chỉ dùng đúng 3 calls có cấu trúc (Planner, Vision, Critic); (3) Đối với ca thiếu bằng chứng như Case C, chúng tôi chỉ cho phép tối đa 1 lần retry (Pass 2 thêm tối đa 3 calls), giới hạn trần toàn bộ vòng đời là 6 calls. Nếu vẫn không đạt, ca khiếu nại chuyển thẳng cho seller, triệt tiêu hoàn toàn rủi ro bùng nổ chi phí."
  2. **Câu hỏi 2 (Cold-Start & Uncataloged Products):**  
     *"Hệ thống xử lý ra sao nếu cửa hàng thêm sản phẩm mới mà chưa kịp cập nhật metadata màu sắc hoặc tem niêm phong vào hệ thống?"*  
     $\rightarrow$ **Trả lời:** "ReturnLens thiết kế theo nguyên tắc Fail-Closed. Nếu dữ liệu Shopify thiếu thông tin màu sắc hoặc thuộc tính tem niêm phong, Policy Engine sẽ đánh dấu trạng thái 'INSUFFICIENT_CATALOG_TRUTH' và chuyển hồ sơ về bàn làm việc của seller thay vì để mô hình tự suy đoán. Người bán có thể gán nhãn nhanh và cập nhật catalog ngay trong giao diện."
  3. **Câu hỏi 3 (Video Deepfake & Hallucination Defense):**  
     *"Làm sao bạn ngăn chặn việc người mua dùng video AI tạo sinh hoặc video cắt ghép từ trên mạng để lừa hệ thống?"*  
     $\rightarrow$ **Trả lời:** "Chúng tôi không bao giờ tin tưởng hoàn toàn vào một khẳng định của vision model. Hệ thống áp dụng 3 chốt chặn: (1) Vision Extractor bắt buộc phải trích dẫn timestamp cụ thể kèm tọa độ bounding box; (2) Policy P-06 và Case D kiểm tra tính liền mạch khung hình và độ phân giải; (3) Quan trọng nhất: Ngay cả khi video hoàn hảo, hệ thống cũng chỉ tạo nháp ở trạng thái `pending_return_receipt`, tiền chỉ được giải ngân sau khi kiện hàng vật lý được quét nhận tại kho bãi của seller."
  4. **Câu hỏi 4 (Fast Path vs. Triage Routing):**  
     *"Làm thế nào để hệ thống phân biệt yêu cầu hỏi trạng thái đơn hàng thông thường với một khiếu nại đổi trả phức tạp?"*  
     $\rightarrow$ **Trả lời:** "Ingress Router sử dụng bộ phân loại ý định tất định (deterministic intent classification kết hợp regex và rule khớp từ khóa). Nếu truy vấn chỉ chứa mã vận đơn hoặc câu hỏi 'đơn hàng ở đâu', nó được rẽ nhánh vào Zero-LLM Fast Path (phản hồi <50ms, 0 token). Chỉ khi xuất hiện khiếu nại đổi trả hoặc tệp video đính kèm, luồng Triage State Machine mới được khởi động."
  5. **Câu hỏi 5 (Financial Safety & Idempotency):**  
     *"Làm sao đảm bảo không xảy ra race condition dẫn đến việc hoàn tiền 2 lần cho cùng một đơn hàng?"*  
     $\rightarrow$ **Trả lời:** "Hệ thống bảo vệ tài chính ở 3 lớp: (1) Server tính toán trần hoàn tiền cứng $\le \min(₹4,999, \text{remaining}, \text{paid})$; (2) Lệnh ủy quyền của seller được ký bằng chữ ký băm ràng buộc `hash(case_id, evidence_sha256, policy_version, nonce)`; (3) Cơ sở dữ liệu SQLite áp dụng unique constraint trên `hash(order_id, return_id, action_nonce)`, đảm bảo tính lũy thỏa (idempotency) tuyệt đối — một yêu cầu đã phê duyệt không bao giờ có thể được kích hoạt lần thứ hai."

### Slide 5: Evaluation Suite: 4 Benchmark Cases
- **Headline:** 4 realistic scenarios. Deterministic outcomes.
- **Visual:** Layout bất đối xứng tôn vinh Case B (Hero card với ảnh video 00:07), bên cạnh 3 thẻ Case A (vỡ hỏng hợp lệ), Case C (video tối 28/255 < 50/255, P-06 FAIL), Case D (kiểm tra tính liên tục chuỗi khung hình).

### Slide 6: 24-Hour Hackathon Execution Roadmap
- **Headline:** 24-hour execution roadmap. Production discipline.
- **Visual:** Biểu đồ Gantt 4 giai đoạn (00–24h), phân công 3 kỹ sư (Person A, B, C), dải phân định phạm vi thi công nghiêm ngặt:
  - **Must Deliver (Bắt buộc hoàn thành):** 3-agent orchestration pipeline, deterministic policies P-01 đến P-08, 4 benchmark test fixtures (Cases A–D), fail-closed seller console, và bộ kiểm thử tự động 10 test.
  - **Cut First (Cắt bỏ đầu tiên nếu thiếu thời gian):** Tích hợp webhook Shopify live production, thanh toán tự động qua Stripe, OCR quét mã vạch trực tiếp, và thuật toán video forensics nâng cao cho Case D.

---

# 6. BẢNG KIỂM TRA CHẤT LƯỢNG VÀ HASH FILE DELIVERABLES

| Deliverable File | Kích thước | SHA256 Checksum |
| :--- | :--- | :--- |
| `ReturnLens_v7_2.pptx` | 1,421,127 B | `01a6b6307bcfdface93929d9cd21558b285818be2eb24d4ecb65ba9a5cfe6af6` |
| `deliverables/ReturnLens_v7_2.pptx` | 1,421,127 B | `01a6b6307bcfdface93929d9cd21558b285818be2eb24d4ecb65ba9a5cfe6af6` |
| `ReturnLens_v7_2.pdf` | 1,824,379 B | `020ddb2bbf69271aeb55a98e5638d2dadea89dbd37d0ee2f4eeccc0ca519b711` |
| `deliverables/ReturnLens_v7_2.pdf` | 1,824,379 B | `020ddb2bbf69271aeb55a98e5638d2dadea89dbd37d0ee2f4eeccc0ca519b711` |
| `ReturnLens_v7_2.html` | 3,138,338 B | `e047974f678be5276f5827e1460cca5c3d2376e9aa19b2e0ad028c868dd6075f` |
| `deliverables/ReturnLens_v7_2.html` | 3,138,338 B | `e047974f678be5276f5827e1460cca5c3d2376e9aa19b2e0ad028c868dd6075f` |
| `ReturnLens_v7_2_preview.png` | 891,812 B | `8c45beb77ed2ac39261fe8ebdafe18f8d9b0068495623a4c1d9412174c4c1f18` |
| `deliverables/ReturnLens_v7_2_preview.png` | 891,812 B | `8c45beb77ed2ac39261fe8ebdafe18f8d9b0068495623a4c1d9412174c4c1f18` |

---

# 7. KHUNG TIÊU CHÍ ĐÁNH GIÁ DÀNH CHO GPT REVIEWER

Khi tiến hành đánh giá tệp tài liệu này, hãy dựa trên 7 tiêu chuẩn sau:
1. **Pitch Flow (Trọng số 20%):** Câu chuyện 6 slide có tạo ra ấn tượng chuyên nghiệp như một sản phẩm thương mại thật sự không?
2. **Track Relevance (Trọng số 15%):** Có giải quyết đúng nỗi đau số 1 của Solo Merchant (bị kẹt giữa 4 hệ thống, sợ mất tiền và mất khách) không?
3. **Evidentiary Grounding & Defensive Honesty (Trọng số 20%):** Các bằng chứng đưa ra có khiêm tốn, trung thực, tránh overclaim (như không nhận bừa barcode) không?
4. **Agentic System Architecture & Safety (Trọng số 20%):** Cơ chế 3 calls/pass, max 6 calls, Zero-LLM Fast Path, và vòng lặp Case C có khả thi và chặt chẽ không?
5. **Financial & Operational Guardrails (Trọng số 10%):** Hàng rào bảo vệ tài chính (Server cap ₹4,999, pending_return_receipt, chống race condition) có đủ an toàn để doanh nghiệp áp dụng không?
6. **Defense Readiness (Trọng số 10%):** Kịch bản bảo vệ 5 câu hỏi có đủ đanh thép và thuyết phục giám khảo kỹ thuật khó tính không?
7. **Deliverables Engineering Quality (Trọng số 5%):** Khả năng tái lập 100%, đồng bộ hash, kiểm thử hình học tự động và bảo tồn lịch sử v5/v6/v7/v7.1.
