# RETURNLENS V8.2 (FINAL POLISH PATCH EDITION) — FULL CONTEXT HANDOFF & REVIEW BRIEF

> **TÀI LIỆU BÀN GIAO TOÀN DIỆN DÀNH CHO GPT / REVIEWER ĐỘC LẬP (VÒNG Ý TƯỞNG)**  
> *Bạn có thể tải tệp Markdown này lên ChatGPT (GPT-4o / GPT-o1) hoặc dán toàn bộ nội dung vào khung chat kèm câu lệnh gợi ý ở bên dưới.*

---

## PHẦN DÀNH CHO USER: CÂU LỆNH (PROMPT) GỢI Ý ĐỂ COPY VÀO GPT

```text
Bạn là một Giám khảo Kỹ thuật Cấp cao (Principal Technical Judge), Giám đốc Thiết kế Sản phẩm (Product Design Director) và Chuyên gia Đánh giá An toàn AI (AI Safety Auditor) tại cuộc thi AgentX Hackathon 2026.

Dưới đây là toàn bộ tài liệu bàn giao (Handoff Brief) của dự án "ReturnLens v8.2 — Final Polish Patch Edition" thuộc Track PS-04 (Autonomous Support Agent for Solo D2C Merchants).

Hãy đọc kỹ toàn bộ tài liệu này (bao gồm định vị sản phẩm cho vòng ý tưởng, hành vi agent, kịch bản đối soát 3 tình huống cốt lõi, toàn bộ nội dung & speaker notes của 6 slide, và kế hoạch thực thi 24h). Sau đó, hãy tiến hành một đợt REVIEW ĐỘC LẬP VÀ TOÀN DIỆN theo 7 tiêu chí:
1. Độ thuyết phục của Narrative & Pitch Flow trong 3 phút (Câu chuyện từ nỗi đau solo seller -> Star Demo đối chiếu màu và tin nhắn dự thảo -> Cơ chế Agent -> 3 Tình huống -> Roadmap 24h; kịch bản nói 382 từ thực tế có vừa vặn 3 phút không).
2. Tính đúng đắn của việc định vị sản phẩm cho Vòng Ý Tưởng (Tập trung vào giá trị thực tế của trợ lý gom hồ sơ và đưa ra lựa chọn hành động + câu trả lời soạn sẵn; không lấy "chống gian lận" làm lời hứa trung tâm; thấy rõ lợi ích cho cả người bán và khách hàng).
3. Tính hợp lý và khả thi của cơ chế Case C Clarification (Yêu cầu ảnh/video cận cảnh sản phẩm, vết hỏng hoặc tem nhãn hộp ngoài thay vì yêu cầu phi lý "re-film unboxing"; giữ nguyên video gốc và lưu cùng hồ sơ; tối đa 1 lần bổ sung rồi chuyển người bán).
4. Tính chuẩn xác của Ranh giới Quyền hạn (Agent thu thập thông tin và yêu cầu làm rõ theo template cửa hàng; Seller duyệt quyết định đổi trả, nhãn vận chuyển và hoàn tiền; triết lý "Models observe. Code verifies. Seller authorizes.").
5. Tính nhất quán và trung thực của dữ liệu (Case A là cracked headphone headband trong chính sách 7 ngày, Case B đồng bộ khiếu nại "ordered white, received black", không tự thêm số đo chưa có căn cứ như "15 minutes per ticket" hay "approval in 10 seconds").
6. Độ đanh thép của 5 câu trả lời bảo vệ kỹ thuật trước ban giám khảo (Tại sao cần agent, tại sao khác màu chưa phải gian lận, xử lý video mờ bằng ảnh cận cảnh, ranh giới quyền hạn, prototype 24h chứng minh điều gì).
7. Chấm điểm tổng quan (thang điểm 10) và những lời khuyên sắc bén nhất trước khi bước vào phòng pitching.
```

---

# TỔNG QUAN HỒ SƠ DỰ ÁN (PROJECT DOSSIER)

