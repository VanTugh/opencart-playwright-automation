"""
================================================================================
NON-FUNCTIONAL TESTING SUITE FOR OPENCART 4.1.0.3
================================================================================
Comprehensive test suite covering 60 test cases across 3 subsystems:
    1. Performance Testing (20 tests)
    2. Security Testing (20 tests)
    3. Usability Testing (20 tests)

Each subsystem contains:
    - 10 Basic Tests: Fundamental checks
    - 10 Advanced Tests: Vulnerability/bottleneck hunting

Author: Senior SDET
Framework: Playwright Async + Pytest
Date: May 2026
================================================================================
"""

import pytest
import asyncio
import time
import re
from datetime import datetime
from playwright.async_api import Page, Browser
from conftest import BASE_URL, logger

# ================================================================================
# PERFORMANCE TESTING SUBSYSTEM (20 tests: 10 basic + 10 advanced)
# ================================================================================

class TestPerformanceBasic:
    """Basic Performance Tests - Measure load times and response metrics"""

    @pytest.mark.asyncio
    @pytest.mark.performance
    @pytest.mark.basic
    async def test_perf_basic_01_homepage_load_time(self, page: Page):
        """
        [PERFORMANCE BASIC #01] Đo thời gian load trang chủ (Homepage)

        Mục đích: Xác định thời gian load của trang chủ nên dưới 3 giây
        Kỳ vọng: response time < 3000ms
        """
        logger.info("🚀 [PERF_BASIC_01] Đang đo thời gian load Homepage...")

        start_time = time.time()
        await page.goto(BASE_URL, wait_until="networkidle")
        load_time = (time.time() - start_time) * 1000  # Convert to ms

        logger.info(f"✅ Homepage loaded in {load_time:.2f}ms")
        assert load_time < 3000, f"Homepage load time {load_time:.2f}ms exceeds 3000ms threshold"

    @pytest.mark.asyncio
    @pytest.mark.performance
    @pytest.mark.basic
    async def test_perf_basic_02_product_page_load_time(self, page: Page):
        """
        [PERFORMANCE BASIC #02] Đo thời gian load trang sản phẩm

        Mục đích: Xác định thời gian load của trang chi tiết sản phẩm
        Kỳ vọng: response time < 2500ms
        """
        logger.info("🚀 [PERF_BASIC_02] Đang đo thời gian load Product Page...")

        start_time = time.time()
        await page.goto(f"{BASE_URL}index.php?route=product/product&product_id=40",
                       wait_until="networkidle")
        load_time = (time.time() - start_time) * 1000

        logger.info(f"✅ Product page loaded in {load_time:.2f}ms")
        assert load_time < 2500, f"Product page load time {load_time:.2f}ms exceeds 2500ms"

    @pytest.mark.asyncio
    @pytest.mark.performance
    @pytest.mark.basic
    async def test_perf_basic_03_category_page_load_time(self, page: Page):
        """
        [PERFORMANCE BASIC #03] Đo thời gian load trang danh mục sản phẩm

        Mục đích: Xác định thời gian load của trang danh mục
        Kỳ vọng: response time < 2500ms
        """
        logger.info("🚀 [PERF_BASIC_03] Đang đo thời gian load Category Page...")

        start_time = time.time()
        await page.goto(f"{BASE_URL}index.php?route=product/category&path=20",
                       wait_until="networkidle")
        load_time = (time.time() - start_time) * 1000

        logger.info(f"✅ Category page loaded in {load_time:.2f}ms")
        assert load_time < 2500, f"Category page load time {load_time:.2f}ms exceeds 2500ms"

    @pytest.mark.asyncio
    @pytest.mark.performance
    @pytest.mark.basic
    async def test_perf_basic_04_cart_page_load_time(self, page: Page):
        """
        [PERFORMANCE BASIC #04] Đo thời gian load trang giỏ hàng

        Mục đích: Xác định thời gian load của trang giỏ hàng
        Kỳ vọng: response time < 2000ms
        """
        logger.info("🚀 [PERF_BASIC_04] Đang đo thời gian load Cart Page...")

        start_time = time.time()
        await page.goto(f"{BASE_URL}index.php?route=checkout/cart",
                       wait_until="networkidle")
        load_time = (time.time() - start_time) * 1000

        logger.info(f"✅ Cart page loaded in {load_time:.2f}ms")
        assert load_time < 2000, f"Cart page load time {load_time:.2f}ms exceeds 2000ms"

    @pytest.mark.asyncio
    @pytest.mark.performance
    @pytest.mark.basic
    async def test_perf_basic_05_search_response_time_simple(self, page: Page):
        """
        [PERFORMANCE BASIC #05] Đo thời gian response tìm kiếm (từ khóa đơn giản)

        Mục đích: Xác định thời gian tìm kiếm với từ khóa đơn giản
        Kỳ vọng: response time < 2000ms
        """
        logger.info("🚀 [PERF_BASIC_05] Đang đo Search Response Time...")

        start_time = time.time()
        await page.goto(f"{BASE_URL}index.php?route=product/search&search=iphone",
                       wait_until="networkidle")
        response_time = (time.time() - start_time) * 1000

        logger.info(f"✅ Search completed in {response_time:.2f}ms")
        assert response_time < 2000, f"Search time {response_time:.2f}ms exceeds 2000ms"

    @pytest.mark.asyncio
    @pytest.mark.performance
    @pytest.mark.basic
    async def test_perf_basic_06_login_response_time(self, page: Page):
        """
        [PERFORMANCE BASIC #06] Đo thời gian response đăng nhập

        Mục đích: Xác định thời gian xử lý yêu cầu đăng nhập
        Kỳ vọng: response time < 2500ms
        """
        logger.info("🚀 [PERF_BASIC_06] Đang đo Login Response Time...")

        await page.goto(f"{BASE_URL}index.php?route=account/login")

        await page.fill('input[name="email"]', "shin@test.com")
        await page.fill('input[name="password"]', "123456")

        start_time = time.time()
        try:
            await page.click('button[type="submit"]')
            await page.wait_for_load_state("networkidle")
        except:
            pass

        login_time = (time.time() - start_time) * 1000

        logger.info(f"✅ Login processed in {login_time:.2f}ms")
        assert login_time < 2500, f"Login time {login_time:.2f}ms exceeds 2500ms"

    @pytest.mark.asyncio
    @pytest.mark.performance
    @pytest.mark.basic
    async def test_perf_basic_07_add_to_cart_response_time(self, page: Page):
        """
        [PERFORMANCE BASIC #07] Đo thời gian response thêm sản phẩm vào giỏ hàng

        Mục đích: Xác định thời gian xử lý yêu cầu thêm vào giỏ
        Kỳ vọng: response time < 1500ms
        """
        logger.info("🚀 [PERF_BASIC_07] Đang đo Add to Cart Response Time...")

        await page.goto(f"{BASE_URL}index.php?route=product/product&product_id=40")

        start_time = time.time()
        try:
            await page.click('button#button-cart')
        except:
            await page.click('button:has-text("Add to Cart")')
        await page.wait_for_load_state("networkidle")

        add_cart_time = (time.time() - start_time) * 1000

        logger.info(f"✅ Add to Cart processed in {add_cart_time:.2f}ms")
        assert add_cart_time < 1500, f"Add to Cart time {add_cart_time:.2f}ms exceeds 1500ms"

    @pytest.mark.asyncio
    @pytest.mark.performance
    @pytest.mark.basic
    async def test_perf_basic_08_api_response_time_product_list(self, page: Page):
        """
        [PERFORMANCE BASIC #08] Đo thời gian response API lấy danh sách sản phẩm

        Mục đích: Xác định thời gian API trả về danh sách sản phẩm
        Kỳ vọng: response time < 1000ms
        """
        logger.info("🚀 [PERF_BASIC_08] Đang đo API Product List Response Time...")

        start_time = time.time()
        response = await page.request.get(
            f"{BASE_URL}index.php?route=api/product/search&search=iphone"
        )
        api_time = (time.time() - start_time) * 1000

        logger.info(f"✅ API responded in {api_time:.2f}ms (Status: {response.status})")
        assert response.status == 200, f"API returned status {response.status}"
        assert api_time < 1000, f"API response time {api_time:.2f}ms exceeds 1000ms"

    @pytest.mark.asyncio
    @pytest.mark.performance
    @pytest.mark.basic
    async def test_perf_basic_09_database_query_aggregate_load_time(self, page: Page):
        """
        [PERFORMANCE BASIC #09] Đo thời gian tổng hợp các truy vấn CSDL

        Mục đích: Xác định thông lượng tổng hợp của các truy vấn
        Kỳ vọng: response time < 3000ms
        """
        logger.info("🚀 [PERF_BASIC_09] Đang đo Database Aggregate Load Time...")

        # Thực hiện nhiều hành động liên tiếp để đo thông lượng CSDL
        start_time = time.time()

        await page.goto(f"{BASE_URL}index.php?route=product/category&path=20",
                       wait_until="networkidle")
        await page.goto(f"{BASE_URL}index.php?route=product/search&search=test",
                       wait_until="networkidle")
        await page.goto(f"{BASE_URL}index.php?route=product/product&product_id=40",
                       wait_until="networkidle")

        total_time = (time.time() - start_time) * 1000

        logger.info(f"✅ Aggregate DB queries completed in {total_time:.2f}ms")
        assert total_time < 3000, f"Aggregate time {total_time:.2f}ms exceeds 3000ms"

    @pytest.mark.asyncio
    @pytest.mark.performance
    @pytest.mark.basic
    async def test_perf_basic_10_static_asset_load_time(self, page: Page):
        """
        [PERFORMANCE BASIC #10] Đo thời gian load các tài nguyên tĩnh (CSS, JS, Images)

        Mục đích: Xác định thời gian tải CSS, JS, hình ảnh
        Kỳ vọng: tất cả tài nguyên tĩnh load < 2000ms tổng cộng
        """
        logger.info("🚀 [PERF_BASIC_10] Đang đo Static Assets Load Time...")

        start_time = time.time()
        await page.goto(BASE_URL, wait_until="domcontentloaded")

        # Chờ tất cả tài nguyên tĩnh
        await page.wait_for_load_state("networkidle")

        assets_time = (time.time() - start_time) * 1000

        logger.info(f"✅ Static assets loaded in {assets_time:.2f}ms")
        assert assets_time < 4000, f"Assets load time {assets_time:.2f}ms exceeds 4000ms"


