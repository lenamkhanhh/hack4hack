# RETURNLENS V8 (IDEA ROUND COMPETITION EDITION) — FULL CONTEXT HANDOFF & REVIEW BRIEF

> **TÀI LIỆU BÀN GIAO TOÀN DIỆN DÀNH CHO GPT / REVIEWER ĐỘC LẬP (VÒNG Ý TƯỞNG)**  
> *Bạn có thể tải tệp Markdown này lên ChatGPT (GPT-4o / GPT-o1) hoặc dán toàn bộ nội dung vào khung chat kèm câu lệnh gợi ý ở bên dưới.*

---

## PHẦN DÀNH CHO USER: CÂU LỆNH (PROMPT) GỢI Ý ĐỂ COPY VÀO GPT

```text
Bạn là một Giám khảo Kỹ thuật Cấp cao (Principal Technical Judge), Giám đốc Thiết kế Sản phẩm (Product Design Director) và Chuyên gia Đánh giá An toàn AI (AI Safety Auditor) tại cuộc thi AgentX Hackathon 2026.

Dưới đây là toàn bộ tài liệu bàn giao (Handoff Brief) của dự án "ReturnLens v8 — Idea Round Competition Edition" thuộc Track PS-04 (Autonomous Support Agent for Solo D2C Merchants).

Hãy đọc kỹ toàn bộ tài liệu này (bao gồm định vị sản phẩm cho vòng ý tưởng, hành vi agent, kịch bản đối soát 3 tình huống cốt lõi, toàn bộ nội dung & speaker notes của 6 slide, và kế hoạch thực thi 24h). Sau đó, hãy tiến hành một đợt REVIEW ĐỘC LẬP VÀ TOÀN DIỆN theo 7 tiêu chí:
1. Độ thuyết phục của Narrative & Pitch Flow trong 3 phút (Câu chuyện từ nỗi đau solo seller -> Star Demo đối chiếu màu -> Cơ chế Agent -> 3 Tình huống -> Roadmap 24h).
2. Tính đúng đắn của việc định vị sản phẩm cho Vòng Ý Tưởng (Tập trung vào giá trị thực tế của trợ lý phân loại, không lấy "chống gian lận" làm lời hứa trung tâm, thấy rõ lợi ích cho cả người bán và khách hàng).
3. Tính trung thực & phòng thủ bằng chứng (Evidentiary Grounding — Thừa nhận trung thực giới hạn camera/mã vạch, gắn nhãn staged mock evidence, không overclaim năng lực thị giác máy tính).
4. Tính hợp lý của kiến trúc Agentic (Chuỗi Thu thập -> Đối chiếu -> Đề xuất -> Phê duyệt; vòng lặp Case C có lưu ngữ cảnh và phục hồi phiên; tách bạch Models observe / Code verifies / Seller authorizes).
5. Hàng rào an toàn Fail-Closed (Zero automated refunds, zero automated rejections, người bán giữ quyền phán quyết cuối cùng).
6. Độ đanh thép của 5 câu trả lời bảo vệ kỹ thuật trước ban giám khảo (Tại sao cần agent, tại sao khác màu chưa phải gian lận, xử lý video mờ, quyền hạn người bán, prototype 24h chứng minh điều gì).
7. Chấm điểm tổng quan (thang điểm 10) và những lời khuyên sắc bén nhất trước khi bước vào phòng pitching.
```

---

# TỔNG QUAN HỒ SƠ DỰ ÁN (PROJECT DOSSIER)

