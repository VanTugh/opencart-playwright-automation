1. # Đăng ký tài khoản  

# 

| Mã Use case | UC\_01 | Tên UC | Đăng ký tài khoản |
| :---: | ----- | :---- | :---- |
| **Tác nhân** | Người dùng |  |  |
| **Mô tả** | Use case này cho phép Người dùng tạo tài khoản mới để mua sắm. |  |  |
| **Luồng sự kiện chính** |  **STT** **Thực hiện bởi** **Hành động ** 1 Người dùng Kích vào liên kết "Register" trên trang chủ Storefront. 2 Hệ thống Hiển thị form đăng ký (Firstname, Lastname, Email, Telephone, Password). 3 Người dùng Nhập đầy đủ thông tin vào các trường yêu cầu. 4 Người dùng Tích chọn đồng ý với điều khoản dịch vụ (Privacy Policy). 5 Người dùng Nhấn nút "Continue". 6 Hệ thống Kiểm tra tính hợp lệ của dữ liệu và kiểm tra Email đã tồn tại trong bảng Customer 7 Hệ thống Lưu thông tin vào bảng Customer, gửi email xác nhận. 8 Hệ thống Hiển thị thông báo "Account Created" và tự động đăng nhập.  |  |  |
| **Luồng sự kiện thay thế** |  **STT Thực hiện bởi Hành động** 6b Hệ thống Nếu Email đã tồn tại hoặc dữ liệu thiếu \-\> Hiển thị cảnh báo màu đỏ tại trường tương ứng.  |  |  |
| **Các điều kiện đặc biệt** | Không có |  |  |
| **Tiền điều kiện** | Người dùng chưa đăng nhập. |  |  |
| **Hậu điều kiện** | Tài khoản mới được lưu thành công vào cơ sở dữ liệu. |  |  |
| **Điểm mở rộng** | Không có |  |  |

# 

2. # Đăng nhập  

# 

| Mã Use case | UC\_02 | Tên UC | Đăng nhập |
| :---: | ----- | :---- | :---- |
| **Tác nhân** | Người dùng |  |  |
| **Mô tả** | Use case này cho phép xác thực danh tính người dùng để truy cập các tính năng cá nhân. |  |  |
| **Luồng sự kiện chính** |  **STT** **Thực hiện bởi** **Hành động ** 1 Người dùng Kích vào "Login" trên menu tài khoản. 2 Hệ thống Hiển thị trang đăng nhập yêu cầu Email và Password. 3 Người dùng Nhập thông tin tài khoản và nhấn "Login". 4 Hệ thống Truy vấn bảng Customer để xác thực thông tin. 5 Hệ thống Khởi tạo Session làm việc và chuyển hướng về trang "My Account"  |  |  |
| **Luồng sự kiện thay thế** |  **STT Thực hiện bởi Hành động** 4b Hệ thống Nếu sai thông tin \-\> Hiển thị thông báo "Warning: No match for E-Mail Address and/or Password."  |  |  |
| **Các điều kiện đặc biệt** | Không có |  |  |
| **Tiền điều kiện** | Người dùng đã có tài khoản. |  |  |
| **Hậu điều kiện** | Người dùng đăng nhập thành công vào hệ thống. |  |  |
| **Điểm mở rộng** | Không có |  |  |

# 

3. # Đăng xuất  

# 

| Mã Use case | UC\_03 | Tên UC | Đăng xuất |
| :---: | ----- | :---- | :---- |
| **Tác nhân** | Người dùng |  |  |
| **Mô tả** | Use case này cho phép người dùng đăng xuất khỏi hệ thống và kết thúc phiên làm việc hiện tại. |  |  |
| **Luồng sự kiện chính** |  **STT** **Thực hiện bởi** **Hành động ** 1 Người dùng  Kích vào nút **Log out** trên giao diện hệ thống. 2 Hệ thống Nhận yêu cầu đăng xuất từ người dùng. 3 Hệ thống  Xóa session đăng nhập của người dùng. 4 Hệ thống Xóa thông tin đăng nhập đã lưu (nếu có “Remember me”). 5 Hệ thống Chuyển hướng người dùng về trang chủ. 6 Hệ thống Hiển thị giao diện dành cho người chưa đăng nhập.  |  |  |
| **Luồng sự kiện thay thế** |  **STT Thực hiện bởi Hành động** 2b Hệ thống Nếu không nhận được yêu cầu hợp lệ → không thực hiện đăng xuất 3b Hệ thống Nếu không tìm thấy session → vẫn tiếp tục chuyển về trang chủ. 4b Hệ thống Nếu không có dữ liệu “Remember me” → bỏ qua bước này. 5b Hệ thống  Nếu lỗi khi chuyển trang → hiển thị “Không thể chuyển trang”. 6b Hệ thống Nếu xảy ra lỗi hệ thống → hiển thị “Hệ thống gặp sự cố, vui lòng thử lại sau”.  |  |  |
| **Các điều kiện đặc biệt** | Không có |  |  |
| **Tiền điều kiện** | Người dùng đã đăng nhập vào hệ thống |  |  |
| **Hậu điều kiện** | \-Session đăng nhập của người dùng bị xóa \-Người dùng không còn quyền truy cập các chức năng yêu cầu đăng nhập \-Hệ thống hiển thị trạng thái chưa đăng nhập |  |  |
| **Điểm mở rộng** | Không có |  |  |

# 

4. # Xem danh sách sản phẩm  

# 

| Mã Use case | UC\_04 | Tên UC | Xem danh sách sản phẩm |
| :---: | ----- | :---- | :---- |
| **Tác nhân** | Người dùng |  |  |
| **Mô tả** | Use case này cho phép người dùng xem danh sách các sản phẩm trong hệ thống. |  |  |
| **Luồng sự kiện chính** |  **STT** **Thực hiện bởi** **Hành động ** 1 Người dùng  Truy cập vào trang sản phẩm trên hệ thống. 2 Hệ thống Lấy danh sách sản phẩm từ bảng PRODUCT gồm: product\_id, tên sản phẩm, giá, số lượng tồn kho, category\_id,mô tả. 3 Hệ thống Kết hợp với bảng CATEGORY để lấy tên danh mục của sản phẩm. 4 Hệ thống Lấy hình ảnh đại diện của sản phẩm từ bảng PRODUCTIMAGE theo product\_id. 5 Hệ thống Hiển thị danh sách sản phẩm lên màn hình gồm: product\_id, tên sản phẩm, giá, hình ảnh, danh mục, tóm tắt, mô tả. 6 Người dùng Chọn một sản phẩm theo product\_id. 7a Hệ thống Chuyển sang màn hình xem chi tiết sản phẩm.  |  |  |
| **Luồng sự kiện thay thế** |  STT Thực hiện bởi Hành động 7b Hệ thống Nếu không tìm thấy sản phẩm theo product\_id, hiển thị thông báo “Sản phẩm không tồn tại”. 8b Hệ thống Nếu danh sách sản phẩm trống, hiển thị thông báo “Không có sản phẩm”. 9b Hệ thống Nếu sản phẩm không có hình ảnh trong bảng PRODUCTIMAGE, hiển thị ảnh mặc định. 10b Hệ thống Nếu xảy ra lỗi truy vấn dữ liệu hoặc lỗi hệ thống, hiển thị thông báo “Hệ thống gặp sự cố, vui lòng thử lại sau”.  |  |  |
| **Các điều kiện đặc biệt** | Không có |  |  |
| **Tiền điều kiện** | Người dùng truy cập được vào hệ thống |  |  |
| **Hậu điều kiện** | Danh sách sản phẩm được hiển thị đúng, người dùng có thể chọn xem chi tiết sản phẩm |  |  |
| **Điểm mở rộng** | Phân trang danh sách sản phẩm |  |  |