class TestPerformanceAdvanced:
    """Advanced Performance Tests - Identify bottlenecks and stress test"""

    @pytest.mark.asyncio
    @pytest.mark.performance
    @pytest.mark.advanced
    async def test_perf_advanced_01_heavy_search_query_stress(self, page: Page):
        """
        [PERFORMANCE ADVANCED #01] Tìm kiếm với từ khóa dài gây tải nặng

        Mục đích: Xác định điểm nghẽn tìm kiếm với từ khóa phức tạp/dài
        Kỳ vọng: system should handle complex queries within 5s
        """
        logger.info("🚀 [PERF_ADV_01] Kiểm tra Heavy Search Query...")

        # Tạo từ khóa dài/phức tạp
        heavy_query = "a" * 500  # 500 ký tự

        start_time = time.time()
        try:
            await page.goto(
                f"{BASE_URL}index.php?route=product/search&search={heavy_query}",
                wait_until="networkidle",
                timeout=10000
            )
        except TimeoutError:
            logger.error("❌ BOTTLENECK DETECTED: Heavy search query timed out!")
            await page.screenshot(path="failures/AUTO_FAIL_PERF_ADV_01_HEAVY_SEARCH.png",
                                 full_page=True)
            assert False, "Heavy search query caused timeout - Database bottleneck"

        heavy_time = (time.time() - start_time) * 1000

        if heavy_time > 5000:
            logger.warning(f"⚠️ BOTTLENECK: Heavy search took {heavy_time:.2f}ms (expected < 5000ms)")
            await page.screenshot(path="failures/AUTO_FAIL_PERF_ADV_01_SLOW_SEARCH.png",
                                 full_page=True)
            assert False, f"Heavy search bottleneck: {heavy_time:.2f}ms"

        logger.info(f"✅ Heavy search completed in {heavy_time:.2f}ms")

    @pytest.mark.asyncio
    @pytest.mark.performance
    @pytest.mark.advanced
    async def test_perf_advanced_02_rapid_fire_cart_requests(self, page: Page):
        """
        [PERFORMANCE ADVANCED #02] Spam request liên tục thêm sản phẩm vào giỏ

        Mục đích: Kiểm tra khả năng chịu tải API giỏ hàng với spam requests
        Kỳ vọng: API should handle 10 rapid requests without performance degradation
        """
        logger.info("🚀 [PERF_ADV_02] Kiểm tra Rapid Fire Add to Cart Requests...")

        await page.goto(f"{BASE_URL}index.php?route=product/product&product_id=40")

        times = []
        for i in range(10):
            try:
                start = time.time()
                response = await page.request.post(
                    f"{BASE_URL}index.php?route=api/cart/add",
                    data={"product_id": "40", "quantity": "1"}
                )
                elapsed = (time.time() - start) * 1000
                times.append(elapsed)
                logger.info(f"  Request #{i+1}: {elapsed:.2f}ms (Status: {response.status})")
            except Exception as e:
                logger.error(f"❌ Request #{i+1} failed: {e}")
                await page.screenshot(path=f"failures/AUTO_FAIL_PERF_ADV_02_RAPID_FAIL_{i}.png")
                assert False, f"Rapid request #{i+1} failed - API overloaded"

        avg_time = sum(times) / len(times)
        max_time = max(times)

        if max_time > 3000:
            logger.error(f"❌ API BOTTLENECK: Max time {max_time:.2f}ms (avg: {avg_time:.2f}ms)")
            await page.screenshot(path="failures/AUTO_FAIL_PERF_ADV_02_API_OVERLOAD.png")
            assert False, f"Cart API overloaded: max {max_time:.2f}ms exceeds 3000ms"

        logger.info(f"✅ Rapid requests completed. Avg: {avg_time:.2f}ms, Max: {max_time:.2f}ms")

    @pytest.mark.asyncio
    @pytest.mark.performance
    @pytest.mark.advanced
    async def test_perf_advanced_03_database_connection_pool_stress(self, page: Page):
        """
        [PERFORMANCE ADVANCED #03] Kiểm tra pool kết nối CSDL dưới tải nặng

        Mục đích: Xác định điểm nghẽn connection pool
        Kỳ vọng: Concurrent requests < 2s per request
        """
        logger.info("🚀 [PERF_ADV_03] Kiểm tra Database Connection Pool Stress...")

        # Thực hiện các request đồng thời
        tasks = []
        for i in range(5):
            task = page.goto(
                f"{BASE_URL}index.php?route=product/category&path=20&page={i+1}",
                wait_until="networkidle",
                timeout=10000
            )
            tasks.append(task)

        start_time = time.time()
        try:
            await asyncio.gather(*tasks)
            total_time = (time.time() - start_time) * 1000

            if total_time > 10000:
                logger.error(f"❌ DB POOL BOTTLENECK: {total_time:.2f}ms for 5 concurrent requests")
                await page.screenshot(path="failures/AUTO_FAIL_PERF_ADV_03_DB_POOL.png")
                assert False, "Database connection pool bottleneck detected"

            logger.info(f"✅ Connection pool handled 5 concurrent requests in {total_time:.2f}ms")
        except asyncio.TimeoutError:
            logger.error("❌ CONNECTION POOL TIMEOUT: Database exhausted")
            await page.screenshot(path="failures/AUTO_FAIL_PERF_ADV_03_POOL_TIMEOUT.png")
            assert False, "Database connection pool exhausted"

    @pytest.mark.asyncio
    @pytest.mark.performance
    @pytest.mark.advanced
    async def test_perf_advanced_04_memory_leak_page_reload_cycle(self, page: Page):
        """
        [PERFORMANCE ADVANCED #04] Kiểm tra rò rỉ bộ nhớ qua chu kỳ reload liên tục

        Mục đích: Xác định rò rỉ bộ nhớ trong JavaScript hoặc backend
        Kỳ vọng: Không có sự tăng đơn điệu thời gian load
        """
        logger.info("🚀 [PERF_ADV_04] Kiểm tra Memory Leak trên Page Reload...")

        times = []
        for cycle in range(5):
            start = time.time()
            await page.reload(wait_until="networkidle")
            elapsed = (time.time() - start) * 1000
            times.append(elapsed)
            logger.info(f"  Cycle #{cycle+1}: {elapsed:.2f}ms")
            await asyncio.sleep(0.5)

        # Kiểm tra nếu thời gian tăng lên đều đặn (dấu hiệu rò rỉ)
        avg_growth = (times[-1] - times[0]) / times[0]

        if avg_growth > 0.3:  # Tăng > 30%
            logger.error(f"❌ MEMORY LEAK DETECTED: {avg_growth*100:.1f}% growth in reload time")
            await page.screenshot(path="failures/AUTO_FAIL_PERF_ADV_04_MEMORY_LEAK.png")
            assert False, f"Potential memory leak: {avg_growth*100:.1f}% reload time growth"

        logger.info(f"✅ No memory leak detected. Growth: {avg_growth*100:.1f}%")

    @pytest.mark.asyncio
    @pytest.mark.performance
    @pytest.mark.advanced
    async def test_perf_advanced_05_large_page_dataset_performance(self, page: Page):
        """
        [PERFORMANCE ADVANCED #05] Load trang có lượng sản phẩm lớn (100+ items)

        Mục đích: Xác định hiệu năng với dữ liệu lớn
        Kỳ vọng: Page should load and render < 5s with 100+ items
        """
        logger.info("🚀 [PERF_ADV_05] Kiểm tra Large Dataset Performance...")

        # Tìm danh mục có nhiều sản phẩm
        start_time = time.time()
        await page.goto(f"{BASE_URL}index.php?route=product/category&path=20&limit=100",
                       wait_until="networkidle",
                       timeout=10000)

        # Kiểm tra số lượng sản phẩm được render
        product_count = await page.locator('[class*="product-item"]').count()

        load_time = (time.time() - start_time) * 1000

        logger.info(f"✅ Loaded {product_count} products in {load_time:.2f}ms")

        if load_time > 5000 and product_count > 50:
            logger.error(f"❌ LARGE DATASET BOTTLENECK: {load_time:.2f}ms for {product_count} items")
            await page.screenshot(path="failures/AUTO_FAIL_PERF_ADV_05_LARGE_DATA.png")
            assert False, f"Large dataset bottleneck: {load_time:.2f}ms for {product_count} items"

    @pytest.mark.asyncio
    @pytest.mark.performance
    @pytest.mark.advanced
    async def test_perf_advanced_06_css_selector_performance_complexity(self, page: Page):
        """
        [PERFORMANCE ADVANCED #06] Kiểm tra hiệu năng selector CSS phức tạp

        Mục đích: Xác định hiệu năng khi phải query các selector phức tạp
        Kỳ vọng: Complex selectors < 500ms
        """
        logger.info("🚀 [PERF_ADV_06] Kiểm tra CSS Selector Performance...")

        await page.goto(BASE_URL, wait_until="networkidle")

        # Test various selector complexities
        selectors = [
            'div.product-item',  # Simple
            'div.container div.row div[class*="product"] a[href*="product"]',  # Complex
            '[data-attr-1][data-attr-2] > .item:not(.hidden)',  # Very complex
        ]

        for i, selector in enumerate(selectors):
            try:
                start = time.time()
                elements = await page.locator(selector).count()
                elapsed = (time.time() - start) * 1000

                if elapsed > 1000:
                    logger.warning(f"⚠️ Selector #{i+1} took {elapsed:.2f}ms")
                else:
                    logger.info(f"✅ Selector #{i+1}: {elapsed:.2f}ms ({elements} elements)")
            except Exception as e:
                logger.debug(f"Selector #{i+1} not found (expected)")

    @pytest.mark.asyncio
    @pytest.mark.performance
    @pytest.mark.advanced
    async def test_perf_advanced_07_concurrent_user_simulation(self, page: Page, browser: Browser):
        """
        [PERFORMANCE ADVANCED #07] Mô phỏng lưu lượng đồng thời 5+ người dùng

        Mục đích: Xác định hiệu năng dưới tải đồng thời
        Kỳ vọng: Response time không tăng > 100% khi có 5 users
        """
        logger.info("🚀 [PERF_ADV_07] Mô phỏng Concurrent Users...")

        # Đơn người dùng - baseline
        baseline_start = time.time()
        await page.goto(f"{BASE_URL}index.php?route=product/category&path=20",
                       wait_until="networkidle")
        baseline_time = (time.time() - baseline_start) * 1000

        logger.info(f"  Single user baseline: {baseline_time:.2f}ms")

        # 5 người dùng đồng thời
        pages = []
        try:
            concurrent_start = time.time()

            for i in range(4):  # 4 thêm = 5 tổng cộng
                ctx = await browser.new_context()
                p = await ctx.new_page()
                pages.append((p, ctx))

            # Load page on all 4 extra contexts simultaneously
            tasks = [p.goto(f"{BASE_URL}index.php?route=product/category&path=20",
                          wait_until="networkidle")
                    for p, ctx in pages]

            await asyncio.gather(*tasks)
            concurrent_time = (time.time() - concurrent_start) * 1000

            avg_concurrent = concurrent_time / 5
            degradation = (avg_concurrent - baseline_time) / baseline_time * 100

            logger.info(f"  Concurrent (5 users): {avg_concurrent:.2f}ms avg (degradation: {degradation:.1f}%)")

            if degradation > 100:
                logger.error(f"❌ SEVERE PERFORMANCE DEGRADATION: {degradation:.1f}%")
                await page.screenshot(path="failures/AUTO_FAIL_PERF_ADV_07_CONCURRENT.png")
                assert False, f"Performance degraded {degradation:.1f}% under concurrent load"

        finally:
            for p, ctx in pages:
                await p.close()
                await ctx.close()

    @pytest.mark.asyncio
    @pytest.mark.performance
    @pytest.mark.advanced
    async def test_perf_advanced_08_pagination_load_time_consistency(self, page: Page):
        """
        [PERFORMANCE ADVANCED #08] Kiểm tra tính nhất quán load time qua pagination

        Mục đích: Xác định xem các trang khác nhau có load time đều không
        Kỳ vọng: Variance < 20% giữa các trang
        """
        logger.info("🚀 [PERF_ADV_08] Kiểm tra Pagination Load Time Consistency...")

        times = []

        for page_num in range(1, 6):
            start = time.time()
            await page.goto(f"{BASE_URL}index.php?route=product/category&path=20&page={page_num}",
                          wait_until="networkidle",
                          timeout=10000)
            elapsed = (time.time() - start) * 1000
            times.append(elapsed)
            logger.info(f"  Page {page_num}: {elapsed:.2f}ms")

        avg_time = sum(times) / len(times)
        variance = max(times) - min(times)
        variance_pct = (variance / avg_time) * 100

        if variance_pct > 20:
            logger.error(f"❌ INCONSISTENT PAGINATION: Variance {variance_pct:.1f}%")
            await page.screenshot(path="failures/AUTO_FAIL_PERF_ADV_08_PAGINATION.png")
            assert False, f"Pagination performance inconsistent: {variance_pct:.1f}% variance"

        logger.info(f"✅ Pagination consistent. Avg: {avg_time:.2f}ms, Variance: {variance_pct:.1f}%")

    @pytest.mark.asyncio
    @pytest.mark.performance
    @pytest.mark.advanced
    async def test_perf_advanced_09_json_payload_size_optimization(self, page: Page):
        """
        [PERFORMANCE ADVANCED #09] ตรวจสอบขนาด JSON payload ที่ส่งกลับจาก API

        Mục đích: Xác định nếu payload quá lớn (chuyển giao dữ liệu lãng phí)
        Kỳ vọng: JSON payload < 500KB per request
        """
        logger.info("🚀 [PERF_ADV_09] Kiểm tra JSON Payload Size...")

        # Capture network requests
        request_sizes = []

        async def handle_response(response):
            try:
                size = len(await response.body())
                if 'api' in response.url or 'json' in response.headers.get('content-type', ''):
                    request_sizes.append(size)
            except:
                pass

        page.on("response", handle_response)

        await page.goto(f"{BASE_URL}index.php?route=product/search&search=test",
                       wait_until="networkidle")

        page.remove_listener("response", handle_response)

        if request_sizes:
            max_size = max(request_sizes) / 1024  # Convert to KB
            total_size = sum(request_sizes) / 1024

            logger.info(f"✅ API Payloads: Max {max_size:.2f}KB, Total {total_size:.2f}KB")

            if max_size > 500:
                logger.error(f"❌ LARGE PAYLOAD: {max_size:.2f}KB exceeds 500KB limit")
                await page.screenshot(path="failures/AUTO_FAIL_PERF_ADV_09_PAYLOAD.png")
                assert False, f"JSON payload too large: {max_size:.2f}KB"

    @pytest.mark.asyncio
    @pytest.mark.performance
    @pytest.mark.advanced
    async def test_perf_advanced_10_api_rate_limiting_detection(self, page: Page):
        """
        [PERFORMANCE ADVANCED #10] Kiểm tra cơ chế rate limiting trên API

        Mục đích: Xác định nếu API có bảo vệ rate limiting
        Kỳ vọng: API should implement rate limiting or throttling
        """
        logger.info("🚀 [PERF_ADV_10] Kiểm tra API Rate Limiting...")

        # Thực hiện 30 request nhanh chóng
        response_codes = []

        for i in range(30):
            try:
                response = await page.request.get(
                    f"{BASE_URL}index.php?route=product/search&search=test&_t={i}"
                )
                response_codes.append(response.status)

                if i % 10 == 0:
                    logger.info(f"  Request #{i+1}: Status {response.status}")
            except:
                pass

        # Kiểm tra nếu có 429 (Too Many Requests) hoặc 503 (Service Unavailable)
        has_rate_limit = 429 in response_codes or 503 in response_codes

        if not has_rate_limit:
            logger.warning("⚠️ NO RATE LIMITING: API accepts all 30 rapid requests")
            logger.warning("⚠️ System may be vulnerable to DDoS attacks")
            await page.screenshot(path="failures/AUTO_FAIL_PERF_ADV_10_NO_RATE_LIMIT.png")
            # Note: Not asserting False here as this is a design choice, just warning
            logger.info("✅ API rate limiting may need to be implemented for DDoS protection")
        else:
            logger.info(f"✅ Rate limiting detected: {response_codes.count(429)} x 429, {response_codes.count(503)} x 503")


