# RETURNLENS V9.3 (PS-04 TOOL-ASSISTED TRIAGE & SAFETY GUARDRAILS EDITION) — FULL CONTEXT HANDOFF & REVIEW BRIEF

Tài liệu này cung cấp toàn bộ bối cảnh dự án, kiến trúc kỹ thuật, kịch bản pitch, nội dung 6 slide, và bộ câu hỏi bảo vệ kỹ thuật của **ReturnLens v9.3** — phiên bản thể hiện đầy đủ yêu cầu của **Track PS-04 (Autonomous Support Agent for Solo D2C Merchants)** ngay trên mặt slide, tích hợp kiến trúc tool execution theo kế hoạch prototype, rào chắn hoàn tiền (refund guardrails & store cap), hệ thống ghi nhật ký kiểm toán (full audit logging) và nhịp điệu pitch 3 phút tinh gọn (311 từ) để nộp chính thức cho Ban Giám Khảo (BGK) tại **Vòng Ý Tưởng (Idea Round) — AgentX Hackathon 2026**.

---

## PHẦN DÀNH CHO USER: CÂU LỆNH (PROMPT) GỢI Ý ĐỂ COPY VÀO GPT / MUSE

Nếu bạn muốn gửi tài liệu này cho ChatGPT, Muse hoặc bất kỳ AI nào khác để review đánh giá, hãy copy toàn bộ đoạn trong khung bên dưới:

```markdown
Bạn là một Giám khảo kỹ thuật cấp cao (Senior Hackathon Technical Judge) và Chuyên gia Đánh giá An toàn Hệ thống AI (AI Safety Auditor) tại AgentX Hackathon 2026. 

Dưới đây là hồ sơ chi tiết của dự án "ReturnLens v9.3" thuộc Track PS-04 (Autonomous Support Agent for Solo D2C Merchants) cho VÒNG Ý TƯỞNG (Idea Round).

Hãy đọc kỹ toàn bộ tài liệu hồ sơ dưới đây và thực hiện review độc lập theo các tiêu chí:
1. ĐỊNH VỊ SẢN PHẨM & GIÁ TRỊ THỰC TẾ THEO TRACK PS-04: Agent có giải quyết đúng các nghiệp vụ chat thường nhật (order status, returns, refunds) và tận dụng bằng chứng video (video evidence) làm điểm khác biệt để sàng lọc các khiếu nại tranh chấp hay không? Có tránh bẫy overclaim không?
2. KIẾN TRÚC TOOL EXECUTION & RANH GIỚI AN TOÀN: Luồng tool gọi mock data, kiểm tra chính sách bằng code tất định (0 <= current_date - delivery_date <= 7 days), hỏi bổ sung tối đa 1 lần, sau seller approval mới gọi tool tạo return, và chuyển seller kèm tóm tắt khi chưa giải quyết được đã đủ an toàn và khả thi cho một bản prototype 24h chưa?
3. REFUND GUARDRAILS & STORE CAP: Thiết kế rào chắn hoàn tiền (bắt buộc seller approval, bị giới hạn bởi store cap và remaining refundable amount) cùng ví dụ số nhất quán (ORD-7729 còn ₹1,499, cap mẫu ₹3,000 ghi rõ là policy mẫu của đội) có đảm bảo an toàn tài chính cho solo seller không? Hệ thống log toàn bộ tool call, approval và blocked/failed actions có minh bạch không?
4. KỶ LUẬT PHẠM VI 24H & PHÂN CÔNG 4 THÀNH VIÊN: Việc đưa "real tool calls trên mock data" vào Build first và dời "live production integrations" sang Later có thực tế không? Phân bổ 4 thành viên (A, B, C, D) làm song song theo schema JSON chung có khả thi để tích hợp sớm trong 24 giờ không?
5. ĐỒNG BỘ NARRATIVE, NHỊP ĐIỆU PITCH 3 PHÚT (311 TỪ) & ART DIRECTION: Câu chuyện xuyên suốt 6 slide có sắc nét không? Nhịp điệu 311 từ có chuẩn 3 phút không? Hệ thống thiết kế phẳng, font Arial, 0 theme blue ngầm, khoảng cách an toàn visual >= 0.30 inch có đạt tiêu chuẩn nộp BGK không?

Đưa ra nhận xét khách quan, chỉ ra các điểm mạnh vượt trội, các điểm cần lưu ý khi bước vào vòng code 24 giờ tiếp theo, và chấm điểm dự kiến cho vòng ý tưởng này.
```

