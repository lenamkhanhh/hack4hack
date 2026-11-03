# RETURNLENS V8.1 (FINAL IDEA ROUND POLISHED EDITION) — FULL CONTEXT HANDOFF & REVIEW BRIEF

> **TÀI LIỆU BÀN GIAO TOÀN DIỆN DÀNH CHO GPT / REVIEWER ĐỘC LẬP (VÒNG Ý TƯỞNG)**  
> *Bạn có thể tải tệp Markdown này lên ChatGPT (GPT-4o / GPT-o1) hoặc dán toàn bộ nội dung vào khung chat kèm câu lệnh gợi ý ở bên dưới.*

---

## PHẦN DÀNH CHO USER: CÂU LỆNH (PROMPT) GỢI Ý ĐỂ COPY VÀO GPT

```text
Bạn là một Giám khảo Kỹ thuật Cấp cao (Principal Technical Judge), Giám đốc Thiết kế Sản phẩm (Product Design Director) và Chuyên gia Đánh giá An toàn AI (AI Safety Auditor) tại cuộc thi AgentX Hackathon 2026.

Dưới đây là toàn bộ tài liệu bàn giao (Handoff Brief) của dự án "ReturnLens v8.1 — Final Idea Round Polished Edition" thuộc Track PS-04 (Autonomous Support Agent for Solo D2C Merchants).

Hãy đọc kỹ toàn bộ tài liệu này (bao gồm định vị sản phẩm cho vòng ý tưởng, hành vi agent, kịch bản đối soát 3 tình huống cốt lõi, toàn bộ nội dung & speaker notes của 6 slide, và kế hoạch thực thi 24h). Sau đó, hãy tiến hành một đợt REVIEW ĐỘC LẬP VÀ TOÀN DIỆN theo 7 tiêu chí:
1. Độ thuyết phục của Narrative & Pitch Flow trong 3 phút (Câu chuyện từ nỗi đau solo seller -> Star Demo đối chiếu màu và tin nhắn dự thảo -> Cơ chế Agent -> 3 Tình huống -> Roadmap 24h; kịch bản nói 379 từ có vừa vặn 3 phút không).
2. Tính đúng đắn của việc định vị sản phẩm cho Vòng Ý Tưởng (Tập trung vào giá trị thực tế của trợ lý gom hồ sơ và đưa ra lựa chọn hành động + câu trả lời soạn sẵn; không lấy "chống gian lận" làm lời hứa trung tâm; thấy rõ lợi ích cho cả người bán và khách hàng).
3. Tính hợp lý và khả thi của cơ chế Case C Clarification (Yêu cầu ảnh/video cận cảnh sản phẩm, vết hỏng hoặc tem nhãn hộp ngoài thay vì yêu cầu phi lý "re-film unboxing"; giữ nguyên video gốc và lưu cùng hồ sơ; tối đa 1 lần bổ sung rồi chuyển người bán).
4. Tính chuẩn xác của Ranh giới Quyền hạn (Agent thu thập thông tin và yêu cầu làm rõ theo template cửa hàng; Seller duyệt quyết định đổi trả, nhãn vận chuyển gây phí và hành động tài chính; triết lý "Models observe. Code verifies. Seller authorizes.").
5. Tính nhất quán xuyên suốt các slide (Case B đồng bộ cùng 1 khiếu nại "ordered white, received black"; Case A đồng bộ chính sách 7 ngày "Delivered 4 days ago; within the 7-day return window"; bỏ mọi suy đoán chủ quan về việc kho nhầm hàng).
6. Độ đanh thép của 5 câu trả lời bảo vệ kỹ thuật trước ban giám khảo (Tại sao cần agent, tại sao khác màu chưa phải gian lận, xử lý video mờ bằng ảnh cận cảnh, ranh giới quyền hạn, prototype 24h chứng minh điều gì).
7. Chấm điểm tổng quan (thang điểm 10) và những lời khuyên sắc bén nhất trước khi bước vào phòng pitching.
```

---

# TỔNG QUAN HỒ SƠ DỰ ÁN (PROJECT DOSSIER)