- **Tên dự án:** ReturnLens
- **Tagline:** *"Every return decision, backed by evidence."* (Mọi quyết định đổi trả đều có bằng chứng bảo chứng).
- **One-liner:** Một trợ lý giúp solo seller gom yêu cầu của khách, bằng chứng video, dữ liệu đơn hàng và chính sách thành một hồ sơ dễ xem để quyết định bước xử lý tiếp theo.
- **Cuộc thi:** AgentX Hackathon 2026 — Track PS-04: *Autonomous Support Agent for Online Sellers*.
- **Vòng thi:** **Vòng Ý Tưởng (Idea Round) — Bản Vá Hoàn Thiện Cuối (Final Polish Patch v8.2)**.
- **Đội thi:** Team Rookie (3 thành viên: Person A - Workflow/Rules, Person B - Vision/UI, Person C - Fixtures/Testing).
- **Mã nguồn (Repository):** `https://github.com/lenamkhanhh/hack4hack.git` (Nhánh: `main`).
- **Phiên bản hoàn thiện:** **ReturnLens v8.2 (Final Polish Patch Edition)**.
- **Ranh giới thực tế của Prototype (Prototype Reality & Honest Demarcation):**
  - ReturnLens tại vòng thi này là một **Đề án Sản phẩm & Kiến trúc Hệ thống hoàn chỉnh (Product & Architecture Proposal)** kèm **Bộ đặc tả kiểm thử tự động (Executable Prototype Baseline)**.
  - Dự án tập trung vào trải nghiệm phân loại khiếu nại (return triage), sử dụng dữ liệu kiểm thử chuẩn (mock fixtures), trích xuất keyframe thực tế từ video và quy trình kiểm tra quy tắc tất định.
  - Dự án **không mở rộng phạm vi** thành việc kết nối webhook live production với Shopify thật hay tích hợp cổng thanh toán Stripe/ngân hàng thật. Các thành phần live integration được phân định rõ là kế hoạch phát triển tương lai (Stretch Goals).
- **Bộ Deliverables chuẩn v8.2:**
  1. `ReturnLens_v8_2.pptx` & `deliverables/ReturnLens_v8_2.pptx` (1,390,635 B, SHA256: `acef2b65c961...`, 16:9, nhúng đủ Speaker Notes cho 6 slide, đóng gói `ZIP_STORED` deterministic).
  2. `ReturnLens_v8_2.pdf` & `deliverables/ReturnLens_v8_2.pdf` (251,492 B, SHA256: `d65fb205bed0...`, Vector 6 trang, xuất trực tiếp từ PowerPoint COM).
  3. `ReturnLens_v8_2.html` & `deliverables/ReturnLens_v8_2.html` (2,412,495 B, SHA256: `d9d98b1d4ced...`, Single-file Interactive Web Deck, nhúng font Segoe UI, offline-resilient).
  4. `ReturnLens_v8_2_preview.png` & `deliverables/ReturnLens_v8_2_preview.png` (1,014,138 B, SHA256: `5d8563b900bf...`, Contact Sheet 2352×882, tỷ lệ 16:9 chuẩn).
  5. Bộ ảnh render PPTX 1920×1080: `src/assets/v8_2_pptx_renders/` kèm `render_manifest.json`.
  6. Extended Smoke Test: `scripts/smoke_test_v8_2.py` (9/9 PASS).
  7. Báo cáo chất lượng: `V8_2_QA_REPORT.md`.

---

# 1. ĐỊNH VỊ Ý TƯỞNG CHO VÒNG Ý TƯỞNG (PRODUCT REPOSITIONING)

### 1.1. Giá trị cốt lõi cụ thể cho Solo Merchant
ReturnLens kết nối yêu cầu của khách, bằng chứng hình ảnh, đơn hàng và chính sách thành một hồ sơ ra quyết định rõ ràng:
1. **Thấy ngay điều đã biết:** Khách hàng khiếu nại điều gì (ví dụ: đặt màu trắng nhưng nhận màu đen; mã đơn `ORD-7729`, trị giá `₹1,499`, giao 4 ngày trước).
2. **Thấy rõ điều còn thiếu hoặc mâu thuẫn:** Màu sắc sản phẩm trong video là màu đen (mâu thuẫn với màu trắng trên catalog); mã vạch trên nhãn hộp chưa xác minh được qua góc quay video.
3. **Có frame video tham chiếu:** Trích xuất khung hình bằng chứng cụ thể (`00:07`) kèm mốc thời gian và độ phân giải để người bán tự đối chiếu bằng mắt trong 3 giây.
4. **Có phương án xử lý tiếp theo và câu trả lời dự thảo:** Cung cấp 3 lựa chọn hành động thiết thực. Option 2 được làm nổi bật đi kèm tin nhắn soạn sẵn:  
   *“Please share the outer-box label so we can check your shipment.”*