---

# TỔNG QUAN HỒ SƠ DỰ ÁN (PROJECT DOSSIER)

### 1. Thông tin chung
- **Tên dự án:** ReturnLens
- **Phiên bản:** v9.3 (PS-04 Tool-Assisted Triage & Safety Guardrails Edition)
- **Cuộc thi:** AgentX Hackathon 2026
- **Track dự thi:** PS-04 — Autonomous Support Agent for Solo D2C Merchants
- **Team thực hiện:** Team Rookie (4 thành viên: A — Tool Execution & Rules; B — Vision & Keyframes; C — Seller Console & Replies; D — Integration & QA)
- **Slogan / Tagline:** *“Every return decision, backed by evidence.”*
- **One-Liner:** Một support agent dành cho solo seller xử lý chat về trạng thái đơn hàng, đổi trả và hoàn tiền—sử dụng bằng chứng video mở hộp để đối chiếu và sàng lọc các khiếu nại tranh chấp thành hồ sơ rõ ràng cho người bán phê duyệt.

### 2. Danh mục Deliverables & Checksum Cryptographic
Tất cả các tệp nghiệm thu đã được tạo, kiểm tra tự động và đồng bộ 100% giữa thư mục gốc và thư mục `deliverables/`:

| Tên Deliverable | Định dạng | Kích thước | SHA256 Checksum | Mô tả |
| :--- | :--- | :--- | :--- | :--- |
| `ReturnLens_v9_3.pptx` | PowerPoint | 1,360,986 bytes | `2116944d4ab2394311209873c1e922e7b1251591d140e639a91088665930981f` | Slide deck phẳng 100%, nhúng speaker notes 311 từ, typography Arial |
| `ReturnLens_v9_3.pdf` | Vector PDF | 242,857 bytes | `82f5218fc1f519e6fbb862c44b905d634920e1d67369529c78f12cf04f32d84e` | Bản in PDF chuẩn vector 6 trang, tỷ lệ 16:9 widescreen (960×540 pt) |
| `ReturnLens_v9_3.html` | Interactive Web | 2,336,562 bytes | `02cd8831b326d75c45afc0b51195cafb43f5c0560315e034c105c67002af04c8` | Trình chiếu web độc lập tương tác bàn phím ($\leftarrow$/$\rightarrow$) |
| `ReturnLens_v9_3_preview.png` | Contact Sheet | 696,638 bytes | `9113d1a7b69f4daff87eae360fbd1bc5569529677df59e5ec47a36b3e952c5a3` | Ảnh tổng quan 6 slide tỷ lệ 2×3 (kích thước chuẩn 2352×882 px) |
| `content/deck_data_v9_3.json` | JSON Data | 13,294 bytes | `7cf9e690a030eda77924e859f9d79977d8eff3bd7851909fbba4755120a65f3b` | Single Source of Truth cho 4 thành viên, kịch bản pitch và Q&A |
| `src/assets/v9_3_pptx_renders/` | PNG Renders | 6 slide PNGs | Đầy đủ 6 slide render ở độ phân giải cao 1920×1080 px kèm manifest |
| `V9_3_QA_REPORT.md` | Báo cáo QA | Markdown | Tài liệu kiểm thử 9 điểm tự động và phân tích hình học an toàn |

---

# 1. ĐỊNH VỊ Ý TƯỞNG THEO TRACK PS-04 (PRODUCT POSITIONING)