# 

5. # Tìm kiếm sản phẩm  

# 

| Mã Use case | UC\_05 | Tên UC | Tìm kiếm sản phẩm |
| :---: | ----- | :---- | :---- |
| **Tác nhân** | Người dùng |  |  |
| **Mô tả** | Use case này cho phép  tìm kiếm các sản phẩm trong hệ thống dựa trên tên sản phẩm. |  |  |
| **Luồng sự kiện chính** |  **STT** **Thực hiện bởi** **Hành động ** 1 Người dùng  Nhập từ khóa tìm kiếm vào ô tìm kiếm sản phẩm 2 Người dùng Nhấn nút Tìm kiếm 3 Hệ thống Nhận từ khóa từ người dùng 4 Hệ thống Truy vấn bảng PRODUCT theo tên sản phẩm 5 Hệ thống Tổng hợp danh sách sản phẩm thỏa mãn điều kiện 6 Hệ thống Hiển thị danh sách kết quả gồm: product\_id, tên, giá, danh mục, hình ảnh, mô tả 7 Người dùng Chọn một sản phẩm theo product\_id để xem chi tiết 8 Hệ thống Chuyển đến trang chi tiết sản phẩm  |  |  |
| **Luồng sự kiện thay thế** |  STT Thực hiện bởi Hành động 4b Hệ thống Nếu không tìm thấy sản phẩm phù hợp, hệ thống hiển thị thông báo “Không tìm thấy sản phẩm phù hợp”. 8b Hệ thống Nếu xảy ra lỗi truy vấn dữ liệu hoặc lỗi hệ thống, hệ thống hiển thị thông báo “Hệ thống gặp sự cố, vui lòng thử lại sau”.  |  |  |
| **Các điều kiện đặc biệt** | Không có |  |  |
| **Tiền điều kiện** | Người dùng đã truy cập vào hệ thống, hệ thống có dữ liệu của sản phẩm  |  |  |
| **Hậu điều kiện** | Danh sách sản phẩm phù hợp được hiển thị đúng theo điều kiện tìm kiếm và lọc, người dùng có thể tiếp tục xem chi tiết sản phẩm  |  |  |
| **Điểm mở rộng** | Tìm kiếm theo nhiều tiêu chí cùng lúc, sắp xếp theo giá, độ phổ biến, gợi ý từ khóa tìm kiếm  |  |  |

# 

6. # Lọc sản phẩm  

# 

| Mã Use case | UC\_06 | Tên UC | Lọc sản phẩm |
| :---: | ----- | :---- | :---- |
| **Tác nhân** | User |  |  |
| **Mô tả** | Use case này cho phép lọc sản phẩm trong hệ thống dựa trên các tiêu chí khác nhau. |  |  |
| **Luồng sự kiện chính** |  **STT** **Thực hiện bởi** **Hành động ** 1 Người dùng Chọn các tiêu chí lọc (danh mục, giá, thuộc tính nếu có) 2 Người dùng Nhấn nút Tìm kiếm 3 Hệ thống Nhận các tiêu chí lọc từ người dùng 4 Hệ thống Truy vấn bảng PRODUCT theo tên sản phẩm 5 Hệ thống Kết hợp với bảng CATEGORY để lọc theo danh mục 6 Hệ thống Lọc theo khoảng giá (price) trong bảng PRODUCT 7 Hệ thống Lọc theo thuộc tính trong bảng PRODUCTATTRIBUTE theo product\_id 8 Hệ thống Tổng hợp danh sách sản phẩm thỏa mãn điều kiện 9 Hệ thống Hiển thị danh sách kết quả gồm: product\_id, tên, giá, danh mục, hình ảnh, mô tả  |  |  |
| **Luồng sự kiện thay thế** |  STT Thực hiện bởi Hành động 4b Hệ thống Nếu không tìm thấy sản phẩm phù hợp, hệ thống hiển thị thông báo “Không tìm thấy sản phẩm phù hợp”. 5b Hệ thống  Nếu danh mục được chọn không tồn tại, hệ thống hiển thị thông báo “Danh mục không tồn tại”. 6b Hệ thống Nếu người dùng nhập khoảng giá không hợp lệ, hệ thống hiển thị thông báo “Khoảng giá không hợp lệ” và yêu cầu nhập lại. 7b Hệ thống Nếu sản phẩm không có dữ liệu thuộc tính trong bảng PRODUCTATTRIBUTE, hệ thống bỏ qua điều kiện lọc thuộc tính và tiếp tục tìm kiếm theo các điều kiện khác. 9b Hệ thống Nếu xảy ra lỗi truy vấn dữ liệu hoặc lỗi hệ thống, hệ thống hiển thị thông báo “Hệ thống gặp sự cố, vui lòng thử lại sau”.  |  |  |
| **Các điều kiện đặc biệt** | Không có |  |  |
| **Tiền điều kiện** | Người dùng đã truy cập vào hệ thống, hệ thống có dữ liệu của sản phẩm  |  |  |
| **Hậu điều kiện** | Danh sách sản phẩm phù hợp được hiển thị đúng theo điều kiện tìm kiếm và lọc, người dùng có thể tiếp tục xem chi tiết sản phẩm |  |  |
| **Điểm mở rộng** | Lọc theo nhiều tiêu chí cùng lúc, sắp xếp theo giá, độ phổ biến, gợi ý từ khóa tìm kiếm  |  |  |

# 

7. # Xem chi tiết sản phẩm  

# 

| Mã Use case | UC\_07 | Tên UC | Xem chi tiết sản phẩm |
| :---: | ----- | :---- | :---- |
| **Tác nhân** | Người dùng |  |  |
| **Mô tả** | Use case này cho phép Người dùng xem thông tin đầy đủ, đánh giá và tùy chọn của một sản phẩm cụ thể.. |  |  |
| **Luồng sự kiện chính** |  **STT** **Thực hiện bởi** **Hành động ** 1 User Kích ảnh hoặc tên sản phẩm trong trang danh sách sản phẩm (trên trang chủ hoặc danh mục) 2 Hệ thống Lấy thông tin chi tiết của sản phẩm bao gồm: product\_id, tên, giá, danh mục, hình ảnh, mô tả, lên màn hình.  |  |  |
| **Luồng sự kiện thay thế** |  **STT Thực hiện bởi Hành động** 1 Hệ thống Hiển thị thông báo lỗi do không kết nối được đến cơ sở dữ liệu  |  |  |
| **Các điều kiện đặc biệt** | Không có |  |  |
| **Tiền điều kiện** | Không có. |  |  |
| **Hậu điều kiện** | Không có |  |  |
| **Điểm mở rộng** | Không có |  |  |

