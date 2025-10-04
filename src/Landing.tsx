import { Shield, CheckCircle, Lock, FileText, Users, ArrowRight, Menu, X } from 'lucide-react';
import { useState } from 'react';

function Landing() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className="fixed w-full bg-white/95 backdrop-blur-sm z-50 border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-20">
            <div className="flex items-center">
              <svg width="180" height="40" viewBox="0 0 180 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M10 8 Q12 10 13 12 L14 16 Q15 20 14 24 L13 28 Q12 30 10 32 Q8 30 7 28 L6 24 Q5 20 6 16 L7 12 Q8 10 10 8 Z" fill="#F97316"/>
                <circle cx="10" cy="20" r="2" fill="#10B981"/>
                <path d="M14 12 Q16 14 16.5 16 L17 20 Q17 22 16.5 24 L16 26" stroke="#10B981" strokeWidth="1.5" fill="none"/>
                <text x="24" y="26" fontFamily="Arial, sans-serif" fontSize="20" fontWeight="700" fill="#1e293b">
                  VeriSyntra
                </text>
              </svg>
            </div>

            <div className="hidden md:flex items-center space-x-8">
              <a href="#features" className="text-gray-600 hover:text-gray-900 transition-colors text-sm font-medium">Tính năng</a>
              <a href="#benefits" className="text-gray-600 hover:text-gray-900 transition-colors text-sm font-medium">Lợi ích</a>
              <a href="#about" className="text-gray-600 hover:text-gray-900 transition-colors text-sm font-medium">Về chúng tôi</a>
              <a href="#contact" className="text-gray-600 hover:text-gray-900 transition-colors text-sm font-medium">Liên hệ</a>
              <button className="bg-teal-600 hover:bg-teal-700 text-white px-6 py-2.5 rounded-lg font-medium transition-all transform hover:scale-105 shadow-sm">
                Bắt đầu ngay
              </button>
            </div>

            <button
              className="md:hidden text-gray-600"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>

        {mobileMenuOpen && (
          <div className="md:hidden border-t border-gray-100 bg-white">
            <div className="px-4 py-4 space-y-3">
              <a href="#features" className="block text-gray-600 hover:text-gray-900 py-2">Tính năng</a>
              <a href="#benefits" className="block text-gray-600 hover:text-gray-900 py-2">Lợi ích</a>
              <a href="#about" className="block text-gray-600 hover:text-gray-900 py-2">Về chúng tôi</a>
              <a href="#contact" className="block text-gray-600 hover:text-gray-900 py-2">Liên hệ</a>
              <button className="w-full bg-teal-600 hover:bg-teal-700 text-white px-6 py-2.5 rounded-lg font-medium">
                Bắt đầu ngay
              </button>
            </div>
          </div>
        )}
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-orange-50 via-teal-50 to-emerald-50">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-8">
              <div className="inline-flex items-center space-x-2 bg-emerald-100 text-emerald-700 px-4 py-2 rounded-full text-sm font-medium">
                <Shield size={16} />
                <span>Tuân thủ PDPL 2025</span>
              </div>

              <h1 className="text-5xl sm:text-6xl font-bold text-gray-900 leading-tight">
                Giải pháp tuân thủ{' '}
                <span className="text-orange-500 bg-gradient-to-r from-orange-500 to-emerald-600 bg-clip-text text-transparent">
                  PDPL 2025
                </span>{' '}
                cho doanh nghiệp Việt
              </h1>

              <p className="text-xl text-gray-600 leading-relaxed">
                Cổng tự phục vụ giúp doanh nghiệp Việt Nam đạt được và duy trì sự tuân thủ PDPL 2025 một cách độc lập, nhanh chóng và hiệu quả.
              </p>

              <div className="flex flex-col sm:flex-row gap-4">
                <button className="group bg-teal-600 hover:bg-teal-700 text-white px-8 py-4 rounded-xl font-semibold transition-all transform hover:scale-105 shadow-lg hover:shadow-xl flex items-center justify-center space-x-2">
                  <span>Dùng thử miễn phí</span>
                  <ArrowRight className="group-hover:translate-x-1 transition-transform" size={20} />
                </button>
                <button className="bg-teal-600 hover:bg-teal-700 text-white px-8 py-4 rounded-xl font-semibold border-2 border-teal-600 transition-all">
                  Xem demo
                </button>
              </div>

              <div className="flex items-center space-x-8 pt-4">
                <div>
                  <div className="text-3xl font-bold text-gray-900">500+</div>
                  <div className="text-sm text-gray-600">Doanh nghiệp tin tưởng</div>
                </div>
                <div className="h-12 w-px bg-gray-300"></div>
                <div>
                  <div className="text-3xl font-bold text-gray-900">99.9%</div>
                  <div className="text-sm text-gray-600">Tỷ lệ tuân thủ</div>
                </div>
                <div className="h-12 w-px bg-gray-300"></div>
                <div>
                  <div className="text-3xl font-bold text-gray-900">24/7</div>
                  <div className="text-sm text-gray-600">Hỗ trợ</div>
                </div>
              </div>
            </div>

            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-tr from-orange-200 to-emerald-300 rounded-3xl transform rotate-3 opacity-20"></div>
              <div className="relative bg-white rounded-3xl shadow-2xl p-8 border border-gray-100">
                <div className="space-y-6">
                  <div className="flex items-start space-x-4 p-4 bg-green-50 rounded-xl border border-green-100">
                    <CheckCircle className="text-green-500 flex-shrink-0 mt-1" size={24} />
                    <div>
                      <h3 className="font-semibold text-gray-900">Đánh giá tự động</h3>
                      <p className="text-sm text-gray-600 mt-1">Hệ thống tự động đánh giá mức độ tuân thủ PDPL</p>
                    </div>
                  </div>

                  <div className="flex items-start space-x-4 p-4 bg-emerald-50 rounded-xl border border-emerald-100">
                    <Lock className="text-emerald-600 flex-shrink-0 mt-1" size={24} />
                    <div>
                      <h3 className="font-semibold text-gray-900">Bảo mật dữ liệu</h3>
                      <p className="text-sm text-gray-600 mt-1">Quản lý và bảo vệ dữ liệu cá nhân theo chuẩn quốc tế</p>
                    </div>
                  </div>

                  <div className="flex items-start space-x-4 p-4 bg-orange-50 rounded-xl border border-orange-100">
                    <FileText className="text-orange-500 flex-shrink-0 mt-1" size={24} />
                    <div>
                      <h3 className="font-semibold text-gray-900">Tài liệu hoàn chỉnh</h3>
                      <p className="text-sm text-gray-600 mt-1">Tạo tự động các tài liệu tuân thủ cần thiết</p>
                    </div>
                  </div>

                  <div className="flex items-start space-x-4 p-4 bg-cyan-50 rounded-xl border border-cyan-100">
                    <Users className="text-cyan-600 flex-shrink-0 mt-1" size={24} />
                    <div>
                      <h3 className="font-semibold text-gray-900">Đào tạo nhân viên</h3>
                      <p className="text-sm text-gray-600 mt-1">Khóa học và tài liệu đào tạo cho đội ngũ</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Tính năng nổi bật
            </h2>
            <p className="text-xl text-gray-600">
              Giải pháp toàn diện giúp doanh nghiệp tuân thủ PDPL 2025 một cách dễ dàng
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: Shield,
                title: 'Đánh giá tuân thủ',
                description: 'Đánh giá tự động và chi tiết mức độ tuân thủ PDPL của doanh nghiệp',
                color: 'bg-orange-100 text-orange-500'
              },
              {
                icon: FileText,
                title: 'Quản lý tài liệu',
                description: 'Tạo và quản lý tất cả tài liệu cần thiết cho việc tuân thủ',
                color: 'bg-emerald-100 text-emerald-600'
              },
              {
                icon: Lock,
                title: 'Bảo mật dữ liệu',
                description: 'Công cụ quản lý và bảo vệ dữ liệu cá nhân theo tiêu chuẩn cao',
                color: 'bg-teal-100 text-teal-600'
              },
              {
                icon: Users,
                title: 'Đào tạo & Hướng dẫn',
                description: 'Khóa học và tài liệu đào tạo cho nhân viên về PDPL',
                color: 'bg-cyan-100 text-cyan-600'
              },
              {
                icon: CheckCircle,
                title: 'Theo dõi tiến độ',
                description: 'Dashboard theo dõi tiến độ tuân thủ theo thời gian thực',
                color: 'bg-lime-100 text-lime-600'
              },
              {
                icon: Shield,
                title: 'Cập nhật liên tục',
                description: 'Cập nhật tự động khi có thay đổi về quy định PDPL',
                color: 'bg-green-100 text-green-600'
              }
            ].map((feature, index) => (
              <div
                key={index}
                className="group p-8 bg-white rounded-2xl border border-gray-100 hover:border-orange-200 hover:shadow-xl transition-all duration-300"
              >
                <div className={`w-14 h-14 ${feature.color} rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform`}>
                  <feature.icon size={28} />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">{feature.title}</h3>
                <p className="text-gray-600 leading-relaxed">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section id="benefits" className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-orange-50 to-emerald-50">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-4xl font-bold text-gray-900 mb-6">
                Tại sao chọn VeriSyntra?
              </h2>
              <div className="space-y-6">
                {[
                  {
                    title: 'Tiết kiệm chi phí',
                    description: 'Giảm đến 70% chi phí so với việc thuê tư vấn bên ngoài'
                  },
                  {
                    title: 'Tiết kiệm thời gian',
                    description: 'Đạt tuân thủ trong vòng 4-6 tuần thay vì 6-12 tháng'
                  },
                  {
                    title: 'Dễ sử dụng',
                    description: 'Giao diện thân thiện, không cần kiến thức chuyên môn sâu'
                  },
                  {
                    title: 'Hỗ trợ tiếng Việt',
                    description: 'Hoàn toàn bằng tiếng Việt, phù hợp với doanh nghiệp Việt Nam'
                  }
                ].map((benefit, index) => (
                  <div key={index} className="flex items-start space-x-4">
                    <div className="flex-shrink-0 w-6 h-6 bg-emerald-600 rounded-full flex items-center justify-center mt-1">
                      <CheckCircle size={16} className="text-white" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900 text-lg mb-1">{benefit.title}</h3>
                      <p className="text-gray-600">{benefit.description}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-white rounded-3xl shadow-2xl p-8 border border-gray-100">
              <div className="text-center mb-8">
                <h3 className="text-2xl font-bold text-gray-900 mb-2">Bắt đầu ngay hôm nay</h3>
                <p className="text-gray-600">Dùng thử miễn phí 14 ngày, không cần thẻ tín dụng</p>
              </div>

              <form className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Tên doanh nghiệp
                  </label>
                  <input
                    type="text"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
                    placeholder="Công ty ABC"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Email công ty
                  </label>
                  <input
                    type="email"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
                    placeholder="contact@company.com"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Số điện thoại
                  </label>
                  <input
                    type="tel"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
                    placeholder="0901234567"
                  />
                </div>

                <button
                  type="submit"
                  className="w-full bg-teal-600 hover:bg-teal-700 text-white px-8 py-4 rounded-xl font-semibold transition-all transform hover:scale-105 shadow-lg hover:shadow-xl"
                >
                  Đăng ký dùng thử miễn phí
                </button>
              </form>

              <p className="text-center text-sm text-gray-500 mt-6">
                Bằng cách đăng ký, bạn đồng ý với{' '}
                <a href="#" className="text-orange-500 hover:underline">Điều khoản dịch vụ</a>
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-300 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <svg width="160" height="36" viewBox="0 0 180 40" fill="none" xmlns="http://www.w3.org/2000/svg" className="mb-4">
                <path d="M10 8 Q12 10 13 12 L14 16 Q15 20 14 24 L13 28 Q12 30 10 32 Q8 30 7 28 L6 24 Q5 20 6 16 L7 12 Q8 10 10 8 Z" fill="#F97316"/>
                <circle cx="10" cy="20" r="2" fill="#10B981"/>
                <path d="M14 12 Q16 14 16.5 16 L17 20 Q17 22 16.5 24 L16 26" stroke="#10B981" strokeWidth="1.5" fill="none"/>
                <text x="24" y="26" fontFamily="Arial, sans-serif" fontSize="20" fontWeight="700" fill="#ffffff">
                  VeriSyntra
                </text>
              </svg>
              <p className="text-sm text-gray-400 leading-relaxed">
                Giải pháp tuân thủ PDPL 2025 hàng đầu cho doanh nghiệp Việt Nam
              </p>
            </div>

            <div>
              <h4 className="font-semibold text-white mb-4">Sản phẩm</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white transition-colors">Tính năng</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Bảng giá</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Tài liệu</a></li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold text-white mb-4">Công ty</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white transition-colors">Về chúng tôi</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Blog</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Liên hệ</a></li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold text-white mb-4">Hỗ trợ</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white transition-colors">Trung tâm hỗ trợ</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Điều khoản dịch vụ</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Chính sách bảo mật</a></li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-800 pt-8 flex flex-col md:flex-row justify-between items-center">
            <p className="text-sm text-gray-400">
              © 2025 VeriSyntra. All rights reserved.
            </p>
            <div className="flex space-x-6 mt-4 md:mt-0">
              <a href="#" className="text-gray-400 hover:text-white transition-colors">Facebook</a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">LinkedIn</a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">Twitter</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default Landing;