### Nỗi đau thực tế của Solo Seller bán hàng D2C:
Một nhà bán hàng độc lập (solo seller) trên Shopify hoặc TikTok Shop phải đối mặt với hàng chục tin nhắn mỗi ngày: từ tra cứu trạng thái đơn hàng (order status), yêu cầu đổi trả (returns) đến khiếu nại đòi hoàn tiền (refunds). 

Khi khách gửi khiếu nại: *"Tôi đặt tai nghe màu trắng, nhưng nhận được màu đen. Hãy hoàn tiền cho tôi!"* kèm theo video mở hộp 18 giây, người bán rơi vào thế kẹt:
1. Phải mở 4 nguồn rời rạc: Chat khách, Shopify (mã SKU, màu đặt), Bưu tá Shippo (ngày giao), và Chính sách cửa hàng (hạn 7 ngày).
2. Tự tua video xem khách mở hộp ra cái gì.
3. Dễ quyết định sai: hoặc hoàn tiền vội vàng (mất tiền oan vì friendly fraud), hoặc từ chối gay gắt (khách đánh giá 1 sao hoặc kiện chargeback).

### Giải pháp của ReturnLens (Bám sát Track PS-04):
ReturnLens là một **support agent toàn diện dành cho solo seller**:
- Xử lý các câu hỏi thường nhật về **trạng thái đơn hàng (order status)**.
- Khi gặp khiếu nại đổi trả hoặc hoàn tiền có tranh chấp, hệ thống kích hoạt năng lực **sàng lọc bằng chứng đa phương thức (video evidence triage)**:
  - Tự động gọi tool lấy dữ liệu đơn hàng và lịch sử bưu tá từ backend.
  - Kiểm tra điều kiện chính sách bằng code tất định ($0 \le \text{current\_date} - \text{delivery\_date} \le 7\text{ days}$).
  - Trích xuất khung hình video để ghi nhận thuộc tính vật lý khách quan (màu sắc đen tại giây 00:07).
  - Soạn sẵn phương án xử lý (drafted return label, câu trả lời mẫu).
  - Yêu cầu khách gửi thêm ảnh cận cảnh tối đa 1 lần nếu video bị mờ/tối.
  - Bắt buộc phải có **phê duyệt của người bán (Seller approval)** trước khi gọi tool tạo đơn đổi trả hoặc hoàn tiền.
  - Tuyệt đối không tự động hoàn tiền hoặc từ chối đơn hàng (No automated refund or rejection).

---

# 2. HỆ NGUYÊN TẮC, TOOL EXECUTION VÀ RÀO CHẮN AN TOÀN (SAFETY & GUARDRAILS)

### Luận điểm kiến trúc cốt lõi (Core Thesis):
$$\textbf{“Models observe. Code verifies. Seller authorizes.”}$$

### 1. Luồng thực thi công cụ (Tool Execution Pipeline - Planned Prototype):
1. **1. Fetch & Observe (Lấy dữ liệu & Quan sát):**
   - Tool tự động truy vấn dữ liệu đơn hàng và mã vận đơn từ mock backend.
   - Vision model trích xuất khung hình then chốt và mô tả thuộc tính bề mặt khách quan (màu sắc vỏ, vết nứt).
2. **2. Verify Rules (Xác thực quy tắc):**
   - Code tất định thực thi phép kiểm tra chính sách đổi trả: $0 \le \text{current\_date} - \text{delivery\_date} \le 7\text{ days}$.
   - So khớp thuộc tính quan sát với thông số catalog (`'Black' != 'White'`).
3. **3. Propose & Clarify (Đề xuất & Làm rõ):**
   - Đề xuất các phương án xử lý tiếp theo và soạn thảo phản hồi lịch sự cho khách.
   - Nếu bằng chứng không rõ (video mờ/tối), agent tự động gửi yêu cầu khách cung cấp **tối đa 1 ảnh chụp cận cảnh hoặc ảnh nhãn hộp ngoài**.
