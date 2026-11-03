# RETURNLENS V9.1 (FINAL POLISH & FLAT RENDERING EDITION) — FULL CONTEXT HANDOFF & REVIEW BRIEF

Tài liệu này cung cấp toàn bộ bối cảnh dự án, kiến trúc kỹ thuật, kịch bản pitch, nội dung 6 slide, và bộ câu hỏi bảo vệ kỹ thuật của **ReturnLens v9.1** — phiên bản tinh chỉnh phẳng thực sự (Flat Rendering), triệt tiêu hoàn toàn lỗi theme xanh/shadow ngầm, nới rộng khoảng cách hiển thị và tối ưu mật độ chữ để nộp chính thức cho Ban Giám Khảo (BGK) tại **Vòng Ý Tưởng (Idea Round) — AgentX Hackathon 2026, Track PS-04**.

---

## PHẦN DÀNH CHO USER: CÂU LỆNH (PROMPT) GỢI Ý ĐỂ COPY VÀO GPT

Nếu bạn muốn gửi tài liệu này cho ChatGPT (hoặc bất kỳ AI nào khác) để review đánh giá, hãy copy toàn bộ đoạn trong khung bên dưới:

```markdown
Bạn là một Giám khảo kỹ thuật cấp cao (Senior Hackathon Technical Judge) và Chuyên gia Đánh giá An toàn Hệ thống AI (AI Safety Auditor) tại AgentX Hackathon 2026. 

Dưới đây là hồ sơ chi tiết của dự án "ReturnLens v9.1" thuộc Track PS-04 (Autonomous Support Agent for Solo D2C Merchants) cho VÒNG Ý TƯỞNG (Idea Round).

Hãy đọc kỹ toàn bộ tài liệu hồ sơ dưới đây và thực hiện review độc lập theo các tiêu chí:
1. ĐỊNH VỊ SẢN PHẨM & GIÁ TRỊ THỰC TẾ: Ý tưởng có giải quyết đúng "nỗi đau" của solo seller bán hàng online khi xử lý đổi trả/khiếu nại không? Có tránh bẫy overclaim hay không?
2. THIẾT KẾ RÀNH MẠCH VỀ QUYỀN HẠN (AUTHORITY BOUNDARIES): Ranh giới giữa Agent và Con người (Solo Seller) đã đủ an toàn chưa? (Agent chỉ trích xuất, đối chiếu, đề xuất và soạn thảo; Con người duyệt các hành động có hậu quả tài chính).
3. TÍNH KHẢ THI KỸ THUẬT (FEASIBILITY TRONG 24H): Lộ trình 24 giờ có tập trung vào cốt lõi (Sprint Core) và tách biệt rõ ràng các tính năng nâng cao (Stretch Goals) không?
4. ĐỒNG BỘ NARRATIVE & SỰ HỢP LÝ CỦA PITCH 3 PHÚT: Câu chuyện xuyên suốt từ Slide 1 đến Slide 6 có mượt mà, logic và thuyết phục không?
5. HỆ THỐNG ART DIRECTION & DESIGN: Nhận xét về sự hoàn thiện trong bản v9.1 (triệt tiêu theme xanh/shadow ngầm, bố cục phẳng thực sự, khoảng cách visual thoáng đãng trên Slide 3, bảng ma trận Slide 5 dùng phông Regular dễ đọc, Slide 6 tách biệt hai cột với gutter rộng).

Đưa ra nhận xét khách quan, chỉ ra các điểm mạnh vượt trội, các điểm cần lưu ý khi bước vào vòng code 24 giờ tiếp theo, và chấm điểm dự kiến cho vòng ý tưởng này.
```

---

# TỔNG QUAN HỒ SƠ DỰ ÁN (PROJECT DOSSIER)

