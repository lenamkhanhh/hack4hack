# RETURNLENS V9.4 (FINAL SUBMISSION PATCH) — FULL CONTEXT HANDOFF & REVIEW BRIEF

Tài liệu này cung cấp toàn bộ bối cảnh dự án, kiến trúc kỹ thuật, kịch bản pitch, nội dung 6 slide, và bộ câu hỏi bảo vệ kỹ thuật của **ReturnLens v9.4** — bản patch tinh chỉnh cuối cùng chốt nộp cho Ban Giám Khảo (BGK) tại **Vòng Ý Tưởng (Idea Round) — AgentX Hackathon 2026, Track PS-04 (Autonomous Support Agent for Solo D2C Merchants)**.

---

## PHẦN DÀNH CHO USER: CÂU LỆNH (PROMPT) GỢI Ý ĐỂ COPY VÀO GPT / MUSE

Nếu bạn muốn gửi tài liệu này cho ChatGPT, Muse hoặc bất kỳ AI nào khác để review đánh giá, hãy copy toàn bộ đoạn trong khung bên dưới:

```markdown
Bạn là một Giám khảo kỹ thuật cấp cao (Senior Hackathon Technical Judge) và Chuyên gia Đánh giá An toàn Hệ thống AI (AI Safety Auditor) tại AgentX Hackathon 2026. 

Dưới đây là hồ sơ chi tiết của dự án "ReturnLens v9.4" thuộc Track PS-04 (Autonomous Support Agent for Solo D2C Merchants) cho VÒNG Ý TƯỞNG (Idea Round).

Hãy đọc kỹ toàn bộ tài liệu hồ sơ dưới đây và thực hiện review độc lập theo các tiêu chí:
1. ĐỊNH VỊ SẢN PHẨM & GIÁ TRỊ THỰC TẾ THEO TRACK PS-04: Agent có giải quyết đúng các nghiệp vụ chat thường nhật (order status, returns, refunds) và tận dụng bằng chứng video (video evidence) làm điểm khác biệt để sàng lọc các khiếu nại tranh chấp hay không? Có tránh bẫy overclaim không?
2. KIẾN TRÚC TOOL EXECUTION & BÓC TÁCH CASE C CHUẨN XÁC: Luồng tool gọi mock data, kiểm tra chính sách bằng code tất định (0 <= current_date - delivery_date <= 7 days), và xử lý Case C (chặn khoản tiền vượt hạn mức ₹1,499; hỏi bổ sung tối đa 1 lần nếu video mờ; chuyển seller kèm tóm tắt nếu chưa giải quyết được) đã đủ an toàn và khả thi cho một bản prototype 24h chưa?
3. REFUND GUARDRAILS & STORE CAP: Thiết kế rào chắn hoàn tiền (bắt buộc seller approval, bị giới hạn bởi store cap và remaining refundable amount) cùng ví dụ số nhất quán (ORD-7729 còn ₹1,499, cap mẫu ₹3,000 ghi rõ là policy mẫu của đội) có đảm bảo an toàn tài chính cho solo seller không? Hệ thống log toàn bộ tool call, approval và blocked/failed actions có minh bạch không?
4. KỶ LUẬT PHẠM VI 24H & PHÂN CÔNG 4 THÀNH VIÊN: Việc đưa "real tool calls trên mock data" vào Build first và dời "live production integrations" sang Later có thực tế không? Phân bổ 4 thành viên (A, B, C, D) chốt shared schema JSON từ đầu và làm song song có khả thi để tích hợp sớm trong 24 giờ không?
5. ĐỒNG BỘ NARRATIVE, NHỊP ĐIỆU PITCH 3 PHÚT (324 TỪ) & ART DIRECTION: Câu chuyện xuyên suốt 6 slide có sắc nét không? Nhịp điệu 324 từ có chuẩn 3 phút không? Hệ thống thiết kế phẳng, font Arial, 0 theme blue ngầm, khoảng cách an toàn visual >= 0.30 inch có đạt tiêu chuẩn nộp BGK không?

Đưa ra nhận xét khách quan, chỉ ra các điểm mạnh vượt trội, các điểm cần lưu ý khi bước vào vòng code 24 giờ tiếp theo, và chấm điểm dự kiến cho vòng ý tưởng này.
```

---

# TỔNG QUAN HỒ SƠ DỰ ÁN (PROJECT DOSSIER)