- **Tên dự án:** ReturnLens
- **Tagline:** *"Every return decision, backed by evidence."* (Mọi quyết định đổi trả đều có bằng chứng bảo chứng).
- **One-liner:** Một trợ lý giúp solo seller gom yêu cầu của khách, bằng chứng video, dữ liệu đơn hàng và chính sách thành một hồ sơ dễ xem để quyết định bước xử lý tiếp theo.
- **Cuộc thi:** AgentX Hackathon 2026 — Track PS-04: *Autonomous Support Agent for Online Sellers*.
- **Vòng thi:** **Vòng Ý Tưởng (Idea Round)**.
- **Đội thi:** Team Rookie (3 thành viên: Person A - Workflow/Rules, Person B - Vision/UI, Person C - Fixtures/Testing).
- **Mã nguồn (Repository):** `https://github.com/lenamkhanhh/hack4hack.git` (Nhánh: `main`).
- **Phiên bản hoàn thiện:** **ReturnLens v8 (Idea Round Competition Edition)**.
- **Ranh giới thực tế của Prototype (Prototype Reality & Honest Demarcation):**
  - ReturnLens tại vòng thi này là một **Đề án Sản phẩm & Kiến trúc Hệ thống hoàn chỉnh (Product & Architecture Proposal)** kèm **Bộ đặc tả kiểm thử tự động (Executable Prototype Baseline)**.
  - Dự án tập trung vào trải nghiệm phân loại khiếu nại (return triage), sử dụng dữ liệu kiểm thử chuẩn (mock fixtures), trích xuất keyframe thực tế từ video và quy trình kiểm tra quy tắc tất định.
  - Dự án **không mở rộng phạm vi** thành việc kết nối webhook live production với Shopify thật hay tích hợp cổng thanh toán Stripe/ngân hàng thật. Các thành phần live integration được phân định rõ là kế hoạch phát triển tương lai (Stretch Goals).
- **Bộ Deliverables chuẩn v8:**
  1. `ReturnLens_v8.pptx` & `deliverables/ReturnLens_v8.pptx` (1,390,060 B, SHA256: `9d4c4a06971b...`, 16:9, nhúng đủ Speaker Notes cho 6 slide, đóng gói `ZIP_STORED` deterministic).
  2. `ReturnLens_v8.pdf` & `deliverables/ReturnLens_v8.pdf` (260,895 B, SHA256: `b123bf2b80cc...`, Vector 6 trang, xuất trực tiếp từ PowerPoint COM).
  3. `ReturnLens_v8.html` & `deliverables/ReturnLens_v8.html` (2,764,642 B, SHA256: `93bbd710241b...`, Single-file Interactive Web Deck, offline-resilient font stacks).
  4. `ReturnLens_v8_preview.png` & `deliverables/ReturnLens_v8_preview.png` (1,189,637 B, SHA256: `c47dfdfcd061...`, Contact Sheet 2352×882, tỷ lệ 16:9 chuẩn).
  5. Bộ ảnh render PPTX 1920×1080: `src/assets/v8_pptx_renders/` kèm `render_manifest.json`.
  6. Extended Smoke Test: `scripts/smoke_test_v8.py` (9/9 PASS).
  7. Báo cáo chất lượng: `V8_QA_REPORT.md`.

---

# 1. ĐỊNH VỊ LẠI Ý TƯỞNG CHO VÒNG Ý TƯỞNG (PRODUCT REPOSITIONING)

### 1.1. Giá trị cốt lõi cụ thể cho Solo Merchant
ReturnLens không phải là một công cụ phức tạp hay hứa hẹn "tiết kiệm 90% thời gian" vô căn cứ. Giá trị của sản phẩm được thể hiện cụ thể qua 5 điểm trên một màn hình:
1. **Thấy ngay khiếu nại:** Seller đọc được ngay khách hàng đang phàn nàn điều gì (màu sắc, vỡ hỏng, thiếu hàng).
2. **Biết rõ điểm khớp và điểm mâu thuẫn:** Điểm nào khớp với dữ liệu kho, điểm nào mâu thuẫn, điểm nào còn thiếu.
3. **Có frame video tham chiếu:** Trích xuất đúng khung hình bằng chứng kèm mốc giây cụ thể để người bán tự kiểm tra bằng mắt trong vài giây.
4. **Phương án xử lý có sẵn:** Chuẩn bị sẵn 3 lựa chọn thực tế kèm câu trả lời dự thảo cho khách.
5. **Người bán giữ quyền quyết định:** 1-click để phê duyệt, không có hành động ngầm nào tự diễn ra.

### 1.2. Không lấy "chống gian lận" làm lời hứa trung tâm
- Việc sản phẩm trong video khác màu với đơn hàng có thể xuất phát từ:
  - Nhân viên kho đóng nhầm hàng (warehouse mis-pack).
  - Khách hàng nhận nhầm bưu kiện của người nhà.
  - Hoặc một ca tráo hàng khi mở hộp.
- ReturnLens **không kết luận khách hàng là kẻ gian lận**. Hệ thống chỉ nêu rõ mâu thuẫn trực quan (`≠ Color Discrepancy`) để người bán nắm bắt tình huống và tự lựa chọn phương án giải quyết phù hợp với uy tín của cửa hàng.