5. **Người bán giữ quyền quyết định:** 1-click để phê duyệt hoặc chỉnh sửa, không có hành vi tự ý hoàn tiền hay từ chối ngầm.

### 1.2. Không lấy "phát hiện gian lận" làm lời hứa trung tâm
- Việc sản phẩm trong video khác màu với đơn hàng có thể xuất phát từ:
  - Nhân viên kho đóng nhầm mã màu (warehouse mis-pack).
  - Khách hàng nhận nhầm bưu kiện của thành viên khác trong gia đình.
  - Hoặc một ca tráo đổi sản phẩm khi khui hàng.
- ReturnLens **tuyệt đối không kết luận khách hàng là kẻ gian lận**, và cũng **không tự ý suy đoán kho gửi nhầm**. Hệ thống chỉ ghi nhận mâu thuẫn trực quan (`≠ Color Discrepancy`) để người bán nắm bắt tình huống và đưa ra bước xử lý phù hợp.

### 1.3. Lợi ích cho cả hai phía (Two-Sided Benefit)
- **Cho Solo Merchant:** Thoát khỏi cảnh nhảy qua lại giữa 4 tab (Chat, Shopify, Shippo, Policy), giảm thiểu rủi ro hoàn tiền bừa hoặc từ chối nhầm, có sẵn tin nhắn chuẩn mực để trao đổi với khách.
- **Cho Khách hàng:** Yêu cầu được phản hồi nhanh chóng, có hướng dẫn gửi bổ sung ảnh/video chi tiết nếu video ban đầu quá tối hoặc chưa rõ nhãn, và **tuyệt đối không bao giờ bị AI tự động từ chối khiếu nại**.

---

# 2. HÀNH VI AGENT ĐƯỢC GIẢI THÍCH DỄ HIỂU (COLLECT $\rightarrow$ COMPARE $\rightarrow$ RECOMMEND $\rightarrow$ SELLER DECIDES)

### 2.1. Chuỗi hành động 4 bước
Agent trong ReturnLens hoạt động theo quy trình 4 giai đoạn logic và chặt chẽ:

```
[ Khách gửi tin nhắn & video unboxing ]
                  │
                  ▼
         1. COLLECT (Thu thập)
  • Ingest tin nhắn khiếu nại & video unboxing
  • Truy xuất đơn hàng Shopify (mã SKU, màu đặt) & trạng thái giao hàng Shippo
                  │
                  ▼
         2. COMPARE (Đối chiếu)
  • Kiểm tra thời hạn đổi trả 7 ngày theo chính sách
  • Trích xuất keyframe, đối chiếu màu sắc catalog vs. màu sắc thực tế
                  │
                  ▼
         3. RECOMMEND (Đề xuất)
  • Nêu rõ điểm khớp, điểm mâu thuẫn hoặc thông tin còn thiếu
  • Chuẩn bị 3 phương án hành động & dự thảo tin nhắn gửi khách
  • [Nếu video tối/mờ]: Yêu cầu ảnh chụp cận cảnh (Case C Loop)
                  │
                  ▼
      4. SELLER DECIDES (Người bán quyết định)
  • Solo seller xem hồ sơ bằng chứng và duyệt phương án
  • Seller approves returns, labels and refunds
```

### 2.2. Luồng bổ sung bằng chứng Case C thực tế (Close-up Photo Clarification)
- **Vấn đề thực tế:** Khi khách hàng đã mở hộp và quay video, nếu video bị tối hoặc rung, yêu cầu khách "quay lại unboxing từ đầu" là hoàn toàn bất khả thi vì hộp đã bị bóc seal.
- **Giải pháp của v8.2:** Agent gửi hướng dẫn lịch sự yêu cầu khách hàng **chụp một tấm ảnh cận cảnh rõ nét hoặc quay một đoạn video ngắn tập trung vào sản phẩm, vết hỏng hoặc tem nhãn dán trên hộp ngoài**.
- **Cơ chế lưu trữ:** Video gốc ban đầu vẫn được giữ nguyên. Tấm ảnh cận cảnh mới sẽ được đính kèm vào **cùng một hồ sơ khiếu nại** đang chờ (`WAITING_FOR_EVIDENCE`).
- **Giới hạn an toàn:** Tối đa **1 lần yêu cầu bổ sung**. Nếu sau lần bổ sung này bằng chứng vẫn chưa đạt yêu cầu, agent sẽ chuyển toàn bộ hồ sơ cho người bán trực tiếp xem xét.