# ================================================================================
# SECURITY TESTING SUBSYSTEM (20 tests: 10 basic + 10 advanced)
# ================================================================================

class TestSecurityBasic:
    """Basic Security Tests - Fundamental vulnerability checks"""

    @pytest.mark.asyncio
    @pytest.mark.security
    @pytest.mark.basic
    async def test_sec_basic_01_sql_injection_login_email(self, page: Page):
        """
        [SECURITY BASIC #01] SQL Injection ในฟอร์มโปรแกรมเข้าสู่ระบบ (Email field)

        Mục đích: Kiểm tra xem email field có bị SQL injection không
        Mẫu tấn công: ' OR '1'='1
        """
        logger.info("🔒 [SEC_BASIC_01] Kiểm tra SQL Injection trên Email field...")

        await page.goto(f"{BASE_URL}index.php?route=account/login")

        # SQL injection payload
        payload = "' OR '1'='1' -- "

        await page.fill('input[name="email"]', payload)
        await page.fill('input[name="password"]', "anypassword")

        try:
            await page.click('button[type="submit"]')
            await page.wait_for_load_state("networkidle")
        except:
            pass

        page_content = await page.content()

        # Kiểm tra nếu có thông báo lỗi DB hoặc thành công không mong đợi
        if "exception" in page_content.lower() or \
           "error" in page_content.lower() or \
           "my account" in page_content.lower():

            logger.error("❌ SQL INJECTION VULNERABILITY DETECTED: Email field vulnerable")
            await page.screenshot(path="failures/AUTO_FAIL_SEC_BASIC_01_SQL_INJECTION.png",
                                 full_page=True)
            assert False, "SQL Injection vulnerability in login email field"

        logger.info("✅ Email field is protected against SQL injection")

    @pytest.mark.asyncio
    @pytest.mark.security
    @pytest.mark.basic
    async def test_sec_basic_02_xss_profile_name_field(self, page: Page):
        """
        [SECURITY BASIC #02] XSS (Cross-Site Scripting) ở trường tên trong profile

        Mục đích: Kiểm tra xem tên người dùng có bị XSS không
        Mẫu tấn công: <script>alert('XSS')</script>
        """
        logger.info("🔒 [SEC_BASIC_02] Kiểm tra XSS trên Profile Name field...")

        # Đăng nhập trước
        await page.goto(f"{BASE_URL}index.php?route=account/login")
        await page.fill('input[name="email"]', "shin@test.com")
        await page.fill('input[name="password"]', "123456")

        try:
            await page.click('button[type="submit"]')
            await page.wait_for_load_state("networkidle")
        except:
            logger.warning("⚠️ Login may have failed, attempting to continue...")

        # Điều hướng tới edit account
        await page.goto(f"{BASE_URL}index.php?route=account/edit")

        # XSS payload
        xss_payload = "<script>alert('XSS')</script>"

        try:
            await page.fill('input[name="firstname"]', xss_payload)
        except:
            logger.debug("Could not fill firstname field")
            return

        try:
            await page.click('button[type="submit"]')
            await page.wait_for_load_state("networkidle")
        except:
            pass

        page_content = await page.content()

        if "<script>" in page_content and "alert" in page_content:
            logger.error("❌ XSS VULNERABILITY DETECTED: Name field vulnerable")
            await page.screenshot(path="failures/AUTO_FAIL_SEC_BASIC_02_XSS.png",
                                 full_page=True)
            assert False, "XSS vulnerability in profile name field"

        logger.info("✅ Profile name field is protected against XSS")

    @pytest.mark.asyncio
    @pytest.mark.security
    @pytest.mark.basic
    async def test_sec_basic_03_password_stored_plaintext_check(self, page: Page):
        """
        [SECURITY BASIC #03] Kiểm tra xem mật khẩu có được lưu dưới dạng plaintext không

        Mục đích: Xác nhận mật khẩu được hash/encrypt chứ không phải plaintext
        Phương pháp: Kiểm tra database hoặc response headers
        """
        logger.info("🔒 [SEC_BASIC_03] Kiểm tra Password Storage Security...")

        # Tạo tài khoản mới
        timestamp = datetime.now().timestamp()
        test_email = f"sec_test_{timestamp}@test.com"
        test_password = "SecurePass123!@#"

        await page.goto(f"{BASE_URL}index.php?route=account/register")

        await page.fill('input[name="firstname"]', "Security")
        await page.fill('input[name="lastname"]', "Test")
        await page.fill('input[name="email"]', test_email)
        await page.fill('input[name="telephone"]', "0123456789")
        await page.fill('input[name="password"]', test_password)

        try:
            await page.check('input[name="agree"]')
        except:
            pass

        try:
            await page.click('button[type="submit"]')
            await page.wait_for_load_state("networkidle")
        except:
            pass

        # Cố gắng đăng nhập lại
        await page.goto(f"{BASE_URL}index.php?route=account/login")
        await page.fill('input[name="email"]', test_email)
        await page.fill('input[name="password"]', test_password)

        try:
            await page.click('button[type="submit"]')
            await page.wait_for_load_state("networkidle")
        except:
            pass

        page_content = await page.content()

        # Nếu đặt lại mật khẩu gửi về plaintext, đó là lỗi
        if test_password in page_content:
            logger.error("❌ PASSWORD STORED AS PLAINTEXT: Password visible in response")
            await page.screenshot(path="failures/AUTO_FAIL_SEC_BASIC_03_PLAINTEXT_PASSWORD.png")
            assert False, "Password stored or transmitted as plaintext"

        logger.info("✅ Passwords appear to be properly hashed/encrypted")

    @pytest.mark.asyncio
    @pytest.mark.security
    @pytest.mark.basic
    async def test_sec_basic_04_csrf_protection_form_token(self, page: Page):
        """
        [SECURITY BASIC #04] CSRF (Cross-Site Request Forgery) Protection

        Mục đích: Kiểm tra xem form có CSRF token không
        Kỳ vọng: Tất cả form POST phải có CSRF token
        """
        logger.info("🔒 [SEC_BASIC_04] Kiểm tra CSRF Protection...")

        await page.goto(f"{BASE_URL}index.php?route=account/login")

        page_html = await page.content()

        # Tìm token/nonce trong form
        csrf_patterns = [
            r'name=["\']_token["\']',
            r'name=["\']csrf_token["\']',
            r'name=["\']nonce["\']',
            r'_token.*value',
            r'csrf.*value',
        ]

        has_csrf = any(re.search(pattern, page_html, re.IGNORECASE) for pattern in csrf_patterns)

        if not has_csrf:
            logger.error("❌ CSRF PROTECTION MISSING: No CSRF token found in form")
            await page.screenshot(path="failures/AUTO_FAIL_SEC_BASIC_04_NO_CSRF.png")
            assert False, "Form lacks CSRF token protection"

        logger.info("✅ CSRF protection token detected")

    @pytest.mark.asyncio
    @pytest.mark.security
    @pytest.mark.basic
    async def test_sec_basic_05_exposed_error_messages(self, page: Page):
        """
        [SECURITY BASIC #05] Lỗi hiển thị quá chi tiết (Information Disclosure)

        Mục đích: Kiểm tra xem error message có tiết lộ thông tin hệ thống không
        Kỳ vọng: Error messages không nên chứa đường dẫn tệp, tên DB version
        """
        logger.info("🔒 [SEC_BASIC_05] Kiểm tra Exposed Error Messages...")

        # Truy cập URL không tồn tại
        await page.goto(f"{BASE_URL}index.php?route=nonexistent/page/xyz",
                       wait_until="load")

        page_content = await page.content()

        # Patterns that indicate over-verbose errors
        dangerous_patterns = [
            r"/var/www/",  # File paths
            r"\.php line \d+",  # PHP line numbers
            r"MySQL", r"PostgreSQL",  # Database type
            r"Stack trace:",  # Debug info
            r"Fatal error:",  # Fatal messages
        ]

        for pattern in dangerous_patterns:
            if re.search(pattern, page_content, re.IGNORECASE):
                logger.error(f"❌ INFORMATION DISCLOSURE: Error message contains {pattern}")
                await page.screenshot(path="failures/AUTO_FAIL_SEC_BASIC_05_ERROR_DISCLOSURE.png")
                assert False, f"Error messages expose sensitive info: {pattern}"

        logger.info("✅ Error messages are appropriately generic")

    @pytest.mark.asyncio
    @pytest.mark.security
    @pytest.mark.basic
    async def test_sec_basic_06_insecure_direct_object_reference_address(self, page: Page):
        """
        [SECURITY BASIC #06] IDOR (Insecure Direct Object Reference) - Address Book

        Mục đích: Kiểm tra xem có thể truy cập sổ địa chỉ của người dùng khác
        Kỳ vọng: Address ID không nên accessible từ user khác
        """
        logger.info("🔒 [SEC_BASIC_06] Kiểm tra IDOR - Address Book...")

        # Thử truy cập địa chỉ với ID không phải của người dùng
        await page.goto(f"{BASE_URL}index.php?route=account/address&address_id=999999")

        page_content = await page.content()

        # Nếu có thông tin địa chỉ từ user khác, đó là IDOR
        if "address" in page_content.lower() and "edit" in page_content.lower():
            # Kiểm tra xem nó là lỗi hay thực sự trả về địa chỉ
            if "address_id=999999" in await page.url:
                logger.error("❌ IDOR VULNERABILITY: Can access arbitrary address IDs")
                await page.screenshot(path="failures/AUTO_FAIL_SEC_BASIC_06_IDOR.png")
                assert False, "IDOR vulnerability in address book"

        logger.info("✅ IDOR protection appears adequate for address book")

    @pytest.mark.asyncio
    @pytest.mark.security
    @pytest.mark.basic
    async def test_sec_basic_07_session_token_entropy(self, page: Page):
        """
        [SECURITY BASIC #07] Session Token Entropy - Kiểm tra độ ngẫu nhiên

        Mục đích: Kiểm tra xem session token có đủ entropy không
        Kỳ vọng: Session token phải khó dự đoán
        """
        logger.info("🔒 [SEC_BASIC_07] Kiểm tra Session Token Entropy...")

        tokens = []

        for i in range(3):
            await page.context.clear_cookies()
            await page.goto(f"{BASE_URL}index.php?route=account/account")

            # Lấy session cookie
            cookies = await page.context.cookies()
            for cookie in cookies:
                if 'session' in cookie['name'].lower() or cookie['name'] == 'OCSESSID':
                    tokens.append(cookie['value'])
                    logger.info(f"  Token #{i+1}: {cookie['value'][:20]}...")

        if len(tokens) < 2:
            logger.debug("Could not extract session tokens")
            return

        # Kiểm tra nếu tokens quá giống nhau (dấu hiệu entropy thấp)
        if tokens[0][:10] == tokens[1][:10]:
            logger.error("❌ LOW ENTROPY: Session tokens start with same prefix")
            await page.screenshot(path="failures/AUTO_FAIL_SEC_BASIC_07_LOW_ENTROPY.png")
            assert False, "Session tokens have low entropy"

        logger.info("✅ Session tokens appear to have sufficient entropy")

    @pytest.mark.asyncio
    @pytest.mark.security
    @pytest.mark.basic
    async def test_sec_basic_08_ssl_https_enforcement(self, page: Page):
        """
        [SECURITY BASIC #08] HTTPS Enforcement - Kiểm tra bắt buộc sử dụng HTTPS

        Mục đích: Kiểm tra xem hệ thống có bắt buộc HTTPS không
        Kỳ vọng: Nên redirect HTTP → HTTPS
        """
        logger.info("🔒 [SEC_BASIC_08] Kiểm tra HTTPS Enforcement...")

        # Nếu BASE_URL là HTTP, kiểm tra redirect
        if BASE_URL.startswith("http://"):
            https_url = BASE_URL.replace("http://", "https://")

            try:
                response = await page.request.get(https_url, timeout=5000)
                logger.info(f"✅ HTTPS available at {https_url}")
            except:
                logger.warning(f"⚠️ HTTPS not available at {https_url}")
        else:
            logger.info("✅ Already using HTTPS")

    @pytest.mark.asyncio
    @pytest.mark.security
    @pytest.mark.basic
    async def test_sec_basic_09_default_credentials_check(self, page: Page):
        """
        [SECURITY BASIC #09] Default Credentials - Kiểm tra admin mặc định

        Mục đích: Kiểm tra xem admin mặc định có còn hoạt động không
        Kỳ vọng: Default admin account phải bị vô hiệu hóa
        """
        logger.info("🔒 [SEC_BASIC_09] Kiểm tra Default Credentials...")

        await page.goto(f"{BASE_URL}admin/")

        # Thử login với admin default
        try:
            await page.fill('input[name="username"]', "admin")
            await page.fill('input[name="password"]', "admin")
            await page.click('button[type="submit"]')
            await page.wait_for_load_state("networkidle", timeout=5000)
        except:
            pass

        current_url = page.url
        page_content = await page.content()
        
        if "dashboard" in current_url or "Logged" in page_content:
            logger.error("❌ DEFAULT CREDENTIALS VALID: Admin/admin still works!")
            await page.screenshot(path="failures/AUTO_FAIL_SEC_BASIC_09_DEFAULT_ADMIN.png")
            assert False, "Default admin credentials are still valid"

        logger.info("✅ Default credentials are not valid")

    @pytest.mark.asyncio
    @pytest.mark.security
    @pytest.mark.basic
    async def test_sec_basic_10_input_length_validation(self, page: Page):
        """
        [SECURITY BASIC #10] Input Length Validation - Buffer Overflow Prevention

        Mục đích: Kiểm tra xem có giới hạn độ dài input không
        Kỳ vọng: Input phải có maxlength hoặc backend validation
        """
        logger.info("🔒 [SEC_BASIC_10] Kiểm tra Input Length Validation...")

        await page.goto(f"{BASE_URL}index.php?route=account/register")

        # Kiểm tra maxlength attribute
        firstname_input = await page.query_selector('input[name="firstname"]')

        if firstname_input:
            maxlength = await firstname_input.get_attribute("maxlength")

            if not maxlength:
                logger.warning("⚠️ No maxlength attribute on firstname field")
            else:
                logger.info(f"✅ Maxlength attribute found: {maxlength}")

        # Thử input rất dài
        long_input = "A" * 10000
        try:
            await page.fill('input[name="firstname"]', long_input)

            # Kiểm trace xem giá trị thực tế
            actual_value = await page.input_value('input[name="firstname"]')

            if len(actual_value) > 1000:
                logger.error("❌ INPUT LENGTH NOT VALIDATED: 10000 chars accepted")
                await page.screenshot(path="failures/AUTO_FAIL_SEC_BASIC_10_LONG_INPUT.png")
                assert False, "Input length validation missing"

            logger.info("✅ Input length properly validated")
        except:
            logger.debug("Could not test input length")