### 1. Thông tin chung
- **Tên dự án:** ReturnLens
- **Phiên bản:** v9.1 (Final Polish & Flat Rendering Edition)
- **Cuộc thi:** AgentX Hackathon 2026
- **Track dự thi:** PS-04 — Autonomous Support Agent for Solo D2C Merchants
- **Team thực hiện:** Team Rookie (3 thành viên: Workflow/Rules, Vision/Frontend, Fixtures/Testing)
- **Slogan / Tagline:** *“Every return decision, backed by evidence.”*
- **One-Liner:** Một trợ lý đối chiếu bằng chứng giúp solo seller kết nối khiếu nại của khách, video mở hộp, dữ liệu đơn hàng và chính sách đổi trả thành một hồ sơ tổng hợp rõ ràng để người bán tự đưa ra quyết định xử lý tiếp theo.

### 2. Danh mục Deliverables & Checksum Cryptographic
Tất cả các tệp nghiệm thu đã được tạo, kiểm tra tự động và đồng bộ 100% giữa thư mục gốc và thư mục `deliverables/`:

| Tên Deliverable | Định dạng | Kích thước | SHA256 Checksum | Mô tả |
| :--- | :--- | :--- | :--- | :--- |
| `ReturnLens_v9_1.pptx` | PowerPoint | 1,362,278 bytes | `c4f7a117f458e17c035711d52d0d288667f45c55b4ba7b62f484db2bbb10eea9` | Slide deck chỉnh sửa trực tiếp, nhúng speaker notes đầy đủ, 100% flat |
| `ReturnLens_v9_1.pdf` | Vector PDF | 243,528 bytes | `0e99fd0317925e11d0052699b744ad12be4b94f0907c2232c2ad1ddb05f68dc4` | Bản in PDF chuẩn vector 6 trang, tỷ lệ 16:9 widescreen (960×540 pt) |
| `ReturnLens_v9_1.html` | Interactive Web | 2,376,770 bytes | `fb446a4fb17f75ae97d119e1b00e110f49fefdb1a6d80ee8727c09951c477a2d` | Trình chiếu web độc lập tương tác bàn phím ($\leftarrow$/$\rightarrow$) |
| `ReturnLens_v9_1_preview.png` | Contact Sheet | 745,747 bytes | `de4919f1375ab54e011ec6516120511302df183e36a47bf51c93d19b81db69f7` | Ảnh tổng quan 6 slide tỷ lệ 2×3 (kích thước chuẩn 2352×882 px) |
| `content/deck_data_v9_1.json` | JSON Data | 15,318 bytes | `9e0bb5cd022b742bd30386b5b3a7e7a96999c661a349fb0c781d33bcae8b16ba` | Single Source of Truth cho nội dung, kịch bản pitch và Q&A |
| `src/assets/v9_1_pptx_renders/` | PNG Renders | 6 slide PNGs | Đầy đủ 6 slide render ở độ phân giải cao 1920×1080 px |
| `V9_1_QA_REPORT.md` | Báo cáo QA | Markdown | Tài liệu kiểm thử 9 điểm tự động và phân tích pixel triệt tiêu theme blue |

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
    1. Chấp nhận lỗi kho gửi nhầm $\rightarrow$ Phát hành nhãn đổi hàng.
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

### Vòng lặp làm rõ trong Case C (Case C Clarification Loop):
Khách hàng không thể "tái diễn" lần mở hộp ban đầu (unboxing là hành động diễn ra một lần). Do đó, nếu video ban đầu quá mờ hoặc tối:
- Agent không bao giờ tự động từ chối khiếu nại của khách.
- Thay vì yêu cầu quay lại mở hộp, Agent gửi thông báo yêu cầu cung cấp thêm **một ảnh chụp cận cảnh rõ nét của sản phẩm, phần hư hỏng hoặc nhãn mã vạch trên vỏ hộp**.
- Bằng chứng mới được lưu vào cùng hồ sơ vụ việc hiện tại.
- Giới hạn tối đa **1 lần yêu cầu bổ sung** tự động. Nếu sau 1 lần vẫn chưa rõ, vụ việc được chuyển trực tiếp cho Seller để tự liên hệ giải quyết.