# 

8. # Thêm sản phẩm vào giỏ hàng  

# 

| Mã Use case | UC\_08 | Tên UC | Thêm sản phẩm vào giỏ hàng |
| :---: | ----- | :---- | :---- |
| **Tác nhân** | Người dùng |  |  |
| **Mô tả** | Use case này cho phép lưu trữ tạm thời các sản phẩm người dùng muốn mua. |  |  |
| **Luồng sự kiện chính** |  **STT** **Thực hiện bởi** **Hành động ** 1 Người dùng Nhấn nút "Add to Cart" tại trang danh sách hoặc chi tiết SP. 2 Hệ thống Kiểm tra tùy chọn bắt buộc (nếu có) và số lượng tồn kho 3 Hệ thống Lưu product\_id và số lượng vào Session hoặc bảng cart. 4 Hệ thống Hiển thị thông báo "Success: You have added \[Product\] to your shopping cart\!".  |  |  |
| **Luồng sự kiện thay thế** |  **STT Thực hiện bởi Hành động** 2b Hệ thống Nếu số lượng hàng trong kho nhỏ hơn số lượng người dùng muốn mua thì thông báo ra màn hình : Số lượng không đủ  |  |  |
| **Các điều kiện đặc biệt** | Không có |  |  |
| **Tiền điều kiện** | Người dùng đã đăng nhập |  |  |
| **Hậu điều kiện** | Không có |  |  |
| **Điểm mở rộng** | Không có |  |  |

# 

9. # Xóa sản phẩm khỏi giỏ hàng  

# 

| Mã Use case | UC\_09 | Tên UC | Xóa sản phẩm ra khỏi giỏ hàng |
| :---: | ----- | :---- | :---- |
| **Tác nhân** | Người dùng |  |  |
| **Mô tả** | Use case này cho phép người dùng loại bỏ sản phẩm không muốn mua khỏi giỏ hàng. |  |  |
| **Luồng sự kiện chính** |  **STT** **Thực hiện bởi** **Hành động ** 1 Người dùng Kích vào biểu tượng giỏ hàng (Shopping Cart). 2 Hệ thống Nhấn biểu tượng "X" (Remove) tại dòng sản phẩm tương ứng. 3 Hệ thống Xóa bản ghi khỏi giỏ hàng và tính lại tổng tiền.  |  |  |
| **Luồng sự kiện thay thế** |  Không có |  |  |
| **Các điều kiện đặc biệt** | \- Thời gian cập nhật lại tổng tiền và biến mất của dòng sản phẩm phải \< 1 giây để đảm bảo trải nghiệm người dùng. \- Hoạt động ổn định trên các trình duyệt Chrome và Edge theo yêu cầu phi chức năng. |  |  |
| **Tiền điều kiện** | \- Người dùng đã truy cập vào hệ thống. \- Giỏ hàng hiện tại phải có ít nhất một sản phẩm |  |  |
| **Hậu điều kiện** | \- Sản phẩm tương ứng bị loại bỏ hoàn toàn khỏi bảng dữ liệu cart. \- Tổng giá trị đơn hàng (Sub-Total) và Thuế (Tax) được tính toán lại chính xác dựa trên danh sách sản phẩm còn lại. |  |  |
| **Điểm mở rộng** | \- Cập nhật Wishlist: Người dùng có thể chọn chuyển sản phẩm sang danh sách yêu thích thay vì xóa hoàn toàn. \- Gợi ý sản phẩm: Hệ thống hiển thị các sản phẩm liên quan sau khi giỏ hàng thay đổi để khuyến khích mua sắm tiếp. |  |  |

# 

10. # Cập nhật số lượng sản phẩm trong giỏ hàng 

# 

| Mã Use case | UC\_10 | Tên UC | Cập nhật giỏ hàng |
| :---: | ----- | :---- | :---- |
| **Tác nhân** | Người dùng |  |  |
| **Mô tả** | Use case này cho phép người dùng cập nhật lại số lượng sản phẩm có trong giỏ hàng |  |  |
| **Luồng sự kiện chính** |  **STT** **Thực hiện bởi** **Hành động ** 1 Người dùng  Thay đổi số lượng (Quantity) trong trang Shopping Cart. 2 Người dùng  Nhấn nút "Update" (biểu tượng mũi tên xoay). 3 Hệ thống Kiểm tra số lượng tồn kho của sản phẩm trong bảng Product 4 Hệ thống Cập nhật lại số lượng mới vào bảng Cart 5 Hệ thống Tính toán lại thành tiền (Total) của sản phẩm và tổng giá trị đơn hàng 6 Hệ thống Hiển thị thông báo: "Success: You have modified your shopping cart\!" và làm mới trang.  |  |  |
| **Luồng sự kiện thay thế** |  **STT Thực hiện bởi Hành động** 3b Hệ thống Số lượng nhập là 0 hoặc số âm: Hệ thống thực hiện xóa bản ghi sản phẩm đó khỏi bảng Cart (tương đương UC\_09).  3c Hệ thống Dữ liệu không hợp lệ (Ký tự chữ): Hiển thị thông báo "Dữ liệu không hợp lệ" và giữ nguyên số lượng cũ 3d Hệ thống Số lượng vượt quá tồn kho: Nếu sản phẩm được cấu hình "Stock Check", hệ thống hiển thị cảnh báo "Products marked with \*\*\* are not available in the desired quantity\!". 4b Hệ thống Lỗi cập nhật: Nếu xảy ra lỗi CSDL \-\> Hiển thị "Cập nhật thất bại, vui lòng thử lại sau".  |  |  |
| **Các điều kiện đặc biệt** | Hệ thống phải tự động tính lại các khoản thuế (Tax) và phí vận chuyển ước tính ngay sau khi cập nhật số lượng. Hoạt động mượt mà trên cả giao diện Desktop và Mobile (Responsive UI) |  |  |
| **Tiền điều kiện** | Người dùng đã truy cập vào trang Shopping Cart. Giỏ hàng phải chứa ít nhất một sản phẩm. |  |  |
| **Hậu điều kiện** | Thông tin về số lượng và tổng tiền được cập nhật chính xác trong cơ sở dữ liệu (Bảng Cart). Trạng thái giỏ hàng mới được hiển thị ngay lập tức cho người dùng. |  |  |
| **Điểm mở rộng** | Áp dụng khuyến mãi: Sau khi cập nhật số lượng, người dùng có thể áp dụng mã giảm giá (Coupon) để kiểm tra lại tổng tiền mới. Ước tính phí giao hàng: Cho phép người dùng nhập địa chỉ để tính toán phí vận chuyển dựa trên số lượng hàng mới cập nhật. |  |  |

# 

11. # Nhập thông tin giao hàng  

# 