4. **4. Seller Approves (Người bán phê duyệt):**
   - Solo seller xem hồ sơ đối chiếu và bấm nút duyệt.
   - Sau khi seller duyệt, hệ thống gọi tool tạo đơn đổi trả (`create_return`) và phát hành nhãn bưu tá.
   - Nếu vụ việc vẫn chưa được giải quyết sau 1 lần hỏi bổ sung, hệ thống chuyển thẳng cho seller kèm tóm tắt hồ sơ (escalate with summary).

### 2. Rào chắn hoàn tiền (Refund Guardrails & Store Cap):
- **Bắt buộc Seller Approval:** Mọi khoản hoàn tiền đều phải do chính người bán trực tiếp phê duyệt, agent tuyệt đối không tự ý phát hành tiền hoàn.
- **Ràng buộc hai lớp:**
  1. **Remaining refundable amount:** Số tiền hoàn không được vượt quá số tiền còn lại có thể hoàn của đơn hàng (ví dụ: ₹1,499 cho đơn ORD-7729).
  2. **Store max refund cap:** Số tiền hoàn bị giới hạn bởi trần hoàn tiền tối đa của cửa hàng (ví dụ minh họa trong kịch bản prototype: team đặt mức cap mẫu là ₹3,000/giao dịch; đây là chính sách mẫu của đội thi để đánh giá prototype, không phải quy định của BTC hackathon).

### 3. Ghi nhật ký kiểm toán toàn diện (Full Audit Log):
- Mọi lượt gọi tool (`fetch_order`, `check_policy`, `request_clarification`, `create_return`), mọi lượt phê duyệt của seller, và mọi hành động bị chặn hoặc thất bại (failed/blocked actions) đều được ghi nhận vĩnh viễn vào nhật ký kiểm toán (audit trail) của vụ việc.

---

# 3. NỘI DUNG VÀ SPEAKER NOTES CHI TIẾT CỦA 6 SLIDE (V9.3)

Tổng số từ nói trong kịch bản: **311 từ** (thời lượng ước tính: 2 phút 45 giây đến 3 phút, tốc độ nói đĩnh đạc ~105-110 từ/phút).