### 1.3. Lợi ích cho cả hai phía (Two-Sided Benefit)
- **Cho Solo Merchant:** Thoát khỏi cảnh nhảy qua lại giữa 4 tab (Chat, Shopify, Shippo, Policy), giảm thiểu rủi ro hoàn tiền bừa hoặc từ chối nhầm.
- **Cho Khách hàng:** Yêu cầu được phản hồi nhanh chóng, có hướng dẫn bổ sung video rõ ràng nếu video đầu tiên bị tối/mờ, và **tuyệt đối không bao giờ bị AI tự động từ chối khiếu nại**.

---

# 2. HÀNH VI AGENT ĐƯỢC GIẢI THÍCH DỄ HIỂU (COLLECT $\rightarrow$ COMPARE $\rightarrow$ RECOMMEND $\rightarrow$ AUTHORIZE)

Agent trong ReturnLens được xây dựng theo một chuỗi hành động trực quan, logic:

```
[ Khách gửi tin nhắn & video unboxing ]
                  │
                  ▼
         1. COLLECT (Thu thập)
  • Ingest tin nhắn, video keyframes
  • Truy xuất đơn hàng Shopify & lịch trình Shippo
                  │
                  ▼
         2. COMPARE (Đối chiếu)
  • Kiểm tra thời hạn đổi trả 7 ngày
  • So sánh màu sắc, thuộc tính sản phẩm
                  │
                  ▼
         3. RECOMMEND (Đề xuất)
  • Phát hiện mâu thuẫn / thiếu sót
  • Chuẩn bị 3 lựa chọn giải quyết & dự thảo câu trả lời
  • [Nếu video tối/mờ]: Kích hoạt Case C Clarification Loop
                  │
                  ▼
         4. AUTHORIZE (Người bán quyết định)
  • Solo seller duyệt 1-click phương án mong muốn
  • Fail-closed: Zero automated refunds, zero auto-denials
```

### Minh họa bằng Case C (Dynamic Clarification Loop):
Khi khách gửi video unboxing chỉ dài 4 giây, quá tối hoặc rung lắc:
1. Agent nhận biết chất lượng bằng chứng không đủ để quan sát tem hoặc sản phẩm (`brightness score < 50/255`).
2. Thay vì từ chối khách, agent gửi tin nhắn hướng dẫn cụ thể: *"Bạn vui lòng bật đèn hoặc quay ở nơi đủ sáng để shop thấy rõ tem niêm phong nhé"*.
3. Agent lưu ngữ cảnh hội thoại, chuyển trạng thái vé sang `WAITING_FOR_EVIDENCE`.
4. Khi khách tải video mới lên, agent tự động tiếp tục xử lý trên cùng một hồ sơ khiếu nại.
5. **Chống lặp vô hạn:** Giới hạn cứng **tối đa 1 lần thử lại (1 retry)**. Nếu video gửi lại vẫn không đạt, ca khiếu nại được chuyển thẳng cho người bán xử lý thủ công kèm toàn bộ lịch sử.

---

# 3. BA TÌNH HUỐNG CỐT LÕI (CORE SCENARIOS)

Dự án tập trung vào 3 kịch bản đại diện cho 95% thực tế đổi trả hàng của solo merchant:

### Tình huống A — Bằng chứng phù hợp (Consistent Claim):
- **Tình huống:** Video unboxing quay rõ gọng tai nghe bị nứt gãy ngay khi mở hộp carton; đơn hàng giao cách đây 4 ngày (trong khung 7 ngày).
- **Hành động của Agent:** Xác thực mốc giao hàng và vết nứt vật lý; chuẩn bị sẵn nhãn đổi trả hàng để seller duyệt.
- **Kết quả cho Seller:** 1-click để duyệt gửi nhãn đổi trả. Tiền hoàn vẫn ở trạng thái chờ (`pending_return_receipt`) cho đến khi bưu tá quét nhận kiện hàng vật lý tại kho.

### Tình huống B — Lệch màu sắc (Color Discrepancy — Star Demo):
- **Tình huống:** Khách đặt Tai nghe Trắng (Matte White, SKU `HEAD-WHT-02`, giá ₹1,499), nhưng video tại 00:07 mở ra tai nghe màu Đen.
- **Nguyên tắc Grounding trung thực:**
  - Agent ghi nhận: *"Observed: Black Casing · Barcode unverified · Exact model unverified"*.
  - Tuyệt đối không overclaim rằng AI đã đọc được mã vạch barcode hay định danh chắc chắn model nếu tem mã vạch không rõ.