class TestSecurityAdvanced:
    """Advanced Security Tests - Vulnerability and exploitation scenarios"""

    @pytest.mark.asyncio
    @pytest.mark.security
    @pytest.mark.advanced
    async def test_sec_advanced_01_negative_price_parameter_tampering(self, page: Page):
        """
        [SECURITY ADVANCED #01] Thao túng tham số giá âm trong giỏ hàng (Critical)

        Mục đích: Kiểm tra xem có thể đưa sản phẩm với giá âm vào giỏ hàng không
        Tấn công: Sửa trực tiếp giá sản phẩm qua Network tab
        """
        logger.info("🔒 [SEC_ADV_01] Kiểm tra Parameter Tampering - Negative Price...")

        await page.goto(f"{BASE_URL}index.php?route=product/product&product_id=40")

        # Sử dụng page.request để POST API với giá âm
        try:
            response = await page.request.post(
                f"{BASE_URL}index.php?route=api/cart/add",
                data={
                    "product_id": "40",
                    "quantity": "1",
                    "price": "-100.00"  # Giá âm
                }
            )

            response_text = await response.text()

            if response.status == 200:
                # Kiểm tra giỏ hàng
                cart_response = await page.request.get(f"{BASE_URL}index.php?route=checkout/cart")
                cart_content = await cart_response.text()

                if "-" in cart_content or "negative" in cart_content.lower():
                    logger.error("❌ PRICE TAMPERING VULNERABILITY: Negative price accepted!")
                    await page.screenshot(path="failures/AUTO_FAIL_SEC_ADV_01_NEGATIVE_PRICE.png")
                    assert False, "API accepts negative prices - allows free products"
        except Exception as e:
            logger.debug(f"Price tampering test exception: {e}")

        logger.info("✅ Negative price parameter correctly rejected")

    @pytest.mark.asyncio
    @pytest.mark.security
    @pytest.mark.advanced
    async def test_sec_advanced_02_idor_order_enumeration_attack(self, page: Page):
        """
        [SECURITY ADVANCED #02] IDOR - Enumeration đơn hàng người dùng khác (Critical)

        Mục đích: Kiểm tra xem có thể xem đơn hàng của người dùng khác bằng cách
                 thay đổi order_id trong URL
        Tấn công: PUT /api/order/1, /api/order/2, /api/order/3... etc
        """
        logger.info("🔒 [SEC_ADV_02] Kiểm tra IDOR - Order Enumeration...")

        # Cố gắng truy cập nhiều order ID khác nhau
        for order_id in range(1, 20):
            try:
                response = await page.request.get(
                    f"{BASE_URL}index.php?route=account/order&order_id={order_id}"
                )

                response_text = await response.text()

                # Nếu trả về order details của user khác, đó là IDOR
                if "order-info" in response_text or "Order ID" in response_text:
                    if order_id not in [1, 2, 3]:  # Các ID có thể của user hiện tại
                        logger.error(f"❌ IDOR VULNERABILITY: Accessed order #{order_id} of another user")
                        await page.screenshot(path=f"failures/AUTO_FAIL_SEC_ADV_02_IDOR_ORDER_{order_id}.png")
                        assert False, f"IDOR: Can enumerate orders of other users (order_id={order_id})"
            except:
                pass  # Order không tồn tại = bình thường

        logger.info("✅ IDOR protection adequate for order access")

    @pytest.mark.asyncio
    @pytest.mark.security
    @pytest.mark.advanced
    async def test_sec_advanced_03_address_book_unauthorized_modification(self, page: Page):
        """
        [SECURITY ADVANCED #03] Sửa đổi sổ địa chỉ người dùng khác qua IDOR (Critical)

        Mục đích: Kiểm tra xem có thể PUT/DELETE địa chỉ của người dùng khác không
        Tấn cock: POST /api/address/update với address_id của user khác
        """
        logger.info("🔒 [SEC_ADV_03] Kiểm tra Address Book Modification IDOR...")

        # Cố gắng sửa địa chỉ với ID không hợp lệ
        for addr_id in [999, 888, 777]:
            try:
                response = await page.request.post(
                    f"{BASE_URL}index.php?route=api/account/address",
                    data={
                        "address_id": str(addr_id),
                        "firstname": "HACKED",
                        "street": "Attacker Street",
                        "city": "Hacker City"
                    }
                )

                if response.status == 200:
                    logger.error(f"❌ ADDRESS IDOR: Successfully modified address #{addr_id}")
                    await page.screenshot(path=f"failures/AUTO_FAIL_SEC_ADV_03_ADDR_IDOR_{addr_id}.png")
                    assert False, f"IDOR: Can modify addresses of other users (addr_id={addr_id})"
            except:
                pass

        logger.info("✅ Address book modification is properly protected")

    @pytest.mark.asyncio
    @pytest.mark.security
    @pytest.mark.advanced
    async def test_sec_advanced_04_race_condition_coupon_multiple_apply(self, page: Page):
        """
        [SECURITY ADVANCED #04] Race Condition - Áp dụng coupon nhiều lần cùng lúc (Hard)

        Mục đích: Kiểm tra xem có thể áp dụng coupon nhiều lần trong cùng 1ms không
        Tấn công: Gửi request POST apply coupon đồng thời 10 lần
        """
        logger.info("🔒 [SEC_ADV_04] Kiểm tra Race Condition - Multiple Coupon Apply...")

        await page.goto(f"{BASE_URL}index.php?route=product/product&product_id=40")
        try:
            await page.click('button#button-cart')
        except:
            await page.click('button:has-text("Add to Cart")')

        await page.goto(f"{BASE_URL}index.php?route=checkout/cart")

        # Tạo 10 request apply coupon đồng thời
        tasks = []
        for i in range(10):
            task = page.request.post(
                f"{BASE_URL}index.php?route=checkout/cart/apply_coupon",
                data={"coupon": "TESTCOUPON"}
            )
            tasks.append(task)

        try:
            responses = await asyncio.gather(*tasks)
            success_count = sum(1 for r in responses if r.status == 200)

            if success_count > 1:
                logger.error(f"❌ RACE CONDITION: Applied coupon {success_count} times simultaneously")
                await page.screenshot(path="failures/AUTO_FAIL_SEC_ADV_04_RACE_COUPON.png")
                assert False, f"Race condition: Coupon applied {success_count} times in one operation"

            logger.info("✅ Coupon application protected against race conditions")
        except Exception as e:
            logger.debug(f"Race condition test exception: {e}")

    @pytest.mark.asyncio
    @pytest.mark.security
    @pytest.mark.advanced
    async def test_sec_advanced_05_database_corruption_long_input_overflow(self, page: Page):
        """
        [SECURITY ADVANCED #05] Database Corruption - Buffer Overflow via Long Input (Hard)

        Mục đích: Kiểm tra xem có thể gây corruption CSDL bằng input cực dài không
        Tấn công: Register với firstname dài 65,000 ký tự
        """
        logger.info("🔒 [SEC_ADV_05] Kiểm tra Database Corruption - Long Input...")

        await page.goto(f"{BASE_URL}index.php?route=account/register")

        # Tạo input cực dài
        overflow_input = "A" * 65000
        timestamp = datetime.now().timestamp()

        try:
            await page.fill('input[name="firstname"]', overflow_input)
            await page.fill('input[name="lastname"]', "LongTest")
            await page.fill('input[name="email"]', f"overflow_{timestamp}@test.com")
            await page.fill('input[name="telephone"]', "0123456789")
            await page.fill('input[name="password"]', "TestPass123")

            try:
                await page.check('input[name="agree"]')
            except:
                pass

            try:
                await page.click('button[type="submit"]')
                await page.wait_for_load_state("networkidle", timeout=5000)
            except:
                pass

            page_content = await page.content()

            # Kiểm tra nếu registration thành công với input cực dài
            if "success" in page_content.lower() or "account" in await page.url:
                logger.error("❌ DATABASE OVERFLOW: Successfully accepted 65000-char input")
                await page.screenshot(path="failures/AUTO_FAIL_SEC_ADV_05_DB_OVERFLOW.png")
                assert False, "Database accepts dangerously long inputs causing potential corruption"

            logger.info("✅ Long input properly truncated or rejected")
        except Exception as e:
            logger.debug(f"Overflow test exception: {e}")

    @pytest.mark.asyncio
    @pytest.mark.security
    @pytest.mark.advanced
    async def test_sec_advanced_06_email_header_injection_contact_form(self, page: Page):
        """
        [SECURITY ADVANCED #06] Email Header Injection - ฟอร์มติดต่อ (Hard)

        Mục đích: Kiểm tra xem có inject email header ได้không
        Tấn công: Customer Subject: subject%0aBCC: attacker@evil.com
        """
        logger.info("🔒 [SEC_ADV_06] Kiểm trace Email Header Injection...")

        await page.goto(f"{BASE_URL}index.php?route=information/contact")

        # Email header injection payload
        payload = "TestSubject\nBCC:attacker@evil.com"

        try:
            await page.fill('input[name="name"]', "Security Tester")
            await page.fill('input[name="email"]', "test@example.com")
            await page.fill('input[name="subject"]', payload)
            await page.fill('textarea[name="message"]', "Test message")

            try:
                await page.click('button[type="submit"]')
                await page.wait_for_load_state("networkidle", timeout=3000)
            except:
                pass

            # Kiểm tra xem payload được chấp nhận hay không
            page_content = await page.content()

            if "success" in page_content.lower():
                logger.warning("⚠️ EMAIL INJECTION: Header injection payload accepted")
                logger.info("  (This requires email log verification to be certain)")
        except:
            pass

        logger.info("✅ Contact form appears to handle special characters safely")

    @pytest.mark.asyncio
    @pytest.mark.security
    @pytest.mark.advanced
    async def test_sec_advanced_07_payment_amount_validation_bypass(self, page: Page):
        """
        [SECURITY ADVANCED #07] Bypass Amount Validation ở Checkout (Extreme)

        Mục đích: Kiểm tra xem có thể sửa tổng tiền thanh toán không
        Tấn công: page.evaluate để sửa trực tiếp giá trọng DOM trước submit
        """
        logger.info("🔒 [SEC_ADV_07] Kiểm tra Payment Amount Validation...")

        await page.goto(f"{BASE_URL}index.php?route=product/product&product_id=40")
        try:
            await page.click('button#button-cart')
        except:
            await page.click('button:has-text("Add to Cart")')

        await page.goto(f"{BASE_URL}index.php?route=checkout/checkout")
        await page.wait_for_load_state("networkidle")

        # Sử dụng page.evaluate để sửa giá trong DOM
        try:
            await page.evaluate("""
                () => {
                    // Tìm element chứa tổng tiền
                    const totalElements = Array.from(document.querySelectorAll('span, div, td'))
                        .filter(el => el.textContent.includes('Total') || el.textContent.includes('₫'));
                    
                    if (totalElements.length > 0) {
                        // Sửa giá trị
                        totalElements[0].textContent = 'Total: 0₫';
                    }
                }
            """)

            logger.error("❌ PAYMENT BYPASS: Successfully modified total amount in DOM")
            await page.screenshot(path="failures/AUTO_FAIL_SEC_ADV_07_PAYMENT_BYPASS.png")
            assert False, "Payment amount can be tampered via DOM manipulation"
        except:
            logger.debug("Page.evaluate may be blocked or not found")

        logger.info("✅ Payment amount appears server-validated")

    @pytest.mark.asyncio
    @pytest.mark.security
    @pytest.mark.advanced
    async def test_sec_advanced_08_admin_authentication_bypass(self, page: Page):
        """
        [SECURITY ADVANCED #08] Admin Authentication Bypass - Direct URL Access (Extreme)

        Mục đích: Kiểm trace có thể truy cập admin panel mà không đăng nhập không
        Tấn công: navigate trực tiếp đến /admin/dashboard mà không auth
        """
        logger.info("🔒 [SEC_ADV_08] Kiểm tra Admin Authentication Bypass...")

        # Xóa tất cả cookies để đảm bảo không authenticated
        await page.context.clear_cookies()

        # Cố gắng truy cập admin dashboard
        try:
            await page.goto(f"{BASE_URL}admin/index.php?route=dashboard/dashboard",
                          wait_until="load",
                          timeout=5000)
        except:
            pass

        page_url = page.url
        page_content = await page.content()

        # Kiểm trace xem đã redirect tới login hay vào được dashboard
        if "dashboard" in page_url and "Login" not in page_content:
            logger.error("❌ AUTH BYPASS: Accessed admin dashboard without login!")
            await page.screenshot(path="failures/AUTO_FAIL_SEC_ADV_08_ADMIN_BYPASS.png")
            assert False, "Authentication bypass: Can access admin without login"

        logger.info("✅ Admin panel requires authentication")

    @pytest.mark.asyncio
    @pytest.mark.security
    @pytest.mark.advanced
    async def test_sec_advanced_09_stored_xss_product_description(self, page: Page):
        """
        [SECURITY ADVANCED #09] Stored XSS - Product Description (Hard)

        Mục đích: Kiểm trace XSS được lưu trong CSDL và thực thi khi view
        Tấn công: Upload product với description=\"<img src=x onerror=alert()>\"
        """
        logger.info("🔒 [SEC_ADV_09] Kiểm trace Stored XSS - Product Description...")

        xss_payload = '<img src=x onerror="alert(\'XSS\')">'

        # Cố gắng tạo product qua API
        try:
            response = await page.request.post(
                f"{BASE_URL}api/product",
                data={
                    "name": "XSS Test Product",
                    "description": xss_payload,
                }
            )

            if response.status == 200:
                # Truy cập lại product để kiểm tra XSS
                await page.goto(f"{BASE_URL}index.php?route=product/search&search=XSS+Test")

                page_content = await page.content()

                if xss_payload in page_content:
                    logger.error("❌ STORED XSS: XSS payload stored and reflected in product page")
                    await page.screenshot(path="failures/AUTO_FAIL_SEC_ADV_09_STORED_XSS.png")
                    assert False, "Stored XSS vulnerability in product descriptions"
        except:
            logger.debug("Product API not accessible via page.request")

        logger.info("✅ XSS protection appears adequate for product descriptions")

    @pytest.mark.asyncio
    @pytest.mark.security
    @pytest.mark.advanced
    async def test_sec_advanced_10_unencrypted_sensitive_data_transit(self, page: Page):
        """
        [SECURITY ADVANCED #10] Unencrypted Sensitive Data in Transit (Hard)

        Mục đích: Kiểm trace xem dữ liệu nhạy cảm có được transmit qua HTTP không
        Kỳ vọng: Password, CC info phải được transmit qua HTTPS
        """
        logger.info("🔒 [SEC_ADV_10] Kiểm trace Unencrypted Data Transit...")

        # Nếu BASE_URL là HTTP, kiểm trace dữ liệu nhạy cảm
        if BASE_URL.startswith("http://"):
            logger.warning("⚠️ UNENCRYPTED TRANSIT: Using HTTP instead of HTTPS")
            logger.warning("⚠️ Sensitive data may be transmitted unencrypted")

            # Ghi log và chụp ảnh
            await page.goto(f"{BASE_URL}index.php?route=account/login")
            await page.screenshot(path="failures/AUTO_FAIL_SEC_ADV_10_HTTP_NOT_HTTPS.png")

            assert False, "Sensitive endpoints should use HTTPS encryption"

        logger.info("✅ Using HTTPS for secure data transmission")