---

# 3. NỘI DUNG VÀ SPEAKER NOTES CHI TIẾT CỦA 6 SLIDE (V9.1)

Tổng số từ nói trong kịch bản: **382 từ** (thời lượng ước tính: 2 phút 45 giây đến 3 phút, tốc độ nói đĩnh đạc ~130 từ/phút).

```
========================================================================================
SLIDE 1: PRODUCT INTRODUCTION & FLAT CONSOLE MOCKUP
========================================================================================
Kicker:      AgentX Hackathon 2026 · Track PS-04
Title:       ReturnLens
Tagline:     Every return decision, backed by evidence.
Value Prop:  An evidence triage assistant that connects customer claims, unboxing video, 
             order records, and store policy into one clear decision pack for solo merchants.
Thesis:      Models observe. Code verifies. Seller authorizes.
Boundary:    Agent collects info & clarifies · Seller approves returns, labels & refunds
Mockup:      CASE #RT-8821 · NEEDS SELLER DECISION
             Order #ORD-7729 · Studio Wireless · ₹1,499 paid · Delivered 4d ago
             Ordered: White (SKU HEAD-WHT-02) | Observed: Black (Frame 00:07)
             Color mismatch: Ordered White vs Observed Black · Barcode unverified
             Recommended Next Step: Request outer-box label photo
             CTA: Review Evidence & Decide →

SPEAKER NOTES (34 words / ~18s):
"For solo merchants, customer returns are a constant headache: messy claims, long unboxing videos, and disconnected order records. ReturnLens connects this evidence into one clear decision pack. Models observe. Code verifies. The seller authorizes every decision."

========================================================================================
SLIDE 2: THE PROBLEM (ONE CLAIM. FOUR SOURCES.)
========================================================================================
Kicker:      The Merchant's Reality
Title:       One claim. Four disconnected sources.
Quote:       “I ordered white headphones, but received black. Please refund me.”
             Attached: unboxing_video.mp4 (18s)
Sources:     01 Customer Chat: Claim text and unboxing video upload
             02 Shopify Order: Matte White (SKU HEAD-WHT-02), ₹1,499 paid
             03 Courier Scan: Shippo confirms delivery 4 days ago
             04 Store Policy: 7-day return window for wrong or damaged items
Question:    Packing mistake, delivery error, or unboxing swap? The seller needs verified 
             facts before deciding to refund, replace, or inspect. (Regular font, generous whitespace)

SPEAKER NOTES (61 words / ~30s):
"A customer requests a refund claiming they received black headphones instead of white, attaching an 18-second video. Today, the solo seller must jump between chat messages, order details on Shopify, courier delivery records, and store return policies. It is manual, slow, and vulnerable to guesswork. The seller has to make a financial call without knowing which facts are actually verified."

========================================================================================
SLIDE 3: THE CORE DEMONSTRATION (WHITE ORDERED. BLACK RECEIVED.)
========================================================================================
Kicker:      Core Evidence Comparison
Title:       White ordered. Black received.
Subtitle:    ReturnLens highlights the visible discrepancy without jumping to unverified conclusions.
Left Box:    STORE SPECIFICATION · SHOPIFY | Ordered: White | HEAD-WHT-02 · ₹1,499 paid · Delivered 4d ago
Center:      ≠
Right Box:   OBSERVED EVIDENCE · VIDEO FRAME 00:07 | Observed: Black | Barcode unverified · Exact model unverified
Options:     1. Accept mis-pack: Issue replacement return label
             2. Request label photo: “Please share the outer-box label so we can check your shipment.”
             3. Hold for inspection: Inspect returned parcel before refund
Footnote:    * Illustrative scenario with staged mock evidence. Barcode and exact model unverified.

SPEAKER NOTES (91 words / ~45s):
"Here is how ReturnLens handles that claim. On the left is the order record: Matte White headphones delivered four days ago. On the right, our vision pipeline extracts keyframe 00:07 from the unboxing video, confirming the customer received black headphones. Instead of guessing fraud or packing errors, ReturnLens surfaces what is verified—the color mismatch—and what is not, such as the outer package barcode. It prepares three next steps. The recommended action drafts a polite clarification asking for the box label, ready for the seller to review and approve with one click."

========================================================================================
SLIDE 4: AGENT WORKFLOW & BOUNDARIES
========================================================================================
Kicker:      Agent Architecture
Title:       From evidence to next step.
Subtitle:    A structured pipeline where models observe, code verifies, and the seller approves.
Stages:      1. Collect (Vision & Ingestion): Ingests chat, courier scan, extracts keyframes.
             2. Compare (Rule Engine): Cross-checks observed color vs catalog specs, dates, 7-day policy.
             3. Recommend (Planning & Drafting): Synthesizes matches/discrepancies into 3 choices & drafted replies.
             4. Seller Decides (Merchant Decision): Reviews evidence dossier and approves returns/labels/refunds.
Loop:        Case C Clarification Loop: Unclear evidence → Request a close-up photo → Add to case file → Continue review.
             If footage is dark or blurry, agent requests 1 close-up photo or box label. Never auto-rejects.

SPEAKER NOTES (86 words / ~40s):
"Behind the scenes, ReturnLens follows a four-step pipeline. Ingestion extracts keyframes from video and gathers customer chat. Our rule engine cross-checks observed visual traits against store policies and courier dates. The planner synthesizes these into three actionable choices and drafts customer replies. Finally, the merchant makes the decision. If video footage is blurry—as in Case C—the agent requests a clear close-up photo of the product or outer label and appends it to the case file. It never auto-rejects a customer."

========================================================================================
SLIDE 5: SCENARIOS MATRIX
========================================================================================
Kicker:      Prototype Scenarios
Title:       Three situations. Clear next steps.
Subtitle:    Expected prototype behavior across clean, conflicting, and unclear evidence.
Table:
- Case A (Consistent Claim): Unboxing video shows cracked headband; delivered 4 days ago, within 7-day window.
  Agent: Validates delivery date & visible headband crack; drafts return shipping label.
  Seller: Approve return label. Refund waits for parcel receipt. (Regular font)
- Case B (Color Discrepancy): Customer claims: “I ordered white headphones, but received black.”
  Agent: Flags color mismatch; notes barcode unverified; drafts 3 resolution choices.
  Seller: Choose a resolution or request the box label. (Regular font)
- Case C (Unclear Evidence): Video footage is too dark or blurry to confirm product condition or serial label.
  Agent: Requests 1 clear close-up photo or box label; appends new evidence to same case file.
  Seller: Review added evidence; handle manually if still unclear. (Regular font)

SPEAKER NOTES (56 words / ~25s):
"Our planned prototype covers three core merchant scenarios. Case A handles consistent claims, such as a cracked headband, drafting a return label for seller approval. Case B handles color discrepancies by offering three clear merchant paths. Case C handles dark or blurry footage by requesting close-up photos, ensuring customers are treated fairly before escalating to the seller."

========================================================================================
SLIDE 6: 24-HOUR PROTOTYPE SPRINT
========================================================================================
Kicker:      24-Hour Prototype Sprint
Title:       A focused 24-hour prototype.
Timeline:    00–06h: Ingestion & Schema (Mock fixtures; case state schema)
             06–12h: Vision & Rules (Keyframe extraction & policy checks)
             12–18h: Seller Console UI (Side-by-side evidence review console)
             18–24h: Walkthrough & QA (Walkthroughs & checks across Cases A, B, C)
Team:        Team:
             • A — Workflow, policy checks and clarification.
             • B — Evidence extraction and seller console.
             • C — Scenario data and walkthrough checks.
Scope:       Build first: Mock order and courier data · Keyframe evidence viewer · 3 core scenarios · Fail-closed seller console
             Later: Live Shopify and courier APIs · Automated payment gateways · Advanced video forensics
Takeaway:    One clear evidence pack. The seller makes the call. (No quotes, directly on canvas)

SPEAKER NOTES (54 words / ~22s):
"For the 24-hour hackathon sprint, we have defined a strict scope. The team will deliver mock data fixtures, frame extraction, policy rule validation, and the seller console across our three scenarios. Live payment gateways and carrier integrations are stretch goals. ReturnLens: one clear evidence pack, so the solo seller can make the call with confidence."
```