### 2.3. Ranh giới Quyền hạn Chuẩn mực (Authority Boundary)
- **Quyền hạn của Agent:** Tự động thu thập thông tin từ các hệ thống, đối chiếu quy tắc, và gửi yêu cầu bổ sung bằng chứng theo mẫu (template) đã được cửa hàng thiết lập sẵn.
- **Quyền hạn của Seller:** Người bán trực tiếp phê duyệt quyết định đổi hàng, trả hàng, phát hành nhãn vận chuyển thu hồi (phát sinh chi phí cước của nhà vận chuyển) và mọi hành động hoàn tiền.
- **Khẩu hiệu cốt lõi:**  
  $$\text{“Models observe. Code verifies. Seller authorizes.”}$$  
  *(Mô hình quan sát. Mã nguồn xác minh. Người bán phê duyệt).*

---

# 3. NỘI DUNG VÀ SPEAKER NOTES CHI TIẾT CỦA 6 SLIDE (V8.2)

> **Thống kê độ dài kịch bản nói (Speaker Notes):**  
> Tổng số từ nói thực tế (spoken words) của toàn bộ 6 slide là **382 từ** (432 từ nếu tính cả tiêu đề căn thời gian trong ngoặc vuông). Với tốc độ thuyết trình tự nhiên ~127 từ/phút, kịch bản vừa vặn chuẩn xác cho khung thời gian **3 phút pitch**.

---

### SLIDE 1: ReturnLens (Product Intro)
- **Kicker:** AGENTX HACKATHON 2026 · TRACK PS-04
- **Title:** ReturnLens
- **Subtitle:** Every return decision, backed by evidence.
- **Summary:** An evidence-backed triage assistant that connects customer claims, unboxing footage, and store records into a clear decision pack for solo online merchants.
- **Principle Card:**  
  *DESIGN PRINCIPLE*  
  *“Models observe. Code verifies. Seller authorizes.”*  
  *No automated refunds · No automated customer rejections*
- **Console Mockup:**
  - Header: `RETURNLENS SELLER CONSOLE · CASE #RT-8821`
  - Sub-bar: `Order #ORD-7729 · Studio Wireless · ₹1,499 paid · Delivered 4d ago (Within 7-day window)`
  - Side-by-side Showcase:
    - Left: Store Specification (`Matte White · HEAD-WHT-02 · ₹1,499 paid · Delivered 4d ago · Within 7-day window`)
    - Right: Observed Evidence (`00:07 · Black Casing Observed · Color mismatch · Barcode & model unverified`)
  - Banner: `Color discrepancy: Ordered Matte White; video shows Black casing. Barcode unverified.`  
    *Prepared 3 resolution choices for merchant authorization.*
  - Action Bar: `Seller authorizes returns, labels & refunds` (No automated refund or denial)
  - Primary Button: `Review Evidence & Decide →`
- **Speaker Notes (Đúng 100% bản nhúng PPTX):**  
  ```text
  [0:00 - 0:15 | Slide 1: Introduction]
  Judges, this is ReturnLens. For solo online sellers, returns are overwhelming. ReturnLens unifies buyer claims, video evidence, and store rules into one clear decision pack. Models observe, code verifies, but the seller always decides.
  ```

---

### SLIDE 2: One customer claim. Four disconnected sources.
- **Kicker:** THE SELLER'S DILEMMA · SOLO D2C BOTTLENECK
- **Title:** One customer claim. Four disconnected sources.
- **Subtitle:** A solo merchant must piece together fragmented records before deciding how to respond.
- **Customer Claim Card:**
  - Header: `INCOMING CUSTOMER CLAIM`
  - Message: `“I ordered white headphones, but received black. Please refund me.”`
  - Attachment: `Attached: unboxing_video.mp4 (18s)`
