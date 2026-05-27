# 10 Test Case Chắc Chắn Fail Cho OpenCart 4.1.0.3

Nguồn đối chiếu: project hiện tại và các file `danh_sach_200_testcase_chi_tiet_bang.md`, `danh_sach_tong_hop_200_testcase.md`, `ket_qua_testcase_khong_pass.md`.

Ghi chú: Các test case dưới đây đặt kỳ vọng theo hướng hệ thống phải validate/chặn/hỗ trợ một chức năng, nhưng source OpenCart 4.1.0.3 hiện tại không có logic tương ứng. Vì vậy khi chạy theo đúng expected result, các case này sẽ fail.

| Test Case ID | Use Case | Tên kịch bản kiểm thử | Bước thực hiện | Dữ liệu kiểm thử | Kết quả mong đợi | Lý do chắc chắn fail theo source | Mức độ ưu tiên |
|---|---|---|---|---|---|---|---|
| TC_FAIL_01 | UC_01: Đăng ký | Đăng ký phải kiểm tra Confirm Password không khớp | 1. Vào trang Register. 2. Nhập đầy đủ thông tin hợp lệ. 3. Nhập Password khác Confirm Password. 4. Tích Privacy Policy. 5. Continue. | Password: `123456`; Confirm Password: `654321` | Hiển thị lỗi `Password confirmation does not match password!`, không tạo tài khoản. | Form Register không có field confirm password; controller chỉ validate `password`, không validate `confirm`. | High |
| TC_FAIL_02 | UC_01: Đăng ký | Đăng ký phải từ chối số điện thoại chứa chữ cái | 1. Vào Register. 2. Nhập thông tin hợp lệ. 3. Nhập Telephone có chữ cái. 4. Continue. | Telephone: `090abc1234` | Hiển thị lỗi định dạng số điện thoại, không tạo tài khoản. | Controller Register chỉ validate độ dài telephone khi cấu hình required, không validate numeric/pattern. | Medium |
| TC_FAIL_03 | UC_05: Tìm kiếm | Tìm kiếm phải báo lỗi khi từ khóa chỉ có 1 ký tự | 1. Nhập từ khóa một ký tự vào ô Search. 2. Nhấn Search. | Keyword: `a` | Hiển thị cảnh báo từ khóa quá ngắn và không thực hiện tìm kiếm. | Search không có rule validate độ dài tối thiểu của keyword; request vẫn được xử lý theo logic search hiện có. | Low |
| TC_FAIL_04 | UC_06: Lọc sản phẩm | Danh mục phải lọc được sản phẩm theo khoảng giá min-max | 1. Mở một category có nhiều sản phẩm. 2. Nhập giá min và max. 3. Apply filter. | Min: `100`; Max: `200` | Chỉ hiển thị sản phẩm có giá từ 100 đến 200. | Storefront mặc định không có UI/input lọc khoảng giá min-max trong category/filter module. | Medium |
| TC_FAIL_05 | UC_08: Thêm vào giỏ | Add to Cart phải chặn số lượng bằng 0 | 1. Mở trang chi tiết sản phẩm đang bán. 2. Nhập quantity = 0. 3. Nhấn Add to Cart. | Product: iPhone; Quantity: `0` | Hiển thị lỗi quantity phải lớn hơn 0, không thêm sản phẩm vào giỏ. | `catalog/controller/checkout/cart.php` cast quantity sang `(int)` rồi gọi `$this->cart->add(...)`; không có validate `> 0` trước khi add. | High |
| TC_FAIL_06 | UC_08: Thêm vào giỏ | Add to Cart phải chặn số lượng âm | 1. Mở trang chi tiết sản phẩm đang bán. 2. Nhập quantity âm. 3. Nhấn Add to Cart. | Product: iPhone; Quantity: `-5` | Hiển thị lỗi quantity không hợp lệ, không thêm sản phẩm vào giỏ. | Quantity bị cast `(int)` và không có rule reject số âm tại action add cart. | High |
| TC_FAIL_07 | UC_10: Cập nhật giỏ hàng | Cập nhật giỏ phải báo lỗi khi quantity là chữ | 1. Thêm một sản phẩm vào giỏ. 2. Vào Cart. 3. Sửa quantity thành chuỗi chữ. 4. Update. | Quantity: `abc` | Hiển thị lỗi quantity chỉ được nhập số nguyên dương, giữ nguyên số lượng cũ. | Action edit cart cast quantity `(int)`; chuỗi không phải số thành `0`, không có warning validate riêng. | Medium |
| TC_FAIL_08 | UC_13: Thanh toán | Checkout phải bắt buộc đồng ý Terms & Conditions | 1. Thêm sản phẩm vào giỏ. 2. Vào Checkout. 3. Chọn shipping/payment hợp lệ. 4. Không tích Terms & Conditions. 5. Confirm order. | Terms: unchecked | Hiển thị lỗi bắt buộc đồng ý Terms & Conditions, không tạo đơn hàng. | Default SQL đặt `config_checkout_id = 0`; controller chỉ bắt Terms khi config này khác 0. | High |
| TC_FAIL_09 | UC_17: Quản lý sản phẩm Admin | Admin phải chặn lưu sản phẩm có giá âm | 1. Đăng nhập Admin. 2. Vào Catalog > Products. 3. Tạo/sửa sản phẩm. 4. Nhập Price âm. 5. Save. | Price: `-100` | Hiển thị lỗi giá không được âm, không lưu sản phẩm. | Admin product controller validate name/meta title/model/SEO/options, không validate `price >= 0`; model cast price sang float và lưu. | High |
| TC_FAIL_10 | UC_17: Quản lý sản phẩm Admin | Admin phải chặn xóa sản phẩm đã từng phát sinh đơn hàng | 1. Đăng nhập Admin. 2. Chọn sản phẩm đã có trong order. 3. Nhấn Delete. 4. Confirm. | Product đã tồn tại trong `order_product` | Hiển thị lỗi không thể xóa sản phẩm đã có đơn hàng, sản phẩm vẫn còn trong catalog. | Model xóa product và các bảng liên quan trực tiếp; không kiểm tra quan hệ `order_product` trước khi delete. | High |

## Bằng chứng source chính

- `upload/catalog/view/template/account/register.twig`: form Register chỉ có `password`, không có `confirm password`.
- `upload/catalog/controller/account/register.php`: validate firstname, lastname, email, password, agree; telephone chỉ kiểm tra độ dài khi required.
- `upload/catalog/controller/checkout/cart.php`: action add/edit cast `quantity` sang `(int)` và không validate số nguyên dương.
- `upload/install/opencart-en-gb.sql`: `config_checkout_id = 0`, nên Terms & Conditions checkout không bật mặc định.
- `upload/admin/controller/catalog/product.php`: save product không validate giá âm.
- `upload/admin/model/catalog/product.php`: delete product không kiểm tra sản phẩm đã nằm trong đơn hàng.