| Mã Use case | UC\_11 | Tên UC | Nhập thông tin giao hàng |
| :---: | ----- | :---- | :---- |
| **Tác nhân** | Người dùng |  |  |
| **Mô tả** | Use case này cho phép người dùng nhập địa chỉ giao hàng trong quá trình thanh toán. Hệ thống xác thực thông tin và lưu địa chỉ vào session để sử dụng cho đơn hàng. |  |  |
| **Luồng sự kiện chính** |  **STT** **Thực hiện bởi** **Hành động ** 1 Người dùng Truy cập trang Checkout, hệ thống hiển thị bước nhập địa chỉ giao hàng 2 Hệ thống Tải danh sách địa chỉ đã lưu của khách hàng, danh sách quốc gia, tỉnh/thành phố và các trường tùy chỉnh tương ứng với nhóm khách hàng. Thêm địa chỉ mới 3 Người dùng Chọn "Thêm địa chỉ mới" và điền form: Họ, Tên, Địa chỉ 1, Thành phố, Quốc gia, Tỉnh/Thành, Mã bưu điện (nếu quốc gia yêu cầu). 4 Hệ thống Kiểm tra giỏ hàng còn sản phẩm hợp lệ, còn hàng trong kho, đạt giá trị đơn hàng tối thiểu. 5 Người dùng Nhấn nút "Tiếp tục" để gửi form. 6 Hệ thống Xác thực: Họ, Tên, Địa chỉ 1, Thành phố, Quốc gia tồn tại, Tỉnh/thành hợp lệ, Mã bưu điện (nếu quốc gia yêu cầu), các trường tùy chỉnh bắt buộc. 7 Hệ thống Xác thực thành công. Thêm địa chỉ mới vào CSDL 8 Hệ thống Giao diện chuyển sang bước chọn phương thức vận chuyển. Chọn địa chỉ đã lưu 9 Người dùng Chọn một địa chỉ đã có trong danh sách địa chỉ lưu sẵn. 10 Hệ thống Kiểm tra giỏ hàng, phiên đăng nhập, yêu cầu giao hàng. 11 Người dùng Xác nhận địa chỉ được chọn. 12 Hệ thống Lấy thông tin địa chỉ từ CSDL 13 Hệ thống Lưu địa chỉ vào CSDL, xóa phương thức vận chuyển và thanh toán cũ. 14 Hệ thống Hiển thị thông báo thành công  |  |  |
| **Luồng sự kiện thay thế** |  **STT Thực hiện bởi Hành động** 4b Hệ thống Giỏ hàng trống hoặc hết hàng hoặc không đạt đơn tối thiểu → chuyển hướng về Giỏ Hàng. 6b Hệ thống Xác thực thất bại (thiếu họ/tên, địa chỉ, thành phố, quốc gia không hợp lệ, thiếu mã bưu điện, thiếu tỉnh/thành bắt buộc) → hiển thị thông báo lỗi tương ứng trên form. 12b Hệ thống Khách hàng chưa đăng nhập → chuyển hướng về trang đăng nhập. 14b Hệ thống Địa chỉ không tồn tại hoặc không thuộc khách hàng → Thông báo Địa chỉ không hợp lệ.  |  |  |
| **Các điều kiện đặc biệt** | Không có |  |  |
| **Tiền điều kiện** | Khách hàng đã đăng nhập, giỏ hàng có ít nhất một sản phẩm cần giao hàng |  |  |
| **Hậu điều kiện** | Địa chỉ giao hàng được lưu vào CSDL. Phương thức vận chuyển và thanh toán cũ bị xóa để tính lại. |  |  |
| **Điểm mở rộng** | Không có |  |  |

# 

12. # Chọn phương thức vận chuyển  

# 

| Mã Use case | UC\_12 | Tên UC | Chọn phương thức vận chuyển   |
| :---: | ----- | :---- | :---- |
| **Tác nhân** | Người dùng |  |  |
| **Mô tả** | Use case này cho phép người dùng sau khi nhập địa chỉ giao hàng thì sẽ xem được danh sách phương thức vận chuyển khả dụng và chọn một phương thức. Hệ thống tính phí vận chuyển dựa trên địa chỉ và lưu lựa chọn. |  |  |
| **Luồng sự kiện chính** |  **STT** **Thực hiện bởi** **Hành động ** 1 Hệ thống Hệ thống hiển thị bước chọn phương thức vận chuyển 2 Hệ thống Kiểm tra xem khách đã chọn kiểu ship chưa. Nếu chọn rồi thì hiện lại lựa chọn cũ thay vì bắt chọn lại. Sau đó mở trang vận chuyển.  Tải danh sách vận chuyển	 3 Hệ thống Hệ thống tự động lấy danh sách phương thức vận chuyển 4 Hệ thống Xác thực: giỏ hàng hợp lệ, thông tin khách hàng, địa chỉ thanh toán (nếu hệ thống yêu cầu), địa chỉ giao hàng đã được chọn. 5 Hệ thống Lấy danh sách các phương thức vận chuyển khả dụng theo địa chỉ. 6 Hệ thống Hiển thị danh sách phương thức vận chuyển. Chọn phương thức 7 Người dùng Chọn một phương thức vận chuyển và nhấn "Tiếp tục". 8 Hệ thống Xác thực giỏ hàng, khách hàng, địa chỉ giao hàng, địa chỉ thanh toán (nếu cần). 9 Hệ thống Xác thực mã phương thức vận chuyển hợp lệ 10 Hệ thống Lưu phương thức đã chọn  |  |  |
| **Luồng sự kiện thay thế** |  **STT Thực hiện bởi Hành động** 4b Hệ thống Giỏ hàng không hợp lệ → chuyển hướng về Giỏ hàng. 4c Hệ thống Chưa có thông tin khách hàng trong session → Thông báo lỗi “Thông tin khách hàng chưa được thiết lập.” 5b Hệ thống Địa chỉ thanh toán chưa được thiết lập (nếu hệ thống yêu cầu) → Thông báo lỗi. 5c Hệ thống Địa chỉ giao hàng chưa được chọn → Thông báo lỗi. 6b Hệ thống Không tìm thấy phương thức vận chuyển nào phù hợp với địa chỉ → Thông báo lỗi. 9b Hệ thống Mã phương thức vận chuyển không hợp lệ hoặc không tồn tại trong danh sách → Thông báo lỗi.  |  |  |
| **Các điều kiện đặc biệt** | Không có |  |  |
| **Tiền điều kiện** | Khách hàng đã đăng nhập, giỏ hàng hợp lệ, địa chỉ giao hàng đã được lưu vào session |  |  |
| **Hậu điều kiện** | Phương thức vận chuyển được lưu vào session. Phương thức thanh toán cũ bị xóa để tính lại. |  |  |
| **Điểm mở rộng** | Không có |  |  |

# 

13. # Chọn phương thức thanh toán  

# 