---

# 4. BỘ 5 CÂU HỎI & TRẢ LỜI BẢO VỆ KỸ THUẬT TRƯỚC BAN GIÁM KHẢO (DEFENSE Q&A)

### Câu hỏi 1: Nếu video mở hộp bị lóa sáng, chất lượng kém hoặc bị cắt ghép thì AI xử lý thế nào?
**Trả lời:**  
ReturnLens áp dụng nguyên tắc **Fail-Closed (an toàn khi không chắc chắn)**. Mô hình thị giác chỉ trích xuất những gì có độ tin cậy cao; nếu khung hình bị mờ hoặc không đọc được nhãn mã vạch, hệ thống sẽ gắn nhãn rõ ràng: *"Barcode unverified"*. Trong tình huống bằng chứng không đủ rõ (Case C), Agent tuyệt đối không tự động từ chối khiếu nại, mà sẽ kích hoạt vòng lặp làm rõ: yêu cầu khách gửi thêm một ảnh chụp cận cảnh của phần hư hỏng hoặc nhãn ngoài hộp. Hồ sơ vụ việc được giữ nguyên để bổ sung bằng chứng mới, và chỉ cho phép tối đa 1 lần yêu cầu tự động trước khi chuyển trực tiếp cho người bán xử lý.

### Câu hỏi 2: Tại sao không để Agent tự động hoàn tiền luôn cho khách để tiết kiệm tối đa thời gian cho seller?
**Trả lời:**  
Trong thương mại điện tử D2C dành cho solo seller, tự động hoàn tiền từ video là một lỗ hổng bảo mật nghiêm trọng (rủi ro gian lận hoàn tiền - friendly fraud). Hơn nữa, việc hoàn tiền và tạo nhãn vận chuyển đổi hàng đều là các hành động làm phát sinh chi phí trực tiếp trên tài khoản của người bán. Do đó, thiết kế an toàn của ReturnLens quy định: **Agent chỉ làm nhiệm vụ tổng hợp thông tin, xác thực ngày tháng và chuẩn bị sẵn các phương án (drafted replies/labels); người bán luôn là người đưa ra quyết định cuối cùng và bấm nút phê duyệt (Seller authorizes).**