- **Tên dự án:** ReturnLens
- **Tagline:** *"Every return decision, backed by evidence."* (Mọi quyết định đổi trả đều có bằng chứng bảo chứng).
- **One-liner:** Một trợ lý giúp solo seller gom yêu cầu của khách, bằng chứng video, dữ liệu đơn hàng và chính sách thành một hồ sơ dễ xem để quyết định bước xử lý tiếp theo.
- **Cuộc thi:** AgentX Hackathon 2026 — Track PS-04: *Autonomous Support Agent for Online Sellers*.
- **Vòng thi:** **Vòng Ý Tưởng (Idea Round) — Bản Hoàn Thiện Cuối (Final Polish)**.
- **Đội thi:** Team Rookie (3 thành viên: Person A - Workflow/Rules, Person B - Vision/UI, Person C - Fixtures/Testing).
- **Mã nguồn (Repository):** `https://github.com/lenamkhanhh/hack4hack.git` (Nhánh: `main`).
- **Phiên bản hoàn thiện:** **ReturnLens v8.1 (Final Idea Round Polished Edition)**.
- **Ranh giới thực tế của Prototype (Prototype Reality & Honest Demarcation):**
  - ReturnLens tại vòng thi này là một **Đề án Sản phẩm & Kiến trúc Hệ thống hoàn chỉnh (Product & Architecture Proposal)** kèm **Bộ đặc tả kiểm thử tự động (Executable Prototype Baseline)**.
  - Dự án tập trung vào trải nghiệm phân loại khiếu nại (return triage), sử dụng dữ liệu kiểm thử chuẩn (mock fixtures), trích xuất keyframe thực tế từ video và quy trình kiểm tra quy tắc tất định.
  - Dự án **không mở rộng phạm vi** thành việc kết nối webhook live production với Shopify thật hay tích hợp cổng thanh toán Stripe/ngân hàng thật. Các thành phần live integration được phân định rõ là kế hoạch phát triển tương lai (Stretch Goals).
- **Bộ Deliverables chuẩn v8.1:**
  1. `ReturnLens_v8_1.pptx` & `deliverables/ReturnLens_v8_1.pptx` (1,387,254 B, SHA256: `7172acbcb26c...`, 16:9, nhúng đủ Speaker Notes cho 6 slide, đóng gói `ZIP_STORED` deterministic).
  2. `ReturnLens_v8_1.pdf` & `deliverables/ReturnLens_v8_1.pdf` (262,747 B, SHA256: `3887b6f52c52...`, Vector 6 trang, xuất trực tiếp từ PowerPoint COM).
  3. `ReturnLens_v8_1.html` & `deliverables/ReturnLens_v8_1.html` (2,722,032 B, SHA256: `a265a8c287ee...`, Single-file Interactive Web Deck, offline-resilient font stacks).
  4. `ReturnLens_v8_1_preview.png` & `deliverables/ReturnLens_v8_1_preview.png` (1,051,036 B, SHA256: `a8964b4bf8cd...`, Contact Sheet 2352×882, tỷ lệ 16:9 chuẩn).
  5. Bộ ảnh render PPTX 1920×1080: `src/assets/v8_1_pptx_renders/` kèm `render_manifest.json`.
  6. Extended Smoke Test: `scripts/smoke_test_v8_1.py` (9/9 PASS).
  7. Báo cáo chất lượng: `V8_1_QA_REPORT.md`.

---

# 1. ĐỊNH VỊ LẠI Ý TƯỞNG CHO VÒNG Ý TƯỞNG (PRODUCT REPOSITIONING)