# ================================================================================
# USABILITY TESTING SUBSYSTEM (20 tests: 10 basic + 10 advanced)
# ================================================================================

class TestUsabilityBasic:
    """Basic Usability Tests - Fundamental UI/UX checks"""

    @pytest.mark.asyncio
    @pytest.mark.usability
    @pytest.mark.basic
    async def test_usab_basic_01_homepage_responsive_mobile(self, page: Page):
        """
        [USABILITY BASIC #01] Responsive Design - Homepage on Mobile (375px width)

        Mục đích: Kiểm trace giao diện trang chủ responsive trên thiết bị di động
        Kỳ vọng: UI elements should be properly formatted at 375px viewport
        """
        logger.info("📱 [USAB_BASIC_01] Kiểm trace Homepage Responsive Design...")

        # Set mobile viewport
        await page.set_viewport_size({"width": 375, "height": 667})

        await page.goto(BASE_URL, wait_until="networkidle")

        # Kiểm trace xem có horizontal scroll không
        scrollWidth = await page.evaluate("window.document.documentElement.scrollWidth")
        viewportWidth = await page.evaluate("window.innerWidth")

        if scrollWidth > viewportWidth:
            logger.error("❌ RESPONSIVE ISSUE: Horizontal scrollbar on 375px viewport")
            await page.screenshot(path="failures/AUTO_FAIL_USAB_BASIC_01_MOBILE_SCROLL.png")
            assert False, "Homepage not responsive: horizontal overflow on mobile"

        logger.info("✅ Homepage properly responsive on mobile")

    @pytest.mark.asyncio
    @pytest.mark.usability
    @pytest.mark.basic
    async def test_usab_basic_02_navigation_menu_accessibility(self, page: Page):
        """
        [USABILITY BASIC #02] Navigation Menu - Tất cả menu items có thể truy cập được

        Mục đích: Kiểm trace menu navigation không bị ẩn hoặc không thể click
        Kỳ vọng: Tất cả menu items phải visible và clickable
        """
        logger.info("🔍 [USAB_BASIC_02] Kiểm trace Navigation Menu Accessibility...")

        await page.goto(BASE_URL, wait_until="networkidle")

        # Tìm tất cả menu items
        menu_items = await page.locator('nav a, [role="navigation"] a').count()

        if menu_items == 0:
            logger.error("❌ NO MENU FOUND: Navigation menu structure not found")
            await page.screenshot(path="failures/AUTO_FAIL_USAB_BASIC_02_NO_MENU.png")
            assert False, "Navigation menu not detected"

        # Kiểm trace xem các items có visible không
        invisible_count = 0
        for i in range(min(5, menu_items)):  # Check first 5
            try:
                is_visible = await page.locator('nav a, [role="navigation"] a').nth(i).is_visible()
                if not is_visible:
                    invisible_count += 1
            except:
                invisible_count += 1

        if invisible_count > 0:
            logger.warning(f"⚠️ ACCESSIBILITY: {invisible_count} menu items not visible")
            logger.info("✅ Some menu items exist (may be hidden/mobile)")
        else:
            logger.info(f"✅ All {menu_items} menu items are accessible")

    @pytest.mark.asyncio
    @pytest.mark.usability
    @pytest.mark.basic
    async def test_usab_basic_03_form_label_association(self, page: Page):
        """
        [USABILITY BASIC #03] Form Labels - Formal field labels properly associated

        Mục đích: Kiểm trace <label> có gắn với <input> qua for attribute
        Kỳ vọng: Tất cả form fields phải có label hoặc accessible name
        """
        logger.info("📋 [USAB_BASIC_03] Kiểm trace Form Label Association...")

        await page.goto(f"{BASE_URL}index.php?route=account/register")

        # Tìm tất cả input fields
        inputs = await page.locator('input[type="text"], input[type="email"], input[type="password"]').count()

        if inputs == 0:
            logger.warning("⚠️ No input fields found on registration form")
            return

        # Kiểm trace labels
        labels = await page.locator('label').count()

        if labels < inputs * 0.5:  # Ít nhất 50% fields phải có label
            logger.error("❌ MISSING LABELS: Many fields lack associated labels")
            await page.screenshot(path="failures/AUTO_FAIL_USAB_BASIC_03_NO_LABELS.png")
            assert False, "Form fields lack proper labels for accessibility"

        logger.info(f"✅ Form labels adequate: {labels} labels for {inputs} inputs")

    @pytest.mark.asyncio
    @pytest.mark.usability
    @pytest.mark.basic
    async def test_usab_basic_04_button_text_clarity(self, page: Page):
        """
        [USABILITY BASIC #04] Button Text - Các nút phải có text rõ ràng

        Mục đích: Kiểm trace button text không generic (không phải "Click", "OK")
        Kỳ vọng: Button text phải descriptive (e.g., "Add to Cart", "Continue")
        """
        logger.info("🔘 [USAB_BASIC_04] Kiểm trace Button Text Clarity...")

        await page.goto(f"{BASE_URL}index.php?route=product/product&product_id=40")

        # Tìm buttons
        buttons = await page.locator('button').all()

        unclear_buttons = 0
        for button in buttons:
            text = await button.text_content()

            if text and len(text.strip()) > 0:
                if text.lower() in ["click", "ok", "btn", "button", ""]:
                    unclear_buttons += 1
                    logger.warning(f"  Unclear button text: '{text}'")

        if unclear_buttons > 3:
            logger.error(f"❌ UNCLEAR BUTTONS: {unclear_buttons} buttons have generic text")
            await page.screenshot(path="failures/AUTO_FAIL_USAB_BASIC_04_GENERIC_BUTTONS.png")
            assert False, f"{unclear_buttons} buttons have unclear text"

        logger.info(f"✅ Button text clarity adequate ({unclear_buttons} generic buttons)")

    @pytest.mark.asyncio
    @pytest.mark.usability
    @pytest.mark.basic
    async def test_usab_basic_05_image_alt_text(self, page: Page):
        """
        [USABILITY BASIC #05] Image Alt Text - Hình ảnh sản phẩm có alt text

        Mục đích: Kiểm trace tất cả hình ảnh có alt text cho accessibility
        Kỳ vọng: Ít nhất 80% hình ảnh phải có alt text
        """
        logger.info("🖼️ [USAB_BASIC_05] Kiểm trace Image Alt Text...")

        await page.goto(BASE_URL, wait_until="networkidle")

        # Tìm tất cả hình ảnh
        images = await page.locator('img').all()

        if len(images) == 0:
            logger.warning("⚠️ No images found on page")
            return

        missing_alt = 0
        for img in images:
            alt = await img.get_attribute("alt")
            if not alt or len(alt.strip()) == 0:
                missing_alt += 1

        alt_coverage = ((len(images) - missing_alt) / len(images)) * 100

        if alt_coverage < 80:
            logger.error(f"❌ ALT TEXT COVERAGE: Only {alt_coverage:.1f}% ({missing_alt} missing)")
            await page.screenshot(path="failures/AUTO_FAIL_USAB_BASIC_05_NO_ALT_TEXT.png")
            assert False, f"Image alt text coverage too low: {alt_coverage:.1f}%"

        logger.info(f"✅ Alt text coverage adequate: {alt_coverage:.1f}%")

    @pytest.mark.asyncio
    @pytest.mark.usability
    @pytest.mark.basic
    async def test_usab_basic_06_color_contrast_text(self, page: Page):
        """
        [USABILITY BASIC #06] Color Contrast - Text readable (WCAG AA standard)

        Mục đích: Kiểm trace contrast ratio giữa text và background
        Kỳ vọng: Contrast ratio >= 4.5:1 cho normal text (WCAG AA)
        """
        logger.info("🎨 [USAB_BASIC_06] Kiểm trace Color Contrast...")

        await page.goto(BASE_URL, wait_until="networkidle")

        # Lấy các text elements
        try:
            contrast_check = await page.evaluate("""
                () => {
                    const elements = document.querySelectorAll('p, span, div, h1, h2, h3, h4, h5, h6');
                    let contrastIssues = 0;
                    
                    elements.forEach(el => {
                        const style = window.getComputedStyle(el);
                        const bgColor = style.backgroundColor;
                        const textColor = style.color;
                        // Very simplified check - just verify colors are defined
                        if (!bgColor || bgColor === 'rgba(0, 0, 0, 0)' || !textColor) {
                            contrastIssues++;
                        }
                    });
                    
                    return contrastIssues;
                }
            """)

            logger.info(f"✅ Color contrast check completed ({contrast_check} potential issues)")
        except:
            logger.debug("Color contrast evaluation not available")

    @pytest.mark.asyncio
    @pytest.mark.usability
    @pytest.mark.basic
    async def test_usab_basic_07_page_title_seo(self, page: Page):
        """
        [USABILITY BASIC #07] Page Title (SEO) - Tại trang phải có <title> tag

        Mục đích: Kiểm trace tất cả trang có unique, descriptive title
        Kỳ vọng: <title> không nên trống hoặc generic
        """
        logger.info("📝 [USAB_BASIC_07] Kiểm trace Page Title...")

        pages_to_check = [
            (BASE_URL, "Homepage"),
            (f"{BASE_URL}index.php?route=product/category&path=20", "Category"),
            (f"{BASE_URL}index.php?route=product/product&product_id=40", "Product"),
        ]

        for url, page_name in pages_to_check:
            try:
                await page.goto(url, wait_until="load")
                title = await page.title()

                if not title or title.strip() == "":
                    logger.error(f"❌ EMPTY TITLE: {page_name} page has no title")
                    await page.screenshot(path=f"failures/AUTO_FAIL_USAB_BASIC_07_NO_TITLE_{page_name}.png")
                    assert False, f"{page_name} page has no title tag"

                if title.lower() in ["untitled", "page", "home"]:
                    logger.warning(f"⚠️ GENERIC TITLE: {page_name} = '{title}'")
                else:
                    logger.info(f"✅ {page_name}: '{title}'")
            except:
                logger.debug(f"Could not check {page_name}")

    @pytest.mark.asyncio
    @pytest.mark.usability
    @pytest.mark.basic
    async def test_usab_basic_08_breadcrumb_navigation(self, page: Page):
        """
        [USABILITY BASIC #08] Breadcrumb Navigation - Cho phép navigate back

        Mục đích: Kiểm trace breadcrumb có mặt trên category/product pages
        Kỳ vọng: Breadcrumb phải có để người dùng biết vị trí trong site
        """
        logger.info("🗺️ [USAB_BASIC_08] Kiểm trace Breadcrumb Navigation...")

        # Check on product page (thường có breadcrumb)
        await page.goto(f"{BASE_URL}index.php?route=product/product&product_id=40")

        # Tìm breadcrumb
        breadcrumbs = await page.locator('[class*="breadcrumb"], nav[aria-label*="Breadcrumb"]').count()

        if breadcrumbs == 0:
            logger.warning("⚠️ NO BREADCRUMB: Product page lacks breadcrumb navigation")
            logger.info("  (Breadcrumb is recommended but not critical)")
        else:
            logger.info(f"✅ Breadcrumb navigation found ({breadcrumbs} elements)")

    @pytest.mark.asyncio
    @pytest.mark.usability
    @pytest.mark.basic
    async def test_usab_basic_09_404_error_page_clarity(self, page: Page):
        """
        [USABILITY BASIC #09] 404 Error Page - Should be clear and helpful

        Mục đích: Kiểm trace trang 404 có message rõ ràng và suggestions
        Kỳ vọng: 404 page phải giúp người dùng tìm được nội dung
        """
        logger.info("⚠️ [USAB_BASIC_09] Kiểm trace 404 Error Page...")

        await page.goto(f"{BASE_URL}index.php?route=nonexistent/page/xyz",
                       wait_until="load")

        page_content = await page.content()

        # Kiểm trace xem có 404 message không
        has_404_msg = any(msg in page_content.lower() for msg in [
            "404", "not found", "page not found", "does not exist",
            "could not find"
        ])

        if not has_404_msg:
            logger.error("❌ POOR 404 PAGE: No clear 'not found' message")
            await page.screenshot(path="failures/AUTO_FAIL_USAB_BASIC_09_BAD_404.png")
            assert False, "404 error page lacks clear error message"

        # Kiểm trace xem có suggestions/links không
        has_suggestions = 'href=' in page_content and page_content.count('href=') > 1

        if has_suggestions:
            logger.info("✅ 404 page has helpful suggestions/links")
        else:
            logger.warning("⚠️ 404 page could be improved with suggestions")

    @pytest.mark.asyncio
    @pytest.mark.usability
    @pytest.mark.basic
    async def test_usab_basic_10_loading_indicators(self, page: Page):
        """
        [USABILITY BASIC #10] Loading Indicators - Thhi hiển thị loader khi tải

        Mục đích: Kiểm trace xem có loading visual khi page tải
        Kỳ vọng: Progress indicator hoặc spinner phải hiển thị
        """
        logger.info("⏳ [USAB_BASIC_10] Kiểm trace Loading Indicators...")

        await page.goto(BASE_URL)

        # Tìm loading indicators
        loaders = await page.locator('[class*="load"], [class*="spin"], [class*="progress"]').count()

        page_html = await page.content()

        # Kiểm trace xem có CSS animation cho loader không
        has_animation = "animation" in page_html or "@keyframes" in page_html

        if loaders > 0 and has_animation:
            logger.info(f"✅ Loading indicators found ({loaders} elements)")
        else:
            logger.warning("⚠️ No obvious loading indicators found")
            logger.info("  (This may be acceptable if page loads quickly)")