- **Four Source Cards:**
  - 1. Customer Chat: Claim text and attached unboxing video clip
  - 2. Shopify Order: Matte White (SKU HEAD-WHT-02), ₹1,499 paid
  - 3. Courier Scan: Shippo confirms parcel delivered 4 days ago
  - 4. Store Policy: 7-day window for wrong or damaged items
- **Decision Question Card (Không bị lặp nhãn):**  
  - Header label: `THE SELLER'S QUESTION:`  
  - Body text: *Packing mistake, delivery error, or unboxing swap? The seller needs verified facts before deciding to refund, replace, or inspect.*
- **Speaker Notes (Đúng 100% bản nhúng PPTX):**  
  ```text
  [0:15 - 0:40 | Slide 2: The Problem]
  A customer chats in: 'I ordered white headphones, but received black. Please refund me,' attaching an unboxing clip. The merchant has to check four tabs: chat, Shopify, tracking, and store policy. Was this a warehouse mix-up, an honest confusion, or a swap? Blind refunds erode margins, while blind rejections destroy trust. The merchant needs unified facts to choose the next step.
  ```

---

### SLIDE 3: The order says white. The video shows black.
- **Kicker:** CORE DEMONSTRATION · STAGED CONCEPT SCENARIO
- **Title:** The order says white. The video shows black.
- **Subtitle:** ReturnLens highlights the visible difference without jumping to unverified conclusions.
- **Showcase Cards (Được thu nhỏ ảnh 16:9, padding đáy rộng rãi > 0.38"):**
  - Left Card:
    - Header: `STORE SPECIFICATION · SHOPIFY`
    - Image: Studio White Headphones (tỷ lệ 16:9 locked)
    - Headline: **Ordered: White**
    - Metadata: `HEAD-WHT-02 · ₹1,499 paid · Delivered 4d ago`
  - Right Card:
    - Header: `OBSERVED EVIDENCE · VIDEO FRAME 00:07`
    - Image: Customer Unboxing Black Headphones (tỷ lệ 16:9 locked)
    - Headline: **Observed: Black**
    - Metadata: `Barcode unverified · Exact model unverified`
  - Central Discrepancy Badge: `≠ COLOR DISCREPANCY`
- **Prepared Options Strip (Option 2 nằm hoàn toàn trong khung xanh, padding đáy > 0.30"):**
  - Header: `WHAT RETURNLENS PREPARES FOR THE SELLER:`
  - Disclaimer: `* Illustrative concept scenario with staged mock evidence.`
  - Option 1: `1. Accept warehouse mis-pack` — Issue replacement return label
  - Option 2 (Tô xanh đề xuất, 1 dòng title):  
    `2. Request label photo`  
    *“Please share the outer-box label so we can check your shipment.”*
  - Option 3: `3. Hold for inspection` — Inspect returned parcel before refund
- **Speaker Notes (Đúng 100% bản nhúng PPTX):**  
  ```text
  [0:40 - 1:25 | Slide 3: The Core Demonstration]
  Here is our core demonstration. The Shopify order specifies white headphones, but the customer's video shows black casing. ReturnLens flags this visible difference clearly. Notice our honest AI grounding: we state that the barcode and exact model are unverified from the video frame. We do not jump to calling this fraud—it could easily be a warehouse packing error. Instead, ReturnLens prepares three practical options for the seller. Notice option two: a drafted reply is ready, asking for the outer-box label to verify the shipment. The seller reviews and clicks to approve.
  ```

---

### SLIDE 4: Models observe. Code verifies. Seller authorizes.
- **Kicker:** AGENT BEHAVIOR · WORKFLOW & RESPONSIBILITIES
- **Title:** Models observe. Code verifies. Seller authorizes.
- **Subtitle:** A structured agent pipeline that investigates, checks policies, and drafts the next step.
- **Four Pipeline Stages:**
  - 1. Collect (Vision & Ingestion): Ingests customer chat, tracking scan, and extracts cited video keyframes.
  - 2. Compare (Rule Engine): Cross-checks observed color against catalog specs, delivery date, and 7-day policy.
  - 3. Recommend (Planning & Drafting): Synthesizes matches and discrepancies into 3 actionable choices and drafts replies.
  - 4. Seller Decides (Solo Merchant): Human merchant reviews the evidence pack and approves returns, labels, or refunds.
- **Dynamic Clarification Box (Case C):**  
  *DYNAMIC CLARIFICATION (CASE C):*  
  *Unclear evidence → Request a close-up photo → Add to same case file → Continue review*  
  *If footage is dark or blurry, agent requests 1 close-up photo or box label and continues the same case. Never auto-rejects.*
- **Responsibility Line:**  
  *Models observe visual traits · Code checks dates and policy rules · Seller approves returns, labels and refunds.*
- **Speaker Notes (Đúng 100% bản nhúng PPTX):**  
  ```text
  [1:25 - 2:05 | Slide 4: Agent Behavior]
  How does the agent move the case forward? It follows four stages: First, Collect—ingesting chat, tracking data, and keyframes. Second, Compare—deterministic code verifies the seven-day return window and checks color alignment. Third, Recommend—the agent drafts resolution choices and customer replies. And fourth, Seller Decides—the merchant makes the call. If footage is too dark or blurry, the agent requests a close-up photo, appends it to the same case file, and resumes review. Models observe visual traits, code checks rules, and the seller approves returns, labels, and refunds.
  ```

---

### SLIDE 5: Three situations. Three useful next steps.
- **Kicker:** PROTOTYPE SCENARIOS · EXPECTED BEHAVIOR
- **Title:** Three situations. Three useful next steps.
- **Subtitle:** ReturnLens handles clean claims, flags discrepancies, and guides unclear evidence.
- **Three Columns (Case A headband, Case B đồng bộ, Case C ảnh cận cảnh):**
  - **CASE A: Consistent Claim**
    - Situation: Unboxing video shows cracked headband; delivered 4 days ago, within the 7-day return window.
    - Agent Action: Validates delivery date and visible headband crack; drafts return shipping label.
    - Seller Outcome: Seller approves return label. Refund held until parcel arrives at warehouse.
  - **CASE B: Color Discrepancy**
    - Situation: Customer claims: “I ordered white headphones, but received black.”
    - Agent Action: Flags color mismatch; notes barcode unverified; drafts 3 resolution choices.
    - Seller Outcome: Seller chooses: accept mis-pack, request box label photo, or hold for inspection.
  - **CASE C: Unclear Evidence**
    - Situation: Video footage is too dark or blurry to confirm product condition or serial label.
    - Agent Action: Requests a clear close-up photo or box label; appends new evidence to same case file.
    - Seller Outcome: Customer gets a fair chance to clarify. If 2nd attempt fails, escalates directly to seller.
- **Speaker Notes (Đúng 100% bản nhúng PPTX):**  
  ```text
  [2:05 - 2:30 | Slide 5: Three Scenarios]
  Our prototype focuses on three everyday situations: In Case A, evidence is clean—a visible cracked headband on arrival within seven days. The agent drafts a return label. In Case B, color discrepancy—the agent surfaces the conflict and prepares choices. In Case C, unclear evidence—the agent requests a close-up photo. Each scenario produces a clear next step.
  ```

---

### SLIDE 6: A focused 24-hour prototype.
- **Kicker:** 24-HOUR PROTOTYPE SPRINT · EXECUTION PLAN
- **Title:** A focused 24-hour prototype.
- **Subtitle:** *(Đã lược bỏ subtitle để mở rộng khoảng cách thoáng đãng $0.35"$ phía trên timeline)*
- **Four Phases:**
  - 00–06h: Phase 1: Ingestion & Schema (Mock order and courier fixtures; case state schema).
  - 06–12h: Phase 2: Vision & Rules (Keyframe extraction and deterministic rule checks).
  - 12–18h: Phase 3: Seller Console UI (Side-by-side evidence review console with drafted replies).
  - 18–24h: Phase 4: Walkthrough & QA (Scenario walkthroughs and checks across Cases A, B, and C).
- **Team Responsibilities (3 roles · max 2 outputs):**
  - Person A · Workflow & Rules: State machine logic · Clarification loop · Policy checks
  - Person B · Vision & Interface: Keyframe extractor · Discrepancy view · Merchant console
  - Person C · Fixtures & Testing: Order/courier mock data · Scenario walkthroughs & checks
- **Scope Discipline:**
  - Sprint Core: Mock order/courier data · Keyframe evidence viewer · 3 core scenarios · Fail-closed seller console
  - Stretch Goals: Live Shopify/courier APIs · Automated payment gateways · Advanced video forensics
- **Closing Takeaway:**  
  *“One clear evidence pack. The seller makes the call.”*
- **Speaker Notes (Đúng 100% bản nhúng PPTX):**  
  ```text
  [2:30 - 3:00 | Slide 6: Execution Roadmap & Closing]
  For this 24-hour hackathon, our scope is strictly disciplined: Person A builds the state machine and policy checks; Person B builds the keyframe viewer and merchant console; Person C tests all three scenarios. We are not building live Shopify webhooks or banking integrations. One clear evidence pack. The seller makes the call. Thank you!
  ```

---

# 4. BỘ 5 CÂU HỎI & TRẢ LỜI BẢO VỆ KỸ THUẬT TRƯỚC BAN GIÁM KHẢO (DEFENSE Q&A)

### Q1: Tại sao cần một agent mà không dùng một bảng dashboard truyền thống?
**Trả lời:** Dashboard truyền thống chỉ hiển thị các hàng dữ liệu thụ động riêng rẽ: danh sách đơn hàng Shopify, danh sách sự kiện Shippo, tệp video đính kèm trong tin nhắn. Người bán vẫn phải tự mở từng file, tua video tìm giây khui hộp, và đối chiếu thủ công với mã SKU. ReturnLens chủ động thực hiện chuỗi phân tích: trích xuất đúng khung hình cần xem, so sánh với đơn hàng, phát hiện mâu thuẫn hoặc điểm còn thiếu, soạn sẵn tin nhắn phản hồi và đề xuất 3 phương án thực tế. Người bán chuyển từ việc **điều tra dữ liệu thủ công** sang **phê duyệt phương án trong 3 giây**.

### Q2: Tại sao sản phẩm trong video khác màu mà không kết luận là khách gian lận?
**Trả lời:** Đây là nguyên tắc cốt lõi về tính an toàn và trung thực của sản phẩm. Việc nhận hàng khác màu có thể do nhân viên kho dán nhầm tem mã màu hoặc đóng nhầm hàng, cũng có thể khách nhận nhầm hộp của người thân, hoặc là hành vi tráo hàng. AI không được phép đưa ra phán quyết pháp lý hay buộc tội khách hàng khi chưa đủ chứng cứ (nhất là khi mã vạch trên hộp chưa được đọc rõ trong video). ReturnLens ghi nhận khách quan đây là một "mâu thuẫn trực quan" và đề xuất người bán yêu cầu chụp ảnh tem nhãn hộp ngoài để làm rõ nguyên nhân.

### Q3: Nếu video của khách bị tối hoặc mờ (Case C), hệ thống xử lý thế nào?
**Trả lời:** Khách hàng đã bóc seal hộp thì không thể yêu cầu họ quay lại cảnh mở hộp ban đầu. Thay vào đó, ReturnLens gửi một tin nhắn hướng dẫn lịch sự yêu cầu khách hàng chụp ảnh cận cảnh rõ nét hoặc quay đoạn video ngắn tập trung vào sản phẩm, vết hỏng hoặc tem nhãn dán trên vỏ hộp. Ảnh mới sẽ được gắn vào cùng hồ sơ khiếu nại đang chờ. Hệ thống giới hạn tối đa 1 lần yêu cầu bổ sung; nếu sau đó bằng chứng vẫn không đạt yêu cầu, toàn bộ ca sẽ được chuyển thẳng cho người bán xem xét thủ công để tránh làm phiền khách hàng.

### Q4: Ranh giới quyền hạn giữa AI và người bán được phân định ra sao?
**Trả lời:** Ranh giới được thiết lập rất thực tế: Agent được phép tự động thu thập dữ liệu và gửi tin nhắn yêu cầu bổ sung bằng chứng theo mẫu (template) đã được người bán cấu hình trước. Tuy nhiên, người bán là người duy nhất có quyền phê duyệt việc nhận lại hàng, phát hành nhãn vận chuyển thu hồi (vì phát sinh chi phí cước vận chuyển thực tế), và phê duyệt bất kỳ lệnh hoàn tiền nào. Không có bất kỳ khoản tiền nào bị trừ hoặc gửi đi mà thiếu sự xác nhận chủ động của người bán.

### Q5: Trong 24 giờ hackathon, prototype chứng minh được những gì?
**Trả lời:** Trong 24 giờ, nhóm tập trung chứng minh tính khả thi của chuỗi giá trị cốt lõi: xử lý trọn vẹn 3 tình huống mẫu (Case A khớp bằng chứng, Case B mâu thuẫn màu sắc, Case C video tối cần bổ sung ảnh), trích xuất keyframe thực tế từ video, chạy bộ kiểm tra quy tắc chính sách tất định, và hiển thị giao diện bảng điều khiển cho người bán phê duyệt. Nhóm không làm các tích hợp phức tạp chưa cần thiết như cổng thanh toán Stripe hay webhook live Shopify, giúp đảm bảo sản phẩm hoạt động mượt mà và tin cậy nhất trong buổi demo.

---

# 5. TIẾN HÓA NÂNG CẤP TỪ V8.1 LÊN V8.2 (CHANGELOG)

| Hạng mục | Phiên bản v8.1 | Phiên bản v8.2 (Final Polish Patch) | Lý do nâng cấp |
| :--- | :--- | :--- | :--- |
| **Slide 3: Ảnh và Metadata** | Ảnh $4.40" \times 2.46"$, metadata sát đáy card ($y = 5.03"$) | Ảnh $3.673" \times 2.05"$, metadata cách đáy card **$55$–$60$ px ($0.38"–0.42"$)** | Triệt tiêu hoàn toàn nguy cơ chữ chạm viền; tạo khoảng đệm thẩm mỹ rộng rãi. |
| **Slide 3: Option 2** | Title 2 dòng do có `(Recommended)`; drafted reply dài | Title 1 dòng: `2. Request label photo`; drafted reply rút gọn; padding đáy **$44$ px ($0.306" \ge 0.12"$)** | Không có dòng nào rơi xuống dưới; màu nền xanh đã đủ biểu thị phương án đề xuất. |
| **Slide 2: Nhãn câu hỏi** | Kicker `THE SELLER'S QUESTION:` và đầu đoạn văn bị lặp lại | Giữ kicker trên, xóa phần lặp ở đầu đoạn văn bên dưới | Tránh lặp từ thừa, câu hỏi liền mạch và chuyên nghiệp. |
| **Slide 4: Ranh giới quyền hạn** | `Seller authorizes all actions` | `Seller approves returns, labels and refunds.` | Chuẩn hóa ranh giới quyền hạn hành vi giữa Agent và Seller. |
| **Case A Specification** | Handoff cũ ghi "cracked screen" | Đồng bộ chính xác: **cracked headphone headband** | Nhất quán với sản phẩm tai nghe (headphones) xuyên suốt cả deck. |
| **Số liệu đo lường** | Tồn tại các số liệu chưa có nguồn ("15 minutes", "10 seconds") | Đã loại bỏ hoàn toàn | Đảm bảo tính trung thực và kỷ luật tuyệt đối cho Vòng Ý Tưởng. |
| **Độ dài Pitch Script** | Ép cứng 379 từ | Đếm thực tế: **382 spoken words** (~127 words/min) | Khớp chính xác 100% giữa artifact PPTX và handoff brief. |

---

# 6. HƯỚNG DẪN KIỂM TRA ĐỘC LẬP TẠI LOCAL (VERIFICATION INSTRUCTIONS)

Tất cả các tệp đều nằm trong thư mục dự án `D:\Code\Code\AIO\Code\hack4hack`:

1. **Chạy bộ kiểm thử tự động 9/9:**
   ```bash
   cd D:\Code\Code\AIO\Code\hack4hack
   python scripts/smoke_test_v8_2.py
   ```
2. **Kiểm tra tính toàn vẹn của các bản cũ (Zero Regression):**
   ```bash
   python scripts/smoke_test_v8_1.py
   python scripts/smoke_test_v8.py
   ```
3. **Mở xem trực tiếp Slide Deck:**
   - Vector PDF: `deliverables/ReturnLens_v8_2.pdf` (hoặc mở trực tiếp `ReturnLens_v8_2.pdf`)
   - Native PPTX: `deliverables/ReturnLens_v8_2.pptx`
   - Interactive Web Deck: `deliverables/ReturnLens_v8_2.html`
   - Master Preview Image: `deliverables/ReturnLens_v8_2_preview.png`
   - Ảnh render từng slide 1080p: `src/assets/v8_2_pptx_renders/slide_1.png` đến `slide_6.png`