### 1. Thông tin chung
- **Tên dự án:** ReturnLens
- **Phiên bản:** v9.4 (Final Submission Patch)
- **Cuộc thi:** AgentX Hackathon 2026
- **Track dự thi:** PS-04 — Autonomous Support Agent for Solo D2C Merchants
- **Team thực hiện:** Team Rookie (4 thành viên: A — Tool Execution & Rules; B — Vision & Keyframes; C — Seller Console & Replies; D — Integration & QA)
- **Slogan / Tagline:** *“Every return decision, backed by evidence.”*
- **One-Liner:** Một support agent dành cho solo seller xử lý chat về trạng thái đơn hàng, đổi trả và hoàn tiền—sử dụng bằng chứng video mở hộp để đối chiếu và sàng lọc các khiếu nại tranh chấp thành hồ sơ rõ ràng cho người bán phê duyệt.

### 2. Danh mục Deliverables & Checksum Cryptographic
Tất cả các tệp nghiệm thu đã được tạo, kiểm tra tự động và đồng bộ 100% giữa thư mục gốc và thư mục `deliverables/`:

| Tên Deliverable | Định dạng | Kích thước | SHA256 Checksum | Mô tả |
| :--- | :--- | :--- | :--- | :--- |
| `ReturnLens_v9_4.pptx` | PowerPoint | 1,361,027 bytes | `a34dbb78adae8cd608c0f889f3930081fd2bc55dc1969861bcfe3524ae703cf0` | Slide deck phẳng 100%, nhúng speaker notes 324 từ, typography Arial |
| `ReturnLens_v9_4.pdf` | Vector PDF | 243,084 bytes | `fd26e1dc7260ed2ae5e1619179a7a6393530c04a5e2112e51d306e1e243c034d` | Bản in PDF chuẩn vector 6 trang, tỷ lệ 16:9 widescreen (960×540 pt) |
| `ReturnLens_v9_4.html` | Interactive Web | 2,334,374 bytes | `2c0b477d6b5bda04a74be3e5d101a67c08f5226ca24e20253a1aba548ebabce8` | Trình chiếu web độc lập tương tác bàn phím ($\leftarrow$/$\rightarrow$) |
| `ReturnLens_v9_4_preview.png` | Contact Sheet | 693,044 bytes | `ff966d55e7bb8840dece53f191ce463a8b32723db9038e2e3ee8b919e94e490e` | Ảnh tổng quan 6 slide tỷ lệ 2×3 (kích thước chuẩn 2352×882 px) |
| `content/deck_data_v9_4.json` | JSON Data | 13,834 bytes | `faaf41177c1d2a5abc2801f4ae334d53dc9260c47193b14d2e21c451dd910f0c` | Single Source of Truth cho 4 thành viên, kịch bản pitch và Q&A |
| `src/assets/v9_4_pptx_renders/` | PNG Renders | 6 slide PNGs | Đầy đủ 6 slide render ở độ phân giải cao 1920×1080 px kèm manifest |
| `V9_4_QA_REPORT.md` | Báo cáo QA | Markdown | Tài liệu kiểm thử 9 điểm tự động và phân tích hình học an toàn |

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
- Phản hồi nhanh các câu hỏi tra cứu thông thường về **trạng thái đơn hàng (order status)** kèm mã vận đơn.
- Khi gặp khiếu nại đổi trả hoặc hoàn tiền có tranh chấp, hệ thống kích hoạt luồng **sàng lọc bằng chứng đa phương thức (video evidence triage)**:
  - Tự động gọi tool lấy dữ liệu đơn hàng và lịch sử bưu tá từ mock backend.
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
   - Các tin nhắn tra cứu thông thường nhận cập nhật vận đơn; khiếu nại tranh chấp kích hoạt tool truy vấn đơn hàng và trích xuất khung hình video.
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

### 2. Xử lý Case C tách bạch chuẩn xác (Decoupled Case C Handling):
- **Vượt giới hạn tiền:** Nếu khoản tiền khách yêu cầu hoàn vượt quá số dư có thể hoàn còn lại (`₹1,499` của đơn ORD-7729), hệ thống tự động chặn khoản yêu cầu vượt mức đó. Việc chặn số tiền vượt hạn mức **không đồng nghĩa với việc tự động từ chối toàn bộ khiếu nại**.
- **Bằng chứng chưa rõ:** Nếu video mở hộp bị tối hoặc mờ, agent gửi thông báo yêu cầu cung cấp thêm **duy nhất 1 ảnh chụp cận cảnh**.
- **Cơ chế chuyển tiếp:** Nếu sau 1 lần yêu cầu vẫn chưa giải quyết được, hồ sơ được chuyển thẳng cho người bán kèm bản tóm tắt đầy đủ.
- **Quyền hạn người bán:** Người bán chỉ có thể duyệt khoản hoàn nằm trong giới hạn cho phép (không vượt quá `₹1,499` còn lại và `₹3,000` trần cửa hàng).