```
========================================================================================
SLIDE 1: PRODUCT INTRODUCTION & FLAT CONSOLE MOCKUP
========================================================================================
Kicker:      AgentX Hackathon 2026 · Track PS-04
Title:       ReturnLens
Tagline:     Every return decision, backed by evidence.
Summary:     A support agent for solo sellers that handles order status, returns and 
             refunds—using video evidence to triage disputed claims.
Principle:   Models observe. Code verifies. Seller authorizes.
Mockup:      CASE #RT-8821 · NEEDS SELLER DECISION
             Order #ORD-7729 · Studio Wireless · ₹1,499 paid · Delivered 4d ago
             Color mismatch: Ordered White vs Observed Black · Barcode unverified
             Recommended Next Step: Request outer-box label photo
             Authority Note: Seller approves returns, labels and refunds.
             Safety Note:    No automated refund or rejection
             CTA Button:     Review Evidence & Decide →

SPEAKER NOTES (46 words / ~25s):
"Judges, this is ReturnLens. For solo merchants, handling customer chat about order status, returns, and refunds is time-consuming and error-prone. ReturnLens handles routine inquiries while using video evidence to triage disputed claims. Models observe, deterministic code verifies, and the merchant always authorizes every consequential financial decision."

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

SPEAKER NOTES (52 words / ~25s):
"A customer chats in: 'I ordered white headphones, but received black. Please refund me,' attaching an 18-second unboxing video. The seller currently checks four separate sources: chat, Shopify, courier tracking, and store policies. The seller needs verified facts before deciding whether to request more evidence, approve a return, or inspect the parcel."

========================================================================================
SLIDE 3: THE CORE DEMONSTRATION (WHITE ORDERED. BLACK SHOWN.)
========================================================================================
Kicker:      Core Evidence Comparison
Title:       White ordered. Black shown.
Subtitle:    Order details, video evidence and the next step—in one view.
Left Box:    STORE SPECIFICATION · SHOPIFY | Ordered: White | HEAD-WHT-02 · ₹1,499 paid · Delivered 4d ago
Center:      ≠
Right Box:   OBSERVED EVIDENCE · VIDEO FRAME 00:07 | Observed: Black | Barcode unverified · Exact model unverified
Options:     1. Approve return: Approve return and draft label.
             2. Request label photo: “Please share the outer-box label so we can check your shipment.”
             3. Hold for inspection: Inspect returned parcel before refund
Footnote:    * Staged example.

SPEAKER NOTES (57 words / ~40s):
"Here is our core demonstration. The Shopify order specifies white headphones, but the video shows black casing. ReturnLens flags this visible difference clearly. Notice our honest AI grounding: the package barcode remains unverified. Instead of guessing, ReturnLens prepares clear next steps. Option two drafts a polite clarification asking for the outer-box label, ready for one-click seller approval."

========================================================================================
SLIDE 4: AGENT ARCHITECTURE & TOOL EXECUTION (PLANNED PROTOTYPE)
========================================================================================
Kicker:      Agent Architecture (Planned Prototype)
Title:       Tool-assisted triage and safety guardrails.
Subtitle:    A structured pipeline where models observe, tools fetch and verify, and the seller approves.
Stages:      1. Fetch & Observe: Tools query mock order and tracking data; vision model inspects video frames.
             2. Verify Rules: Deterministic code checks return window (0 ≤ days ≤ 7) and store policies.
             3. Propose & Clarify: Suggests next action; asks customer for 1 close-up photo if evidence is unclear.
             4. Seller Approves: Seller authorizes; tool creates return; escalates with summary if unresolved.
Guardrails:  PROTOTYPE SAFETY GUARDRAILS & AUDIT LOG
             • Refund Guardrails: Refunds require seller approval · Limited by store cap and remaining refundable amount
             • Full Audit Log: Every tool call, seller approval, blocked action and outcome is recorded in audit trail

SPEAKER NOTES (59 words / ~40s):
"Our planned prototype executes real tools against a mock backend. The agent fetches order and tracking records, verifies the seven-day return window in code, and asks for one close-up photo if evidence is unclear. Refunds require seller approval, bounded by the remaining refundable amount (₹1,499) and our sample store cap of ₹3,000. Every tool call and outcome is logged."

========================================================================================
SLIDE 5: SCENARIOS MATRIX
========================================================================================
Kicker:      Planned scenarios
Title:       Three situations. Clear next steps.
Table:
- Case A (Damage on arrival): Cracked headband; delivery 4d ago (within 7d window).
  Agent: Checks the delivery date; drafts return shipping label.
  Seller: Approve return. Refund waits for parcel receipt. (Regular font)
- Case B (Evidence clarification): White ordered; black shown in unboxing video.
  Agent: Flags mismatch; drafts label request (max 1 clarification).
  Seller: Choose resolution or request outer-box photo. (Regular font)
- Case C (Refund guardrail): Unclear video; refund claim exceeds remaining amount.
  Agent: Blocks instant refund; requests 1 photo; logs audit trace.
  Seller: Review dossier; seller decides refund or manual check. (Regular font)

SPEAKER NOTES (47 words / ~25s):
"Our prototype handles three distinct branches: In Case A, verified delivery dates produce a draft return label. In Case B, color discrepancies trigger a single clarification request. In Case C, unclear evidence activates refund guardrails and escalates directly to the merchant. All actions remain transparent and audit-logged."

========================================================================================
SLIDE 6: 24-HOUR PROTOTYPE SPRINT (4-PERSON TEAM)
========================================================================================
Kicker:      24-Hour Prototype Sprint
Title:       A focused 24-hour prototype.
Timeline:    00–06h: Ingestion & Schema (Mock backend data & shared JSON state schema.)
             06–12h: Tools & Vision (Real tool execution on mock data & frame extraction.)
             12–18h: Console & Guardrails (Seller console, refund cap checks & drafted replies.)
             18–24h: Integration & QA (Early integration across A/B/C/D & scenario walkthroughs.)
Team:        Team (Parallel Execution to Shared Schema):
             • A — Tool execution, policy engine and refund caps.
             • B — Video frame extraction and visual observations.
             • C — Seller console, drafted replies and audit view.
             • D — Mock data fixtures, scenario walkthroughs and QA.
Scope:       Build first: Real tool calls on mock data · 3 scenario branches · Refund caps & audit log · Seller approval gate
             Later: Live store and courier integrations.
Takeaway:    One clear evidence pack. The seller makes the call.

SPEAKER NOTES (50 words / ~25s):
"In our 24-hour sprint, four teammates build in parallel against a shared schema: tool execution, vision extraction, seller UI, and integration testing. Build first includes real tool calls on mock data and safety guardrails, saving live production APIs for later. ReturnLens: one clear evidence pack. The seller makes the call."
```