| Mã Use case | UC\_13 | Tên UC | Chọn phương thức thanh toán |
| :---: | ----- | :---- | :---- |
| **Tác nhân** | Người dùng |  |  |
| **Mô tả** | Use case này cho phép người dùng chọn phương thức thanh toán cho đơn hàng. Hệ thống lấy danh sách phương thức thanh toán khả dụng dựa trên địa chỉ và cấu hình, lưu lựa chọn. Người dùng có thể thêm ghi chú và chấp nhận điều khoản. |  |  |
| **Luồng sự kiện chính** |  **STT** **Thực hiện bởi** **Hành động ** 1 Hệ thống Hiển thị bước chọn phương thức thanh toán 2 Hệ thống Kiểm tra payment\_method đã chọn trước đó Tải danh sách phương thức thanh toán 3 Hệ thống Tự động gọi API lấy danh sách phương thức thanh toán 4 Hệ thống Xác thực: giỏ hàng hợp lệ, thông tin khách hàng trong session, địa chỉ thanh toán (nếu bắt buộc), địa chỉ giao hàng và phương thức vận chuyển (nếu đơn hàng cần giao). 5 Hệ thống Xác định địa chỉ để tính phương thức thanh toán 6 Hệ thống Lấy danh sách Phương thức thanh toán và hiển thị Chọn phương thức 7 Người dùng Chọn phương thức thanh toán, tùy chọn điền ghi chú đơn hàng, tích vào ô đồng ý điều khoản, nhấn "Tiếp tục". 8 Hệ thống Xác thực giỏ hàng, địa chỉ thanh toán, phương thức vận chuyển (nếu cần). 9 Hệ thống Xác thực mã phương thức thanh toán hợp lệ 10 Hệ thống Lưu phương thức thanh toán vào session và thông báo thành công.  |  |  |
| **Luồng sự kiện thay thế** |  **STT Thực hiện bởi Hành động** 4b Hệ thống Giỏ hàng không hợp lệ → redirect về Giỏ hàng 4c Hệ thống Thông tin khách hàng không hợp lệ → thông báo lỗi. 5b Hệ thống Địa chỉ thanh toán chưa có → thông báo lỗi. 5c Hệ thống Địa chỉ giao hàng hoặc phương thức vận chuyển chưa được chọn → thông báo lỗi  6b Admin Không có phương thức thanh toán nào phù hợp → thông báo lỗi 9b Hệ thống Mã phương thức thanh toán không hợp lệ → thông báo lỗi  |  |  |
| **Các điều kiện đặc biệt** | Không có |  |  |
| **Tiền điều kiện** | Khách hàng đã chọn phương thức vận chuyển (nếu đơn hàng cần giao). Session có phương thức vận chuyển hợp lệ. |  |  |
| **Hậu điều kiện** | Khách hàng sẵn sàng chuyển sang bước xác nhận đơn hàng. |  |  |
| **Điểm mở rộng** | Không có |  |  |

# 

14. # Xác nhận đơn hàng  

| Mã Use case | UC\_14 | Tên UC | Xem lịch sử đơn hàng |
| :---: | ----- | :---- | :---- |
| **Tác nhân** | Người dùng |  |  |
| **Mô tả** | Use Case này cho phép khách hàng thực hiện bước kiểm tra cuối cùng và xác nhận đặt hàng để chuyển từ giỏ hàng tạm thời thành đơn hàng chính thức trong hệ thống. |  |  |
| **Luồng sự kiện chính** |  **STT** **Thực hiện bởi** **Hành động ** 1 Hệ thống Hệ thống hiển thị bảng tóm tắt đơn hàng bao gồm: Tên sản phẩm, Model, Số lượng, Đơn giá và Tổng tiền 2 Hệ thống Hệ thống hiển thị chi tiết các khoản phí: Tạm tính (Sub-Total), Phí vận chuyển (Flat Shipping Rate), Thuế (Eco Tax), và Tổng cộng (Total). 3 Người dùng  Kiểm tra thông tin và nhấn nút "Confirm Order". 4 Hệ thống Thực hiện các tác vụ ngầm: Tạo bản ghi mới trong bảng dữ liệu đơn hàng (oc\_order). Trừ số lượng sản phẩm tương ứng trong kho hàng (oc\_product). Xóa toàn bộ sản phẩm trong giỏ hàng hiện tại. Gửi email xác nhận đơn hàng tự động đến địa chỉ email của khách hàng 5 Hệ thống Hệ thống chuyển hướng người dùng đến trang thông báo đặt hàng thành công ("Your order has been placed\!").  |  |  |
| **Luồng sự kiện thay thế** |  **STT Thực hiện bởi Hành động** 3b Hệ thống Nếu trong lúc xác nhận, sản phẩm bị người khác mua hết, hệ thống báo lỗi và yêu cầu quay lại giỏ hàng. 5b Hệ thống ệ thống hiển thị thông báo lỗi kỹ thuật và giữ nguyên trạng thái đơn hàng để người dùng thử lại.  |  |  |
| **Các điều kiện đặc biệt** | Không có |  |  |
| **Tiền điều kiện** | Khách hàng đã hoàn thành bước 5 (Phương thức thanh toán) và đang ở giao diện bước 6 (Confirm Order) của quy trình Checkout. |  |  |
| **Hậu điều kiện** | Đơn hàng được tạo thành công trong CSDL. Số lượng tồn kho được cập nhật. Giỏ hàng được làm trống và email xác nhận được gửi cho người dùng. |  |  |
| **Điểm mở rộng** | Không có |  |  |

15. # Xem lịch sử đơn hàng  

# 

| Mã Use case | UC\_15 | Tên UC | Xem lịch sử đơn hàng |
| :---: | ----- | :---- | :---- |
| **Tác nhân** | Người dùng |  |  |
| **Mô tả** | Khách hàng xem danh sách tất cả đơn hàng đã đặt, kiểm tra trạng thái từng đơn và xem chi tiết đơn hàng bao gồm sản phẩm, địa chỉ, phương thức thanh toán/vận chuyển và lịch sử cập nhật trạng thái. |  |  |
| **Luồng sự kiện chính** |  **STT** **Thực hiện bởi** **Hành động ** 1 Khách hàng Truy cập trang "Đơn hàng của tôi" từ menu tài khoản 2 Hệ thống Kiểm tra trạng thái đăng nhập. Nếu chưa đăng nhập, chuyển đến trang đăng nhập. Danh sách đơn hàng 3 Hệ thống Truy vấn danh sách đơn hàng của khách hàng hiện tại 4 Hệ thống Với mỗi đơn hàng: tính tổng số sản phẩm, định dạng tổng tiền theo đơn vị tiền tệ. 5 Hệ thống Hiển thị danh sách đơn hàng dạng bảng: Mã đơn, Ngày đặt, Trạng thái, Số sản phẩm, Tổng tiền, Nút "Xem chi tiết". Hiển thị phân trang. 6 Khách hàng	 Nhấn "Xem chi tiết" trên một đơn hàng cụ thể. Chi tiết đơn hàng 7 Hệ thống Truy vấn thông tin đơn hàng, xác thực đơn hàng thuộc khách hàng hiện tại. 8 Hệ thống Hiển thị chi tiết đơn hàng 9 Khách hàng Xem thông tin xong, có thể nhấn "Quay lại" để trở về danh sách đơn hàng hoặc tiếp tục mua sắm.  |  |  |
| **Luồng sự kiện thay thế** |  **STT Thực hiện bởi Hành động** 2b Hệ thống Khách hàng chưa đăng nhập → chuyển đến trang đăng nhập. Sau đăng nhập sẽ tự chuyển về trang đơn hàng. 3b Hệ thống Khách hàng chưa có đơn hàng nào → hiển thị thông báo "Bạn chưa có đơn hàng nào."  |  |  |
| **Các điều kiện đặc biệt** | Không có |  |  |
| **Tiền điều kiện** | Khách hàng đã đăng nhập vào tài khoản. |  |  |
| **Hậu điều kiện** | Khách hàng xem được thông tin đơn hàng. Không có thay đổi dữ liệu. |  |  |
| **Điểm mở rộng** | Không có |  |  |