### 3. Rào chắn hoàn tiền (Refund Guardrails & Store Cap):
- **Bắt buộc Seller Approval:** Mọi khoản hoàn tiền đều phải do chính người bán trực tiếp phê duyệt, agent tuyệt đối không tự ý phát hành tiền hoàn.
- **Ràng buộc hai lớp:**
  1. **Remaining refundable amount:** Số tiền hoàn không được vượt quá số tiền còn lại có thể hoàn của đơn hàng (ví dụ: ₹1,499 cho đơn ORD-7729).
  2. **Store max refund cap:** Số tiền hoàn bị giới hạn bởi trần hoàn tiền tối đa của cửa hàng (ví dụ minh họa trong kịch bản prototype: team đặt mức cap mẫu là ₹3,000/giao dịch; đây là chính sách mẫu của đội thi để đánh giá prototype, không phải quy định của BTC hackathon).

### 4. Ghi nhật ký kiểm toán toàn diện (Full Audit Log):
- Mọi lượt gọi tool (`fetch_order`, `check_policy`, `request_clarification`, `create_return`), mọi lượt phê duyệt của seller, và mọi hành động bị chặn hoặc thất bại (failed/blocked actions) đều được ghi nhận vĩnh viễn vào nhật ký kiểm toán (audit trail) của vụ việc.

---

# 3. NỘI DUNG VÀ SPEAKER NOTES CHI TIẾT CỦA 6 SLIDE (V9.4)

Tổng số từ nói trong kịch bản: **324 từ** (thời lượng ước tính: 2 phút 50 giây đến 3 phút, tốc độ nói đĩnh đạc ~108 từ/phút).

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

SPEAKER NOTES (45 words / ~25s):
"Judges, this is ReturnLens. For solo merchants, handling customer chat about order status, returns, and refunds is time-consuming and error-prone. ReturnLens handles routine inquiries while using video evidence to triage disputed claims. Models observe, deterministic code verifies, and the merchant authorizes every consequential financial decision."

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
Options:     1. Approve return: Create return and prepare label.
             2. Request label photo: “Please share the outer-box label so we can check your shipment.”
             3. Hold for inspection: Inspect returned parcel before refund
Footnote:    * Staged example.

SPEAKER NOTES (54 words / ~40s):
"Here is our core demonstration. The Shopify order specifies white headphones, but the video shows black casing. ReturnLens flags this visible difference clearly. The barcode and exact model remain unverified. Instead of guessing, ReturnLens prepares clear next steps. Option two drafts a polite clarification asking for the outer-box label, ready for one-click seller approval."

========================================================================================
SLIDE 4: AGENT ARCHITECTURE & TOOL EXECUTION (PLANNED PROTOTYPE)
========================================================================================
Kicker:      Agent Architecture (Planned Prototype)
Title:       Tool-assisted triage and safety guardrails.
Subtitle:    A structured pipeline where models observe, tools fetch, code verifies, and the seller approves.
Stages:      1. Fetch & Observe: Routine chats get tracking updates; disputed claims fetch mock order and video frames.
             2. Verify Rules: Deterministic code checks return window (0 ≤ days ≤ 7) and store policies.
             3. Propose & Clarify: Suggests next action; asks customer for 1 close-up photo if evidence is unclear.
             4. Seller Approves: Seller authorizes; tool creates return; escalates with summary if unresolved.
Guardrails:  PROTOTYPE SAFETY GUARDRAILS & AUDIT LOG
             • Refund Guardrails: Refunds require seller approval · Limited by store cap and remaining refundable amount
             • Full Audit Log: Every tool call, seller approval, blocked action and outcome is recorded in audit trail

SPEAKER NOTES (60 words / ~40s):
"In our planned prototype, routine order-status chats receive a tracking update; disputed claims enter evidence review. Tools fetch mock order data, and code verifies the return window. If footage is unclear, the agent asks for one close-up. Refunds require seller approval, bounded by the ₹1,499 balance and our team's sample cap of ₹3,000. All actions and blocked amounts are logged."

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
- Case C (Refund guardrail): Unclear video; requested refund exceeds ₹1,499 remaining.
  Agent: Blocks excess amount; requests one close-up; logs both actions.
  Seller: Review evidence; approve only within refund limits. (Regular font)

SPEAKER NOTES (59 words / ~25s):
"Our prototype focuses on three planned situations: Case A validates delivery dates for damaged goods. Case B flags color mismatches and requests outer packaging. In Case C, the requested amount exceeds the remaining refundable balance, so the tool blocks that amount. Unclear evidence prompts one close-up request; if still unresolved, the case goes to the seller with a summary."