- **Hành động của Agent:** Chặn tự động hóa; làm nổi bật sự khác biệt màu sắc; chuẩn bị sẵn 3 phương án thực tế.
- **3 Lựa chọn cho Seller:**
  1. *Accept warehouse mis-pack:* Chấp nhận do nhân viên kho đóng nhầm hộp màu đen $\rightarrow$ Gửi nhãn đổi hàng.
  2. *Request box label photo:* Yêu cầu khách chụp tem vận đơn dán ngoài vỏ hộp carton để truy xuất ca đóng gói.
  3. *Hold for parcel inspection:* Phê duyệt nhận lại hàng, nhưng giữ lại khoản hoàn tiền để kiểm tra trực tiếp khi hàng về kho.

### Tình huống C — Bằng chứng không rõ (Unclear Evidence):
- **Tình huống:** Video 4 giây bị thiếu sáng nghiêm trọng (<50/255 độ sáng), rung lắc, không thể thấy rõ tình trạng sản phẩm.
- **Hành động của Agent:** Hướng dẫn khách quay lại với ánh sáng tốt; tạm dừng vé ở `WAITING_FOR_EVIDENCE`; tự động phục hồi phiên khi có video mới.
- **Kết quả cho Seller:** Khách hàng có cơ hội giải thích công bằng. Nếu lần 2 vẫn không đạt, chuyển thẳng cho seller quyết định kèm đầy đủ video lịch sử.

*(Lưu ý: Tình huống D về kiểm tra chuỗi khung hình liên tục / video forensics được xếp vào nhóm tính năng mở rộng - Stretch Goal, không phải lời hứa cốt lõi).*

---

# 4. CẤU TRÚC 6 SLIDE CHO 3 PHÚT PITCH & FULL TECHNICAL SPEAKER NOTES

### Slide 1: Product Introduction (~15 giây)
- **Tiêu đề:** ReturnLens — *Every return decision, backed by evidence.*
- **Nội dung:** Giới thiệu giải pháp trợ lý phân loại đổi trả có bảo chứng bằng chứng số.
- **Console Mockup trực quan:** Thể hiện đơn hàng #ORD-7729 (Matte White, ₹1,499), video unboxing frame 00:07 (Black casing), cờ mâu thuẫn màu sắc, và nút bấm hành động duy nhất: **`Review Evidence & Decide →`**.
- **Speaker Notes (Script 0:00 - 0:15):**
  > "Judges, this is ReturnLens. For independent online sellers, returns are exhausting. When a customer claims they received the wrong product, the solo merchant is stuck cross-referencing customer chat, Shopify orders, and courier tracking just to figure out what happened. ReturnLens unifies customer claims, video evidence, and store rules into one simple decision pack. Notice our core button: 'Review Evidence & Decide'. We never automate refunds or rejections. The model observes, our code verifies, but the seller always authorizes the decision."

---

### Slide 2: A Seller's Decision Problem (~25 giây)
- **Tiêu đề:** One customer claim. Four disconnected sources.
- **Nội dung:**
  - Tin nhắn khiếu nại thực tế: *"I opened the delivery box today and the headphones inside are black, not the white ones I ordered. I want an immediate refund."*
  - 4 nguồn dữ liệu rời rạc: Chat khách hàng, Đơn Shopify, Tra cứu Shippo, Chính sách shop.
  - Câu hỏi nan giải: *"Lỗi do kho, do nhầm lẫn hay tráo hàng?"* Hoàn bừa thì mất tiền, từ chối vội thì mất khách.
- **Speaker Notes (Script 0:15 - 0:40):**
  > "A customer chats in: 'You sent the wrong color, refund me immediately' and attaches an unboxing clip. Right now, the merchant has to jump across four separate tabs: checking the chat claim, looking up the SKU in Shopify, verifying courier delivery on Shippo, and re-reading their store return policy. Was this a warehouse mix-up, an honest confusion, or an item swap? Blindly refunding burns scarce margin, but blindly rejecting the customer destroys brand loyalty. Solo merchants don't have a fraud department—they need a unified view of the facts."

---