# 

16. # Cập nhật thông tin cá nhân  

# 

| Mã Use case | UC\_16 | Tên UC | Cập nhật thông tin cá nhân |
| :---: | ----- | :---- | :---- |
| **Tác nhân** | Người dùng |  |  |
| **Mô tả** | Use case này cho phép người dùng chỉnh sửa thông tin tài khoản cá nhân gồm họ, tên, email, số điện thoại và các trường tùy chỉnh. Hệ thống xác thực dữ liệu và cập nhật vào CSDL. |  |  |
| **Luồng sự kiện chính** |  **STT** **Thực hiện bởi** **Hành động ** 1 Người dùng Vào trang "Chỉnh sửa thông tin tài khoản" từ menu tài khoản 2 Hệ thống Xác thực đăng nhập. Nếu chưa đăng nhập, lưu redirect và chuyển đến trang đăng nhập. 3 Hệ thống Tải thông tin khách hàng hiện tại từ CSDL. Hiển thị form với dữ liệu hiện tại. 4 Người dùng Chỉnh sửa thông tin: Họ, Tên, Email, Số điện thoại (nếu được cấu hình hiển thị), các trường tùy chỉnh. 5 Người dùng Nhấn nút "Lưu thay đổi". 6 Hệ thống Xác thực đăng nhập lại. 7 Hệ thống Xác thực thành công. Cập nhật thông tin vào CSDL  |  |  |
| **Luồng sự kiện thay thế** |  **STT Thực hiện bởi Hành động** 2b Hệ thống Chưa đăng nhập → chuyển đến trang đăng nhập. 7b Hệ thống Họ hoặc Tên không đủ độ dài → thông báo lỗi 7c Hệ thống Email không hợp lệ → thông báo lỗi 7d Hệ thống Email đã tồn tại trong hệ thống → thông báo lỗi  |  |  |
| **Các điều kiện đặc biệt** | Không có |  |  |
| **Tiền điều kiện** | Khách hàng đã đăng nhập vào tài khoản. |  |  |
| **Hậu điều kiện** | Thông tin cá nhân được cập nhật trong CSD. |  |  |
| **Điểm mở rộng** | Không có |  |  |

# 

17. # Quản lý sản phẩm

# 

| Mã Use case | UC\_17 | Tên UC | Quản lý sản phẩm |
| :---: | ----- | :---- | :---- |
| **Tác nhân** | Admin  |  |  |
| **Mô tả** | Admin thực hiện các thao tác quản lý sản phẩm: xem danh sách, thêm mới, chỉnh sửa và xóa sản phẩm trong hệ thống OpenCart. Bao gồm quản lý thông tin đa ngôn ngữ, hình ảnh, giá, tồn kho, danh mục, SEO và nhiều thuộc tính khác. |  |  |
| **Luồng sự kiện chính** |  **STT** **Thực hiện bởi** **Hành động ** 1 Admin  Truy cập Catalog \> Products trong trang quản trị 2 Hệ thống Hiển thị danh sách sản phẩm có phân trang, hỗ trợ lọc theo tên, model, giá, số lượng, trạng thái. Hiển thị các cột: Tên SP, Model, Giá, Tồn kho, Trạng thái, Ngày sửa. Thêm sản phẩm 3 Admin Nhấn nút "Add New". 4 Hệ thống Hiển thị form thêm sản phẩm 5 Admin Điền thông tin bắt buộc: Tên sản phẩm (ít nhất 1 ngôn ngữ), Model. Điền các thông tin khác: Giá, Tồn kho, Danh mục, Hình ảnh chính, SEO URL... 6 Admin Nhấn "Save" để lưu. 7 Hệ thống Xác thực: Tên sản phẩm không rỗng, Model không rỗng. Kiểm tra quyền hạn. 8 Hệ thống Xác thực thành công. Lưu sản phẩm vào CSDL 9 Hệ thống Chuyển về danh sách sản phẩm, hiển thị thông báo: "Thêm sản phẩm thành công\!". Sửa sản phẩm 11 Admin Nhấn icon "Edit" trên dòng sản phẩm cần sửa. 12 Hệ thống Tải toàn bộ thông tin sản phẩm từ CSDL. Hiển thị form chỉnh sửa với dữ liệu hiện tại (tất cả các tab như khi thêm mới). 13 Admin Chỉnh sửa các thông tin cần thay đổi (tên, giá, tồn kho, hình ảnh, danh mục, trạng thái...). 14 Admin Nhấn "Save" để lưu thay đổi. 15 Hệ thống Xác thực dữ liệu. Cập nhật sản phẩm trong CSDL 16 Hệ thống Thông báo: "Cập nhật sản phẩm thành công\!". Xóa sản phẩm 17 Admin Tích chọn checkbox một hoặc nhiều sản phẩm trong danh sách. Nhấn nút "Delete". 18 Hệ thống Hiển thị hộp thoại xác nhận: "Bạn có chắc chắn muốn xóa các sản phẩm đã chọn không?". 19a Admin Nhấn "OK" để xác nhận xóa. 20a Hệ thống Kiểm tra quyền hạn. Xóa sản phẩm và tất cả dữ liệu liên quan: mô tả, hình ảnh, danh mục, thuộc tính, tùy chọn, giảm giá, đặc biệt, điểm thưởng, SEO URL, và file hình ảnh trên server. 21a Hệ thống Thông báo: "Xóa sản phẩm thành công\!".  |  |  |
| **Luồng sự kiện thay thế** |  **STT Thực hiện bởi Hành động** 7b Hệ thống Tên sản phẩm bị bỏ trống hoặc model bị bỏ trống → hiển thị lỗi tương ứng trên form, không lưu. 9b Hệ thống Lỗi hệ thống khi lưu (lỗi CSDL...) → hiển thị thông báo lỗi, giữ nguyên form. 12b Hệ thống Sản phẩm không tồn tại → redirect về danh sách với thông báo lỗi. 15b Hệ thống Xác thực thất bại khi sửa → hiển thị lỗi trên form, không lưu. 19b Admin Nhấn "Cancel" trong hộp thoại xác nhận → hủy thao tác, không xóa. 20b Hệ thống Admin không có quyền xóa → hiển thị thông báo lỗi phân quyền. 20c Hệ thống Không có sản phẩm nào được chọn khi nhấn Delete → hiển thị cảnh báo "Vui lòng chọn ít nhất một sản phẩm\!".  |  |  |
| **Các điều kiện đặc biệt** | Không có |  |  |
| **Tiền điều kiện** | Admin đã đăng nhập vào trang quản trị. Có quyền truy cập module Catalog \> Products. |  |  |
| **Hậu điều kiện** | Dữ liệu sản phẩm được lưu/cập nhật/xóa trong CSDL. Cache sản phẩm được làm mới. |  |  |
| **Điểm mở rộng** | Không có |  |  |