========================================================================================
SLIDE 6: 24-HOUR PROTOTYPE SPRINT (4-PERSON TEAM)
========================================================================================
Kicker:      24-Hour Prototype Sprint
Title:       A focused 24-hour prototype.
Timeline:    00–06h: Ingestion & Schema (Mock backend data & shared JSON state schema.)
             06–12h: Tools & Vision (Real tool execution on mock data & frame extraction.)
             12–18h: Console & Guardrails (Seller console, refund cap checks & drafted replies.)
             18–24h: Integration & QA (Final integration and scenario walkthroughs.)
Team:        Team (Parallel Execution to Shared Schema):
             • A — Tool execution, policy engine and refund caps.
             • B — Video frame extraction and visual observations.
             • C — Seller console, drafted replies and audit view.
             • D — Mock data fixtures, scenario walkthroughs and QA.
Scope:       Build first: Real tool calls on mock data · 3 scenario branches · Refund caps & audit log · Seller approval gate
             Later: Live store and courier integrations.
Takeaway:    One clear evidence pack. The seller makes the call.

SPEAKER NOTES (54 words / ~25s):
"For our 24-hour sprint, all four members lock a shared schema and test one integrated thread early. Then we build in parallel: tools, vision extraction, seller UI, and testing. Build first focuses on real tool calls over mock data, leaving live integrations for later. ReturnLens: one clear evidence pack. The seller makes the call."
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
Cả 4 thành viên chốt một JSON state schema chung và tích hợp thử một luồng cơ bản ngay từ giai đoạn đầu, sau đó phát triển song song theo 4 module độc lập:
- **Thành viên A (Tool Execution & Rules):** Xây dựng các tool thực thi tất định, kiểm tra quy tắc thời hạn ($0 \le \text{current\_date} - \text{delivery\_date} \le 7\text{ days}$) và logic giới hạn trần hoàn tiền.
- **Thành viên B (Vision & Keyframes):** Xây dựng pipeline trích xuất khung hình từ video mở hộp, phân tích thuộc tính bề mặt và bounding box.
- **Thành viên C (Seller Console & Replies):** Xây dựng giao diện web cho solo seller đối chiếu bằng chứng song song, xem nhật ký kiểm toán và duyệt phản hồi.
- **Thành viên D (Mock Fixtures & QA):** Chuẩn bị fixtures dữ liệu mock (Shopify, Shippo) cho 3 tình huống tranh chấp (Case A, B, C) và chạy kiểm thử tích hợp end-to-end.
Về phạm vi, team bám sát nguyên tắc **Build first** (chỉ làm real tool calls trên mock data + console + guardrails), dời API live và thanh toán thật sang giai đoạn sau (Later).

### Câu hỏi 4: Điểm khác biệt cốt lõi của ReturnLens so với các giải pháp hỗ trợ khách hàng hiện nay là gì?
**Trả lời:**  
ReturnLens chuyên biệt hóa cho việc xử lý các tranh chấp đổi trả và hoàn tiền sản phẩm vật lý bằng cách **đối chiếu đa phương thức giữa khung hình video mở hộp thực tế của khách hàng với thông số đơn hàng và chính sách đổi trả của cửa hàng**. Thay vì chỉ dừng lại ở tin nhắn văn bản, ReturnLens tổng hợp các điểm mâu thuẫn trực quan và các phép kiểm tra chính sách thành một hồ sơ quyết định trực quan duy nhất (decision dossier) cho solo seller, đi kèm các phương án hành động và câu trả lời soạn thảo sẵn để người bán phê duyệt chỉ với 1 cú nhấp chuột.

### Câu hỏi 5: Làm sao để đảm bảo AI không đưa ra kết luận thiên kiến hoặc suy đoán chủ quan (hallucination)?
**Trả lời:**  
Chúng tôi tách bạch hoàn toàn nhiệm vụ quan sát và nhiệm vụ kết luận:
- Mô hình thị giác chỉ trả lời câu hỏi thực nghiệm: *"Màu sắc của vật thể chính trong khung hình là màu gì?"* $\rightarrow$ Trả về `Black`.
- Mã lệnh logic Python sẽ so sánh chuỗi: `'Black' != 'White'` $\rightarrow$ Bật cờ `color_mismatch: True`.
- Hệ thống tuyệt đối không sinh ra các câu suy đoán gian lận. Mọi tool call, quyết định của seller và kết quả đều được ghi nhận vào nhật ký kiểm toán (audit trail) để người bán tự thẩm định minh bạch.

---

