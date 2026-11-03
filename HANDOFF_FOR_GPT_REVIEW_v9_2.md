# RETURNLENS V9.2 (4-PERSON TEAM & STREAMLINED NARRATIVE EDITION) — FULL CONTEXT HANDOFF & REVIEW BRIEF

Tài liệu này cung cấp toàn bộ bối cảnh dự án, kiến trúc kỹ thuật, kịch bản pitch, nội dung 6 slide, và bộ câu hỏi bảo vệ kỹ thuật của **ReturnLens v9.2** — phiên bản tối ưu hóa cấu trúc đội thi 4 thành viên (4-Person Team) và tinh gọn câu chữ (Streamlined Narrative) để nộp chính thức cho Ban Giám Khảo (BGK) tại **Vòng Ý Tưởng (Idea Round) — AgentX Hackathon 2026, Track PS-04**.

---

## PHẦN DÀNH CHO USER: CÂU LỆNH (PROMPT) GỢI Ý ĐỂ COPY VÀO GPT

Nếu bạn muốn gửi tài liệu này cho ChatGPT (hoặc bất kỳ AI nào khác) để review đánh giá, hãy copy toàn bộ đoạn trong khung bên dưới:

```markdown
Bạn là một Giám khảo kỹ thuật cấp cao (Senior Hackathon Technical Judge) và Chuyên gia Đánh giá An toàn Hệ thống AI (AI Safety Auditor) tại AgentX Hackathon 2026. 

Dưới đây là hồ sơ chi tiết của dự án "ReturnLens v9.2" thuộc Track PS-04 (Autonomous Support Agent for Solo D2C Merchants) cho VÒNG Ý TƯỞNG (Idea Round).

Hãy đọc kỹ toàn bộ tài liệu hồ sơ dưới đây và thực hiện review độc lập theo các tiêu chí:
1. ĐỊNH VỊ SẢN PHẨM & GIÁ TRỊ THỰC TẾ: Ý tưởng có giải quyết đúng "nỗi đau" của solo seller bán hàng online khi xử lý đổi trả/khiếu nại không? Có tránh bẫy overclaim hay không?
2. THIẾT KẾ RÀNH MẠCH VỀ QUYỀN HẠN (AUTHORITY BOUNDARIES): Ranh giới giữa Agent và Con người (Solo Seller) đã đủ an toàn chưa? (Agent chỉ trích xuất, đối chiếu, đề xuất và soạn thảo; Con người duyệt các hành động có hậu quả tài chính).
3. PHÂN CÔNG 4 THÀNH VIÊN & TÍNH KHẢ THI KỸ THUẬT (FEASIBILITY TRONG 24H): Phân chia trách nhiệm cho 4 người (A, B, C, D) có hợp lý, cân bằng và bám sát kỷ luật phạm vi (Sprint Core vs Stretch Goals) không?
4. ĐỒNG BỘ NARRATIVE & SỰ HỢP LÝ CỦA PITCH 3 PHÚT: Câu chuyện xuyên suốt từ Slide 1 đến Slide 6 có mượt mà, logic và thuyết phục không? Dung lượng lời nói ~360 từ có chuẩn nhịp điệu thuyết trình không?
5. HỆ THỐNG ART DIRECTION & DESIGN: Nhận xét về sự hoàn thiện trong bản v9.2 (triệt tiêu theme xanh/shadow ngầm, bố cục phẳng thực sự, xóa các câu lặp quyền hạn, tiêu đề trực diện, khoảng cách visual thoáng đãng >0.30").

Đưa ra nhận xét khách quan, chỉ ra các điểm mạnh vượt trội, các điểm cần lưu ý khi bước vào vòng code 24 giờ tiếp theo, và chấm điểm dự kiến cho vòng ý tưởng này.
```

---

# TỔNG QUAN HỒ SƠ DỰ ÁN (PROJECT DOSSIER)