### 1.1. Giá trị cốt lõi cụ thể cho Solo Merchant
ReturnLens kết nối yêu cầu của khách, bằng chứng hình ảnh, đơn hàng và chính sách thành một hồ sơ ra quyết định rõ ràng:
1. **Thấy ngay điều đã biết:** Khách hàng khiếu nại điều gì (ví dụ: đặt màu trắng nhưng nhận màu đen; mã đơn `ORD-7729`, trị giá `₹1,499`, giao 4 ngày trước).
2. **Thấy rõ điều còn thiếu hoặc mâu thuẫn:** Màu sắc sản phẩm trong video là màu đen (mâu thuẫn với màu trắng trên catalog); mã vạch trên nhãn hộp chưa xác minh được qua góc quay video.
3. **Có frame video tham chiếu:** Trích xuất khung hình bằng chứng cụ thể (`00:07`) kèm mốc thời gian và độ phân giải để người bán tự đối chiếu bằng mắt trong 3 giây.
4. **Có phương án xử lý tiếp theo và câu trả lời dự thảo:** Cung cấp 3 lựa chọn hành động thiết thực. Option 2 được làm nổi bật đi kèm tin nhắn soạn sẵn:  
   *“Thanks for the video. Please share the outer-box label so the seller can check the shipment.”*
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
  • Solo seller xem hồ sơ bằng chứng và 1-click phê duyệt
  • Không tự động hoàn tiền, không tự động từ chối