### Slide 3: The Core Demonstration (~45 giây)
- **Tiêu đề:** The order says white. The video shows black.
- **Nội dung:**
  - Hai hình ảnh lớn khóa đúng tỷ lệ 16:9 ($1376 \times 768$): Ảnh catalog tai nghe trắng vs Ảnh video tai nghe đen tại 00:07 kèm huy hiệu `≠ COLOR DISCREPANCY`.
  - Ghi nhận trung thực: Mã vạch và model chính xác chưa được xác minh từ góc quay video.
  - 3 lựa chọn seller rõ ràng, dễ hiểu. Có nhãn: `* Illustrative concept scenario with staged mock evidence.`
- **Speaker Notes (Script 0:40 - 1:25):**
  > "Here is our core demonstration. The Shopify order clearly specifies Matte White headphones. But in the unboxing clip at frame seven seconds, the customer unboxes black headphones. ReturnLens instantly flags this visible color mismatch. Crucially, we practice honest AI grounding: our agent acknowledges that the barcode and exact SKU are unverified from the video frame. We do not jump to calling the customer a fraudster—this could easily be a warehouse packing error. Instead, ReturnLens presents three clear, practical options with drafted customer replies ready for the seller to approve."

---

### Slide 4: How the Agent Moves the Case Forward (~40 giây)
- **Tiêu đề:** Models observe. Code verifies. Seller authorizes.
- **Nội dung:**
  - Quy trình 4 bước mạch lạc: **1. Collect $\rightarrow$ 2. Compare $\rightarrow$ 3. Recommend $\rightarrow$ 4. Authorize**.
  - Nhánh xử lý động cho Case C: Khi video tối/mờ, xin bổ sung 1 lần, chờ upload, phục hồi phiên.
  - Phân định ranh giới trách nhiệm: Models quan sát & soạn thảo, Code kiểm tra quy tắc & thời hạn, Seller phê duyệt.
- **Speaker Notes (Script 1:25 - 2:05):**
  > "How does the agent actually work? It follows four clear stages: First, Collect—ingesting the chat, tracking data, and video keyframes. Second, Compare—deterministic code verifies the 7-day window and checks color alignment. Third, Recommend—the agent drafts clear resolution choices. And fourth, Authorize—the merchant makes the call. If evidence is dark or blurry, like in our Case C, the agent guides the customer to turn on a light, pauses the case, and resumes when the new clip arrives. Notice the clean separation: models observe, code verifies rules, and the human seller authorizes."

---

### Slide 5: Three Situations, Three Useful Next Steps (~25 giây)
- **Tiêu đề:** Three situations. Three useful next steps.
- **Nội dung:**
  - 3 cột rõ ràng: **Case A (Khiếu nại hợp lệ / Lỗi vật lý rõ ràng)**, **Case B (Lệch màu sắc / Mâu thuẫn quan sát)**, **Case C (Bằng chứng không rõ / Hướng dẫn quay lại)**.
  - Mỗi cột trình bày gọn: Tình huống $\rightarrow$ Hành vi Agent $\rightarrow$ Kết quả cho Seller.
  - Gắn nhãn: `* Expected prototype behavior across core test scenarios.`
- **Speaker Notes (Script 2:05 - 2:30):**
  > "In our prototype, we focus on three core situations that represent 95% of returns: In Case A, the evidence is consistent—a visible crack on arrival. The agent drafts a return label ready for one-click approval. In Case B, there is a color discrepancy—the agent surfaces the conflict and offers options without accusing the customer. In Case C, the footage is too dark—instead of rejecting the customer, the agent politely asks for a clearer clip with helpful tips. Each scenario leads to an actionable, low-stress outcome for the solo merchant."

---

### Slide 6: A Focused 24-Hour Prototype (~30 giây)
- **Tiêu đề:** A focused 24-hour prototype. Clear scope boundaries.
- **Nội dung:**
  - Timeline 4 giai đoạn: 00–06h (Schema & Fixtures), 06–12h (Vision & Rules), 12–18h (Console UI), 18–24h (End-to-end Walkthrough & QA).
  - 3 vai trò (Person A, B, C; tối đa 2 đầu ra mỗi người).
  - Scope Discipline: **Must Deliver** (Mock fixtures, Keyframe viewer, 3 scenarios, Fail-closed console) vs. **Cut First** (Shopify live API, Cổng thanh toán, Video forensics).
  - Câu kết đắt giá: *“ReturnLens gives solo sellers the clarity of a dedicated returns department, while keeping every final decision in human hands.”*