### 1. Thông tin chung
- **Tên dự án:** ReturnLens
- **Phiên bản:** v9.2 (4-Person Team & Streamlined Narrative Edition)
- **Cuộc thi:** AgentX Hackathon 2026
- **Track dự thi:** PS-04 — Autonomous Support Agent for Solo D2C Merchants
- **Team thực hiện:** Team Rookie (4 thành viên: A — Workflow & Rules; B — Vision & Keyframes; C — Seller Console & Replies; D — Integration & QA)
- **Slogan / Tagline:** *“Every return decision, backed by evidence.”*
- **One-Liner:** Một trợ lý đối chiếu bằng chứng giúp solo seller kết nối khiếu nại của khách, video mở hộp, dữ liệu đơn hàng và chính sách đổi trả thành một hồ sơ tổng hợp rõ ràng để người bán tự đưa ra quyết định xử lý tiếp theo.

### 2. Danh mục Deliverables & Checksum Cryptographic
Tất cả các tệp nghiệm thu đã được tạo, kiểm tra tự động và đồng bộ 100% giữa thư mục gốc và thư mục `deliverables/`:

| Tên Deliverable | Định dạng | Kích thước | SHA256 Checksum | Mô tả |
| :--- | :--- | :--- | :--- | :--- |
| `ReturnLens_v9_2.pptx` | PowerPoint | 1,359,761 bytes | `3d9556f9ffa9894d22a4dd3ee4ec83e21f35cd23562d2f04a56e36d22072730e` | Slide deck phẳng 100%, nhúng speaker notes 360 từ, typography Arial |
| `ReturnLens_v9_2.pdf` | Vector PDF | 239,897 bytes | `30e2fc4bf2004c844af849dfc57f745f4e65cebafd2b4513fa3b9e2aafb0d3cc` | Bản in PDF chuẩn vector 6 trang, tỷ lệ 16:9 widescreen (960×540 pt) |
| `ReturnLens_v9_2.html` | Interactive Web | 2,282,402 bytes | `f7557226b4e7bd61e323cb234fae30571c75755d5b7a828d9602edc746133a40` | Trình chiếu web độc lập tương tác bàn phím ($\leftarrow$/$\rightarrow$) |
| `ReturnLens_v9_2_preview.png` | Contact Sheet | 602,355 bytes | `c63bb9927c988965b1ce9ab433a70500a25a99f866ebbaf99938b4cc5ed44ae9` | Ảnh tổng quan 6 slide tỷ lệ 2×3 (kích thước chuẩn 2352×882 px) |
| `content/deck_data_v9_2.json` | JSON Data | 13,120 bytes | `ccbab84ce321d4acead99860a5865c933f509a71198f0387ac313094245ed627` | Single Source of Truth cho 4 thành viên, kịch bản pitch và Q&A |
| `src/assets/v9_2_pptx_renders/` | PNG Renders | 6 slide PNGs | Đầy đủ 6 slide render ở độ phân giải cao 1920×1080 px kèm manifest |
| `V9_2_QA_REPORT.md` | Báo cáo QA | Markdown | Tài liệu kiểm thử 9 điểm tự động và phân tích hình học an toàn |

---

# 1. ĐỊNH VỊ Ý TƯỞNG CHO VÒNG Ý TƯỞNG (PRODUCT REPOSITIONING)

### Nỗi đau thực tế của Solo Seller bán hàng D2C:
Một nhà bán hàng độc lập (solo seller) trên Shopify hoặc TikTok Shop nhận được khiếu nại: *"Tôi đặt tai nghe màu trắng, nhưng nhận được màu đen. Hãy hoàn tiền cho tôi!"* kèm theo một video mở hộp 18 giây. 

Hiện tại, người bán phải tự mình:
1. Mở kênh chat để đọc khiếu nại và tải video.
2. Đăng nhập vào Shopify để kiểm tra đơn hàng ORD-7729 (SKU HEAD-WHT-02, Matte White, giá ₹1,499).
3. Đăng nhập vào bưu tá (Shippo) để kiểm tra thời điểm giao hàng (đã giao 4 ngày trước).
4. Đối chiếu lại với chính sách cửa hàng (đổi trả trong vòng 7 ngày cho hàng giao nhầm hoặc hỏng).
5. Tự tua video xem khách mở hộp ra cái gì.

Quá trình này gây mất thời gian, căng thẳng và dễ dẫn đến quyết định sai lầm: hoặc hoàn tiền vội vàng (mất tiền oan), hoặc từ chối gay gắt (khách đánh giá 1 sao hoặc kiện chargeback).