# 

18. # Quản lý đơn hàng (Order Management) 

# 

| Mã Use case | UC\_18 | Tên UC | Quản lý đơn hàng |
| :---: | ----- | :---- | :---- |
| **Tác nhân** | Admin |  |  |
| **Mô tả** | Admin xem danh sách đơn hàng, tìm kiếm/lọc theo nhiều tiêu chí, xem chi tiết từng đơn, cập nhật trạng thái đơn hàng, thêm lịch sử xử lý, in hóa đơn và xóa đơn hàng. |  |  |
| **Luồng sự kiện chính** |  **STT** **Thực hiện bởi** **Hành động ** 1 Admin  Truy cập Sales \> Orders trong trang quản trị 2 Hệ thống Hiển thị danh sách đơn hàng Xem chi tiết đơn hàng 3 Admin Nhấn icon "View" trên dòng đơn hàng cần xem. 4 Hệ thống Tải đầy đủ thông tin đơn hàng: thông tin khách hàng, địa chỉ thanh toán/giao hàng, phương thức thanh toán/vận chuyển, danh sách sản phẩm với số lượng/giá/tùy chọn, các dòng tổng tiền, ghi chú, lịch sử trạng thái. 5 Admin Xem thông tin chi tiết đơn hàng, lịch sử xử lý. 6 Admin Cập nhật trạng thái đơn hàng: chọn trạng thái mới (Pending, Processing, Shipped, Complete, Cancelled...), điền ghi chú, tích chọn "Thông báo cho khách hàng" nếu muốn gửi email. 7 Hệ thống Xác thực thông tin cập nhật. Ghi nhận lịch sử thay đổi trạng thái 8 Hệ thống Nếu admin tích gửi email: gửi thông báo thay đổi trạng thái cho khách hàng. 9 Hệ thống Hiển thị thông báo cập nhật thành công. Làm mới phần lịch sử đơn hàng trên trang. 10 Hệ thống Nếu trạng thái là "Complete", hệ thống tự động cộng điểm thưởng cho khách hàng (nếu sản phẩm có điểm thưởng và khách hàng thuộc nhóm tích điểm). Xóa đơn hàng  11 Admin Tích chọn một hoặc nhiều đơn hàng trong danh sách. Nhấn "Delete". 12 Hệ thống Hiển thị xác nhận xóa. 13 Admin Xác nhận xóa. 14 Hệ thống Hệ thống xóa đơn hàng và tất cả dữ liệu liên quan: sản phẩm, tùy chọn, tổng tiền, lịch sử, thông tin địa chỉ trong đơn hàng. 15 Hệ thống Chuyển hướng về danh sách, thông báo "Xóa đơn hàng thành công\!". 16 Hệ thống Cập nhật số lượng tồn kho nếu cấu hình yêu cầu khôi phục hàng khi hủy đơn.  |  |  |
| **Luồng sự kiện thay thế** |  **STT Thực hiện bởi Hành động** 7b Hệ thống Không chọn trạng thái mới → hiển thị lỗi "Vui lòng chọn trạng thái đơn hàng\!". 9b Hệ thống Lỗi gửi email → vẫn cập nhật trạng thái thành công nhưng hiển thị lỗi gửi mail. 12b Hệ thống Đơn hàng không tồn tại → chuyển hướng với thông báo lỗi. 15b Hệ thống Admin không đủ quyền xóa → thông báo lỗi phân quyền. 19b Admin Hủy xác nhận xóa → không xóa, giữ nguyên. 20b Hệ thống Không có đơn hàng nào được chọn → cảnh báo chọn ít nhất một đơn. 20c Hệ thống In hóa đơn: Admin nhấn "Print Invoice" → hệ thống render template hóa đơn PDF và mở để in.  |  |  |
| **Các điều kiện đặc biệt** | Không có |  |  |
| **Tiền điều kiện** | Admin đã đăng nhập vào trang quản trị. Có quyền truy cập module Sales \> Orders. |  |  |
| **Hậu điều kiện** | Trạng thái đơn hàng được cập nhật. Lịch sử thay đổi được ghi nhận. Email thông báo được gửi cho khách hàng (nếu được cấu hình). |  |  |
| **Điểm mở rộng** | Không có |  |  |

# 

19. # Cấu hình tiền tệ & Tỷ giá  

# 

| Mã Use case | UC\_19 | Tên UC | Cấu hình tiền tệ & Tỷ giá |
| :---: | ----- | :---- | :---- |
| **Tác nhân** | Admin |  |  |
| **Mô tả** | Admin quản lý danh sách tiền tệ được hỗ trợ trong hệ thống: thêm tiền tệ mới, cập nhật tỷ giá (thủ công hoặc tự động từ API), đặt tiền tệ mặc định, bật/tắt tiền tệ và xóa tiền tệ không cần thiết. |  |  |
| **Luồng sự kiện chính** |  **STT** **Thực hiện bởi** **Hành động ** 1 Admin  Truy cập Localisation \> Currencies 2 Hệ thống Hiển thị danh sách tiền tệ: Tên tiền tệ, Mã ISO (VD: USD, VND, EUR), Ký hiệu trái/phải, Tỷ giá so với tiền tệ mặc định, Trạng thái (Enabled/Disabled), Ngày cập nhật. 3 Admin Nhấn "Add New". 4 Hệ thống Hiển thị form thêm tiền tệ: Tên tiền tệ, Mã tiền tệ (ISO 4217, VD: VND), Ký hiệu bên trái (VD: $), Ký hiệu bên phải (VD: VND), Số thập phân, Dấu phân cách thập phân, Dấu phân cách hàng nghìn, Tỷ giá quy đổi, Trạng thái. 5 Admin Điền đầy đủ thông tin tiền tệ và nhấn "Save". 6 Hệ thống Xác thực: Tên tiền tệ không rỗng, Mã tiền tệ đúng định dạng 3 ký tự, Tỷ giá \> 0\. 7 Hệ thống Lưu tiền tệ mới vào CSDL. 8 Hệ thống Chuyển hướng về danh sách với thông báo "Thêm tiền tệ thành công\!". 9 Hệ thống Tiền tệ mới xuất hiện trong danh sách và có thể được chọn bởi khách hàng trên cửa hàng. Sửa tiền tệ / Cập nhật tỷ giá 10 Admin Nhấn "Edit" trên dòng tiền tệ cần sửa. 11 Hệ thống Tải thông tin tiền tệ hiện tại, hiển thị form chỉnh sửa. 12 Admin Cập nhật tỷ giá mới (nhập thủ công) hoặc nhấn "Refresh" để tự động lấy tỷ giá 13 Admin Nhấn "Save" để lưu thay đổi. 14 Admin Xác thực dữ liệu. Cập nhật CSDL. 15 Hệ thống Chuyển hướng về danh sách với thông báo cập nhật thành công. Giá sản phẩm tức thì phản ánh tỷ giá mới. Xóa tiền tệ 16 Admin Tích chọn tiền tệ cần xóa. Nhấn "Delete". 17 Hệ thống Hiển thị xác nhận xóa. 18 Admin 	Xác nhận xóa. 19a Hệ thống Kiểm tra tiền tệ không phải tiền tệ mặc định của hệ thống. Xóa khỏi bảng CSDL 20a Hệ thống Chuyển hướngvề danh sách với thông báo "Xóa tiền tệ thành công\!". 21a Hệ thống  |  |  |
| **Luồng sự kiện thay thế** |  **STT Thực hiện bởi Hành động** 7b Hệ thống Tên tiền tệ bị bỏ trống hoặc mã tiền tệ không đúng định dạng → hiển thị lỗi xác thực, không lưu. 9b Hệ thống Tỷ giá từ API không lấy được → hiển thị thông báo lỗi, giữ nguyên tỷ giá cũ. 15b Hệ thống Xác thực thất bại khi sửa → hiển thị lỗi trên form. 19b Admin Hủy xác nhận xóa → không xóa, giữ nguyên. 20b Hệ thống Admin cố xóa tiền tệ mặc định → hiển thị cảnh báo "Không thể xóa tiền tệ mặc định của hệ thống\!". 20c Hệ thống Không có tiền tệ nào được chọn khi nhấn Delete → cảnh báo chọn ít nhất một mục.  |  |  |
| **Các điều kiện đặc biệt** | Không có |  |  |
| **Tiền điều kiện** | Admin đã đăng nhập vào trang quản trị. Có quyền truy cập Localisation \> Currencies. |  |  |
| **Hậu điều kiện** | Thông tin tiền tệ và tỷ giá được cập nhật trong CSDL. Giá sản phẩm hiển thị theo tỷ giá mới. |  |  |
| **Điểm mở rộng** | Không có |  |  |