- **Speaker Notes (Script 2:30 - 3:00):**
  > "For this 24-hour hackathon, our scope is strictly disciplined: Person A builds the state machine and policy checks; Person B builds the keyframe viewer and merchant console; Person C prepares realistic mock fixtures and tests all three scenarios. We are not building live Shopify webhooks or banking integrations during the sprint—our focus is proving the end-to-end evidence triage workflow. ReturnLens gives solo online sellers the clarity of a full-scale returns department, while keeping every decision firmly in human hands. Thank you!"

---

# 5. KỊCH BẢN BẢO VỆ 5 CÂU HỎI KỸ THUẬT HÓC BÚA NHẤT (Q&A DEFENSE)

### Câu hỏi 1: Tại sao cần Agent mà không dùng một biểu mẫu (Form) hay Rules Engine truyền thống?
> **Trả lời:**  
> "Rules Engine truyền thống chỉ kiểm tra được dữ liệu bảng có cấu trúc như ngày giao hàng hay số tiền. Nó hoàn toàn bất lực trước dữ liệu đa phương thức hỗn độn: video mở hộp của khách, tin nhắn chat tự do, và việc phát hiện vết nứt hay màu sắc casing. Agent đóng vai trò là cây cầu nối thông minh: mô hình thị giác trích xuất các quan sát có mốc thời gian cụ thể, còn mã nguồn tất định đối chiếu quy tắc và soạn thảo sẵn các phương án cho người bán duyệt."

### Câu hỏi 2: Tại sao phát hiện khác màu chưa thể kết luận là khách hàng gian lận?
> **Trả lời:**  
> "Trong thương mại điện tử thực tế, tai nghe đen trong hộp tai nghe trắng rất có thể do lỗi nhân viên kho dán nhầm tem hoặc đóng gói nhầm lô hàng. Nếu hệ thống tự động gắn mác 'gian lận' và từ chối khách, thương hiệu sẽ bị hủy hoại uy tín ngay lập tức. ReturnLens định vị trung thực: chúng tôi chỉ nêu rõ có mâu thuẫn màu sắc ('≠ Color Discrepancy') và đưa ra 3 phương án để người bán tự chọn dựa trên hiểu biết về độ chính xác kho bãi của họ."

### Câu hỏi 3: Hệ thống xử lý thế nào khi video unboxing bị tối, mờ hoặc không rõ chi tiết?
> **Trả lời:**  
> "Trong Case C, khi video có chỉ số độ sáng thấp (<50/255) hoặc rung lắc, agent không từ chối khách. Thay vào đó, nó kích hoạt vòng lặp Dynamic Clarification: hướng dẫn khách quay lại nơi đủ sáng, lưu trạng thái vé là `WAITING_FOR_EVIDENCE`, và tự động phục hồi phiên khi có video mới. Để chống lặp vô hạn, chúng tôi áp dụng quy tắc cứng tối đa 1 lần thử lại (1 retry)—nếu vẫn không đạt, ca khiếu nại chuyển thẳng lên người bán xử lý thủ công."

### Câu hỏi 4: Người bán thực sự giữ quyền hạn gì trong hệ thống này?
> **Trả lời:**  
> "Người bán nắm giữ 100% quyền phán quyết cuối cùng. ReturnLens áp dụng triệt để nguyên tắc Fail-Closed: AI không bao giờ được phép tự giải ngân tiền, không tự gửi nhãn vận chuyển hoàn tất và không tự từ chối khách. Agent chỉ chuẩn bị hồ sơ bằng chứng và dự thảo câu trả lời; mọi hành động tài chính đều bắt buộc phải có sự xác nhận 1-click của người bán."

### Câu hỏi 5: Bản prototype 24 giờ của các bạn chứng minh được điều gì khả thi?
> **Trả lời:**  
> "Trong 24 giờ, chúng tôi không cố gắng xây dựng cổng thanh toán thật hay kết nối live API của các sàn. Bản prototype chứng minh tính khả thi của quy trình cốt lõi: từ trích xuất keyframe video unboxing, chạy động cơ kiểm tra quy tắc tất định, điều phối vòng lặp bổ sung bằng chứng Case C, cho đến việc hiển thị bàn làm việc trực quan giúp người bán xử lý trơn tru 3 tình huống đổi trả phổ biến nhất."