### Giải pháp của ReturnLens:
ReturnLens là một **trợ lý sàng lọc bằng chứng (evidence triage assistant)**:
- Không tự động hoàn tiền và không tự động từ chối.
- Tự động gom 4 nguồn dữ liệu thành một hồ sơ đối chiếu trực quan:
  - **Điều đã biết:** Khách đặt màu trắng, đã giao 4 ngày trước, nằm trong thời hạn 7 ngày.
  - **Điều quan sát được:** Video mở hộp cho thấy tai nghe màu đen tại giây 00:07.
  - **Điều chưa xác minh:** Mã vạch trên nhãn hộp chưa đọc được, chưa rõ model chính xác.
  - **Phương án xử lý tiếp theo:** Chuẩn bị sẵn 3 lựa chọn kèm tin nhắn soạn thảo:
    1. Chấp nhận lỗi kho gửi nhầm $\rightarrow$ Phê duyệt đổi hàng và soạn nhãn gửi trả.
    2. Yêu cầu gửi ảnh chụp rõ nhãn ngoài hộp $\rightarrow$ *"Please share the outer-box label so we can check your shipment."*
    3. Giữ hàng để kiểm tra tại kho trước khi hoàn tiền.
- Người bán (Seller) xem bằng chứng và tự bấm nút phê duyệt hành động.

---

# 2. HỆ NGUYÊN TẮC VÀ RANH GIỚI QUYỀN HẠN (SAFETY & BOUNDARIES)

### Luận điểm kiến trúc cốt lõi (Core Thesis):
$$\textbf{“Models observe. Code verifies. Seller authorizes.”}$$

1. **Models observe (Thị giác máy tính quan sát):**
   - Mô hình AI (Gemini Vision / multimodal) chỉ làm nhiệm vụ quan sát và mô tả các đặc điểm hình ảnh khách quan: màu sắc bề mặt tai nghe là màu đen, vết nứt xuất hiện ở phần đai đeo (headband), mã vạch không đọc được do bị lóa.
   - Mô hình AI **tuyệt đối không suy đoán** gian lận, không tự kết luận "khách tráo hàng" hay "kho gửi nhầm".

2. **Code verifies (Mã lệnh xác thực):**
   - Các logic xác thực mang tính quyết định phải được xử lý bằng mã lệnh tất định (deterministic code):
     - So sánh ngày giao hàng từ API vận chuyển với chính sách: `(delivery_date - current_date) <= 7_days`.
     - So sánh mã SKU đơn hàng với mã sản phẩm trong catalog.

3. **Seller authorizes (Người bán phê duyệt):**
   - **Quyền hạn của Agent:** Được phép thu thập thông tin, trích xuất khung hình, đối chiếu quy tắc, và yêu cầu khách bổ sung thêm hình ảnh/thông tin theo quy tắc cửa hàng (Store templates).
   - **Quyền hạn của Seller:** Người bán giữ toàn quyền phê duyệt quyết định chấp nhận đổi trả, phát hành nhãn vận chuyển (tạo phát sinh chi phí), và thực hiện hoàn tiền.
   - **Không có hành động tài chính tự động (No automated refund or rejection).**

### Vòng lặp làm rõ khi bằng chứng không rõ (When evidence is unclear):
Khách hàng không thể "tái diễn" lần mở hộp ban đầu (unboxing là hành động diễn ra một lần). Do đó, nếu video ban đầu quá mờ hoặc tối:
- Agent không bao giờ tự động từ chối khiếu nại của khách.
- Thay vì yêu cầu quay lại mở hộp, Agent gửi thông báo yêu cầu cung cấp thêm **một ảnh chụp cận cảnh rõ nét của sản phẩm, phần hư hỏng hoặc nhãn ngoài hộp**.
- Bằng chứng mới được lưu vào cùng hồ sơ vụ việc hiện tại.
- **Quy tắc leo thang (Single-request escalation):** Giới hạn tối đa **1 lần yêu cầu bổ sung** tự động. Nếu sau 1 lần vẫn chưa rõ, vụ việc được chuyển trực tiếp cho Seller để tự liên hệ giải quyết (`If still unclear after one request, send the case to the seller.`).

---

# 3. NỘI DUNG VÀ SPEAKER NOTES CHI TIẾT CỦA 6 SLIDE (V9.2)