# 

20. # Quản lý nhóm khách hàng (Customer Groups) 

# 

| Mã Use case | UC\_20 | Tên UC | Quản lý nhóm khách hàng |
| :---: | ----- | :---- | :---- |
| **Tác nhân** | Admin |  |  |
| **Mô tả** | Admin quản lý các nhóm khách hàng trong hệ thống: thêm nhóm mới, chỉnh sửa thông tin nhóm (tên, mô tả, mức giảm giá, phê duyệt), đặt nhóm mặc định và xóa nhóm không còn sử dụng. Nhóm khách hàng ảnh hưởng đến giá sản phẩm, trường tùy chỉnh và quyền lợi riêng. |  |  |
| **Luồng sự kiện chính** |  **STT** **Thực hiện bởi** **Hành động ** 1 Admin  Truy cập Customers \> Customer Groups 2 Hệ thống Hiển thị danh sách nhóm khách hàng với các cột: Tên nhóm, Tỷ lệ giảm giá (%), Trạng thái phê duyệt (Approval). Có hỗ trợ lọc theo tên nhóm. Thêm nhóm khách hàng 3 Admin Nhấn "Add New" để thêm nhóm mới. 4 Hệ thống Hiển thị form thêm nhóm: Tên nhóm (đa ngôn ngữ), Mô tả nhóm (đa ngôn ngữ), Tỷ lệ giảm giá (%), Yêu cầu phê duyệt tài khoản (Approval: Yes/No). 5 Admin Điền tên nhóm, mô tả, tỷ lệ giảm giá, cấu hình phê duyệt. 6 Admin Nhấn "Save". 7 Hệ thống Xác thực: Tên nhóm không rỗng (ít nhất theo ngôn ngữ mặc định). Tỷ lệ giảm giá từ 0-100. 8 Hệ thống Lưu nhóm mới vào CSDL 9 Hệ thống Chuyển hướng về danh sách với thông báo "Thêm nhóm khách hàng thành công\!". 10 Hệ thống Nhóm mới có thể được gán cho khách hàng và sử dụng để cấu hình giá đặc biệt, trường tùy chỉnh, phương thức thanh toán/vận chuyển riêng. Sửa nhóm khách hàng 11 Admin Nhấn "Edit" trên dòng nhóm cần sửa. 12 Hệ thống Tải thông tin nhóm khách hàng hiện tại từ CSDL (tên đa ngôn ngữ, mô tả, tỷ lệ giảm, phê duyệt). Hiển thị form chỉnh sửa với dữ liệu hiện tại. 13 Admin Chỉnh sửa thông tin: tên, mô tả, tỷ lệ giảm giá, yêu cầu phê duyệt. 14 Admin Nhấn "Save" để lưu thay đổi. 15 Hệ thống Xác thực dữ liệu. Cập nhật CSDL 16 Hệ thống Chuyển hướng về danh sách với thông báo "Cập nhật nhóm khách hàng thành công\!". Chính sách giá mới áp dụng ngay cho khách hàng thuộc nhóm này. Xóa nhóm khách hàng	 17 Admin Tích chọn một hoặc nhiều nhóm cần xóa. Nhấn "Delete". 18 Hệ thống Hiển thị xác nhận xóa: "Bạn có chắc muốn xóa các nhóm đã chọn?". 19a Admin Nhấn "OK" xác nhận xóa. 20a Hệ thống Kiểm tra nhóm không phải nhóm mặc định, . Kiểm tra không còn khách hàng nào thuộc nhóm này. Xóa khỏi CSDL 21a Hệ thống Chuyển hướng về danh sách với thông báo "Xóa nhóm khách hàng thành công\!".  |  |  |
| **Luồng sự kiện thay thế** |  **STT Thực hiện bởi Hành động** 7b Hệ thống Tên nhóm bị bỏ trống → hiển thị lỗi "Tên nhóm không được để trống\!", không lưu. 9b Hệ thống Lỗi CSDL khi lưu → hiển thị thông báo lỗi hệ thống, giữ nguyên form. 15b Hệ thống Xác thực thất bại (tên rỗng, tỷ lệ sai) → hiển thị lỗi trên form, không lưu. 19b Admin Nhấn "Cancel" → hủy xóa, giữ nguyên dữ liệu. 20b Hệ thống Nhóm được chọn là nhóm mặc định của hệ thống → hiển thị cảnh báo "Không thể xóa nhóm khách hàng mặc định\!". 20c Hệ thống Nhóm vẫn còn khách hàng đang sử dụng → hiển thị cảnh báo "Không thể xóa nhóm có khách hàng\! Vui lòng chuyển khách hàng sang nhóm khác trước.".  |  |  |
| **Các điều kiện đặc biệt** | Không có |  |  |
| **Tiền điều kiện** | Admin đã đăng nhập vào trang quản trị. Có quyền truy cập Customers \> Customer Groups. |  |  |
| **Hậu điều kiện** | Nhóm khách hàng được cập nhật trong CSDL. Khách hàng thuộc nhóm được hưởng chính sách giá và quyền lợi tương ứng. |  |  |
| **Điểm mở rộng** | Không có |  |  |

# 