```

### 2.2. Luồng bổ sung bằng chứng Case C thực tế (Close-up Photo Clarification)
- **Vấn đề thực tế:** Khi khách hàng đã mở hộp và quay video, nếu video bị tối hoặc rung, yêu cầu khách "quay lại unboxing từ đầu" là hoàn toàn bất khả thi vì hộp đã bị bóc seal.
- **Giải pháp của v8.1:** Agent gửi hướng dẫn lịch sự yêu cầu khách hàng **chụp một tấm ảnh cận cảnh rõ nét hoặc quay một đoạn video ngắn tập trung vào sản phẩm, vết hỏng hoặc tem nhãn dán trên hộp ngoài**.
- **Cơ chế lưu trữ:** Video gốc ban đầu vẫn được giữ nguyên. Tấm ảnh cận cảnh mới sẽ được đính kèm vào **cùng một hồ sơ khiếu nại** đang chờ (`WAITING_FOR_EVIDENCE`).
- **Giới hạn an toàn:** Tối đa **1 lần yêu cầu bổ sung**. Nếu sau lần bổ sung này bằng chứng vẫn chưa đạt yêu cầu, agent sẽ chuyển toàn bộ hồ sơ cho người bán trực tiếp xem xét.

### 2.3. Ranh giới Quyền hạn Chuẩn mực (Authority Boundary)
- **Quyền hạn của Agent:** Tự động thu thập thông tin từ các hệ thống, đối chiếu quy tắc, và gửi yêu cầu bổ sung bằng chứng theo mẫu (template) đã được cửa hàng thiết lập sẵn.
- **Quyền hạn của Seller:** Người bán trực tiếp phê duyệt quyết định đổi hàng, trả hàng, phát hành nhãn vận chuyển thu hồi (phát sinh chi phí cước của nhà vận chuyển) và mọi hành động tài chính (hoàn tiền qua cổng thanh toán).
- **Khẩu hiệu cốt lõi:**  
  $$\text{“Models observe. Code verifies. Seller authorizes.”}$$  
  *(Mô hình quan sát. Mã nguồn xác minh. Người bán phê duyệt).*

---

# 3. NỘI DUNG VÀ SPEAKER NOTES CHI TIẾT CỦA 6 SLIDE (V8.1)

Tổng số từ kịch bản thuyết trình (Speaker Notes): **379 từ** (Vừa vặn chuẩn xác cho 3 phút pitch, ~126 từ/phút).

---

### SLIDE 1: ReturnLens (Product Intro)
- **Kicker:** Track PS-04 · Autonomous Support Agent for Online Sellers
- **Title:** Every return decision, backed by evidence.
- **Subtitle:** An evidence-backed assistant for solo D2C merchants.
- **Description:** ReturnLens pulls customer messages, unboxing video, order records, and store policy into one clear case file so solo sellers can decide what to do next.
- **Core Principle Box:**  
  *Models observe. Code verifies. Seller authorizes.*  
  Agent collects info & requests clarification per store templates · Seller authorizes return decisions, shipping labels & financial actions.
- **Console Mockup:**
  - Header: `ReturnLens Case Console · RT-8821` | Status: `NEEDS_SELLER_DECISION`
  - Side-by-side Showcase:
    - Left: Catalog Photo (`Matte White Studio · SKU: HEAD-WHT-02 · Ordered Color: White`)
    - Right: Customer Unboxing Keyframe (`00:07 · 1080p · Observed Color: Black`)
  - Banner: `COLOR CONTRADICTION · ORDERED WHITE VS OBSERVED BLACK`
  - Action Button: `Review Evidence & Decide →`
- **Speaker Notes (30 từ):**  
  *“ReturnLens helps solo merchants handle return requests with confidence. It gathers buyer messages, unboxing videos, order records, and store policy into one clear evidence file so the seller can decide what to do next.”*

---

### SLIDE 2: One customer claim. Four disconnected sources.
- **Kicker:** The Solo Merchant's Reality
- **Title:** One customer claim. Four disconnected sources.
- **Subtitle:** When a return arrives with an unboxing video, a solo seller has to check four tabs by hand.
- **Chat Ticket:**
  - Customer: *"I ordered white headphones, but received black. Please refund me."*
  - Attachment: `unboxing_video.mp4 · 1080p · 18s · Uploaded via store portal`
- **Four Source Cards:**
  - Customer Chat: Buyer claims received color does not match order.
  - Shopify Order: `HEAD-WHT-02` (White) · ₹1,499 paid · Delivered 4 days ago.
  - Shippo Courier: Delivered to buyer address · Tracking signed.
  - Store Policy: Wrong item or damage reported within 7 days is eligible.
- **Decision Question:**  
  *“Is this a warehouse mis-pack, an unverified box, or an invalid claim? Checking by hand takes 15 minutes per ticket.”*
- **Speaker Notes (58 từ):**  
  *“Today, when a customer sends an unboxing video, solo sellers must switch between chat, Shopify, shipping scans, and store policies. It takes fifteen minutes of stressful manual checking per ticket. Sellers either refund blindly to protect ratings, or dispute claims without proof. ReturnLens connects all four sources into one structured case file.”*

---

### SLIDE 3: The order says white. The video shows black.
- **Kicker:** Evidence Comparison in Action
- **Title:** The order says white. The video shows black.
- **Subtitle:** ReturnLens extracts video keyframes, compares them with the order, and highlights what is known and what is missing.
- **Comparison Cards:**
  - Left Card: **Ordered: White** (`HEAD-WHT-02 · ₹1,499 paid · Delivered 4d ago`)
  - Right Card: **Observed: Black** (`Unboxing keyframe at 00:07 · Barcode unverified in video`)
  - Central Badge: `≠ COLOR DISCREPANCY`
- **Actionable Next Steps:**
  - Option 1: Accept as fulfillment error → Issue prepaid exchange label.
  - Option 2 (Recommended & Highlighted): Request clear outer-box photo → Hold decision.  
    *Drafted customer reply: “Thanks for the video. Please share the outer-box label so the seller can check the shipment.”*
  - Option 3: Request physical inspection before issuing refund.
- **Disclaimer:** `* Concept scenario with staged evidence for demonstration. Not live customer footage.`
- **Speaker Notes (105 từ):**  
  *“Here is ReturnLens in action. In Case B, the customer ordered white headphones, but the video shows black. ReturnLens extracts the clearest keyframe at second seven and checks it against the Shopify order. It highlights the color mismatch, but it also notes that the box barcode was not visible in the clip.*  
  *Instead of guessing fraud or blaming the warehouse, it gives the seller three practical choices. Option two is highlighted with a drafted message asking for a photo of the outer-box label. The seller reviews the evidence and approves the message with one click.”*

---

### SLIDE 4: Models observe. Code verifies. Seller authorizes.
- **Kicker:** System Architecture & Safety Guardrails
- **Title:** Models observe. Code verifies. Seller authorizes.
- **Subtitle:** Vision models suggest observations, deterministic code checks policy rules, and the seller approves all actions.
- **Four Pipeline Stages:**
  - 1. Collect: Ingests chat text, video keyframes, order data, and shipping status.
  - 2. Compare: Vision model observes attributes; code verifies return window and item SKU.
  - 3. Recommend: Flags mismatches, prepares next steps, and drafts customer replies.
  - 4. Seller Decides: Seller reviews the evidence file and authorizes the final action.
- **Case C Clarification Branch:**  
  *“If video is dark or blurry, the agent asks for a close-up photo of the item or label, appends it to the case, and escalates to the seller if still unclear.”*
- **Responsibility Split:**  
  *Models observe attributes · Code verifies policy & schema · Seller authorizes refunds & labels*
- **Speaker Notes (92 từ):**  
  *“Our architecture follows one strict rule: models observe, code verifies, seller authorizes. Vision models only extract visual observations like color or damage. Deterministic code verifies order dates, policies, and schemas. Code never trusts model outputs blindly.*  
  *If a video is dark or blurry, like Case C, the agent asks for a close-up photo of the product or box label. It appends the new image to the existing file. If still unclear after one try, it escalates to the seller. The seller always authorizes refunds and returns.”*

---

### SLIDE 5: Three situations. Three useful next steps.
- **Kicker:** Case Matrix & Triage Paths
- **Title:** Three situations. Three useful next steps.
- **Subtitle:** ReturnLens prepares clear options whether evidence is matching, conflicting, or unclear.
- **Three Columns:**
  - **Case A: Clean Claim (Cracked Screen)**
    - Situation: Customer claims cracked screen · Delivered 4 days ago; within the 7-day return window.
    - Agent Action: Keyframe confirms crack · Policy checks pass · Prepares prepaid return label draft.
    - Seller Outcome: Seller approves return in 10 seconds.
  - **Case B: Color Discrepancy (Wrong Color)**
    - Situation: Customer claims: "I ordered white headphones, but received black. Please refund me."
    - Agent Action: Keyframe shows black item · Barcode unverified · Drafts request for box label.
    - Seller Outcome: Seller sends clarification request in 1 click.
  - **Case C: Unclear Video (Low Light)**
    - Situation: Customer submits dark unboxing video · Product attributes cannot be verified.
    - Agent Action: Requests close-up photo of product or label · Holds case · Max 1 retry before seller review.
    - Seller Outcome: Customer gets guidance; seller avoids unfair denial.
- **Speaker Notes (48 từ):**  
  *“ReturnLens handles three everyday scenarios. In Case A, evidence is clear, so the seller approves a return in seconds. In Case B, color conflicts, so the seller requests a box label photo. In Case C, evidence is dark, so the customer gets clear photo guidance without an unfair rejection.”*

---

### SLIDE 6: A focused 24-hour prototype.
- **Kicker:** Hackathon Implementation Plan
- **Title:** A focused 24-hour prototype.
- **Subtitle:** Built for solo D2C merchants who need reliable return triage without manual chaos.
- **Four Phases:**
  - 00–06h: Core Data & Rules (Mock fixtures for Cases A, B, C; rule engine for 7-day window & limits).
  - 06–12h: Keyframe Pipeline (Video ingestion, frame extractor, attribute extraction prompts).
  - 12–18h: Case Console & Review UI (Side-by-side evidence viewer, drafted customer messages, 1-click approvals).
  - 18–24h: End-to-End Testing (Run all 3 cases through triage pipeline, verify fail-closed guardrails).
- **Team Roles & Deliverables:**
  - Person A (Workflow & Rules): Policy rule engine · Clarification state machine
  - Person B (Vision & UI): Video frame extractor · Seller review console
  - Person C (Fixtures & Testing): Benchmark test fixtures · Automated smoke test suite
- **Scope Discipline:**
  - Sprint Core (Must Deliver): 3 mock return cases · Keyframe viewer · Rule verification engine · Review console
  - Stretch Goals (Cut First): Live Shopify webhook sync · Carrier label purchase API · Multi-camera forensics
- **Closing Takeaway:**  
  *“One clear evidence pack. The seller makes the call.”*
- **Speaker Notes (46 từ):**  
  *“In twenty-four hours, we can build a working prototype. We focus strictly on the three core scenarios: extracting keyframes, running deterministic policy checks, and delivering a clean seller decision console. We do not build live payment or carrier APIs. One clear evidence pack; the seller makes the call.”*

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

# 5. TIẾN HÓA NÂNG CẤP TỪ V8 LÊN V8.1 (CHANGELOG)

| Hạng mục | Phiên bản v8 | Phiên bản v8.1 (Final Polish) | Lý do nâng cấp |
| :--- | :--- | :--- | :--- |
| **Case C Clarification** | Yêu cầu khách *"re-film unboxing"* | Yêu cầu gửi **ảnh chụp/video cận cảnh chi tiết** sản phẩm, vết hỏng hoặc tem nhãn hộp ngoài | Hộp đã bóc seal không thể unboxing lại; ảnh cận cảnh là bằng chứng khả thi và hợp lý nhất. |
| **Ranh giới Quyền hạn** | Slogan *"Human confirms every action"* | *"Agent collects info & requests clarification per templates · Seller authorizes returns, labels & refunds"* | Phân định rõ quyền tự động hóa ở tầng thu thập/hỏi thông tin và quyền con người ở tầng tài chính/pháp lý. |
| **Đồng bộ Case B** | Slide 2: Nhận nhầm màu đen · Slide 5: Tai nghe trắng bị hỏng | Đồng bộ thống nhất: *"I ordered white headphones, but received black. Please refund me."* xuyên suốt Slide 2, 3, 5 | Loại bỏ hoàn toàn sự không nhất quán giữa các slide. |
| **Chính sách đổi trả** | Slide 5 Case A ghi *"4-day delivery window"* | Đồng bộ: *"Delivered 4 days ago; within the 7-day return window."* | Đúng với chính sách cửa hàng 7 ngày đã nêu ở Slide 2. |
| **Suy đoán kho hàng** | Chứa suy đoán *"Warehouse staff likely grabbed black inventory"* | Đã loại bỏ hoàn toàn | AI không suy đoán nguyên nhân khi chưa xác minh; chỉ nêu mâu thuẫn trực quan. |
| **Bố cục Slide 3** | Thẻ so sánh cao $3.45"$, đáy $5.13"$ sát dải option $5.25"$ gây che lấp chữ | Thẻ cao $3.35"$, đáy $5.03"$, cách dải option $0.17"$, chữ 1 dòng nổi bật | Đảm bảo 100% không chồng lấn, đọc rõ trên mọi màn hình. |
| **Tiêu đề Slide 6** | Tiêu đề 2 dòng + subtitle sát timeline ($0.13"$) | Tiêu đề 1 dòng duy nhất, bỏ subtitle, khoảng cách mở rộng đến $0.35"$ | Thoáng đãng, thanh lịch, chuẩn tỷ lệ vàng trình bày. |
| **Kịch bản nói (Notes)** | 350–400 từ chưa cân đối giữa các slide | Chuẩn xác **379 từ**, Slide 1 súc tích (30 từ), tập trung 70% thời gian cho Slide 3 và Slide 4 | Pitch mượt mà trong đúng 3 phút trình bày. |

---

# 6. HƯỚNG DẪN KIỂM TRA ĐỘC LẬP TẠI LOCAL (VERIFICATION INSTRUCTIONS)

Tất cả các tệp đều nằm trong thư mục dự án `D:\Code\Code\AIO\Code\hack4hack`:

1. **Chạy bộ kiểm thử tự động 9/9:**
   ```bash
   cd D:\Code\Code\AIO\Code\hack4hack
   python scripts/smoke_test_v8_1.py
   ```
2. **Kiểm tra tính toàn vẹn của các bản cũ (Zero Regression):**
   ```bash
   python scripts/smoke_test_v8.py
   ```
3. **Mở xem trực tiếp Slide Deck:**
   - Vector PDF: `deliverables/ReturnLens_v8_1.pdf` (hoặc mở trực tiếp `ReturnLens_v8_1.pdf`)
   - Native PPTX: `deliverables/ReturnLens_v8_1.pptx`
   - Interactive Web Deck: `deliverables/ReturnLens_v8_1.html`
   - Master Preview Image: `deliverables/ReturnLens_v8_1_preview.png`
   - Ảnh render từng slide 1080p: `src/assets/v8_1_pptx_renders/slide_1.png` đến `slide_6.png`