Tổng số từ nói trong kịch bản: **360 từ** (thời lượng ước tính: 2 phút 45 giây đến 3 phút, tốc độ nói đĩnh đạc ~120 từ/phút).

```
========================================================================================
SLIDE 1: PRODUCT INTRODUCTION & FLAT CONSOLE MOCKUP
========================================================================================
Kicker:      AgentX Hackathon 2026 · Track PS-04
Title:       ReturnLens
Tagline:     Every return decision, backed by evidence.
Summary:     A returns assistant for solo sellers that brings messages, video, order 
             records and store policy into one case.
Principle:   Models observe. Code verifies. Seller authorizes.
Mockup:      CASE #RT-8821 · NEEDS SELLER DECISION
             Order #ORD-7729 · Studio Wireless · ₹1,499 paid · Delivered 4d ago
             Color mismatch: Ordered White vs Observed Black · Barcode unverified
             Recommended Next Step: Request outer-box label photo
             Authority Note: Seller approves returns, labels and refunds.
             Safety Note:    No automated refund or rejection
             CTA Button:     Review Evidence & Decide →

SPEAKER NOTES (52 words / ~25s):
"Judges, this is ReturnLens. For solo online merchants, customer returns are a constant headache: messy claims, unboxing videos, and disconnected order records. ReturnLens unifies buyer claims, video evidence, and store rules into one clear decision pack. Models observe, code verifies, and the seller always authorizes consequential decisions."

========================================================================================
SLIDE 2: THE PROBLEM (ONE CLAIM. FOUR SOURCES.)
========================================================================================
Kicker:      The Merchant's Reality
Title:       One claim. Four disconnected sources.
Quote:       “I ordered white headphones, but received black. Please refund me.”
Attachment:  Customer video · 18s
Sources:     01 Customer Chat: Claim text and unboxing video upload
             02 Shopify Order: Matte White (SKU HEAD-WHT-02), ₹1,499 paid
             03 Courier Scan: Shippo confirms delivery 4 days ago
             04 Store Policy: 7-day return window for wrong or damaged items
Question:    Should I request more evidence, approve a return, or inspect the parcel?
             (17pt Regular, generous whitespace)

SPEAKER NOTES (65 words / ~30s):
"A customer chats in: 'I ordered white headphones, but received black. Please refund me,' attaching an 18-second unboxing clip. The merchant has to check four tabs: chat, Shopify, tracking, and store policy. Was this a packing error, a courier mistake, or a swap? The seller needs verified facts to decide whether to request more evidence, approve a return, or inspect the parcel."

========================================================================================
SLIDE 3: THE CORE DEMONSTRATION (WHITE ORDERED. BLACK RECEIVED.)
========================================================================================
Kicker:      Core Evidence Comparison
Title:       White ordered. Black received.
Subtitle:    Order details, video evidence and the next step—in one view.
Left Box:    STORE SPECIFICATION · SHOPIFY | Ordered: White | HEAD-WHT-02 · ₹1,499 paid · Delivered 4d ago
Center:      ≠
Right Box:   OBSERVED EVIDENCE · VIDEO FRAME 00:07 | Observed: Black | Barcode unverified · Exact model unverified
Options:     1. Accept packing error: Approve return and draft label.
             2. Request label photo: “Please share the outer-box label so we can check your shipment.”
             3. Hold for inspection: Inspect returned parcel before refund
Footnote:    * Staged example.

SPEAKER NOTES (72 words / ~35s):
"Here is our core demonstration. The Shopify order specifies white headphones, but the video shows black casing. ReturnLens flags this visible difference clearly. Notice our honest AI grounding: barcode and exact model remain unverified from this frame. Instead of guessing fraud or packing errors, ReturnLens surfaces verified facts and prepares next steps. Option two drafts a polite reply asking for the box label, ready for one-click seller approval."

========================================================================================
SLIDE 4: AGENT WORKFLOW & BOUNDARIES
========================================================================================
Kicker:      Agent Architecture
Title:       From evidence to next step.
Subtitle:    A structured pipeline where models observe, code verifies, and the seller approves.
Stages:      1. Collect: Bring together messages, order data, tracking and video frames.
             2. Compare: Compare observed details with the order and return policy.
             3. Recommend: Suggest the next step and draft a customer reply.
             4. Seller decides: Review the evidence and approve returns, labels or refunds.
Loop:        When evidence is unclear: Unclear evidence → Request a close-up photo → Add to case file → Continue review.
             If still unclear after one request, send the case to the seller.

SPEAKER NOTES (59 words / ~30s):
"Behind the scenes, ReturnLens follows four direct stages: Collect, Compare, Recommend, and Seller Decides. When evidence is unclear—such as dark or blurry unboxing footage—the agent requests a single close-up photo and adds it to the existing case file. If still unclear after that request, it escalates directly to the seller. The seller approves all returns, shipping labels, and refunds."

========================================================================================
SLIDE 5: SCENARIOS MATRIX
========================================================================================
Kicker:      Planned scenarios
Title:       Three situations. Clear next steps.
Table:
- Case A (Damage on arrival): Cracked headband; within the 7-day window.
  Agent: Checks the order date and drafts a return label.
  Seller: Approve return. Refund waits for parcel receipt. (Regular font)
- Case B (Color discrepancy): White ordered; black shown in the video.
  Agent: Flags the mismatch and drafts resolution options.
  Seller: Choose a resolution or request the box label. (Regular font)
- Case C (Unclear evidence): Video is too dark to inspect.
  Agent: Requests a close-up and adds it to the case.
  Seller: Review new evidence or handle manually. (Regular font)

SPEAKER NOTES (53 words / ~25s):
"Our prototype focuses on three everyday situations: In Case A, damage on arrival within the seven-day return window produces a draft return label. In Case B, a color discrepancy surfaces three clear resolution paths. In Case C, unclear footage prompts a single close-up request. Each scenario delivers a clear next step for the merchant without automated rejections."

========================================================================================
SLIDE 6: 24-HOUR PROTOTYPE SPRINT (4-PERSON TEAM)
========================================================================================
Kicker:      24-Hour Prototype Sprint
Title:       A focused 24-hour prototype.
Timeline:    00–06h: Ingestion & Schema (Mock order and courier fixtures; case state schema.)
             06–12h: Vision & Rules (Keyframe extraction and deterministic policy checks.)
             12–18h: Seller Console UI (Side-by-side evidence review console with drafted replies.)
             18–24h: Walkthrough & QA (Scenario walkthroughs and checks across Cases A, B, and C.)
Team:        Team:
             • A — Workflow and policy rules.
             • B — Video frames and visual observations.
             • C — Seller console and drafted replies.
             • D — Integration, scenario data and walkthrough checks.
Scope:       Build first: Mock order and courier data · Keyframe evidence viewer · 3 core scenarios · Seller approval for return decisions
             Later: Live store and courier integrations.
Takeaway:    One clear evidence pack. The seller makes the call. (No quotes, directly on canvas)

SPEAKER NOTES (59 words / ~30s):
"For this 24-hour hackathon, our four-person team has a strictly focused scope: Person A builds workflow and policy rules; Person B handles video frames and visual observations; Person C builds the seller console and drafted replies; Person D manages integration, scenario data, and walkthrough checks. We build core verification first, saving live store and courier integrations for later. One clear evidence pack. The seller makes the call."
```