---

# 4. BỘ 5 CÂU HỎI & TRẢ LỜI BẢO VỆ KỸ THUẬT TRƯỚC BAN GIÁM KHẢO (DEFENSE Q&A)

### Câu hỏi 1: Nếu video mở hộp bị lóa sáng, chất lượng kém hoặc bị cắt ghép thì AI xử lý thế nào?
**Trả lời:**  
ReturnLens áp dụng nguyên tắc **Fail-Closed (an toàn khi không chắc chắn)**. Mô hình thị giác chỉ trích xuất những gì có độ tin cậy cao; nếu khung hình bị mờ hoặc không đọc được nhãn mã vạch, hệ thống sẽ gắn nhãn rõ ràng: *"Barcode unverified"*. Trong tình huống bằng chứng không đủ rõ (Case C), Agent tuyệt đối không tự động từ chối khiếu nại, mà sẽ kích hoạt vòng lặp làm rõ: yêu cầu khách gửi thêm một ảnh chụp cận cảnh của phần hư hỏng hoặc nhãn ngoài hộp. Hồ sơ vụ việc được giữ nguyên để bổ sung bằng chứng mới, và chỉ cho phép tối đa 1 lần yêu cầu tự động trước khi chuyển trực tiếp cho người bán xử lý kèm bản tóm tắt vụ việc.

### Câu hỏi 2: Tại sao không để Agent tự động hoàn tiền luôn cho khách để tiết kiệm tối đa thời gian cho seller?
**Trả lời:**  
Trong thương mại điện tử D2C dành cho solo seller, tự động hoàn tiền từ video là một lỗ hổng bảo mật nghiêm trọng (rủi ro gian lận hoàn tiền - friendly fraud). Hơn nữa, việc hoàn tiền và tạo nhãn vận chuyển đổi hàng đều là các hành động làm phát sinh chi phí trực tiếp trên tài khoản của người bán. Do đó, thiết kế an toàn của ReturnLens quy định: **Agent chỉ làm nhiệm vụ tổng hợp thông tin, xác thực ngày tháng và chuẩn bị sẵn các phương án (drafted replies/labels); người bán luôn là người đưa ra quyết định cuối cùng và bấm nút phê duyệt (Seller authorizes).** Ngoài ra, mọi khoản hoàn tiền đều bị chặn cứng bởi 2 lớp rào chắn: không vượt quá số tiền còn lại có thể hoàn (remaining refundable amount) và không vượt quá trần quy định của cửa hàng (store cap).