# 5. CHI TIẾT NÂNG CẤP TỪ V9.3 LÊN V9.4 (CHANGELOG)

1. **Slide 5 — Bóc tách chuẩn xác Case C (Unclear video vs Exceeding refund):**
   - Phân định rạch ròi 2 cơ chế:
     + **Situation:** *“Unclear video; requested refund exceeds ₹1,499 remaining.”*
     + **Agent response:** *“Blocks excess amount; requests one close-up; logs both actions.”*
     + **Seller’s next step:** *“Review evidence; approve only within refund limits.”*
   - Khẳng định rõ: Việc chặn khoản tiền vượt hạn mức không đồng nghĩa tự động từ chối toàn bộ khiếu nại; bằng chứng chưa rõ kích hoạt yêu cầu tối đa 1 ảnh cận cảnh; nếu vẫn chưa giải quyết được thì chuyển seller kèm tóm tắt; seller approval không được vượt quá số dư ₹1,499 hay trần ₹3,000.

2. **Slide 4 & Notes — Định tuyến nghiệp vụ Order Status:**
   - Bổ sung định tuyến rõ ràng trên Slide 4 Step 1 và speaker notes: *“Routine order-status chats receive a tracking update; disputed claims enter evidence review.”*
   - Khẳng định 3 scenario trên Slide 5 là 3 tình huống tranh chấp vật lý cần đối chiếu (damage on arrival, evidence clarification, refund guardrail), trong khi order status thông thường được giải quyết trực tiếp qua tool tra cứu.

3. **Chuẩn hóa câu chữ toàn deck:**
   - **Slide 3 Option 1:** Giữ tiêu đề *“1. Approve return”*; đổi dòng hành động bên dưới thành *“Create return and prepare label.”*.
   - **Slide 3 Notes:** Thay câu generic grounding bằng mô tả khách quan trực tiếp: *“The barcode and exact model remain unverified.”*.
   - **Slide 4 Subtitle:** Bổ sung đầy đủ 4 vế: *“A structured pipeline where models observe, tools fetch, code verifies, and the seller approves.”*.
   - **Slide 6 Phase 4 (18–24h):** Đổi thành *“Final integration and scenario walkthroughs.”*.
   - **Slide 6 Notes:** Làm rõ 4 thành viên chốt shared schema JSON và tích hợp thử một luồng từ giai đoạn đầu.
   - **Q&A Khác biệt sản phẩm:** Bỏ nhận định chung về công cụ bên ngoài; tập trung trực tiếp vào thế mạnh đối chiếu video và lập hồ sơ quyết định của ReturnLens.

4. **Hiệu chỉnh nhịp điệu Pitch 3 phút (324 từ):**
   - Tổng số từ nói toàn bài được hiệu chỉnh chính xác ở mức **324 từ** (~108 từ/phút), chia đều cho 6 slide và khớp hoàn hảo cho 3 phút trình bày.

5. **Bảo đảm hình học visual & an toàn kiểm thử:**
   - Khoảng cách an toàn tới footer trên toàn bộ 6 slide đạt **$\ge 0.30\text{ inch}$** (từ $0.36"$ đến $1.17"$).
   - 100% theme lines (`<p:style>`, `<a:lnRef>`) và shadows (`<a:effectRef>`) bị loại bỏ, phân tích pixel đạt **0 theme blue pixels**.
   - Bộ kiểm thử tự động `scripts/smoke_test_v9_4.py` đạt **9/9 PASS**, bảo toàn nguyên vẹn 100% các phiên bản cũ (v5 đến v9.3).

---

# 6. HƯỚNG DẪN KIỂM TRA ĐỘC LẬP TẠI LOCAL (VERIFICATION INSTRUCTIONS)

Nếu muốn chạy kiểm thử lại toàn bộ hệ thống deliverables v9.4 tại máy local:

```powershell
# Di chuyển vào thư mục dự án
cd D:\Code\Code\AIO\Code\hack4hack

# Chạy bộ test tự động 9 điểm của v9.4 (tất cả 9 bài test phải PASS)
python scripts/smoke_test_v9_4.py

# Kiểm tra đảm bảo không gây regression lên các bản cũ (v9.3, v9.2, v9.1, v9)
python scripts/smoke_test_v9_3.py
python scripts/smoke_test_v9_2.py
python scripts/smoke_test_v9_1.py
python scripts/smoke_test_v9.py

# Kiểm tra git status
git status --short
```

---
*Tài liệu bàn giao được biên soạn bởi Senior Product & AI Systems Engineer, phục vụ thẩm định kỹ thuật và nộp bài chính thức tại AgentX Hackathon 2026.*