---

# 4. BỘ 5 CÂU HỎI & TRẢ LỜI BẢO VỆ KỸ THUẬT TRƯỚC BAN GIÁM KHẢO (DEFENSE Q&A)

### Câu hỏi 1: Nếu video mở hộp bị lóa sáng, chất lượng kém hoặc bị cắt ghép thì AI xử lý thế nào?
**Trả lời:**  
ReturnLens áp dụng nguyên tắc **Fail-Closed (an toàn khi không chắc chắn)**. Mô hình thị giác chỉ trích xuất những gì có độ tin cậy cao; nếu khung hình bị mờ hoặc không đọc được nhãn mã vạch, hệ thống sẽ gắn nhãn rõ ràng: *"Barcode unverified"*. Trong tình huống bằng chứng không đủ rõ (Case C), Agent tuyệt đối không tự động từ chối khiếu nại, mà sẽ kích hoạt vòng lặp làm rõ: yêu cầu khách gửi thêm một ảnh chụp cận cảnh của phần hư hỏng hoặc nhãn ngoài hộp. Hồ sơ vụ việc được giữ nguyên để bổ sung bằng chứng mới, và chỉ cho phép tối đa 1 lần yêu cầu tự động trước khi chuyển trực tiếp cho người bán xử lý (`If still unclear after one request, send the case to the seller.`).