### Câu hỏi 3: Trong 24 giờ hackathon, làm sao team có thể tích hợp được cả Shopify, Shippo bưu tá và cổng thanh toán Stripe?
**Trả lời:**  
Team xác định kỷ luật phạm vi rất rõ ràng trong Slide 6:
- **Build first (Phải hoàn thành trong 24h):** Sử dụng các file fixture JSON mô phỏng chính xác cấu trúc dữ liệu đơn hàng Shopify, lịch sử quét mã bưu tá Shippo, trích xuất khung hình từ video mở hộp thực tế, và xây dựng giao diện Console đối chiếu cho Seller với 3 kịch bản kiểm thử (Case A, B, C).
- **Later (Không đưa vào cam kết 24h):** Tích hợp webhook Shopify trực tiếp, kết nối API bưu tá thật, và cổng thanh toán tự động được xếp vào giai đoạn sau hackathon. Điều này đảm bảo tính khả thi tuyệt đối của prototype trong ngày thi.

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

# 5. CHI TIẾT NÂNG CẤP TỪ V9 LÊN V9.1 (CHANGELOG)

1. **Triệt tiêu 100% theme xanh và shadow kế thừa:**
   - Đã xóa toàn bộ thẻ `<p:style>` khỏi các thẻ shape trong file OpenXML (giảm từ 30 thẻ về 0).
   - Kiểm tra phân tích pixel trên các slide render cho thấy số pixel màu xanh theme đã giảm từ hơn 116.000 pixel ở bản v9 về 0 pixel ở bản v9.1.
   - Thêm thẻ `<a:effectLst/>` rỗng để vô hiệu hóa hoàn toàn hiệu ứng bóng đổ và góc nổi mặc định.