### Câu hỏi 3: Đội thi có 4 thành viên sẽ phân chia công việc như thế nào để hoàn thành prototype trong 24 giờ?
**Trả lời:**  
Team 4 người thực thi song song theo một schema trạng thái JSON chung đã thống nhất từ đầu:
- **Thành viên A (Tool Execution & Rules):** Xây dựng các tool thực thi tất định, kiểm tra quy tắc thời hạn ($0 \le \text{current\_date} - \text{delivery\_date} \le 7\text{ days}$) và logic giới hạn trần hoàn tiền.
- **Thành viên B (Vision & Keyframes):** Xây dựng pipeline trích xuất khung hình từ video mở hộp, phân tích thuộc tính bề mặt và bounding box.
- **Thành viên C (Seller Console & Replies):** Xây dựng giao diện web cho solo seller đối chiếu bằng chứng song song, xem nhật ký kiểm toán và duyệt phản hồi.
- **Thành viên D (Mock Fixtures & QA):** Chuẩn bị fixtures dữ liệu mock (Shopify, Shippo) cho 3 tình huống (A, B, C) và chạy kiểm thử tích hợp sớm end-to-end.
Về phạm vi, team bám sát nguyên tắc **Build first** (chỉ làm real tool calls trên mock data + console + guardrails), dời API live và cổng thanh toán thật sang mục **Later**.

### Câu hỏi 4: Điểm khác biệt lớn nhất giữa ReturnLens và các chatbot hỗ trợ khách hàng thông thường (như Zendesk AI, Gorgias hay Intercom) là gì?
**Trả lời:**  
Các chatbot CSKH hiện nay chủ yếu tập trung vào **xử lý ngôn ngữ tự nhiên (NLP) dựa trên tin nhắn văn bản**, trả lời FAQ hoặc tra cứu đơn hàng cơ bản. ReturnLens mở rộng năng lực CSKH theo chuẩn Track PS-04: bên cạnh việc hỗ trợ chat thường nhật, ReturnLens đóng vai trò là một **hệ thống đối chiếu bằng chứng đa phương thức (Multimodal Evidence Triage Assistant)** chuyên biệt cho khiếu nại sản phẩm vật lý. ReturnLens kết nối hình ảnh/video thực tế của sản phẩm mở hộp với dữ liệu đơn hàng và chính sách, chỉ ra sự mâu thuẫn trực quan và lập hồ sơ quyết định có rào chắn bảo vệ cho chủ shop.

### Câu hỏi 5: Làm sao để đảm bảo AI không đưa ra kết luận thiên kiến hoặc suy đoán chủ quan (hallucination)?
**Trả lời:**  
Chúng tôi tách bạch hoàn toàn nhiệm vụ quan sát và nhiệm vụ kết luận:
- Mô hình thị giác chỉ trả lời câu hỏi thực nghiệm: *"Màu sắc của vật thể chính trong khung hình là màu gì?"* $\rightarrow$ Trả về `Black`.
- Mã lệnh logic Python sẽ so sánh chuỗi: `'Black' != 'White'` $\rightarrow$ Bật cờ `color_mismatch: True`.
- Hệ thống tuyệt đối không sinh ra các câu suy đoán gian lận. Mọi tool call, quyết định của seller và kết quả đều được ghi nhận vào nhật ký kiểm toán (audit trail) để người bán tự thẩm định minh bạch.

---

# 5. CHI TIẾT NÂNG CẤP TỪ V9.2 LÊN V9.3 (CHANGELOG)

1. **Slide 1 — Thể hiện rõ định vị Track PS-04:**
   - Cập nhật định vị trên slide face: *"A support agent for solo sellers that handles order status, returns and refunds—using video evidence to triage disputed claims."*
   - Khẳng định rõ agent hỗ trợ chat toàn diện về order status, returns và refunds, trong đó video evidence là vũ khí cốt lõi để đối chiếu các khiếu nại tranh chấp.

2. **Slide 3 — Chuẩn hóa câu chữ:**
   - Đổi tiêu đề từ *"White ordered. Black received."* thành **"White ordered. Black shown."** (phản ánh trung thực quan sát hình ảnh thay vì suy đoán giao dịch nhận).
   - Đổi Lựa chọn 1 từ *"1. Accept packing error"* thành **"1. Approve return"** (hành động phê duyệt đổi trả chuẩn xác).