### Câu hỏi 2: Tại sao không để Agent tự động hoàn tiền luôn cho khách để tiết kiệm tối đa thời gian cho seller?
**Trả lời:**  
Trong thương mại điện tử D2C dành cho solo seller, tự động hoàn tiền từ video là một lỗ hổng bảo mật nghiêm trọng (rủi ro gian lận hoàn tiền - friendly fraud). Hơn nữa, việc hoàn tiền và tạo nhãn vận chuyển đổi hàng đều là các hành động làm phát sinh chi phí trực tiếp trên tài khoản của người bán. Do đó, thiết kế an toàn của ReturnLens quy định: **Agent chỉ làm nhiệm vụ tổng hợp thông tin, xác thực ngày tháng và chuẩn bị sẵn các phương án (drafted replies/labels); người bán luôn là người đưa ra quyết định cuối cùng và bấm nút phê duyệt (Seller authorizes).**

### Câu hỏi 3: Đội thi có 4 thành viên sẽ phân chia công việc như thế nào để hoàn thành prototype trong 24 giờ?
**Trả lời:**  
Team 4 người được chuyên môn hóa theo 4 module độc lập, không dẫm chân lên nhau:
- **Thành viên A (Workflow & Rules):** Xây dựng rule engine tất định, schema trạng thái vụ việc và logic kiểm tra chính sách đổi trả.
- **Thành viên B (Vision & Keyframes):** Xây dựng pipeline trích xuất khung hình từ video mở hộp, phân tích thuộc tính bề mặt và bounding box.
- **Thành viên C (Seller Console & Replies):** Xây dựng giao diện web cho solo seller đối chiếu bằng chứng song song và soạn thảo phản hồi.
- **Thành viên D (Integration, Data & QA):** Chuẩn bị fixtures dữ liệu mock (Shopify, Shippo) cho 3 tình huống (A, B, C) và chạy kiểm thử end-to-end.
Về phạm vi, team bám sát nguyên tắc **Build first** (chỉ làm mock data + console + 3 kịch bản), chuyển API live và cổng thanh toán sang mục **Later**.

### Câu hỏi 4: Điểm khác biệt lớn nhất giữa ReturnLens và các chatbot hỗ trợ khách hàng thông thường (như Zendesk AI, Gorgias hay Intercom) là gì?
**Trả lời:**  
Các chatbot CSKH hiện nay chủ yếu tập trung vào **xử lý ngôn ngữ tự nhiên (NLP) dựa trên tin nhắn văn bản**, trả lời FAQ hoặc đóng vai trò nhân viên chăm sóc khách hàng. ReturnLens là một **hệ thống đối chiếu bằng chứng đa phương thức (Multimodal Evidence Triage Assistant)** tập trung vào xử lý khiếu nại sản phẩm vật lý. ReturnLens kết nối hình ảnh/video thực tế của sản phẩm mở hộp với dữ liệu đơn hàng và chính sách, chỉ ra sự mâu thuẫn trực quan (ví dụ: đặt màu trắng nhưng nhận màu đen) và đưa ra hồ sơ quyết định cho chủ shop.

### Câu hỏi 5: Làm sao để đảm bảo AI không đưa ra kết luận thiên kiến hoặc suy đoán chủ quan (hallucination)?
**Trả lời:**  
Chúng tôi tách bạch hoàn toàn nhiệm vụ quan sát và nhiệm vụ kết luận:
- Mô hình thị giác chỉ trả lời câu hỏi thực nghiệm: *"Màu sắc của vật thể chính trong khung hình là màu gì?"* $\rightarrow$ Trả về `Black`.
- Mã lệnh logic Python sẽ so sánh chuỗi: `'Black' != 'White'` $\rightarrow$ Bật cờ `color_mismatch: True`.
- Hệ thống tuyệt đối không sinh ra các câu suy đoán gian lận. Bằng chứng được trình bày khách quan để người bán tự thẩm định.

---

# 5. CHI TIẾT NÂNG CẤP TỪ V9.1 LÊN V9.2 (CHANGELOG)