2. **Slide 1:**
   - Seller mockup sử dụng viền xám siêu mảnh 0.5pt, không bóng đổ.
   - Nút CTA xanh rừng phẳng hoàn toàn, chữ `Review Evidence & Decide →` nằm trên một dòng duy nhất.

3. **Slide 2:**
   - Xóa bỏ nhãn `THE SELLER'S QUESTION:` bị lặp.
   - Đổi đoạn câu hỏi kết luận sang phông Regular (16.5pt), không in đậm toàn bộ đoạn, chừa khoảng trắng thoáng đãng.

4. **Slide 3:**
   - Nới rộng khoảng cách giữa Subtitle và nhãn ảnh (đạt $0.203"$).
   - Thu nhỏ hai ảnh đồng tỷ lệ 16:9 ($4.60" \times 2.57"$).
   - Khoảng trống từ dòng metadata cuối đến đường kẻ ngang divider đạt $0.179"$ (vượt mức yêu cầu 0.12–0.15").
   - Khoảng cách từ divider xuống hàng 3 lựa chọn đạt $0.133"$.
   - Option 2 dùng vạch xanh rừng phẳng, không bóng đổ.

5. **Slide 4:**
   - Bỏ khung chữ nhật có bóng đổ bao quanh Case C; chuyển sang phân nhóm bằng khoảng trắng và đường kẻ mảnh.
   - Xóa dòng tóm tắt trách nhiệm ở đáy slide để tránh lặp lại tiêu đề và flow; ý này được giữ nguyên trong speaker notes.

6. **Slide 5:**
   - Chuyển toàn bộ nội dung cột 4 (Seller's Next Step) sang phông Regular, loại bỏ hoàn toàn khối chữ đậm dày.
   - Rút gọn nội dung mỗi ô thành 1-2 ý súc tích, giữ nguyên đầy đủ ý nghĩa và chính sách đổi trả.

7. **Slide 6:**
   - Rút gọn vai trò 3 thành viên: A, B, C.
   - Thay các nhãn tài liệu nội bộ (SCOPE DISCIPLINE) bằng các nhãn tự nhiên: `Team`, `Build first`, `Later`.
   - Gutter giữa hai cột rộng $2.38"$ ($171.2\text{ pt}$), đảm bảo không bao giờ chạm chữ.
   - Câu kết luận `One clear evidence pack. The seller makes the call.` đặt trực tiếp trên nền, không dùng dấu ngoặc kép.

---

# 6. HƯỚNG DẪN KIỂM TRA ĐỘC LẬP TẠI LOCAL (VERIFICATION INSTRUCTIONS)

Nếu muốn chạy kiểm thử lại toàn bộ hệ thống deliverables v9.1 tại máy local:

```powershell
# Di chuyển vào thư mục dự án
cd D:\Code\Code\AIO\Code\hack4hack

# Chạy bộ test tự động 9 điểm của v9.1 (tất cả 9 bài test phải PASS)
python scripts/smoke_test_v9_1.py

# Kiểm tra đảm bảo không gây regression lên bản cũ v9
python scripts/smoke_test_v9.py

# Kiểm tra git status (đảm bảo không bị commit, push hay deploy ngoài ý muốn)
git status --short
```

---
*Tài liệu bàn giao được biên soạn bởi Senior Product & AI Systems Engineer, phục vụ thẩm định kỹ thuật và nộp bài chính thức tại AgentX Hackathon 2026.*