---

# 6. DANH MỤC FILE DELIVERABLES V8 VÀ MÃ BĂM SHA256

```text
D:\Code\Code\AIO\Code\hack4hack\HANDOFF_FOR_GPT_REVIEW_v8.md
D:\Code\Code\AIO\Code\hack4hack\V8_QA_REPORT.md
D:\Code\Code\AIO\Code\hack4hack\deliverables\ReturnLens_v8.pdf
D:\Code\Code\AIO\Code\hack4hack\deliverables\ReturnLens_v8.pptx
D:\Code\Code\AIO\Code\hack4hack\deliverables\ReturnLens_v8.html
D:\Code\Code\AIO\Code\hack4hack\deliverables\ReturnLens_v8_preview.png
```

| Deliverable File | Kích thước | SHA256 Checksum |
| :--- | :--- | :--- |
| `ReturnLens_v8.pptx` | 1,390,060 B | `9d4c4a06971b3eeb0c9d784a0c868018e69ee80db9a2f7c006fb179eb42b36e8` |
| `deliverables/ReturnLens_v8.pptx` | 1,390,060 B | `9d4c4a06971b3eeb0c9d784a0c868018e69ee80db9a2f7c006fb179eb42b36e8` |
| `ReturnLens_v8.pdf` | 260,895 B | `b123bf2b80cc2ce57cb5a3d7b87201b1cb417f7d98341ae5fcb621ffc28fcb04` |
| `deliverables/ReturnLens_v8.pdf` | 260,895 B | `b123bf2b80cc2ce57cb5a3d7b87201b1cb417f7d98341ae5fcb621ffc28fcb04` |
| `ReturnLens_v8.html` | 2,764,642 B | `93bbd710241bf97116743306db30a103c8bfaef22c19e5c464efc354ae7bfe42` |
| `deliverables/ReturnLens_v8.html` | 2,764,642 B | `93bbd710241bf97116743306db30a103c8bfaef22c19e5c464efc354ae7bfe42` |
| `ReturnLens_v8_preview.png` | 1,189,637 B | `c47dfdfcd061266b0cf91f165998dfc303f27f88417c805a81caec2a1f1dfeb5` |
| `deliverables/ReturnLens_v8_preview.png` | 1,189,637 B | `c47dfdfcd061266b0cf91f165998dfc303f27f88417c805a81caec2a1f1dfeb5` |
| `src/assets/v8_pptx_renders/render_manifest.json` | 841 B | `c36d39d91f9393a5b6c0e5a8204620f4f9f4a56a6552ea631484e55e094d4d6e` |

---

# 7. KHUNG TIÊU CHÍ ĐÁNH GIÁ DÀNH CHO GPT REVIEWER

Khi thực hiện đợt đánh giá độc lập này, đề nghị GPT xem xét theo thang điểm 10 dựa trên 7 khía cạnh sau:
1. **Pitch Flow & Storytelling (20%):** Câu chuyện 3 phút có cuốn hút, đi thẳng vào vấn đề và giúp ban giám khảo hiểu ngay sản phẩm trong 15 giây đầu không?
2. **Track Fit & Problem Relevance (15%):** Có giải quyết đúng và trúng điểm nghẽn của solo merchant bán hàng trực tuyến không?
3. **Product Positioning for Idea Round (20%):** Định vị như một trợ lý phân loại đổi trả (triage assistant) thay vì công cụ "bắt gian lận" có hợp lý và thực tế hơn không?
4. **Agentic System Architecture (15%):** Luồng xử lý Collect $\rightarrow$ Compare $\rightarrow$ Recommend $\rightarrow$ Authorize và cơ chế Case C có thể hiện rõ tính chất của một AI Agent tự chủ có kiểm soát không?
5. **Safety, Ethics & Human Oversight (15%):** Nguyên tắc Fail-Closed và việc không tự động từ chối/hoàn tiền có bảo vệ quyền lợi của cả người bán lẫn người mua không?
6. **Defensive Readiness & Q&A (10%):** Các câu trả lời cho 5 câu hỏi kỹ thuật có đủ sức thuyết phục và đanh thép trước ban giám khảo không?
7. **Execution Feasibility in 24h (5%):** Ranh giới giữa Must Deliver và Cut First có thực tế cho một kỳ hackathon 24 giờ không?