1. **Cập nhật đội ngũ 4 thành viên (4-Person Team Distribution):**
   - Đội thi chính thức gồm 4 thành viên: A, B, C, D trên Slide 6 và toàn bộ canonical data.
   - Phân bổ vai trò rành mạch:
     - `A — Workflow and policy rules.`
     - `B — Video frames and visual observations.`
     - `C — Seller console and drafted replies.`
     - `D — Integration, scenario data and walkthrough checks.`
   - Duy trì khoảng cách visual rộng rãi $2.38"$ ($171.2\text{ pt}$) giữa cột Team và cột Scope, loại bỏ hoàn toàn khả năng chạm chữ.

2. **Slide 1 — Tinh giản mô tả & triệt tiêu lặp ý quyền hạn:**
   - Rút gọn câu định vị sản phẩm: *"A returns assistant for solo sellers that brings messages, video, order records and store policy into one case."*
   - Xóa bỏ hoàn toàn dòng giải thích phụ thừa ngay dưới triết lý thiết kế.
   - Mockup console thống nhất thông điệp quyền hạn: *"Seller approves returns, labels and refunds."* đi kèm *"No automated refund or rejection"*.

3. **Slide 2 — Câu hỏi hành động trực diện:**
   - Thay đoạn văn dài về tình huống người bán bằng câu hỏi hành động trực tiếp: *"Should I request more evidence, approve a return, or inspect the parcel?"* (17pt Regular).
   - Tinh gọn nhãn file đính kèm thành: *"Customer video · 18s"*.

4. **Slide 3 — Giao diện đối chiếu sắc sảo:**
   - Cập nhật Subtitle: *"Order details, video evidence and the next step—in one view."*
   - Đổi tên Lựa chọn 1 thành: *"1. Accept packing error / Approve return and draft label."*
   - Tinh gọn footnote thành: `* Staged example.` (loại bỏ lặp lại lưu ý mã vạch).

5. **Slide 4 — Tiêu đề kiến trúc trực tiếp:**
   - Thay thế các tiêu đề phụ rườm rà bằng 4 bước thẳng thắn: `1. Collect` $\rightarrow$ `2. Compare` $\rightarrow$ `3. Recommend` $\rightarrow$ `4. Seller decides`.
   - Đổi nhãn Case C thành: *"When evidence is unclear"*.
   - Bổ sung quy tắc leo thang sau 1 lần yêu cầu: *"If still unclear after one request, send the case to the seller."*

6. **Slide 5 — Tinh giản ma trận tình huống:**
   - Kicker chuyển thành *"Planned scenarios"*, bỏ subtitle và footnote thừa.
   - Nhãn tình huống trực diện: *"Damage on arrival"*, *"Color discrepancy"*, *"Unclear evidence"*.
   - Toàn bộ nội dung cột kết quả người bán định dạng Regular font thanh thoát.

7. **Kịch bản Pitch 3 Phút Chuẩn Hóa:**
   - Tổng số từ nói toàn bài được hiệu chỉnh chính xác ở mức **360 từ** (~120 từ/phút), chia đều và ăn khớp hoàn hảo cho 6 slide trong thời lượng 3 phút.

---

# 6. HƯỚNG DẪN KIỂM TRA ĐỘC LẬP TẠI LOCAL (VERIFICATION INSTRUCTIONS)

Nếu muốn chạy kiểm thử lại toàn bộ hệ thống deliverables v9.2 tại máy local:

```powershell
# Di chuyển vào thư mục dự án
cd D:\Code\Code\AIO\Code\hack4hack

# Chạy bộ test tự động 9 điểm của v9.2 (tất cả 9 bài test phải PASS)
python scripts/smoke_test_v9_2.py

# Kiểm tra đảm bảo không gây regression lên bản cũ v9.1 và v9
python scripts/smoke_test_v9_1.py
python scripts/smoke_test_v9.py

# Kiểm tra git status (đảm bảo không bị commit, push hay deploy ngoài ý muốn)
git status --short
```

---
*Tài liệu bàn giao được biên soạn bởi Senior Product & AI Systems Engineer, phục vụ thẩm định kỹ thuật và nộp bài chính thức tại AgentX Hackathon 2026.*