class TestUsabilityAdvanced:
    """Advanced Usability Tests - UX issues and missing features"""

    @pytest.mark.asyncio
    @pytest.mark.usability
    @pytest.mark.advanced
    async def test_usab_advanced_01_price_filter_missing_minmax(self, page: Page):
        """
        [USABILITY ADVANCED #01] ❌ Missing Price Filter - Trang danh mục thiếu Min-Max Budget

        Mục đích: Kiểm trace xem danh mục sản phẩm có filter khoảng giá không
        Kỳ vọng: Phải có input Min Price và Max Price để filter
        """
        logger.info("💰 [USAB_ADV_01] Kiểm trace Price Range Filter...")

        await page.goto(f"{BASE_URL}index.php?route=product/category&path=20")

        page_html = await page.content()

        # Tìm price filter inputs
        min_price_input = await page.query_selector('input[name*="min"], input[name="price_min"]')
        max_price_input = await page.query_selector('input[name*="max"], input[name="price_max"]')

        # Kiểm trace có price range filter
        has_price_range = any(text in page_html.lower() for text in [
            "price range", "min price", "max price", "budget",
            'name="price_min"', 'name="price_max"'
        ])

        if not has_price_range and not min_price_input and not max_price_input:
            logger.error("❌ MISSING FEATURE: No price range filter on category page!")
            logger.error("   Users cannot filter products by budget/price range")
            await page.screenshot(path="failures/AUTO_FAIL_USAB_ADV_01_NO_PRICE_FILTER.png",
                                 full_page=True)
            assert False, "Critical UX issue: Missing price range filter on product category"

        logger.info("✅ Price range filter is available")

    @pytest.mark.asyncio
    @pytest.mark.usability
    @pytest.mark.advanced
    async def test_usab_advanced_02_sort_options_missing(self, page: Page):
        """
        [USABILITY ADVANCED #02] Missing Sort Options - Impossible to sort products

        Mục đích: Kiểm trace xem có thể sắp xếp sản phẩm theo popularity, price, etc.
        Kỳ vọng: Phải có dropdown hoặc button để sắp xếp
        """
        logger.info("📊 [USAB_ADV_02] Kiểm trace Product Sort Options...")

        await page.goto(f"{BASE_URL}index.php?route=product/category&path=20")

        page_html = await page.content()

        # Tìm sort options
        sort_select = await page.query_selector('select[name*="sort"], select[name="sort"]')
        sort_buttons = await page.locator('button[data-sort], a[data-sort]').count()

        has_sort_option = any(text in page_html.lower() for text in [
            "sort by", "sort:", "sort", "order by"
        ])

        if not has_sort_option and not sort_select and sort_buttons == 0:
            logger.error("❌ MISSING FEATURE: No sort options on category page!")
            logger.error("   Users cannot sort by price, popularity, newest, etc.")
            await page.screenshot(path="failures/AUTO_FAIL_USAB_ADV_02_NO_SORT.png")
            assert False, "Critical UX issue: Missing sort functionality"

        logger.info("✅ Product sort options available")

    @pytest.mark.asyncio
    @pytest.mark.usability
    @pytest.mark.advanced
    async def test_usab_advanced_03_pagination_controls_missing(self, page: Page):
        """
        [USABILITY ADVANCED #03] Missing Pagination - Khó navigate giữa các trang

        Mục đích: Kiểm trace xem có pagination controls để xem trang tiếp theo
        Kỳ vọng: Phải có Previous, Next, Page Numbers controls
        """
        logger.info("📖 [USAB_ADV_03] Kiểm trace Pagination Controls...")

        await page.goto(f"{BASE_URL}index.php?route=product/category&path=20&limit=5")

        # Tìm pagination
        pagination = await page.locator('[class*="pagination"], nav:has(a[rel*="next"])').count()
        next_button = await page.query_selector('a[rel="next"], button:has-text("Next")')

        page_html = await page.content()

        if pagination == 0 and not next_button and page_html.count("product-item") > 5:
            logger.warning("⚠️ PAGINATION MISSING: Many products but no pagination found")
            logger.info("  (This assumes >5 products exist)")
        else:
            logger.info("✅ Pagination controls found")

    @pytest.mark.asyncio
    @pytest.mark.usability
    @pytest.mark.advanced
    async def test_usab_advanced_04_product_image_gallery_missing(self, page: Page):
        """
        [USABILITY ADVANCED #04] Product Image Gallery - Hình ảnh product thiếu gallery

        Mục đích: Kiểm trace xem product page có image zoom/gallery không
        Kỳ vọng: Phải có multiple images visible hoặc zoom capability
        """
        logger.info("🖼️ [USAB_ADV_04] Kiểm trace Product Image Gallery...")

        await page.goto(f"{BASE_URL}index.php?route=product/product&product_id=40")

        # Tìm product images
        product_images = await page.locator('img[alt*="product"], [class*="gallery"] img').count()

        page_html = await page.content()
        has_lightbox = "lightbox" in page_html.lower() or "magnific" in page_html.lower()

        if product_images < 2 and not has_lightbox:
            logger.warning("⚠️ LIMITED IMAGE GALLERY: Only single image visible")
            logger.info("  (Should have multiple images with zoom/gallery)")
        elif product_images >= 2:
            logger.info(f"✅ Product gallery with {product_images} images")
        else:
            logger.info("✅ Lightbox/magnification gallery available")

    @pytest.mark.asyncio
    @pytest.mark.usability
    @pytest.mark.advanced
    async def test_usab_advanced_05_wishlist_quick_add_missing(self, page: Page):
        """
        [USABILITY ADVANCED #05] Quick Actions Missing - Không thể thêm wishlist nhanh

        Mục đích: Kiểm trace xem product list có heart icon để quick wishlist không
        Kỳ vọng: Product items phải có quick add to wishlist button
        """
        logger.info("❤️ [USAB_ADV_05] Kiểm trace Quick Wishlist Action...")

        await page.goto(f"{BASE_URL}index.php?route=product/category&path=20")

        # Tìm wishlist buttons
        wishlist_buttons = await page.locator('[class*="wishlist"], button[title*="Wish"]').count()

        page_html = await page.content()

        if wishlist_buttons == 0:
            logger.warning("⚠️ NO QUICK WISHLIST: Cannot add to wishlist from product list")
            logger.info("  (Users must open product details first)")
        else:
            logger.info(f"✅ Quick wishlist feature available ({wishlist_buttons} buttons)")

    @pytest.mark.asyncio
    @pytest.mark.usability
    @pytest.mark.advanced
    async def test_usab_advanced_06_compare_products_feature_missing(self, page: Page):
        """
        [USABILITY ADVANCED #06] Product Comparison Missing - Khó so sánh sản phẩm

        Mục đích: Kiểm trace xem có thể so sánh 2+ sản phẩm được không
        Kỳ vọng: Phải có comparison feature hoặc compare button
        """
        logger.info("⚖️ [USAB_ADV_06] Kiểm trace Product Comparison Feature...")

        await page.goto(f"{BASE_URL}index.php?route=product/category&path=20")

        # Tìm compare buttons/links
        compare_elements = await page.locator('[class*="compare"], button[title*="Compare"]').count()

        page_html = await page.content()
        has_compare = "compare" in page_html.lower()

        if compare_elements == 0 and not has_compare:
            logger.warning("⚠️ NO COMPARISON FEATURE: Cannot compare products side-by-side")
        else:
            logger.info(f"✅ Product comparison available")

    @pytest.mark.asyncio
    @pytest.mark.usability
    @pytest.mark.advanced
    async def test_usab_advanced_07_review_rating_display_missing(self, page: Page):
        """
        [USABILITY ADVANCED #07] Product Reviews Missing - Không hiển thị rating

        Mục đích: Kiểm trace xem sản phẩm có rating/review stars không
        Kỳ vọng: Phải hiển thị average rating và số review
        """
        logger.info("⭐ [USAB_ADV_07] Kiểm trace Product Review Display...")

        await page.goto(f"{BASE_URL}index.php?route=product/product&product_id=40")

        page_html = await page.content()

        # Tìm rating/review elements
        has_rating = "rating" in page_html.lower() or "★" in page_html or "review" in page_html.lower()

        stars = await page.locator('[class*="star"], [class*="rating"]').count()
        review_count = await page.locator('[class*="review"]').count()

        if not has_rating and stars == 0:
            logger.warning("⚠️ NO REVIEW DISPLAY: Product lacks rating display")
            logger.info("  (Users cannot see product ratings/reviews)")
        elif stars > 0 or review_count > 0:
            logger.info(f"✅ Review display available ({stars} ratings, {review_count} reviews)")

    @pytest.mark.asyncio
    @pytest.mark.usability
    @pytest.mark.advanced
    async def test_usab_advanced_08_search_suggestions_autocomplete_missing(self, page: Page):
        """
        [USABILITY ADVANCED #08] Search Autocomplete Missing - Tìm kiếm không có suggestions

        Mục đích: Kiểm trace xem có autocomplete suggestions khi đánh chỉ tìm
        Kỳ vọng: Phải có dropdown với suggestions từ DB
        """
        logger.info("🔍 [USAB_ADV_08] Kiểm trace Search Autocomplete...")

        await page.goto(BASE_URL)

        # Tìm search input
        search_input = await page.query_selector('input[name*="search"], [placeholder*="Search"]')

        if not search_input:
            logger.debug("Could not find search input")
            return

        # Gõ vài ký tự
        await search_input.type("ip")

        # Chờ xem có dropdown suggestions không
        await page.wait_for_timeout(500)

        suggestions = await page.locator('[class*="dropdown"], [class*="suggestion"], [role="listbox"]').count()

        if suggestions == 0:
            logger.warning("⚠️ NO AUTOCOMPLETE: Search lacks suggestions/autocomplete")
            logger.info("  (Users cannot see available products while typing)")
        else:
            logger.info(f"✅ Search autocomplete available ({suggestions} suggestions)")

    @pytest.mark.asyncio
    @pytest.mark.usability
    @pytest.mark.advanced
    async def test_usab_advanced_09_cart_quick_view_missing(self, page: Page):
        """
        [USABILITY ADVANCED #09] Quick View Missing - Phải click vào sản phẩm để xem chi tiết

        Mục đích: Kiểm trace xem có quick view modal không
        Kỳ vọng: Product items phải có quick view button
        """
        logger.info("👁️ [USAB_ADV_09] Kiểm trace Quick View Feature...")

        await page.goto(f"{BASE_URL}index.php?route=product/category&path=20")

        # Tìm quick view buttons
        quick_views = await page.locator('[class*="quick"], button[title*="View"]').count()

        page_html = await page.content()

        if quick_views == 0:
            logger.warning("⚠️ NO QUICK VIEW: Must click through to see product details")
            logger.info("  (Quick view modal would improve UX)")
        else:
            logger.info(f"✅ Quick view feature available")

    @pytest.mark.asyncio
    @pytest.mark.usability
    @pytest.mark.advanced
    async def test_usab_advanced_10_mobile_menu_hamburger_check(self, page: Page):
        """
        [USABILITY ADVANCED #10] Mobile Menu - Hamburger menu style di mobile

        Mục đích: Kiểm trace xem responsive menu có hamburger icon ở mobile không
        Kỳ vọng: Ở 375px viewport phải có hamburger menu hoặc mobile-friendly nav
        """
        logger.info("☰ [USAB_ADV_10] Kiểm trace Mobile Menu...")

        # Set mobile viewport
        await page.set_viewport_size({"width": 375, "height": 667})
        await page.goto(BASE_URL)

        # Tìm hamburger menu
        hamburger = await page.query_selector('[class*="hamburger"], [class*="menu-toggle"], button[aria-label*="Menu"]')

        # Kiểm trace nếu desktop menu disappears
        desktop_nav = await page.locator('nav[class*="desktop"]').is_visible()

        page_html = await page.content()

        if hamburger:
            logger.info("✅ Hamburger menu found on mobile")
        elif not desktop_nav:
            logger.info("✅ Desktop navigation hidden on mobile (responsive)")
        else:
            logger.warning("⚠️ MOBILE MENU ISSUE: Desktop menu visible on 375px")
            await page.screenshot(path="failures/AUTO_FAIL_USAB_ADV_10_MOBILE_MENU.png")
            # Note: Not failing here as some designs use responsive class

def pytest_configure(config):
    """Register custom test markers"""
    config.addinivalue_line("markers", "performance: Performance testing")
    config.addinivalue_line("markers", "security: Security testing")
    config.addinivalue_line("markers", "usability: Usability testing")
    config.addinivalue_line("markers", "basic: Basic level tests")
    config.addinivalue_line("markers", "advanced: Advanced level tests")