3. **Slide 4 — Luồng Tool Execution, Rào chắn hoàn tiền & Audit Log:**
   - Thay mô tả chung chung bằng quy trình 4 bước có tool execution:
     + `1. Fetch & Observe`: Tools truy vấn mock order và tracking; vision model kiểm tra frames.
     + `2. Verify Rules`: Code tất định kiểm tra hạn đổi trả ($0 \le \text{current\_date} - \text{delivery\_date} \le 7\text{ days}$).
     + `3. Propose & Clarify`: Đề xuất bước tiếp theo; hỏi 1 ảnh cận cảnh nếu bằng chứng mờ.
     + `4. Seller Approves`: Seller duyệt; tool tạo return; chuyển seller nếu chưa giải quyết được.
   - Thêm panel rào chắn an toàn:
     + `Refund Guardrails`: Bắt buộc seller approval, bị giới hạn bởi store cap và remaining refundable amount.
     + `Full Audit Log`: Ghi nhận mọi tool call, approval, kết quả và cả hành động bị chặn/thất bại (failed/blocked actions).
   - Ghi rõ số liệu minh họa nhất quán trong notes (đơn ORD-7729 còn ₹1,499; cap mẫu ₹3,000 là policy mẫu của đội, không phải quy định BTC).

4. **Slide 5 — Phân nhánh nghiệp vụ súc tích & chuẩn hóa ngày:**
   - Đổi *"Checks the order date"* thành **"Checks the delivery date"**.
   - Thể hiện ngắn gọn 3 nhánh nghiệp vụ: Order status / Damage return (Case A), Evidence clarification (Case B), Refund guardrail & Escalation (Case C) mà không làm tăng mật độ chữ.

5. **Slide 6 — Kỷ luật Sprint 24h & Phân công song song:**
   - Làm rõ: **Real tool calls trên mock data** nằm trong **Build first**; chỉ **Live production integrations** mới ở **Later**.
   - Cập nhật phân công 4 thành viên (A, B, C, D) làm việc song song theo schema JSON chung, tích hợp sớm trong 24h.

6. **Hiệu chỉnh nhịp điệu Pitch 3 phút (311 từ):**
   - Rút gọn toàn bộ kịch bản nói xuống đúng **311 từ** (nằm chính xác trong dải yêu cầu 310–330 từ), cân chỉnh timestamp cho bài pitch 3 phút.

7. **Bảo đảm hình học an toàn & triệt tiêu theme blue:**
   - Khoảng cách an toàn tới footer trên toàn bộ 6 slide đạt **$\ge 0.30\text{ inch}$** (từ $0.36"$ đến $1.17"$).
   - 100% theme lines (`<p:style>`, `<a:lnRef>`) và shadows (`<a:effectRef>`) bị loại bỏ, phân tích pixel đạt **0 theme blue pixels**.

---

# 6. HƯỚNG DẪN KIỂM TRA ĐỘC LẬP TẠI LOCAL (VERIFICATION INSTRUCTIONS)

Nếu muốn chạy kiểm thử lại toàn bộ hệ thống deliverables v9.3 tại máy local:

```powershell
# Di chuyển vào thư mục dự án
cd D:\Code\Code\AIO\Code\hack4hack

# Chạy bộ test tự động 9 điểm của v9.3 (tất cả 9 bài test phải PASS)
python scripts/smoke_test_v9_3.py

# Kiểm tra đảm bảo không gây regression lên các bản cũ (v9.2, v9.1, v9)
python scripts/smoke_test_v9_2.py
python scripts/smoke_test_v9_1.py
python scripts/smoke_test_v9.py

# Kiểm tra git status
git status --short
```

---
*Tài liệu bàn giao được biên soạn bởi Senior Product & AI Systems Engineer, phục vụ thẩm định kỹ thuật và nộp bài chính thức tại AgentX Hackathon 2026.*
